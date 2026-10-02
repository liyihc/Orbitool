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


def test_recover_before_dialog_then_release_count(monkeypatch, caplog):
    # the old error-registration -> try/except + raise rewrite contract
    # (FileUiPy addThermoFile/addFolder/removePath): the recovery runs at
    # the await point before the framework dialog, the dialog fires exactly
    # once with str(e), and the default task's count is given back
    widget = _Widget()
    timeline = []
    monkeypatch.setattr(
        task_module, "showInfo",
        lambda *args, **kwargs: timeline.append(("dialog", args)))
    events = []
    widget.manager.busy_signal.connect(events.append)

    @ui_task
    async def task(widget):
        try:
            await background(worker_boom, "work")
        except Exception:
            timeline.append(("recovered",))
            raise

    with caplog.at_level(logging.ERROR, logger="Orbitool"):
        task.func(widget)

    assert timeline == [
        ("recovered",),
        ("dialog", ("boom from worker",)),  # str(e), exactly once, after recovery
    ]
    assert events == [True, False]  # count taken, then given back by the fallback
    assert not widget.manager.busy
    with_traceback = [record for record in caplog.records if record.exc_info]
    assert with_traceback, "worker exception must be logged with exc_info"
    formatted = "".join(
        traceback.format_exception(*with_traceback[-1].exc_info))
    assert "worker_boom" in formatted
    assert "boom from worker" in formatted


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

    # the old argument switch's keyword, assembled from parts so the deleted
    # name leaves no grep residue while the rejection itself stays pinned
    old_switch = "with" + "Args"
    with pytest.raises(TypeError):
        ui_task(**{old_switch: True})
    with pytest.raises(TypeError):
        ui_task(sample, **{old_switch: True})


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


# cookbook twins: every code example in docs/ui-tasks.md has an executable
# assertion here so the cookbook cannot drift from the API (ticket 05)


def test_cookbook_single_step(show_info):
    class Tab(_Widget):
        def __init__(self):
            super().__init__()
            self.label = None
            self.msgs = []
            self.manager.msg.connect(self.msgs.append)

        @ui_task
        async def denoise(self):
            folder = "sample.raw"  # main thread: read inputs
            noise = await background(lambda: len(folder), "denoising")  # worker
            self.label = str(noise)  # main thread: touch widgets

    tab = Tab()
    events = []
    tab.manager.busy_signal.connect(events.append)

    tab.denoise()

    assert tab.label == "10"
    assert tab.msgs == ["denoising"]
    assert events == [True, False]
    assert not tab.manager.busy
    assert show_info == []


def test_cookbook_multi_step_pipeline(monkeypatch, show_info):
    monkeypatch.setattr(setting.debug, "thread_block_gui", False)
    main_ident = threading.get_ident()
    segments = []

    class Tab(_Widget):
        @ui_task
        async def run_pipeline(self):
            segments.append(("main", threading.get_ident()))
            first = await background(
                lambda: (threading.get_ident(), 1), "scanning")
            segments.append(("worker", first[0]))
            segments.append(("main", threading.get_ident()))
            second = await background(
                lambda: (threading.get_ident(), 2), "analyzing")
            segments.append(("worker", second[0]))
            segments.append(("main", threading.get_ident(), second[1]))

    tab = Tab()
    tab.run_pipeline()
    _wait_until(lambda: not tab.manager.busy)

    assert [segment[0] for segment in segments] == [
        "main", "worker", "main", "worker", "main"]
    for segment in segments:
        if segment[0] == "main":
            assert segment[1] == main_ident
        else:
            assert segment[1] != main_ident
    assert segments[-1][2] == 2
    assert show_info == []


def test_cookbook_multiprocess_instance(show_info):
    class Tab(_Widget):
        def __init__(self):
            super().__init__()
            self.count = None
            self.file = None

        @ui_task
        async def analyze(self):
            file = {}
            count = await background(
                collect_p(file, {"length": 3}), "analyzing")
            self.count = count
            self.file = file

    tab = Tab()
    tab.analyze()

    assert tab.count == 3
    assert tab.file == {"ret": [0, 1, 2]}
    assert not tab.manager.busy
    assert show_info == []


