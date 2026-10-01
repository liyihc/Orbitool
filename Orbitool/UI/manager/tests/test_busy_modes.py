import importlib
import logging
import threading
import time

import pytest
from PyQt6 import QtCore, QtWidgets

from Orbitool import setting
from ..manager import Manager
from ..state_node import node
from ..task import background, ui_task

task_module = importlib.import_module("Orbitool.UI.manager.task")
state_node_module = importlib.import_module("Orbitool.UI.manager.state_node")

# a QApplication with no references gets destroyed, breaking every event
# loop that runs afterwards (state_node's / ui_task's busy sleep)
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


@pytest.fixture
def show_node_info(monkeypatch):
    calls = []
    monkeypatch.setattr(
        state_node_module, "showInfo",
        lambda *args, **kwargs: calls.append(args))
    return calls


@pytest.fixture
def held_threads(monkeypatch):
    # Driver only keeps the newest thread on manager.running_thread; while
    # two real-thread tasks overlap, earlier workers would otherwise be
    # garbage-collected mid-run, so keep every Thread created in this test
    held = []
    original = task_module.Thread

    class HeldThread(original):
        def __init__(self, func, args=(), kwargs={}):
            super().__init__(func, args, kwargs)
            held.append(self)

    monkeypatch.setattr(task_module, "Thread", HeldThread)
    return held


def _wait_until(cond, timeout=5.0):
    deadline = time.monotonic() + timeout
    while not cond() and time.monotonic() < deadline:
        app.processEvents()
        QtCore.QThread.msleep(5)
    assert cond()


def worker_boom():
    raise ValueError("boom from worker")


@pytest.mark.parametrize("letter", ["w", "x", "a", "e", "n"])
def test_letter_mode_aliases_rejected_at_decoration(letter):
    with pytest.raises(ValueError):
        ui_task(mode=letter)


def test_light_runs_without_touching_busy_or_signal(show_info):
    widget = _Widget()
    events = []
    widget.manager.busy_signal.connect(events.append)
    seen = []

    @ui_task(mode="light")
    async def task(widget):
        seen.append(widget.manager.busy)
        await background(lambda: "work", "work")

    task.func(widget)

    assert seen == [False]
    assert not widget.manager.busy
    assert events == []
    assert show_info == []


def test_light_error_shows_dialog_but_leaves_busy_alone(show_info, caplog):
    widget = _Widget()
    widget.manager.set_busy(True)
    events = []
    widget.manager.busy_signal.connect(events.append)

    @ui_task(mode="light")
    async def task(widget):
        raise RuntimeError("light boom")

    with caplog.at_level(logging.ERROR, logger="Orbitool"):
        task.func(widget)

    assert any(record.exc_info for record in caplog.records)
    assert show_info and "light boom" in show_info[0][0]
    assert widget.manager.busy
    assert events == []


def test_default_refused_when_count_holds_busy(
        show_info, held_threads, monkeypatch):
    monkeypatch.setattr(setting.debug, "thread_block_gui", False)
    widget = _Widget()
    release = threading.Event()
    join_finished = threading.Event()
    default_ran = []

    @ui_task(mode="join")
    async def join_task(widget):
        await background(lambda: release.wait(5), "join")
        join_finished.set()

    @ui_task
    async def default_task(widget):
        default_ran.append(True)

    join_task.func(widget)
    assert widget.manager.busy

    default_task.func(widget)

    assert default_ran == []
    assert show_info == [("Wait for process", 'busy')]
    assert widget.manager.busy

    release.set()
    _wait_until(lambda: join_finished.is_set() and not widget.manager.busy)
    assert show_info == [("Wait for process", 'busy')]


def test_join_returns_only_the_count_it_took(show_info):
    widget = _Widget()
    widget.manager.set_busy(True)
    events = []
    widget.manager.busy_signal.connect(events.append)
    seen = []

    @ui_task(mode="join")
    async def join_task(widget):
        seen.append(widget.manager.busy)
        await background(lambda: "ok")

    join_task.func(widget)

    assert seen == [True]
    assert widget.manager.busy
    assert events == []
    widget.manager.set_busy(False)
    assert not widget.manager.busy
    assert events == [False]


