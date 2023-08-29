from __future__ import annotations

import itertools
import multiprocessing
import os
import threading
import traceback
from logging import getLogger
from multiprocessing import Process, Queue
from multiprocessing.context import ForkServerProcess, SpawnProcess
from threading import Thread
from typing import Any, Generator, Iterator, Optional, Type, Union

from ...base import (
    CheckpointableDataset,
    CheckpointableIterator,
    FilterMapFn,
    ParallelExecutorType,
    Sample,
    StateDict,
)


logger = getLogger(__name__)
mp_ctx = multiprocessing.get_context("forkserver")  # TODO: customization?


class StopToken:
    pass


WorkerClass = Union[Type[Process], Type[Thread], Type[ForkServerProcess], Type[SpawnProcess]]
WorkerInput = Union[Sample, StopToken]


class WorkerResult:
    error: Optional[
        tuple[Exception, str]
    ]  # (Exception, traceback string) --- The actual traceback is not picklable
    result: Optional[Sample]

    def __init__(self, error: Optional[tuple[Exception, str]], result: Optional[Sample]) -> None:
        self.error = error
        self.result = result

    def log_error(self) -> None:
        assert self.error
        e, exc_traceback = self.error
        logger.error(
            f"Exception in worker: {repr(e)}. The actual traceback is as follows:\n"
            f"{'=' * 80}\n"
            f"{exc_traceback}"
            f"(The exception is going to be raised again, but its traceback can be misleading.)\n"
            f"{'=' * 80}"
        )


def _get_worker_class(executor_type: str) -> WorkerClass:
    if executor_type == "process":
        return mp_ctx.Process
    elif executor_type == "thread":
        return Thread
    else:
        raise ValueError('Invalid executor_type. Choose either "process" or "thread".')


def _worker(fn: FilterMapFn, rx: Queue[WorkerInput], tx: Queue[WorkerResult]) -> None:
    process_id = os.getpid()
    thread_id = threading.get_ident()
    logger.debug(f"Worker starting. Process ID: {process_id}, Thread ID: {thread_id}.")

    while True:
        try:
            item = rx.get()
            if isinstance(item, StopToken):
                break

            result = fn(item)
            tx.put(WorkerResult(error=None, result=result))
        except Exception as e:
            logger.exception(
                f"Exception in worker. Process ID: {process_id}, Thread ID: {thread_id}."
            )
            # Traceback objects are not picklable, so we need to convert them to strings
            exc_traceback = traceback.format_exc()
            tx.put(WorkerResult(error=(e, exc_traceback), result=None))

    logger.debug(f"Worker ending. Process ID: {process_id}, Thread ID: {thread_id}.")


def _imap_ordered(
    fn: FilterMapFn,
    source: Iterator[Sample],
    max_workers: int,
    queue_len: int,
    executor_type: str,
) -> Generator[Optional[Sample], None, None]:
    worker_class = _get_worker_class(executor_type)

    workers = []
    try:
        logger.debug(f"Starting {max_workers} workers. This may take some time.")
        for _ in range(max_workers):
            worker_queue_len = queue_len // max_workers + 1
            rx: Queue[WorkerInput] = mp_ctx.Queue(worker_queue_len)
            tx: Queue[WorkerResult] = mp_ctx.Queue(worker_queue_len)
            worker = worker_class(target=_worker, args=(fn, rx, tx), daemon=True)
            worker.start()
            workers.append((worker, rx, tx))
        logger.debug(f"Started {max_workers} workers.")

        # Sample index to read and put
        get_index = 0
        put_index = 0

        # Fill the queues
        for x in itertools.islice(source, queue_len):
            _, rx, _ = workers[put_index % max_workers]
            rx.put(x)
            put_index += 1

        # Read from the queues
        while get_index < put_index:
            _, _, tx = workers[get_index % max_workers]
            result = tx.get()
            if result.error:
                result.log_error()
                raise result.error[0]
            yield result.result
            get_index += 1

            _, rx, _ = workers[put_index % max_workers]
            try:
                rx.put(next(source))
                put_index += 1
            except StopIteration:
                # All tasks submitted, just wait for them to complete
                continue
    finally:
        logger.debug(f"Terminating {max_workers} workers.")
        if executor_type == "process":
            for worker, _, _ in workers:
                assert not isinstance(worker, Thread)
                worker.terminate()
        else:
            # Thread does not have terminate method
            for _, rx, _ in workers:
                rx.put(StopToken())
            for worker, _, _ in workers:
                worker.join()

        logger.debug(f"Terminated {max_workers} workers.")


