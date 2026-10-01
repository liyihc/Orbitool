import functools
import inspect
import logging
from typing import Any, Callable, Optional

from PyQt6 import QtCore

from ... import setting
from ..utils import showInfo, sleep
from .manager import Manager
from .thread import EXCEPTION, Thread

logger = logging.getLogger("Orbitool")


class Step:
    """
    One background step, handed from an awaited `background(...)` call to
    the driver. `__await__` suspends exactly once (`yield self`) so the
    driver can run the worker and send the result (or throw the worker
    exception) back to the await point.
    """
    __slots__ = ("work", "msg")

    def __init__(self, work: Any, msg: str = "processing") -> None:
        self.work = work
        self.msg = msg

    def __await__(self):
        result = yield self
        return result


def background(work: Any, msg: str = "processing") -> Step:
    """
    Worker boundary for `ui_task` coroutines: `await background(...)`
    suspends the task, runs `work` (a callable or an already constructed
    Thread/MultiProcess) on a worker thread with progress message `msg`,
    and resumes with its result — or with its exception thrown at the
    await point.
    """
    if not isinstance(work, QtCore.QThread) and not callable(work):
        raise TypeError(
            "background() expects a callable or a Thread/MultiProcess"
            f" instance, got {work!r}")
    return Step(work, msg)


class Driver:
    """
    Shared engine for both task styles: advances a legacy generator
    (`yield` payload style) or a coroutine (`await background(...)` style)
    through the same send/throw protocol, launching each yielded step on a
    worker thread and resuming on the main thread.
    """
    def __init__(self, container: Any, *, manager: Manager,
                 on_done: Callable[[], None],
                 on_error: Callable[[BaseException], None]) -> None:
        if not (hasattr(container, "send") and hasattr(container, "throw")):
            raise TypeError(
                f"task must be a generator or coroutine, got {container!r}")
        self.container = container
        self.is_coroutine = inspect.iscoroutine(container)
        self.manager = manager
        self.on_done = on_done
        self.on_error = on_error
        self._finished = False

        def deliver(payload: tuple):
            self._on_worker_finished(payload)
        self._deliver = deliver

    def start(self) -> None:
        self._advance(None, None)

    def _advance(self, value: Any, exc: Optional[BaseException]) -> None:
        try:
            if exc is None:
                yielded = self.container.send(value)
            else:
                yielded = self.container.throw(exc)
            self._launch(yielded)
        except StopIteration:
            self._complete()
        except Exception as e:
            self._fail(e)

    def _on_worker_finished(self, payload: tuple) -> None:
        channel, value = payload[0], payload[1]
        if channel != EXCEPTION:
            self._advance(value, None)
        elif self.is_coroutine:
            self._advance(None, value)
        else:
            self._fail(value)

    def _launch(self, yielded: Any) -> None:
        if self.is_coroutine:
            if not isinstance(yielded, Step):
                raise TypeError(
                    "only background(...) steps can be awaited,"
                    f" got {yielded!r}")
            work, msg = yielded.work, yielded.msg
        elif isinstance(yielded, tuple):
            work, msg = yielded
        else:
            work, msg = yielded, "processing"
        manager = self.manager
        manager.msg.emit(msg)
        thread = work if isinstance(work, QtCore.QThread) else Thread(work)
        thread.set_tqdmer(manager.tqdm)
        thread.finished.connect(self._deliver)
        manager.running_thread = thread
        if setting.debug.thread_block_gui:
            thread.run()
        else:
            thread.start()

    def _complete(self) -> None:
        if self._finished:
            return
        self._finished = True
        self.on_done()

    def _fail(self, e: BaseException) -> None:
        if self._finished:
            return
        self._finished = True
        self.on_error(e)


class ui_task:
    """
    Decorator for async UI tasks: `@ui_task` on an `async def` method,
    worker boundaries written as `await background(...)`. The wrapper
    enforces the mode's busy policy (default mode: busy -> refuse with a
    prompt, idle -> take busy, release on finish or error) and drives the
    coroutine through the shared Driver. Uncaught task/worker exceptions
    are logged with traceback, shown via one uniform dialog, and release
    busy before the chain terminates.
    """
    def __init__(self, func: Optional[Callable] = None, *,
                 mode: str = "default") -> None:
        if mode not in ("default",):
            raise ValueError(f"unsupported ui_task mode: {mode!r}")
        if func is not None and not callable(func):
            raise TypeError(
                f"ui_task expects a callable task function, got {func!r}")
        self._func = func
        self._mode = mode
        self._bind_cache = functools.lru_cache(None)(self._bind)

    @property
    def func(self) -> Optional[Callable]:
        func = self._func
        if func is None:
            return None

        @functools.wraps(func)
        def wrapper(selfWidget, *args, **kwargs):
            manager: Manager = selfWidget.manager
            if manager.busy:
                showInfo("Wait for process", 'busy')
                return
            manager.set_busy(True)
            sleep(.05)

            def on_done():
                manager.set_busy(False)

            def on_error(e: BaseException):
                logger.error(str(e), exc_info=e)
                showInfo(str(e))
                manager.set_busy(False)

            try:
                driver = Driver(
                    func(selfWidget, *args, **kwargs), manager=manager,
                    on_done=on_done, on_error=on_error)
            except Exception as e:
                on_error(e)
                return
            driver.start()

        return wrapper

    def __call__(self, func: Callable):
        if self._func is not None:
            raise RuntimeError("ui_task is already bound to a function")
        self._func = func
        return self

    def __get__(self, obj, objtype=None):
        if obj is None or isinstance(obj, ui_task):
            return self
        return self._bind_cache(obj)

    def _bind(self, obj):
        return functools.partial(self.func, obj)
