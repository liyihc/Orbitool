"""Executable coverage for the ticket-09 migration (Calibration,
CalibrationDetail, PeakFitFloat): the legacy generator tasks were
rewritten as ui_task coroutines.

The batch carries three non-default mode sites (`mouseRelease` `'n'` and
the two drag handlers `'e'` -> light), twelve former argument-switch slots
whose arguments are now forwarded by signature, and two `MultiProcess`
worker instances (`SplitAndFitPeak` in `calcInfo`,
`CalibrateMergeDenoise` in `calibrate`). `calcInfo` is the longest
multi-step pipeline in the migration: a worker step followed by two plain
closures, all before the synchronous `showAllInfo` tail.

No RAW data is available, so file dialogs are answered through
`Orbitool.UI.utils.test.input` / module `openfile` stubs, user-facing
`showInfo` is recorded instead of shown, and the full main window is
built once. `thread_block_gui` makes workers run inline for deterministic
busy edges.

Placed at the batch root (all three files are top-level `Orbitool/UI`
modules) and listed in `pytest.ini`.
"""
import importlib
from array import array
from datetime import datetime, timedelta

import numpy as np
import pytest
from PyQt6 import QtCore, QtGui, QtWidgets

from ..models.file import FileSpectrumInfo
from ..models.peakfit.normal_distribution import NormalDistributionFunc
from ..models.spectrum import FittedPeak, Peak, Spectrum
from ..models.workspace.calibration import default_ions
# debug_settings is an autouse fixture re-exported for pytest
from .tests.migration_harness import (  # noqa: F401
    MigrationEnv, debug_settings, task_module)

calibration_module = importlib.import_module("Orbitool.UI.CalibrationUiPy")
calibration_detail_module = importlib.import_module(
    "Orbitool.UI.CalibrationDetailUiPy")
peak_fit_float_module = importlib.import_module("Orbitool.UI.PeakFitFloatUiPy")

_START = datetime(2024, 1, 1, 12)


@pytest.fixture(scope="module")
def env(request):
    return MigrationEnv().build(
        request, extra_dialog_modules=(calibration_module,))


@pytest.fixture(autouse=True)
def reset_state(env):
    env.reset()


def _spectrum(path="none:"):
    return Spectrum(
        mz=np.array([100.0, 100.01, 100.02]),
        intensity=np.array([1.0, 2.0, 1.0]),
        path=path, start_time=_START, end_time=_START + timedelta(minutes=1))


def _file_spectrum_info(path="none:"):
    return FileSpectrumInfo(
        start_time=_START, end_time=_START + timedelta(minutes=1),
        path=path, filter={}, stats_filter={}, average_index=0)


def _mouse_release_event():
    return QtGui.QMouseEvent(
        QtCore.QEvent.Type.MouseButtonRelease,
        QtCore.QPointF(0, 0), QtCore.QPointF(0, 0),
        QtCore.Qt.MouseButton.LeftButton,
        QtCore.Qt.MouseButton.LeftButton,
        QtCore.Qt.KeyboardModifier.NoModifier)


class _FakeDragEvent:
    def __init__(self):
        mime = QtCore.QMimeData()
        mime.setText("C6H5O3NNO3-")
        self._mime = mime
        self.accepted = False
        self.drop_action = None

    def mimeData(self):
        return self._mime

    def setDropAction(self, action):
        self.drop_action = action

    def accept(self):
        self.accepted = True


def _install_peak_fit(window):
    workspace = window.manager.workspace
    info = workspace.info.peak_fit_tab
    mz = np.linspace(99.99, 100.01, 201)
    intensity = np.exp(-((mz - 100.0) / 0.002) ** 2)
    raw = Peak(mz=mz, intensity=intensity)
    fitted = FittedPeak(
        mz=mz, intensity=intensity,
        fitted_param=np.array([1.0, 100.0]),
        peak_position=100.0, peak_intensity=1.0, area=1.0,
        tags="", formulas=[])
    info.raw_peaks = [raw]
    info.peaks = [fitted]
    info.original_indexes = array("i", [0])
    info.shown_indexes = array("i", [0])
    info.raw_split_num = array("i", [1])
    workspace.info.peak_shape_tab.func = NormalDistributionFunc(
        peak_fit_sigma=2.852197450904393e-06,
        peak_fit_res=148889.02590153966)


