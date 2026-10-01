"""Executable coverage for the ticket-06 file_tab migration (legacy
generator tasks -> ui_task coroutines): real signal wiring, busy edges per
mode, the signature-forwarding paths (signals, the dropEvent virtual
method, direct calls), and the 3 old error-recovery registrations rewritten
as try/except + raise.

No RAW data is available in the test environment, so file dialogs are
answered through Orbitool.UI.utils.test.input, the period/detail dialogs
are stubbed where they would exec() a nested event loop, and drag & drop
goes through a stubbed DragHelper.
"""
import importlib
from datetime import datetime

import pytest
from PyQt6 import QtCore, QtGui, QtWidgets

from Orbitool import setting
from ..MainUiPy import Window
from ..utils import test as uitest
from . import CustomPeriodUiPy, FileDetailUiPy

# the package rebinds names it re-exports, so the module itself must be
# resolved through importlib, not through attribute lookup
task_module = importlib.import_module("Orbitool.UI.manager.task")

# a QApplication with no references gets destroyed, breaking every event
# loop that runs afterwards
app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


@pytest.fixture(autouse=True)
def debug_settings(monkeypatch):
    monkeypatch.setattr(setting.debug, "thread_block_gui", True)
    monkeypatch.setattr(setting.debug, "NO_MULTIPROCESS", True)


def _drain_dialog_queue():
    # a leftover test.input() answer would leak into a later dialog call
    while not uitest.q.empty():
        uitest.q.get_nowait()


class _FileTabEnv:
    def __init__(self):
        self.window = None
        self.manager = None
        self.filetab = None
        self.helper = None
        self.dialogs = []       # patched task showInfo args
        self.timeline = []      # ("dialog", args), for recovery-before-dialog order
        self.busy = []
        self.msgs = []
        self.callback_hits = []
        self.startup_dialogs = []

    def reset(self):
        self.dialogs.clear()
        self.timeline.clear()
        self.busy.clear()
        self.msgs.clear()
        self.callback_hits.clear()
        _drain_dialog_queue()


@pytest.fixture(scope="module")
def env(request):
    state = _FileTabEnv()
    original_show_info = task_module.showInfo

    def record_show_info(*args, **kwargs):
        state.dialogs.append(args)
        state.timeline.append(("dialog", args))

    def teardown():
        task_module.showInfo = original_show_info
        _drain_dialog_queue()
        if state.window is not None:
            state.window.close()

    task_module.showInfo = record_show_info
    request.addfinalizer(teardown)

    state.window = window = Window()
    state.manager = window.manager
    state.filetab = window.fileTab
    state.helper = window.fileTab.filter_helper
    state.startup_dialogs = list(state.dialogs)

    # isolate the file tab: file_tab_finish drives the spectra/noise tabs
    window.fileTab.callback.disconnect(window.file_tab_finish)
    window.fileTab.callback.connect(lambda: state.callback_hits.append(1))
    window.manager.busy_signal.connect(state.busy.append)
    window.manager.msg.connect(state.msgs.append)
    return state


@pytest.fixture(autouse=True)
def reset_state(env):
    env.reset()


def _install_refresh_spy(state, calls):
    """record showPaths/show_filter calls around the recovery under test"""
    filetab, helper = state.filetab, state.helper
    orig_paths, orig_filter = filetab.showPaths, helper.show_filter

    def spy_paths():
        calls.append("showPaths")
        state.timeline.append(("showPaths",))
        orig_paths()

    def spy_filter():
        calls.append("show_filter")
        state.timeline.append(("show_filter",))
        orig_filter()

    filetab.showPaths = spy_paths
    helper.show_filter = spy_filter


def _remove_refresh_spy(state):
    del state.filetab.showPaths
    del state.helper.show_filter


def test_startup_clean_and_bindings_cached(env):
    assert env.startup_dialogs == []
    assert not env.manager.busy
    # ui_task binding cache: stable identity while the host lives,
    # for a QObject host and for the non-QObject helper alike
    assert env.filetab.addThermoFile is env.filetab.addThermoFile
    assert env.helper.refresh_filter is env.helper.refresh_filter