def _imap_unordered(
    fn: FilterMapFn,
    source: Iterator[Sample],
    max_workers: int,
    queue_len: int,
    executor_type: str,
) -> Generator[Optional[Sample], None, None]:
    worker_class = _get_worker_class(executor_type)
    rx: Queue[WorkerInput] = mp_ctx.Queue(queue_len + 1)
    tx: Queue[WorkerResult] = mp_ctx.Queue(queue_len + 1)

    workers = []
    try:
        logger.debug(f"Starting {max_workers} workers. This may take some time.")
        for _ in range(max_workers):
            worker = worker_class(target=_worker, args=(fn, rx, tx))
            worker.start()
            workers.append((worker, rx, tx))
        logger.debug(f"Started {max_workers} workers.")

        get_index = 0
        put_index = 0

        # Fill the queues
        for x in itertools.islice(source, queue_len):
            rx.put(x)
            put_index += 1

        # Read from the queues
        while get_index < put_index:
            result = tx.get()
            if result.error:
                result.log_error()
                raise result.error[0]
            yield result.result
            get_index += 1

            try:
                rx.put(next(source))
                put_index += 1
            except StopIteration:
                # All tasks submitted, just wait for them to complete
                continue
    finally:
        logger.debug(f"Terminating {max_workers} workers.")
        if executor_type == "process":
            for worker, _, _ in workers:
                assert not isinstance(worker, Thread)
                worker.terminate()
        else:
            # Thread does not have terminate method
            for _, rx, _ in workers:
                rx.put(StopToken())
            for worker, _, _ in workers:
                worker.join()

        logger.debug(f"Terminated {max_workers} workers.")


class ParallelFilterMapIterator(CheckpointableIterator):
    def __init__(
        self,
        source: CheckpointableIterator,
        dataset: ParallelFilterMapDataset,
        unconsumed_outputs: list[Sample],
    ) -> None:
        self.source = source
        self.dataset = dataset
        self._closing = False
        self._iter = self._start(unconsumed_outputs)

    def _source_iter(self) -> Generator[Sample, None, None]:
        while not self._closing:
            try:
                yield next(self.source)
            except StopIteration:
                break

    def _output_iter(self, unconsumed_outputs: list[Sample]) -> Generator[Sample, None, None]:
        # `self.closing = False` should not be in this method; it should be done before calling
        # this method. This is because the execution is delayed until the first `next()` call.
        # In the edge case where `state_dict` (and thus `_close`) is called before `next`,
        # `_source_iter` cannot be closed properly.

        if self.dataset.ordered:
            it = _imap_ordered(
                self.dataset.fn,
                self._source_iter(),
                self.dataset.max_workers,
                self.dataset.queue_len,
                self.dataset.executor_type,
            )
        else:
            it = _imap_unordered(
                self.dataset.fn,
                self._source_iter(),
                self.dataset.max_workers,
                self.dataset.queue_len,
                self.dataset.executor_type,
            )
        yield from itertools.chain(unconsumed_outputs, it)

    def __next__(self) -> Sample:
        while True:
            sample = next(self._iter)
            if sample is not None:
                return sample

    def _start(self, unconsumed_outputs: list[Sample]) -> Generator[Sample, None, None]:
        self._closing = False
        return self._output_iter(unconsumed_outputs)

    def _close(self) -> list[Sample]:
        self._closing = True
        return list(self._iter)

    def state_dict(self) -> StateDict:
        unconsumed_outputs = self._close()
        state_dict = {
            "source": self.source.state_dict(),
            "unconsumed_outputs": unconsumed_outputs,
        }
        self._closing = False
        self._iter = self._output_iter(unconsumed_outputs)
        return state_dict


def _get_default_max_workers() -> int:
    n_cpus = os.cpu_count() or 1
    local_world_size = int(os.environ.get("LOCAL_WORLD_SIZE", 1))
    return max(n_cpus // local_world_size, 1)


class ParallelFilterMapDataset(CheckpointableDataset):
    def __init__(
        self,
        source: CheckpointableDataset,
        fn: FilterMapFn,
        max_workers: Optional[int],
        prefetch_factor: int,
        ordered: bool,
        executor_type: ParallelExecutorType,
    ):
        self.source = source
        self.fn = fn

        if max_workers is None:
            self.max_workers = _get_default_max_workers()
        else:
            self.max_workers = max_workers
        if self.max_workers < 1:
            raise ValueError("max_workers must be greater than 0: {self.max_workers}")

        if prefetch_factor < 1:
            raise ValueError("prefetch_factor must be greater than 0: {prefetch_factor}")
        self.queue_len = self.max_workers * prefetch_factor

        self.ordered = ordered
        self.executor_type = executor_type

    def iter(self, state_dict: Optional[dict[str, Any]] = None) -> CheckpointableIterator:
        if state_dict is not None:
            unconsumed_outputs = state_dict.pop("unconsumed_outputs")
            source_state_dict = state_dict.pop("source")
            if state_dict:
                raise ValueError(f"Unexpected keys in state_dict: {state_dict.keys()}")
        else:
            unconsumed_outputs = []
            source_state_dict = None
        iter = self.source.iter(state_dict=source_state_dict)
        return ParallelFilterMapIterator(iter, self, unconsumed_outputs)
