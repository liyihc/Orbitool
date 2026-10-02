from contextvars import ContextVar
from typing import Iterable, Optional, Sized

from .manager import TQDM, TQDMER

# The reporter the running worker should report through. Installed by the
# driver for the duration of a `background(...)` worker call (see
# `Thread.run` / `MultiProcess.run`); absent everywhere else (main-thread
# segments, plain slots), hence the ContextVar default of None.
_current: ContextVar[Optional[TQDMER]] = ContextVar(
    "Orbitool_progress", default=None)


def _noop(percent: int, msg: str) -> None:
    pass


class ProgressScope:
    """
    Install `reporter` for the duration of a worker call. Used by `Thread.run`
    and `MultiProcess.run`; the driver already hands the reporter over via
    `set_tqdmer`.
    """
    __slots__ = ("reporter", "_token")

    def __init__(self, reporter: Optional[TQDMER]) -> None:
        self.reporter = reporter
        self._token = None

    def __enter__(self) -> "ProgressScope":
        self._token = _current.set(self.reporter)
        return self

    def __exit__(self, *exc) -> None:
        _current.reset(self._token)


class _Progress:
    """
    Module-level accessor for the reporter of the running worker:

        for peak in progress.tqdm(peaks, msg="calc formulas"):
            ...

    Inside a `background(...)` worker it resolves to that step's reporter.
    With no worker context (main-thread code) it is a harmless no-op — it
    never raises. Worker code needs no reference to `Manager`.
    """
    __slots__ = ()

    def tqdm(self, iter: Iterable = None, msg: str = "", *,
             length: int = None, immediate: bool = False) -> TQDM:
        reporter = _current.get()
        if reporter is None:
            if iter is not None and length is None:
                length = len(iter) if isinstance(iter, Sized) else 0
            return TQDM(_noop, iter, length or 0, msg)
        return reporter(iter, msg, length=length, immediate=immediate)


progress = _Progress()