def test_addThermoFile_success(env):
    # real clicked signal, dialog answered with an empty file list
    uitest.input([])
    env.filetab.ui.addFilePushButton.click()

    assert env.dialogs == []
    assert env.busy == [True, False]      # default: +1 then -1
    assert "read files" in env.msgs       # worker progress message
    assert not env.manager.busy


def test_addFolder_success(env, tmp_path):
    uitest.input((True, str(tmp_path)))   # empty folder -> worker reads nothing
    env.filetab.ui.addFolderPushButton.click()

    assert env.dialogs == []
    assert env.busy == [True, False]
    assert not env.manager.busy


def test_addThermoFile_error_recovers_before_dialog(env):
    # replaces the old recovery handler on addThermoFile: refresh the table,
    # then re-raise so the framework logs, dialogs once, and releases the
    # count. The queued answer makes the worker fail before any ThermoFile
    # is built -- a failing ThermoFile.__init__ leaves a half-built object
    # whose __del__ raises (pre-existing thermo.py noise, out of scope
    # here, so sidestepped)
    calls = []
    _install_refresh_spy(env, calls)
    try:
        uitest.input(5)  # openfiles answer -> `for f in files` raises in the worker
        env.filetab.ui.addFilePushButton.click()

        assert calls == ["showPaths"]  # the old handler refreshed only the table
        assert [entry[0] for entry in env.timeline] == ["showPaths", "dialog"]
        assert env.dialogs == [("'int' object is not iterable",)]  # str(e), once
        assert not env.manager.busy
    finally:
        _remove_refresh_spy(env)


def test_addFolder_error_recovers_before_dialog(env, tmp_path):
    # replaces the old recovery handler on addFolder: refresh table + filter
    # table, then re-raise; FolderTraveler asserts the folder exists,
    # inside the worker
    calls = []
    _install_refresh_spy(env, calls)
    try:
        uitest.input((True, str(tmp_path / "no-such-dir")))
        env.filetab.ui.addFolderPushButton.click()

        assert calls == ["showPaths", "show_filter"]
        assert [entry[0] for entry in env.timeline] == [
            "showPaths", "show_filter", "dialog"]
        assert len(env.dialogs) == 1  # bare AssertionError: str(e) == ""
        assert not env.manager.busy
    finally:
        _remove_refresh_spy(env)


def test_removePath_error_recovers_before_dialog(env):
    # replaces the old recovery handler on removePath; a stub path makes
    # the worker raise without needing RAW data
    class _BoomPath:
        startDatetime = datetime(2026, 1, 1)
        endDatetime = datetime(2026, 1, 1, 1)
        scanNum = 1
        path = "boom"

        def get_show_name(self):
            return "boom"

        def getFileHandler(self):
            raise ValueError("boom handler")

    filetab = env.filetab
    paths = filetab.pathlist.paths
    boom = _BoomPath()
    paths.append(boom)
    try:
        filetab.showPaths()  # one table row for the stub
        filetab.ui.tableWidget.selectRow(0)
        env.reset()
        calls = []
        _install_refresh_spy(env, calls)
        try:
            filetab.ui.removeFilePushButton.click()

            assert calls == ["showPaths", "show_filter"]
            assert [entry[0] for entry in env.timeline] == [
                "showPaths", "show_filter", "dialog"]
            assert env.dialogs == [("boom handler",)]  # str(e), once
            assert not env.manager.busy
        finally:
            _remove_refresh_spy(env)
    finally:
        if boom in paths:
            paths.remove(boom)
        filetab.showPaths()


def test_removePath_and_adjust_time_slots(env):
    # empty selection on both: default tasks still take and release busy
    env.filetab.ui.removeFilePushButton.click()
    assert env.dialogs == []
    assert env.busy == [True, False]
    assert "processing" in env.msgs  # msgless background uses the default message

    env.reset()
    env.filetab.ui.timeAdjustPushButton.click()
    assert env.dialogs == []
    assert env.busy == [True, False]
    assert not env.manager.busy


