import importlib
import logging
import traceback

import pytest
from PyQt6 import QtWidgets

from Orbitool import setting
from ..manager import Manager
from ..state_node import node
from ..thread import MultiProcess

# the package rebinds the `state_node` name to the node class, so the module
# itself must be resolved through importlib, not through attribute lookup
state_node_module = importlib.import_module("Orbitool.UI.manager.state_node")

# a QApplication with no references gets destroyed, breaking every event
# loop (state_node's busy sleep) that runs afterwards
app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


class _Widget:
    def __init__(self):
        self.manager = Manager()
        self.manager.set_busy(False)


class _Collect(MultiProcess):
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


@pytest.fixture(autouse=True)
def debug_settings(monkeypatch):
    monkeypatch.setattr(setting.debug, "thread_block_gui", True)
    monkeypatch.setattr(setting.debug, "NO_MULTIPROCESS", True)


@pytest.fixture
def show_info(monkeypatch):
    calls = []
    monkeypatch.setattr(
        state_node_module, "showInfo",
        lambda *args, **kwargs: calls.append(args))
    return calls


@pytest.mark.parametrize("value", [0, (), None, False, ""])
def test_falsy_worker_result_reaches_resume_point(value, show_info):
    widget = _Widget()
    captured = []

    @node
    def task(widget):
        captured.append((yield (lambda: value), "work"))

    task.func(widget)

    assert captured == [value]
    assert not widget.manager.busy
    assert show_info == []


def worker_boom():
    raise ValueError("boom from worker")


def test_exception_instance_as_return_value_passes_through(show_info):
    # an Exception delivered through the RESULT channel is data, not a
    # failure: the old truthiness/isinstance check re-raised it as an error
    widget = _Widget()
    captured = []
    sentinel = ValueError("returned, not raised")

    @node
    def task(widget):
        captured.append((yield (lambda: sentinel), "work"))

    task.func(widget)

    assert len(captured) == 1
    assert captured[0] is sentinel
    assert show_info == []
    assert not widget.manager.busy


def test_worker_exception_logs_worker_traceback(show_info, caplog):
    widget = _Widget()

    @node
    def task(widget):
        yield worker_boom, "work"

    with caplog.at_level(logging.ERROR, logger="Orbitool"):
        task.func(widget)

    with_traceback = [record for record in caplog.records if record.exc_info]
    assert with_traceback, "worker exception must be logged with exc_info"
    formatted = "".join(
        traceback.format_exception(*with_traceback[-1].exc_info))
    assert "worker_boom" in formatted
    assert "boom from worker" in formatted

    assert show_info and "boom from worker" in show_info[0][0]
    assert not widget.manager.busy


def test_yield_worker_instance_payload(show_info):
    widget = _Widget()
    msgs = []
    widget.manager.msg.connect(msgs.append)
    captured = []

    @node
    def task(widget):
        file = {}
        captured.append(
            (yield _Collect(file, {"length": 3}), "multiprocess work"))
        captured.append(file)

    task.func(widget)

    assert captured == [3, {"ret": [0, 1, 2]}]
    assert msgs == ["multiprocess work"]
    assert not widget.manager.busy
    assert show_info == []