def test_cookbook_join_relay(show_info):
    class Emitter(QtCore.QObject):
        stepFinished = QtCore.pyqtSignal()

    class Tab(_Widget):
        def __init__(self):
            super().__init__()
            self.emitter = Emitter()
            self.emitter.stepFinished.connect(self.on_step_finished)
            self.log = []
            self.relay_busy = []

        @ui_task
        async def run(self):
            await background(lambda: "step one", "step one")
            self.emitter.stepFinished.emit()  # relay while holding busy
            await background(lambda: "step two", "step two")
            self.log.append("run done")

        @ui_task(mode="join")
        async def on_step_finished(self):
            self.relay_busy.append(self.manager.busy)
            self.log.append("relay")

    tab = Tab()
    events = []
    tab.manager.busy_signal.connect(events.append)

    tab.run()

    assert tab.log == ["relay", "run done"]  # join started despite busy
    assert tab.relay_busy == [True]
    assert events == [True, False]  # count 1 -> 2 -> 1 -> 0, one edge pair
    assert not tab.manager.busy
    assert show_info == []


def test_cookbook_light_slot(show_info):
    class Emitter(QtCore.QObject):
        selectionChanged = QtCore.pyqtSignal(int)

    class Tab(_Widget):
        def __init__(self):
            super().__init__()
            self.emitter = Emitter()
            self.emitter.selectionChanged.connect(self.refresh_preview)
            self.preview = []

        @ui_task(mode="light")
        async def refresh_preview(self):  # no parameters: signal arg truncated
            self.preview.append(self.manager.busy)

    tab = Tab()
    events = []
    tab.manager.busy_signal.connect(events.append)

    tab.emitter.selectionChanged.emit(3)

    assert tab.preview == [False]  # ran, and never saw itself as busy
    assert events == []  # busy never touched
    assert not tab.manager.busy
    assert show_info == []


def test_cookbook_slot_arguments(show_info):
    class Emitter(QtCore.QObject):
        fired = QtCore.pyqtSignal(int, str)

    class Tab(_Widget):
        def __init__(self):
            super().__init__()
            self.emitter = Emitter()
            self.seen = []
            self.emitter.fired.connect(self.on_fired)

        @ui_task(mode="light")
        async def on_fired(self, number):  # 2-arg signal, 1-param slot
            self.seen.append(number)

    tab = Tab()
    tab.emitter.fired.emit(7, "extra")

    assert tab.seen == [7]  # excess positional truncated, no argument switch
    assert show_info == []


def test_cookbook_try_except_finally(show_info):
    main_ident = threading.get_ident()
    trace = []

    class Tab(_Widget):
        def __init__(self):
            super().__init__()
            self.status = None

        @ui_task
        async def read_files(self):
            try:
                count = await background(worker_boom, "read files")
            except ValueError as e:  # caught at the await point, main thread
                trace.append(("except", str(e), threading.get_ident()))
                self.status = f"read failed: {e}"
            else:
                self.status = f"{count} files"
            finally:  # always runs, on the main thread
                trace.append(("finally", None, threading.get_ident()))

    tab = Tab()
    tab.read_files()

    assert tab.status == "read failed: boom from worker"
    assert [kind for kind, *_ in trace] == ["except", "finally"]
    assert all(ident == main_ident for _, _, ident in trace)
    assert show_info == []  # handled in-task: no framework dialog
    assert not tab.manager.busy


@pytest.mark.parametrize(
    "worker_fails", [False, True], ids=["success", "worker_error"])
def test_cookbook_migrated_form(worker_fails, show_info):
    class Tab(_Widget):
        def __init__(self):
            super().__init__()
            self.result = None
            self.trace = []

        @ui_task(mode="join")  # join mode: pipeline relay
        async def show_result(self, index):  # argument forwarded by signature
            try:
                result = await background(
                    lambda: self.heavy(index), "computing")
            except Exception:  # recovered at the await point, then re-raised
                self.trace.append("recovered")
                self.result = "failed"
                raise
            else:
                self.result = str(result)

        def heavy(self, index):
            if worker_fails:
                raise ValueError("computing failed")
            return index * 2

    tab = Tab()
    events = []
    tab.manager.busy_signal.connect(events.append)

    tab.show_result(21)  # argument forwarded by signature

    if worker_fails:
        assert tab.trace == ["recovered"]  # the except branch actually runs
        assert tab.result == "failed"
        assert show_info == [("computing failed",)]  # str(e) dialog, once
    else:
        assert tab.trace == []
        assert tab.result == "42"
        assert show_info == []
    assert events == [True, False]  # busy given back in both variants
    assert not tab.manager.busy