def test_process_slots(env):
    # nothing selected -> early return, callback never fires
    env.filetab.ui.selectedPushButton.click()
    assert env.callback_hits == []
    assert env.dialogs == []

    env.reset()
    # an empty pathlist only survives the non-averaging branch (the averaging
    # one has a pre-existing IndexError on empty input, identical pre/post
    # migration); the checkable group box disables its children while
    # unchecked, so restore it afterwards
    env.filetab.ui.averageGroupBox.setChecked(False)
    try:
        env.filetab.ui.allPushButton.click()
    finally:
        env.filetab.ui.averageGroupBox.setChecked(True)

    assert env.callback_hits == [1]
    assert env.dialogs == []
    assert env.busy == [True, False]
    assert not env.manager.busy


def test_default_refused_while_busy(env):
    stats = env.filetab.info.getCastedScanstatsFilters()
    before = str(stats)
    env.manager.set_busy(True)  # disables the tab widget -> call the slot directly
    try:
        env.helper.add_filter()
    finally:
        env.manager.set_busy(False)

    assert env.dialogs == [("Wait for process", 'busy')]
    assert str(stats) == before  # refused before running
    assert not env.manager.busy


def test_showFileDetail_forwards_item_from_signal(env, monkeypatch):
    recorded = []

    class _StubDetail:
        def __init__(self, manager, row):
            recorded.append(row)

        def exec(self):
            return 1

    monkeypatch.setattr(FileDetailUiPy, "Dialog", _StubDetail)

    table = env.filetab.ui.tableWidget
    table.setRowCount(1)
    item = QtWidgets.QTableWidgetItem("fake")
    table.setItem(0, 0, item)
    try:
        table.itemDoubleClicked.emit(item)
    finally:
        table.setRowCount(0)

    assert recorded == [0]  # formerly needed the manual args switch; forwarded by signature now
    assert env.dialogs == []
    assert env.busy == [True, False]


def test_tableDropEvent_forwards_event_and_runs_worker(env, monkeypatch, tmp_path):
    (tmp_path / "notes.txt").write_text("not raw")
    dragged = [tmp_path, tmp_path / "notes.txt"]  # dir -> traveler, txt -> skipped

    class _FakeDragHelper:
        def yield_file(self, data):
            return iter(dragged)

    class _FakeMime:
        pass

    class _FakeEvent:
        def mimeData(self):
            return _FakeMime()

    monkeypatch.setattr(env.filetab, "drag_helper", _FakeDragHelper())
    env.filetab.tableDropEvent(_FakeEvent())

    assert env.dialogs == []
    assert env.busy == [True, False]
    assert not env.manager.busy


def test_filter_helper_tasks_and_focus_out(env):
    info = env.filetab.info
    helper = env.helper
    # deterministic seed: known-empty filter state
    info.getCastedUsedSpectrumFilters().clear()
    info.getCastedScanstatsFilters().clear()

    env.filetab.ui.refreshFilterPushButton.click()
    assert env.dialogs == []
    assert env.busy == [True, False]  # refresh_filter is default mode

    env.reset()
    env.filetab.ui.addFilterToolButton.click()  # file_filter empty -> stats row
    row0 = [helper.table.item(0, c).text() for c in range(3)]
    assert row0[0] == "TIC"
    assert env.busy == [True, False]

    env.reset()
    env.filetab.ui.delFilterToolButton.click()  # empty selection -> rebuild only
    assert env.dialogs == []
    env.filetab.ui.addFilterToolButton.click()  # same TIC key overwritten

    # edit_filter (light) through the real itemDoubleClicked signal, col 1
    env.reset()
    helper.table.itemDoubleClicked.emit(helper.table.item(0, 1))
    assert isinstance(helper.current_filter_widget, QtWidgets.QComboBox)
    assert env.busy == []  # light: never touches busy

    # direct no-arg call while current_edit_filter_pos is set
    helper.text_changed()
    assert env.dialogs == []
    assert env.busy == []

    # re-emit: pos was reset, so the pair is re-read fresh from the table
    helper.table.itemDoubleClicked.emit(helper.table.item(0, 1))
    assert isinstance(helper.current_filter_widget, QtWidgets.QComboBox)

    # real currentTextChanged signal: str argument truncated to 0-param slot
    helper.current_filter_widget.setCurrentText("<=")
    scanstats = info.getCastedScanstatsFilters()
    assert "TIC" in scanstats and "<=" in scanstats["TIC"]
    assert env.dialogs == []
    assert env.busy == []

    # col 2 -> QDoubleSpinBox with focusOutEvent monkeypatched to text_changed
    helper.table.itemDoubleClicked.emit(helper.table.item(0, 2))
    spin = helper.current_filter_widget
    assert isinstance(spin, QtWidgets.QDoubleSpinBox)
    assert env.busy == []

    # invoke focusOutEvent for real: the QFocusEvent argument must truncate
    # to the 0-param slot, and the widget value change must be applied
    spin.setValue(6000)
    spin.focusOutEvent(QtGui.QFocusEvent(QtCore.QEvent.Type.FocusOut))
    assert info.getCastedScanstatsFilters()["TIC"]["<="] == 6000.0
    assert env.dialogs == []
    assert env.busy == []