# --------------------------------------------------------------------------
# Decoration: every migrated site is a ui_task bound to an async def
# --------------------------------------------------------------------------

_MIGRATED_SITES = {
    calibration_module.Widget: [
        "addSegment", "mouseRelease", "mergeSegment", "changeSegment",
        "addIon", "removeIon", "importIons", "exportIons",
        "tableDragEnterEvent", "tableDragMoveEvent", "tableDropEvent",
        "calcInfo", "showDetail", "calibrate"],
    calibration_detail_module.Widget: [
        "showSpectrumAt", "showIonAt", "next_ion", "showFileAt"],
    peak_fit_float_module.Window: [
        "finetuneFormula", "replotPeak", "refit", "save"],
}


def test_calibration_all_sites_are_coroutine_tasks():
    count = 0
    for cls, names in _MIGRATED_SITES.items():
        for name in names:
            assert isinstance(cls.__dict__[name], task_module.ui_task), name
            count += 1
    assert count == 22


# --------------------------------------------------------------------------
# Calibration: the three former `'e'`/`'n'` sites -> light
# --------------------------------------------------------------------------

def test_calibration_light_sites_ignore_busy(env):
    widget = env.window.calibrationTab
    manager = env.window.manager
    manager.set_busy(True)
    env.busy.clear()
    try:
        widget.mouseRelease(_mouse_release_event())        # was a light letter mode
        widget.tableDragEnterEvent(_FakeDragEvent())       # was a light letter mode
        widget.tableDragMoveEvent(_FakeDragEvent())        # was a light letter mode
        assert env.dialogs == []
        assert env.busy == []                              # light: no transition
        assert manager.busy is True
    finally:
        manager.set_busy(False)


# --------------------------------------------------------------------------
# Calibration: default slots take and release busy, args forwarded
# --------------------------------------------------------------------------

def test_calibration_default_slots_take_busy(env):
    widget = env.window.calibrationTab

    widget.ui.separatorDoubleSpinBox.setValue(400.0)
    widget.addSegment()
    assert env.dialogs == []
    assert env.busy == [True, False]
    assert not env.window.manager.busy
    env.reset()

    widget.ui.ionLineEdit.setText("C2H2O2-")
    widget.addIon()
    assert env.dialogs == []
    assert env.busy == [True, False]
    assert not env.window.manager.busy


def test_calibration_change_segment_forwards_signal_args(env):
    widget = env.window.calibrationTab
    listwidget = widget.ui.separatorListWidget
    widget.showSegments()
    assert listwidget.count() >= 1
    item = listwidget.item(0)

    listwidget.itemDoubleClicked.emit(item)      # was the old argument switch

    assert env.dialogs == []
    assert env.busy == [True, False]
    assert widget.info.current_segment_index == 0


# --------------------------------------------------------------------------
# Calibration: calcInfo multi-step pipeline
# --------------------------------------------------------------------------

def test_calibration_calc_info_without_ions_skips_split(env):
    widget = env.window.calibrationTab
    info = widget.info
    info.ions = []
    info.last_ions = []

    widget.calcInfo()

    assert env.dialogs == []
    assert env.busy == [True, False]
    assert "split and fit target peaks" not in env.msgs
    assert "calculate calibration infos" in env.msgs
    assert widget.ui.caliInfoTableWidget.columnCount() == 0


def test_calibration_calc_info_runs_split_pipeline(env):
    widget = env.window.calibrationTab
    info = widget.info
    info.ions = default_ions()
    info.last_ions = []

    widget.calcInfo()

    assert env.dialogs == []
    assert env.busy == [True, False]
    for msg in ("split and fit target peaks",
                "calculate ions points",
                "calculate calibration infos"):
        assert msg in env.msgs
    assert len(info.last_ions) == len(info.ions)
    assert widget.ui.caliInfoTableWidget.columnCount() == len(info.ions)


# --------------------------------------------------------------------------
# Calibration: calibrate pipeline + callback
# --------------------------------------------------------------------------

