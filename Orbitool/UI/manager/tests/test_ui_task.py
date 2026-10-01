import importlib
import logging
import threading
import time
import traceback

import pytest
from PyQt6 import QtCore, QtWidgets

from Orbitool import setting
from ..manager import Manager
from ..state_node import node
from ..task import background, ui_task
from ..thread import MultiProcess

# the package rebinds the `ui_task` name, so the module itself must be
# resolved through importlib, not through attribute lookup
task_module = importlib.import_module("Orbitool.UI.manager.task")

# a QApplication with no references gets destroyed, breaking every event
# loop that runs afterwards
app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


class _Widget:
    def __init__(self):
        self.manager = Manager()
        self.manager.set_busy(False)


@pytest.fixture(autouse=True)
def debug_settings(monkeypatch):
    monkeypatch.setattr(setting.debug, "thread_block_gui", True)
    monkeypatch.setattr(setting.debug, "NO_MULTIPROCESS", True)


@pytest.fixture
def show_info(monkeypatch):
    calls = []
    monkeypatch.setattr(
        task_module, "showInfo",
        lambda *args, **kwargs: calls.append(args))
    return calls


def _wait_until(cond, timeout=5.0):
    deadline = time.monotonic() + timeout
    while not cond() and time.monotonic() < deadline:
        app.processEvents()
        QtCore.QThread.msleep(5)
    assert cond()


def worker_boom():
    raise ValueError("boom from worker")


class collect_p(MultiProcess):
    @staticmethod
    def func(input):
        return input

    @staticmethod
    def read(file, length):
        for i in range(length):
            yield i

    @staticmethod
    def read_len(file, length) -> int:
        return length

    @staticmethod
    def write(file, rets):
        target = []
        file["ret"] = target
        cnt = 0
        for ret in rets:
            target.append(ret)
            cnt += 1
        return cnt

    @staticmethod
    def exception(file, **kwargs):
        file.pop("ret", None)


@pytest.mark.parametrize("value", [0, (), None, False, ""])
def test_falsy_worker_result_reaches_after_await(value, show_info):
    widget = _Widget()
    captured = []

    @ui_task
    async def task(widget):
        captured.append(await background(lambda: value, "work"))
        captured.append(await background(lambda: value))

    task.func(widget)

    assert captured == [value, value]
    assert not widget.manager.busy
    assert show_info == []


def test_default_mode_takes_busy_until_task_finishes(show_info):
    widget = _Widget()
    seen = []

    @ui_task
    async def task(widget):
        seen.append(("start", widget.manager.busy))
        await background(lambda: seen.append(("worker", widget.manager.busy)))
        seen.append(("resume", widget.manager.busy))

    task.func(widget)

    assert seen == [("start", True), ("worker", True), ("resume", True)]
    assert not widget.manager.busy
    assert show_info == []


def test_default_mode_rejects_start_while_busy(show_info):
    widget = _Widget()
    widget.manager.set_busy(True)
    ran = []

    @ui_task
    async def task(widget):
        ran.append(True)

    task.func(widget)

    assert ran == []
    assert show_info == [("Wait for process", 'busy')]
    assert widget.manager.busy


def test_worker_exception_caught_at_await_point(show_info):
    widget = _Widget()
    captured = []

    @ui_task
    async def task(widget):
        try:
            await background(worker_boom, "work")
        except ValueError as e:
            captured.append(str(e))
            captured.append(await background(lambda: "resumed"))
        finally:
            captured.append("finally")

    task.func(widget)

    assert captured == ["boom from worker", "resumed", "finally"]
    assert show_info == []
    assert not widget.manager.busy


def test_uncaught_worker_exception_logged_shown_and_busy_reset(
        show_info, caplog):
    widget = _Widget()
    reached = []

    @ui_task
    async def task(widget):
        try:
            await background(worker_boom, "work")
        finally:
            reached.append("finally")
        reached.append("after")

    with caplog.at_level(logging.ERROR, logger="Orbitool"):
        task.func(widget)

    assert reached == ["finally"]
    with_traceback = [record for record in caplog.records if record.exc_info]
    assert with_traceback, "worker exception must be logged with exc_info"
    formatted = "".join(
        traceback.format_exception(*with_traceback[-1].exc_info))
    assert "worker_boom" in formatted
    assert "boom from worker" in formatted
    assert show_info == [("boom from worker",)]
    assert not widget.manager.busy


def test_exception_in_task_body_logged_shown_and_busy_reset(
        show_info, caplog):
    widget = _Widget()

    @ui_task
    async def task(widget):
        raise RuntimeError("body boom")

    with caplog.at_level(logging.ERROR, logger="Orbitool"):
        task.func(widget)

    assert any(record.exc_info for record in caplog.records)
    assert show_info and "body boom" in show_info[0][0]
    assert not widget.manager.busy


def test_background_rejects_non_callable_payload(show_info):
    widget = _Widget()

    @ui_task
    async def task(widget):
        await background(42)

    task.func(widget)

    assert show_info and "background" in show_info[0][0]
    assert not widget.manager.busy


def test_background_accepts_three_payload_forms(show_info):
    widget = _Widget()
    captured = []
    msgs = []
    widget.manager.msg.connect(msgs.append)

    @ui_task
    async def task(widget):
        captured.append(await background(lambda: "closure"))
        captured.append(await background(lambda: "closure+msg", "working"))
        file = {}
        captured.append(
            await background(collect_p(file, {"length": 3}), "multiprocess"))
        captured.append(file)

    task.func(widget)

    assert captured == ["closure", "closure+msg", 3, {"ret": [0, 1, 2]}]
    assert msgs == ["processing", "working", "multiprocess"]
    assert not widget.manager.busy
    assert show_info == []


def test_finally_runs_on_main_thread_with_real_worker_thread(
        monkeypatch, show_info):
    monkeypatch.setattr(setting.debug, "thread_block_gui", False)
    widget = _Widget()
    main_ident = threading.get_ident()
    worker_idents = []
    resumed = []

    def work():
        worker_idents.append(threading.get_ident())
        return "done"

    @ui_task
    async def task(widget):
        try:
            resumed.append(("body", threading.get_ident(),
                            await background(work, "work")))
        finally:
            resumed.append(("finally", threading.get_ident()))

    task.func(widget)
    assert widget.manager.busy
    _wait_until(lambda: not widget.manager.busy)

    assert worker_idents and worker_idents[0] != main_ident
    assert resumed == [("body", main_ident, "done"),
                       ("finally", main_ident)]
    assert show_info == []


def test_descriptor_binding_and_parenthesized_decorator(show_info):
    class W(_Widget):
        @ui_task()
        async def task(self):
            self.done = True

    w = W()
    w.task()

    assert w.done
    assert not w.manager.busy
    assert show_info == []


def test_unknown_mode_rejected_at_decoration():
    with pytest.raises(ValueError):
        ui_task(mode="bogus")


def test_non_callable_positional_argument_rejected():
    with pytest.raises(TypeError):
        ui_task("default")


def test_legacy_generator_and_new_coroutine_share_manager(show_info):
    widget = _Widget()
    captured = []

    @node
    def legacy(widget):
        captured.append((yield (lambda: "legacy"), "old work"))

    @ui_task
    async def new(widget):
        captured.append(await background(lambda: "new"))

    legacy.func(widget)
    new.func(widget)

    assert captured == ["legacy", "new"]
    assert not widget.manager.busy
    assert show_info == []
