"""Session-wide guards for the process-wide ``Orbitool`` logger.

``Orbitool.logger`` configures a logger that lives for the whole process, so
every test shares it: one test can leave a handler, a level or ``propagate``
behind for all the later ones — and, because ``build.py`` runs ``pytest.main``
inside its own process, for the packaging run too.  This module

* moves the application's file log out of the repository for the duration of
  the run — to `.pytest_cache/orbitool-tests.log`, or to the system temporary
  directory when that cannot be written, or nowhere at all when neither can be
  — so the suite never writes to the ``log.txt`` a user sends to support, and
* snapshots the logger around every test, warns when the test left it
  reconfigured, and puts the old configuration back.

A test is free to attach a handler to see what a task logged; it just has to
put it back, or it will hear about it.
"""

import logging
import tempfile
import warnings
from pathlib import Path

import pytest

APP_LOGGER = "Orbitool"
REPO_ROOT = Path(__file__).resolve().parent
TEST_LOG = REPO_ROOT / ".pytest_cache" / "orbitool-tests.log"


def _is_pytest_handler(handler: logging.Handler) -> bool:
    """Whether pytest owns this handler (it attaches and detaches it itself).

    ``catching_logs`` puts its capture handlers on the root logger *and* on
    every logger with ``propagate = False``, so a test that stops propagation
    sees them appear on the application logger during its own teardown.
    """
    return type(handler).__module__.startswith("_pytest")


def _file_handlers_in_repo(logger: logging.Logger):
    """The logger's file handlers that write inside the repository."""
    for handler in list(logger.handlers):
        if not isinstance(handler, logging.FileHandler):
            continue
        path = Path(handler.baseFilename).resolve()
        if path == TEST_LOG or REPO_ROOT not in path.parents:
            continue
        yield handler


def _test_log_handler() -> logging.Handler:
    """A handler for the test log, or a null handler when nothing is writable.

    Dropping records is the last resort: writing them to the repository's own
    ``log.txt`` is the one thing this must not do.
    """
    for path in (TEST_LOG, Path(tempfile.gettempdir()) / "orbitool-tests.log"):
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            return logging.FileHandler(path, mode="a", encoding="utf-8")
        except OSError:
            continue
    return logging.NullHandler()


def _log_outside_the_repo(logger: logging.Logger) -> None:
    """Point the application's file log at the test log.

    Runs on every test but only acts on the first one: once the handler points
    at the test log, `_file_handlers_in_repo` finds nothing left to move.
    """
    for handler in _file_handlers_in_repo(logger):
        replacement = _test_log_handler()
        replacement.setLevel(handler.level)
        replacement.setFormatter(handler.formatter)
        logger.handlers[logger.handlers.index(handler)] = replacement
        handler.close()


@pytest.fixture(autouse=True)
def _isolate_orbitool_logger():
    logger = logging.getLogger(APP_LOGGER)
    _log_outside_the_repo(logger)
    handlers = list(logger.handlers)
    level = logger.level
    propagate = logger.propagate

    yield

    leaked = []
    added = [
        h for h in logger.handlers
        if h not in handlers and not _is_pytest_handler(h)]
    removed = [h for h in handlers if h not in logger.handlers]
    if added or removed:
        leaked.append(
            f"handlers +{[type(h).__name__ for h in added]}"
            f" -{[type(h).__name__ for h in removed]}")
    if logger.level != level:
        leaked.append(
            f"level {logging.getLevelName(level)}"
            f" -> {logging.getLevelName(logger.level)}")
    if logger.propagate is not propagate:
        leaked.append(f"propagate {propagate} -> {logger.propagate}")

    # put the application's handlers back in their original order, leaving
    # pytest's own capture handlers attached where they are
    logger.handlers[:] = handlers + [
        h for h in logger.handlers
        if _is_pytest_handler(h) and h not in handlers]
    logger.setLevel(level)
    logger.propagate = propagate

    if leaked:
        warnings.warn(
            f"this test left the {APP_LOGGER!r} logger reconfigured"
            f" ({'; '.join(leaked)}); conftest.py restored it",
            pytest.PytestWarning)
