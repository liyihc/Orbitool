import functools
import inspect
import logging
import weakref
from typing import Any, Callable, Optional

from PyQt6 import QtCore

from ... import setting
from ..utils import showInfo, sleep
from .manager import Manager
from .thread import EXCEPTION, Thread

logger = logging.getLogger("Orbitool")

_TASK_MODES = ("default", "join", "light")


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
    Coroutine driver: advances a `ui_task` coroutine through the
    send/throw protocol, launching each awaited `background(...)` step on
    a worker thread and resuming on the main thread.
    """
    def __init__(self, container: Any, *, manager: Manager,
                 on_done: Callable[[], None],
                 on_error: Callable[[BaseException], None]) -> None:
        if not inspect.iscoroutine(container):
            raise TypeError(
                f"task must be a coroutine, got {container!r}")
        self.container = container
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
        else:
            self._advance(None, value)

    def _launch(self, yielded: Any) -> None:
        if not isinstance(yielded, Step):
            raise TypeError(
                "only background(...) steps can be awaited,"
                f" got {yielded!r}")
        work, msg = yielded.work, yielded.msg
        manager = self.manager
        manager.msg.emit(msg)
        thread = work if isinstance(work, QtCore.QThread) else Thread(work)
        thread.set_tqdmer(manager.tqdm)
        if setting.debug.thread_block_gui:
            thread.result_ready.connect(self._deliver)  # inline, same thread
        else:
            thread.result_ready.connect(
                self._deliver, QtCore.Qt.ConnectionType.QueuedConnection)
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


def _forward_arguments(sig: inspect.Signature, func: Callable,
                       host: Any, args: tuple, kwargs: dict):
    """
    Trickle one slot invocation's arguments down to what the decorated
    coroutine's signature declares (its first, host parameter excluded
    when that parameter can take the host positionally — a leading
    `*args` with no declared self keeps the host in the forwarded set
    and `sig.bind` drops it into the varargs):

    - positional arguments are truncated to the declared positional
      slots (all of them when the coroutine declares `*args`);
    - keyword arguments are kept only when a declared parameter or
      `**kwargs` can absorb them (dropped ones are logged at debug);
    - what remains must still bind: a required parameter that cannot be
      filled raises a clear TypeError instead of being silently
      dropped (duplicates of a positionally filled parameter likewise).

    Returns the (positional, keyword) pair to call `func(host, ...)` with.
    """
    name = getattr(func, "__qualname__", None) or repr(func)
    parameters = list(sig.parameters.values())
    if parameters and parameters[0].kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD):
        parameters = parameters[1:]
    positional_count = 0
    var_positional = False
    for param in parameters:
        if param.kind in (inspect.Parameter.POSITIONAL_ONLY,
                          inspect.Parameter.POSITIONAL_OR_KEYWORD):
            positional_count += 1
        elif param.kind is inspect.Parameter.VAR_POSITIONAL:
            var_positional = True
            break
        else:
            break
    if var_positional:
        positional = tuple(args)
    else:
        positional = tuple(args[:positional_count])

    var_keyword = any(param.kind is inspect.Parameter.VAR_KEYWORD
                      for param in parameters)
    accepted = {param.name for param in parameters
                if param.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                  inspect.Parameter.KEYWORD_ONLY)}
    forwarded = {}
    for key, value in kwargs.items():
        if var_keyword or key in accepted:
            forwarded[key] = value
        else:
            logger.debug(
                "dropping keyword argument %r: %s does not declare it",
                key, name)

    try:
        sig.bind(host, *positional, **forwarded)
    except TypeError as exc:
        raise TypeError(
            f"cannot forward call arguments args={args!r}"
            f" kwargs={kwargs!r} to {name}: {exc}") from exc
    return positional, forwarded


class ui_task:
    """
    Decorator for async UI tasks: `@ui_task` on an `async def` method,
    worker boundaries written as `await background(...)`. The wrapper
    enforces the mode's busy policy and drives the coroutine through the
    shared Driver. Slot call arguments are forwarded according to the
    decorated coroutine's own signature — excess positional arguments
    are truncated, extra keywords are dropped unless `**kwargs` absorbs
    them, and an unbindable required parameter raises through the
    uniform error fallback — so no argument switch is needed. Method
    binding is cached with weak references, so closed hosts can be
    garbage collected. `mode` accepts exactly three words (no letter aliases):

    - default: hold busy, refuse to start while busy ("Wait for process");
    - join: hold busy, start even while busy (pipeline relay);
    - light: never touch busy, error fallback only.

    default/join tasks follow the counting rule: Manager.begin_task at
    start (+1), Manager.end_task at finish (+0/-1), so busy stays until
    the last holder finishes — each task only returns the count it took.
    Uncaught task/worker exceptions are logged with traceback, shown via
    one uniform dialog, and release the task's count (light: nothing)
    before the chain terminates.
    """
    def __init__(self, func: Optional[Callable] = None, *,
                 mode: str = "default") -> None:
        if mode not in _TASK_MODES:
            raise ValueError(f"unsupported ui_task mode: {mode!r}")
        if func is not None and not callable(func):
            raise TypeError(
                f"ui_task expects a callable task function, got {func!r}")
        self._func = func
        self._signature = inspect.signature(func) if func is not None else None
        self._mode = mode
        self._bind_cache = weakref.WeakKeyDictionary()

    @property
    def func(self) -> Optional[Callable]:
        func = self._func
        if func is None:
            return None

        @functools.wraps(func)
        def wrapper(selfWidget, *args, **kwargs):
            manager: Manager = selfWidget.manager
            mode = self._mode
            counts = mode != "light"
            if mode == "default" and manager.busy:
                showInfo("Wait for process", 'busy')
                return
            if counts:
                was_idle = not manager.busy
                manager.begin_task()
                if was_idle:
                    sleep(.05)

            def on_done():
                if counts:
                    manager.end_task()

            def on_error(e: BaseException):
                logger.error(str(e), exc_info=e)
                try:
                    showInfo(str(e))
                except Exception:
                    logger.error(
                        "failed to show the task error dialog", exc_info=True)
                finally:
                    if counts:
                        manager.end_task()

            try:
                pos_args, kw_args = _forward_arguments(
                    self._signature, func, selfWidget, args, kwargs)
                driver = Driver(
                    func(selfWidget, *pos_args, **kw_args), manager=manager,
                    on_done=on_done, on_error=on_error)
            except Exception as e:
                on_error(e)
                return
            driver.start()

        return wrapper

    def __call__(self, func: Callable):
        if self._func is not None:
            raise RuntimeError("ui_task is already bound to a function")
        signature = inspect.signature(func)
        self._func = func
        self._signature = signature
        return self

    def __get__(self, obj, objtype=None):
        if obj is None or isinstance(obj, ui_task):
            return self
        try:
            cached = self._bind_cache.get(obj)
        except TypeError:
            # host is not hashable or not weakref-able: bind without caching
            return self._bind(obj)
        if cached is not None:
            return cached
        bound = self._bind(obj)
        self._bind_cache[obj] = bound
        return bound

    def _bind(self, obj):
        if self._func is None:
            raise TypeError(
                "ui_task has no task function; decorate a function with it"
                " before binding")
        wrapper = self.func
        name = getattr(self._func, "__qualname__", None) or repr(self._func)
        try:
            ref = weakref.ref(obj)
        except TypeError:
            # hosts without weak-reference support (e.g. __slots__ without
            # __weakref__) get a plain strong binding, never cached
            return functools.partial(wrapper, obj)

        @functools.wraps(self._func)
        def bound(*args, **kwargs):
            host = ref()
            if host is None:
                raise ReferenceError(
                    f"cannot call {name}: its host object has been"
                    " garbage collected")
            return wrapper(host, *args, **kwargs)

        return bound