def test_default_error_releases_count_with_busy_edges(show_info, caplog):
    widget = _Widget()
    events = []
    widget.manager.busy_signal.connect(events.append)

    @ui_task
    async def task(widget):
        await background(worker_boom, "work")

    with caplog.at_level(logging.ERROR, logger="Orbitool"):
        task.func(widget)

    assert events == [True, False]
    assert not widget.manager.busy
    assert show_info == [("boom from worker",)]


def test_join_error_releases_count_with_busy_edges(show_info, caplog):
    widget = _Widget()
    events = []
    widget.manager.busy_signal.connect(events.append)

    @ui_task(mode="join")
    async def task(widget):
        await background(worker_boom, "work")

    with caplog.at_level(logging.ERROR, logger="Orbitool"):
        task.func(widget)

    assert events == [True, False]
    assert not widget.manager.busy
    assert show_info == [("boom from worker",)]


def test_dialog_failure_still_returns_count_without_leaking(caplog,
                                                             monkeypatch):
    widget = _Widget()
    events = []
    widget.manager.busy_signal.connect(events.append)

    def broken_dialog(*args, **kwargs):
        raise RuntimeError("dialog boom")

    monkeypatch.setattr(task_module, "showInfo", broken_dialog)

    @ui_task
    async def task(widget):
        await background(worker_boom, "work")

    with caplog.at_level(logging.ERROR, logger="Orbitool"):
        task.func(widget)

    assert not widget.manager.busy
    assert events == [True, False]
    messages = [record.getMessage() for record in caplog.records]
    assert any("boom from worker" in m for m in messages)
    assert any("failed to show the task error dialog" in m
               for m in messages)


def test_end_task_without_begin_warns_and_keeps_count(caplog):
    widget = _Widget()
    events = []
    widget.manager.busy_signal.connect(events.append)

    with caplog.at_level(logging.WARNING, logger="Orbitool"):
        widget.manager.end_task()

    assert any("begin_task" in record.getMessage()
               for record in caplog.records)
    assert events == []
    assert not widget.manager.busy

    widget.manager.begin_task()
    assert widget.manager.busy
    assert events == [True]


def test_nested_inner_finishes_first_busy_held_until_outer_finishes(
        show_info):
    widget = _Widget()
    events = []
    widget.manager.busy_signal.connect(events.append)
    inner_seen = []
    after_inner = []

    @ui_task(mode="join")
    async def inner(widget):
        inner_seen.append(widget.manager.busy)
        await background(lambda: "inner")

    @ui_task
    async def outer(widget):
        inner.func(widget)
        after_inner.append(widget.manager.busy)
        await background(lambda: "outer")

    outer.func(widget)

    assert inner_seen == [True]
    assert after_inner == [True]
    assert events == [True, False]
    assert not widget.manager.busy
    assert show_info == []


def test_nested_outer_finishes_first_busy_held_until_inner_finishes(
        show_info, held_threads, monkeypatch):
    monkeypatch.setattr(setting.debug, "thread_block_gui", False)
    widget = _Widget()
    events = []
    widget.manager.busy_signal.connect(events.append)
    release = threading.Event()
    inner_finished = threading.Event()

    @ui_task(mode="join")
    async def inner(widget):
        await background(lambda: release.wait(5), "inner")
        inner_finished.set()

    @ui_task
    async def outer(widget):
        inner.func(widget)

    outer.func(widget)

    assert widget.manager.busy
    assert events == [True]

    release.set()
    _wait_until(lambda: inner_finished.is_set() and not widget.manager.busy)
    assert events == [True, False]
    assert show_info == []


def test_old_task_and_new_join_hold_busy_until_both_finish(
        show_info, show_node_info, held_threads, monkeypatch):
    monkeypatch.setattr(setting.debug, "thread_block_gui", False)
    widget = _Widget()
    events = []
    widget.manager.busy_signal.connect(events.append)
    release_old = threading.Event()
    release_join = threading.Event()
    old_finished = threading.Event()
    join_finished = threading.Event()
    old_seen = []
    join_seen = []

    @node
    def old_task(widget):
        yield lambda: release_old.wait(5), "old work"
        old_seen.append(widget.manager.busy)
        old_finished.set()

    @ui_task(mode="join")
    async def join_task(widget):
        await background(lambda: release_join.wait(5), "new work")
        join_seen.append(widget.manager.busy)
        join_finished.set()

    old_task.func(widget)
    assert widget.manager.busy

    join_task.func(widget)
    assert widget.manager.busy
    assert events == [True]

    release_old.set()
    _wait_until(old_finished.is_set)
    assert old_seen == [True]
    assert widget.manager.busy
    assert events == [True]

    release_join.set()
    _wait_until(lambda: join_finished.is_set() and not widget.manager.busy)
    assert join_seen == [True]
    assert events == [True, False]
    assert show_info == []
    assert show_node_info == []


