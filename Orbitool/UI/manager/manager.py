from __future__ import annotations

import itertools
import logging
import weakref
from datetime import datetime
from functools import wraps
from typing import (
    Callable, Dict, Generic, Iterable, Iterator, Type, TypeVar,
    List, overload, Set, Sized)
from types import MethodType

import numpy as np
from PySide6.QtCore import QObject, QThread, QTimer, Signal
from PySide6.QtWidgets import QMainWindow, QTableWidget, QWidget

from Orbitool.models.workspace import WorkSpace

logger = logging.getLogger("Orbitool")


class BindData:
    def __init__(self) -> None:
        self.peak_fit_left_index: DataBindSignal[int] = DataBindSignal()


class Values:
    def __init__(self) -> None:
        self.calibration_info_selected_index: ValueGetter[int] = ValueGetter()
        self.mass_list_selected_indexes: ValueGetter[np.ndarray] = ValueGetter(
        )
        self.spectra_list_selected_index: ValueGetter[int] = ValueGetter()
        self.peak_list_selected_true_index: ValueGetter[List[int]] = ValueGetter()


class Signals:
    def __init__(self) -> None:
        self.peak_refit_finish = MySignal()
        self.peak_list_show = MySignal()


class Manager(QObject):
    """
    storage common resources
    """
    busy_signal = Signal(bool)
    msg = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.running_thread: QThread = None
        self._live_threads: Set[QThread] = set()
        self.workspace: WorkSpace = None
        self._busy_count: int = 0

        self.formulas_result_win: QMainWindow = None
        self.calibration_detail_win: QMainWindow = None
        self.peak_float_wins: Dict[int, QMainWindow] = {}
        self.mass_defect_wins: List[QWidget] = []

        self.tqdm = TQDMER()

        self.init_or_restored = MySignal()  # for exception catch
        self.save = MySignal()  # for exception catch
        self.signals = Signals()

        self.bind = BindData()
        self.getters = Values()

    def set_busy(self, busy: bool):
        """
        Acquire (True) or release (False) one manual busy hold, used to
        simulate a running operation. It is the same counter `begin_task`/
        `end_task` use, so call it in pairs; docs and tests rely on that.
        """
        if busy:
            self.begin_task()
        else:
            self.end_task()

    def begin_task(self) -> None:
        """
        Hold one busy count, shared by ui_task and `set_busy`. busy_signal
        fires only on the idle -> busy edge.
        """
        self._busy_count += 1
        if self._busy_count == 1:
            self.busy_signal.emit(True)

    def end_task(self) -> None:
        """
        Give back one busy count (success or failure). busy_signal fires
        only on the busy -> idle edge, when the last holder finishes.
        """
        if self._busy_count <= 0:
            logger.warning(
                "end_task called without a matching begin_task")
            return
        self._busy_count -= 1
        if self._busy_count == 0:
            self.busy_signal.emit(False)

    @property
    def busy(self):
        return self._busy_count > 0

    def start_thread(self, thread: QThread) -> None:
        """
        Start a worker thread, holding a strong reference to it until Qt
        reports it finished.

        `running_thread` only remembers the newest worker, so the next
        background step overwrites the previous one while it may still be
        winding down. PySide6 then deletes the QThread wrapper as soon as
        the Python reference count drops, destroying the C++ thread while
        it is still running ("QThread: Destroyed while thread '' is still
        running"). Here the reference is released on `finished`, which
        reaches the main thread.

        The release slot holds the thread through a weakref, not a closure:
        a direct capture would leave a thread <-> connection reference cycle
        and the wrapper would never be freed by reference counting.
        """
        self._live_threads.add(thread)
        ref = weakref.ref(thread)

        def release():
            t = ref()
            if t is not None:
                self._live_threads.discard(t)

        thread.finished.connect(release)
        try:
            thread.start()
        except BaseException:
            self._live_threads.discard(thread)
            raise


T = TypeVar("T")