def test_calibration_calibrate_runs_merge_and_emits_callback(env):
    window = env.window
    widget = window.calibrationTab
    noise_info = window.manager.workspace.info.noise_tab
    noise_info.skip = True
    noise_info.denoised_spectrum_infos = [_file_spectrum_info()]
    window.manager.workspace.data.raw_spectra.clear()
    window.manager.workspace.data.raw_spectra.append(_spectrum())

    hits = []
    widget.callback.connect(lambda: hits.append(1))

    widget.calibrate(skip=True)                 # worker background step

    assert env.dialogs == []
    assert env.busy == [True, False]
    assert "merge" in env.msgs
    assert hits == [1]
    info = window.manager.workspace.info.calibration_tab
    assert len(info.calibrated_spectrum_infos) == 1
    assert len(window.manager.workspace.data.calibrated_spectra) == 1


def test_calibration_calibrate_without_info_is_blocked(env):
    window = env.window
    widget = window.calibrationTab
    noise_info = window.manager.workspace.info.noise_tab
    noise_info.denoised_spectrum_infos = [_file_spectrum_info()]
    widget.info.calibrator_segments.clear()

    hits = []
    widget.callback.connect(lambda: hits.append(1))

    widget.calibrate(skip=False)

    assert env.dialogs == [("please calculate calibration info first",)]
    assert env.msgs == []
    assert hits == []
    assert not window.manager.busy


def test_calibration_calibrate_after_calc_without_ions_is_blocked(env):
    window = env.window
    widget = window.calibrationTab
    info = widget.info
    info.ions = []
    info.last_ions = []
    info.path_ion_infos.clear()

    widget.calcInfo()
    assert info.calibrator_segments == {}
    env.reset()

    window.manager.workspace.info.noise_tab.denoised_spectrum_infos = [
        _file_spectrum_info()]

    widget.calibrate(skip=False)

    assert env.dialogs == [("please calculate calibration info first",)]
    assert env.msgs == []


def test_calibration_calibrate_without_denoise_is_blocked(env):
    window = env.window
    widget = window.calibrationTab
    window.manager.workspace.info.noise_tab.denoised_spectrum_infos = []

    hits = []
    widget.callback.connect(lambda: hits.append(1))

    widget.calibrate(skip=False)
    assert env.dialogs == [("please denoise first",)]
    assert env.msgs == []
    assert hits == []
    assert not window.manager.busy
    env.reset()

    widget.calibrate(skip=True)
    assert env.dialogs == [("please denoise first",)]
    assert env.msgs == []
    assert hits == []
    assert not window.manager.busy


# --------------------------------------------------------------------------
# CalibrationDetail: async slots callable, busy released
# --------------------------------------------------------------------------

def test_calibration_detail_async_slots(env, monkeypatch):
    window = env.window
    win = calibration_detail_module.Widget(window.manager)
    seen = []
    monkeypatch.setattr(win, "showIon", lambda index: seen.append(index))
    try:
        item = QtWidgets.QTableWidgetItem("x")

        win.showSpectrumAt(item)                # was the old argument switch
        assert env.dialogs == []
        assert env.busy == [True, False]
        env.reset()

        win.showIonAt(item)
        assert env.dialogs == []
        assert env.busy == [True, False]
        assert seen == [-1]
        env.reset()

        win.next_ion(1)                         # spectrum None -> return
        assert env.dialogs == []
        assert env.busy == [True, False]
        env.reset()

        win.showFileAt(item)
        assert env.dialogs == []
        assert env.busy == [True, False]
    finally:
        win.close()


# --------------------------------------------------------------------------
# PeakFitFloat: async slots on a real float window
# --------------------------------------------------------------------------

def test_calibration_peak_float_async_slots(env):
    window = env.window
    _install_peak_fit(window)
    calls = []
    sink = lambda: calls.append(1)  # MySignal is weak: keep a strong ref
    window.manager.signals.peak_refit_finish.connect(sink)
    win = peak_fit_float_module.Window.get_or_create(window.manager, 0)
    try:
        win.replotPeak()
        assert env.dialogs == []
        assert env.busy == [True, False]
        assert not window.manager.busy
        env.reset()

        win.refit()
        assert env.dialogs == []
        assert env.busy == [True, False]
        assert len(win.peaks) >= 1
        env.reset()

        win.save()
        assert env.dialogs == []
        assert env.busy == [True, False]
        assert calls == [1]
    finally:
        win.close()