def test_edit_period_default_task_holds_busy(env, monkeypatch):
    # the period button lives inside this checkable group box
    env.filetab.ui.averageGroupBox.setChecked(True)
    captured = {}

    class _StubDialog:
        def __init__(self, manager, start, end, num_interval, time_interval):
            captured["args"] = (start, end, num_interval, time_interval)

        def init_periods(self, *args):
            pass

        def show_periods(self):
            pass

        def exec(self):
            captured["busy"] = env.manager.busy
            return 1

    monkeypatch.setattr(CustomPeriodUiPy, "Dialog", _StubDialog)
    env.filetab.ui.periodToolButton.click()

    assert "args" in captured  # slot ran through its real signal
    assert captured["busy"] is True  # default mode holds busy through exec()
    assert env.busy == [True, False]
    assert env.dialogs == []


def test_custom_period_dialog_tasks(env, tmp_path):
    start = datetime(2026, 1, 1)
    end = datetime(2026, 1, 2)
    dialog = CustomPeriodUiPy.Dialog(env.manager, start, end, 5, "2h5m")
    try:
        dialog.init_periods(start, end, "2h5m")
        dialog.show_periods()  # -> plot_periods (light; no paths -> early return)
        assert env.dialogs == []

        dialog.ui.generateNumPeriodPushButton.click()  # no paths -> early return
        assert env.dialogs == []
        assert env.busy == []

        dialog.ui.generateTimePeriodPushButton.click()
        assert len(dialog.periods) > 0
        assert env.dialogs == []
        assert env.busy == []

        dialog.ui.plotHideLabelCheckBox.setChecked(True)  # toggled -> plot_periods
        assert env.dialogs == []
        assert env.busy == []

        # modify start points: positive delta on contiguous generated periods
        dialog.ui.modifyLineEdit.setText("5m")
        dialog.ui.modifyStartPointsPushButton.click()
        assert env.dialogs == []
        assert env.busy == []

        # regenerate contiguous, then modify end points with a negative delta
        dialog.ui.generateTimePeriodPushButton.click()
        dialog.ui.modifyLineEdit.setText("-5m7s")
        dialog.ui.modifyEndPointsPushButton.click()
        assert env.dialogs == []
        assert env.busy == []

        # light error fallback: one dialog, busy never touched, state intact
        env.reset()
        dialog.ui.generateTimePeriodPushButton.click()
        n_periods = len(dialog.periods)
        dialog.ui.modifyLineEdit.setText("bogus")
        dialog.ui.modifyStartPointsPushButton.click()
        assert len(env.dialogs) == 1
        assert env.busy == []
        assert len(dialog.periods) == n_periods
        dialog.ui.modifyLineEdit.setText("5m")

        # export -> csv
        env.reset()
        csv_path = tmp_path / "periods.csv"
        uitest.input((True, str(csv_path)))
        dialog.ui.exportPushButton.click()
        assert csv_path.exists() and csv_path.stat().st_size > 0
        assert env.dialogs == []
        assert env.busy == []

        # import round trip
        env.reset()
        dialog.ui.generateTimePeriodPushButton.click()
        n_gen = len(dialog.periods)
        uitest.input((True, str(csv_path)))
        dialog.ui.importPushButton.click()
        assert len(dialog.periods) == n_gen
        assert env.dialogs == []
        assert env.busy == []
    finally:
        dialog.close()