class TQDM(Generic[T]):
    def __init__(self, callback_func, iter: Iterable = None, length: int = 0, msg: str = "") -> None:
        self.callback_func = callback_func
        self.iter = iter
        self.msg = msg

        self.length = length
        self.now = 0

        self.begin_time = self.last_show_time = datetime.now()

    def showMsg(self):
        now = datetime.now()
        if (now - self.last_show_time).total_seconds() > .01 or self.length < 1000:
            passed_time = now - self.begin_time
            if self.length > self.now:
                if self.now:
                    left_time = passed_time * \
                        (self.length - self.now) / self.now
                    minute = int(left_time.total_seconds() / 60)
                    second = format(left_time.total_seconds() % 60, '.2f')
                else:
                    minute = "inf"
                    second = "inf"
                text = f"{self.msg} {self.now}/{self.length} ~{minute}:{second}"
                percent = 100 * self.now // self.length
            else:
                minute = int(passed_time.total_seconds() / 60)
                second = format(passed_time.total_seconds() % 60, '.2f')
                text = f"{self.msg} {self.now} {minute}:{second} passed"
                if self.length == self.now:
                    percent = 100
                else:
                    percent = 70
            self.callback_func(percent, text)
            self.last_show_time = now

    def start_time(self):
        self.begin_time = datetime.now()

    def update(self, step=1):
        self.now += step
        self.showMsg()

    def __iter__(self) -> Iterator[T]:
        self.start_time()
        for x in self.iter:
            self.update()
            yield x


class TQDMER(QObject):
    tqdm_signal = Signal(int, int, str)  # label, percent, msg

    def __init__(self) -> None:
        super().__init__()
        self.progress_cnt = itertools.count()

    @overload
    def __call__(self, iter: Iterable[T], msg: str = "") -> TQDM[T]:
        pass

    @overload
    def __call__(self, iter: Iterable[T], msg: str = "", *, length: int = 0, immediate=False) -> TQDM[T]:
        pass

    @overload
    def __call__(self, *, msg: str = "", length: int = 0) -> TQDM:
        pass

    @overload
    def __call__(self, *, msg: str = "") -> TQDM:
        pass

    def __call__(self, iter: Iterable = None, msg: str = "", *, length=None, immediate=False):
        if iter is not None:
            if length is None:
                if isinstance(iter, Sized):
                    length = len(iter)
                else:
                    length = 0
        label = next(self.progress_cnt)
        tqdm = TQDM((lambda percent, msg: self.tqdm_signal.emit(label, percent, msg)),
                    iter, length, msg)
        if immediate:
            tqdm.showMsg()
        return tqdm


def get_callable_weak_ref(handler, callback=None):
    if isinstance(handler, MethodType):
        return weakref.WeakMethod(handler, callback)
    else:
        return weakref.ref(handler, callback)


class MySignal(Generic[T]):
    def __init__(self) -> None:
        self.handlers: Set[weakref.ReferenceType] = set()

    def connect(self, handler: Callable):
        self.handlers.add(get_callable_weak_ref(handler, self.remove_ref))

    def disconnect(self, handler: Callable):
        ref = get_callable_weak_ref(handler)
        self.remove_ref(ref)

    def remove_ref(self, handler_ref):
        self.handlers.discard(handler_ref)

    @overload
    def emit(self, args: T): ...
    @overload
    def emit(self, *args, **kwargs): ...

    def emit(self, *args, **kwargs):
        # emit; one failing handler must not prevent the others from running.
        # handlers live in a set, so which error propagates first is arbitrary;
        # the propagated one goes to the caller (a task logs it, an
        # unguarded caller surfaces it to the top-level exception handler)
        first_error = None
        for handler in list(self.handlers):
            try:
                handler()(*args, **kwargs)
            except Exception as e:
                if first_error is None:
                    first_error = e
                else:
                    logger = logging.getLogger("Orbitool")
                    logger.error(str(e), exc_info=e)
        if first_error is not None:
            raise first_error


class DataBindSignal(Generic[T]):
    def __init__(self) -> None:
        self.handlers: Dict[str, weakref.ReferenceType] = {}

    def connect(self, label: str, handler: Callable):
        self.handlers[label] = get_callable_weak_ref(
            handler, lambda x: self.remove_label(label))

    def remove_label(self, label):
        self.handlers.pop(label, None)

    @overload
    def emit_except(self, except_label, arg: T):
        pass

    @overload
    def emit_except(self, except_label, *args, **kwargs):
        pass

    def emit_except(self, except_label, *args, **kwargs):
        for label, handler in self.handlers.items():
            if except_label != label:
                handler()(*args, **kwargs)

    def emit(self, *args, **kwargs):
        for handler in self.handlers.values():
            handler()(*args, **kwargs)


class ValueGetter(Generic[T]):
    def __init__(self) -> None:
        self.getter = None

    def connect(self, getter):
        self.getter = getter

    def get(self) -> T:
        if self.getter is None:
            raise RuntimeError("Haven't connect to a value getter")
        return self.getter()
