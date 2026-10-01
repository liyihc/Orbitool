import gc
import importlib
import logging
import threading
import time
import traceback
import weakref

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


def test_slot_arguments_forwarded_by_signature(show_info):
    class W(_Widget):
        def __init__(self):
            super().__init__()
            self.seen = []

        @ui_task(mode="light")
        async def takes_all(self, first, second):
            self.seen.append(("all", first, second))

        @ui_task(mode="light")
        async def takes_one(self, skip):
            self.seen.append(("one", skip))

        @ui_task(mode="light")
        async def takes_none(self):
            self.seen.append(("none",))

        @ui_task(mode="light")
        async def takes_rest(self, first, **rest):
            self.seen.append(("rest", first, rest))

        @ui_task(mode="light")
        async def takes_varargs(self, *items):
            self.seen.append(("varargs", tuple(items)))

    w = W()
    w.takes_all(1, 2)                      # full signature -> everything
    w.takes_one(True, "extra-from-signal")  # partial -> excess truncated
    w.takes_one(skip=False)                # keyword form binds too
    w.takes_one(True, extra="dropped")     # unknown keyword dropped
    w.takes_none(1, 2, 3)                  # no parameters -> nothing
    w.takes_rest(1, x=2, y=3)              # **kwargs absorbs leftovers
    w.takes_varargs(1, 2, 3)               # *args accepts every positional

    assert w.seen == [
        ("all", 1, 2),
        ("one", True),
        ("one", False),
        ("one", True),
        ("none",),
        ("rest", 1, {"x": 2, "y": 3}),
        ("varargs", (1, 2, 3)),
    ]
    assert not w.manager.busy
    assert show_info == []


def test_unbindable_arguments_raise_clear_error_and_reset_busy(
        show_info, caplog):
    class W(_Widget):
        def __init__(self):
            super().__init__()
            self.ran = []

        @ui_task
        async def needs_required(self, required):
            self.ran.append(required)

    w = W()
    events = []
    w.manager.busy_signal.connect(events.append)

    with caplog.at_level(logging.ERROR, logger="Orbitool"):
        w.needs_required()  # required argument missing -> clear error

    assert w.ran == []
    with_traceback = [record for record in caplog.records if record.exc_info]
    assert with_traceback, "binding failure must be logged with exc_info"
    assert show_info and show_info[0][0].startswith(
        "cannot forward call arguments")
    assert "needs_required" in show_info[0][0]
    # begin_task ran before the failure, the fallback gave the count back
    assert events == [True, False]
    assert not w.manager.busy


def test_new_api_rejects_with_args_switch():
    async def sample(widget):
        pass

    with pytest.raises(TypeError):
        ui_task(withArgs=True)
    with pytest.raises(TypeError):
        ui_task(sample, withArgs=True)


def test_legacy_state_node_still_honors_with_args():
    widget = _Widget()
    received = []

    @node(withArgs=True)
    def legacy(widget, value):
        received.append(value)

    legacy.func(widget, 42)

    assert received == [42]
    assert not widget.manager.busy


def test_ui_task_binding_cache_releases_host():
    class W(_Widget):
        @ui_task(mode="light")
        async def task(self):
            pass

    w = W()
    ref = weakref.ref(w)
    bound = w.task
    assert bound is w.task  # binding identity is cached while host lives
    bound()                 # and the binding works

    del w
    gc.collect()
    assert ref() is None  # the cache keeps only a weak reference

    with pytest.raises(ReferenceError):
        bound()  # a stale binding fails loudly instead of crashing later


def test_legacy_state_node_binding_still_pins_host():
    # contrast group for the ui_task weak cache above: the old decorator
    # lru_caches __get__ with the host object as a strong key, so bound
    # hosts stay alive until state_node itself is deleted (ticket 12)
    class W:
        @node
        def legacy(self):
            if False:
                yield

    w = W()
    ref = weakref.ref(w)
    bound = w.legacy
    assert bound is w.legacy
    del w, bound
    gc.collect()
    assert ref() is not None  # strong-reference cache pins the host


def test_leading_varargs_without_self_keeps_host_and_signal_args(show_info):
    seen = []

    class W(_Widget):
        @ui_task(mode="light")
        async def seed(*args):  # no declared self: host lands in *args
            seen.append(args)

    w = W()
    w.seed(1, 2)

    assert seen == [(w, 1, 2)]  # host plus every signal argument, in order
    assert show_info == []


def test_duplicate_positional_and_keyword_argument_falls_back(
        show_info, caplog):
    class W(_Widget):
        def __init__(self):
            super().__init__()
            self.ran = []

        @ui_task
        async def two(self, a):
            self.ran.append(a)

    w = W()
    with caplog.at_level(logging.ERROR, logger="Orbitool"):
        w.two(1, a=2)

    assert w.ran == []  # binding failed before the coroutine was created
    assert any(record.exc_info for record in caplog.records)
    assert show_info and show_info[0][0].startswith(
        "cannot forward call arguments")
    assert "two" in show_info[0][0]
    assert not w.manager.busy  # begin/end pair gave the count back


def test_default_values_fill_omitted_arguments(show_info):
    class W(_Widget):
        def __init__(self):
            super().__init__()
            self.seen = []

        @ui_task(mode="light")
        async def defaulted(self, a=1, b=2):
            self.seen.append((a, b))

    w = W()
    w.defaulted()      # zero arguments -> every default
    w.defaulted(5)     # one argument -> a given, b default
    w.defaulted(b=7)   # keyword form -> b given, a default

    assert w.seen == [(1, 2), (5, 2), (1, 7)]
    assert show_info == []


def test_keyword_only_parameter_accepts_keyword_position_fails(show_info):
    class W(_Widget):
        def __init__(self):
            super().__init__()
            self.seen = []

        @ui_task(mode="light")
        async def kwonly(self, first, *, flag):
            self.seen.append((first, flag))

    w = W()
    w.kwonly(1, flag=True)
    assert w.seen == [(1, True)]

    w.kwonly(1, True)  # positional value cannot fill the keyword-only slot
    assert w.seen == [(1, True)]  # body not re-run
    assert show_info and show_info[0][0].startswith(
        "cannot forward call arguments")
    assert "flag" in show_info[0][0]


def test_signal_connect_truncates_and_disconnects_by_identity(show_info):
    class Emitter(QtCore.QObject):
        fired = QtCore.pyqtSignal(int, str)

    class W(_Widget):
        def __init__(self):
            super().__init__()
            self.seen = []
            self.emitter = Emitter()

        @ui_task(mode="light")
        async def slot(self, number):  # 1-parameter slot for a 2-arg signal
            self.seen.append(number)

    w = W()
    w.emitter.fired.connect(w.slot)
    w.emitter.fired.emit(7, "extra")  # excess positional truncated

    assert w.seen == [7]
    assert show_info == []

    w.emitter.fired.disconnect(w.slot)  # identity cache: same object works
    w.emitter.fired.emit(8, "extra")
    assert w.seen == [7]
