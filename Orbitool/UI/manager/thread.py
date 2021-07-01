from abc import ABC, abstractmethod
from collections import deque
from enum import Enum
from multiprocessing.pool import Pool as PoolType, AsyncResult
from queue import Queue
from typing import List, Tuple, final, Deque, Iterable, Generator

from PyQt5 import QtCore

from ...config import logger, multi_cores
from ..utils import sleep


class threadtype(Enum):
    thread = 0
    multiprocess = 1


class Thread(QtCore.QThread):
    finished = QtCore.pyqtSignal(tuple)
    sendStatus = QtCore.pyqtSignal(str, int, int)

    def __init__(self, func, args=(), kwargs={}) -> None:
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit((result,))
        except Exception as e:
            self.finished.emit((e, ))

    def sendStatusFunc(self, *args):
        self.sendStatus.emit(*args)


class MultiProcess(QtCore.QThread):
    finished = QtCore.pyqtSignal(tuple)
    sendStatus = QtCore.pyqtSignal(str, int, int)

    @final
    def __init__(self, file, kwargs: dict, pool: PoolType) -> None:
        super().__init__()
        self.file = file
        self.kwargs = kwargs
        self.pool = pool
        self.aborted = False

    @final
    def run(self):
        results: Deque[AsyncResult] = deque()
        pool: PoolType = self.pool
        file = self.file
        kwargs = self.kwargs
        queue = Queue()

        def iter_queue():
            while True:
                result = queue.get()
                if result is None:
                    break
                yield result

        write_thread = Thread(self.write, (file, iter_queue()), kwargs)
        write_thread.start()

        for i, input_data in enumerate(self.read(file, **kwargs)):
            if self.aborted:
                queue.put(None)
                return self.exception(file, kwargs)
            results.append(pool.apply_async(
                self.process, (i, self.func, input_data, kwargs)))
            if i >= multi_cores:
                ret = results.popleft()
                while not ret.ready():
                    sleep(0.01)
                ret = ret.get()
                if isinstance(ret, Exception):
                    self.exception(file, kwargs)
                    self.finished.emit(
                        (ret, (self.func, self.file, self.kwargs)))
                    queue.put(None)
                    return
                queue.put(ret)

        while results:
            ret = results.popleft()
            while not ret.ready():
                sleep(0.01)
            ret = ret.get()
            if isinstance(ret, Exception):
                self.exception(file, **kwargs)
                self.finished.emit(
                    (ret, (self.func, self.file, kwargs)))
                queue.put(None)
                return
            queue.put(ret)

        queue.put(None)

        write_thread.wait()

        self.finished.emit((True, (self.file, kwargs)))

    @final
    def abort(self, send=True):
        if send:
            self.finished.emit(
                (RuntimeError("Aborted"), (self.func, self.file, self.args)))
        self.aborted = True

    @final
    @staticmethod
    def process(label, func, data, kwargs):
        try:
            ret = func(data, **kwargs)
        except Exception as e:
            logger.error(str(e), exc_info=e)
            return e
        return ret

    @staticmethod
    def func(data, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def read(file, **kwargs) -> Generator:
        raise NotImplementedError()
        # example
        for i in range(10):
            yield i

    @staticmethod
    def write(file, rets: Iterable, **kwargs):
        raise NotImplementedError()
        # example
        for ret in rets:
            print(ret)

    @staticmethod
    def exception(file, **kwargs):
        raise NotImplementedError()