def test_new_default_refused_while_old_task_running(
        show_info, show_node_info, held_threads, monkeypatch):
    monkeypatch.setattr(setting.debug, "thread_block_gui", False)
    widget = _Widget()
    release = threading.Event()
    old_finished = threading.Event()
    new_ran = []

    @node
    def old_task(widget):
        yield lambda: release.wait(5), "old work"
        old_finished.set()

    @ui_task
    async def new_task(widget):
        new_ran.append(True)

    old_task.func(widget)
    new_task.func(widget)

    assert new_ran == []
    assert show_info == [("Wait for process", 'busy')]
    assert widget.manager.busy

    release.set()
    _wait_until(lambda: old_finished.is_set() and not widget.manager.busy)
    assert show_info == [("Wait for process", 'busy')]
    assert show_node_info == []


def test_old_default_refused_while_new_task_running(
        show_info, show_node_info, held_threads, monkeypatch):
    monkeypatch.setattr(setting.debug, "thread_block_gui", False)
    widget = _Widget()
    release = threading.Event()
    new_finished = threading.Event()
    old_ran = []

    @ui_task
    async def new_task(widget):
        await background(lambda: release.wait(5), "new work")
        new_finished.set()

    @node
    def old_task(widget):
        old_ran.append(True)

    new_task.func(widget)
    old_task.func(widget)

    assert old_ran == []
    assert show_node_info == [("Wait for process", 'busy')]
    assert show_info == []
    assert widget.manager.busy

    release.set()
    _wait_until(lambda: new_finished.is_set() and not widget.manager.busy)
    assert show_node_info == [("Wait for process", 'busy')]


def test_light_during_old_task_leaves_busy_signal_untouched(
        show_info, show_node_info, held_threads, monkeypatch):
    monkeypatch.setattr(setting.debug, "thread_block_gui", False)
    widget = _Widget()
    events = []
    widget.manager.busy_signal.connect(events.append)
    release = threading.Event()
    old_finished = threading.Event()
    light_finished = threading.Event()
    light_seen = []

    @node
    def old_task(widget):
        yield lambda: release.wait(5), "old work"
        old_finished.set()

    @ui_task(mode="light")
    async def light_task(widget):
        light_seen.append(widget.manager.busy)
        await background(lambda: "light work")
        light_finished.set()

    old_task.func(widget)
    assert widget.manager.busy

    light_task.func(widget)
    _wait_until(light_finished.is_set)

    assert light_seen == [True]
    assert widget.manager.busy
    assert events == [True]
    assert show_info == []
    assert show_node_info == []

    release.set()
    _wait_until(lambda: old_finished.is_set() and not widget.manager.busy)
    assert events == [True, False]


def test_join_error_keeps_busy_held_by_old_task(
        show_info, show_node_info, held_threads, monkeypatch):
    monkeypatch.setattr(setting.debug, "thread_block_gui", False)
    widget = _Widget()
    events = []
    widget.manager.busy_signal.connect(events.append)
    release = threading.Event()
    old_finished = threading.Event()

    @node
    def old_task(widget):
        yield lambda: release.wait(5), "old work"
        old_finished.set()

    @ui_task(mode="join")
    async def join_task(widget):
        await background(worker_boom, "work")

    old_task.func(widget)
    assert widget.manager.busy

    join_task.func(widget)
    _wait_until(lambda: len(show_info) >= 1)

    assert show_info == [("boom from worker",)]
    assert widget.manager.busy
    assert events == [True]

    release.set()
    _wait_until(lambda: old_finished.is_set() and not widget.manager.busy)
    assert events == [True, False]
    assert show_node_info == []
