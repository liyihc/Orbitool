"""Executable coverage for the ticket-10 migration (PeakFit): the legacy
generator tasks were rewritten as ui_task coroutines.

The batch is the largest single-file batch (25 decorated sites). Four were
`mode='n'` view operations (`moveRight`, `y_times`, `timer_timeout`,
`step_accord_toggled`) and became `mode="light"`; the remaining 21 (including
the view operations that were default mode, so zero behaviour change) stayed
default. Seven former `withArgs=True` slots now forward their slot arguments
by signature. `showSelect` drives the one `MultiProcess` instance of the batch
(`SplitPeaks`) plus two plain closures; three generator helpers
(`_general_action`, `fit_formula`, `fit_mass_list`) were converted to `async
def` in this ticket and are awaited by their callers.

No RAW data is available, so the `showSelect` pipeline is driven against a
synthetic calibrated spectrum built with the same normal-distribution peak
shape the real workflow uses, and user-facing `showInfo` is recorded instead
of shown. The full main window is built once. `thread_block_gui` makes workers
run inline for deterministic busy edges.

Placed at the batch root (all files are top-level `Orbitool/UI` modules) and
listed in `pytest.ini`.
"""
import importlib
import inspect
from array import array
from datetime import datetime, timedelta

import numpy as np
import pytest
from PyQt6 import QtWidgets

from Orbitool import setting
from ..models.peakfit.normal_distribution import NormalDistributionFunc
from ..models.spectrum import FittedPeak, Peak, Spectrum
from .MainUiPy import Window
from .utils import test as uitest

task_module = importlib.import_module("Orbitool.UI.manager.task")
peakfit_module = importlib.import_module("Orbitool.UI.PeakFitUiPy")

# a QApplication with no references gets destroyed, breaking every event
# loop that runs afterwards
app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

_START = datetime(2024, 1, 1, 12)

_SIGMA = 2.852197450904393e-06
_RES = 148889.02590153966


@pytest.fixture(autouse=True)
def debug_settings(monkeypatch):
    monkeypatch.setattr(setting.debug, "thread_block_gui", True)
    monkeypatch.setattr(setting.debug, "NO_MULTIPROCESS", True)


def _drain_dialog_queue():
    while not uitest.q.empty():
        uitest.q.get_nowait()


class _Env:
    def __init__(self):
        self.dialogs = []
        self.busy = []
        self.msgs = []

    def reset(self):
        self.dialogs.clear()
        self.busy.clear()
        self.msgs.clear()
        _drain_dialog_queue()


@pytest.fixture(scope="module")
def env(request):
    state = _Env()
    original_task_show_info = task_module.showInfo

    def record_show_info(*args, **kwargs):
        state.dialogs.append(args)

    def teardown():
        task_module.showInfo = original_task_show_info
        _drain_dialog_queue()
        if state.window is not None:
            state.window.close()

    task_module.showInfo = record_show_info
    request.addfinalizer(teardown)

    state.window = window = Window()
    window.manager.busy_signal.connect(state.busy.append)
    window.manager.msg.connect(state.msgs.append)
    return state


@pytest.fixture(autouse=True)
def reset_state(env):
    env.reset()
    window = env.window
    info = window.manager.workspace.info.peak_fit_tab
    empty = np.empty(0, float)
    info.spectrum = None
    info.raw_peaks = []
    info.raw_split_num = array("i")
    info.original_indexes = array("i")
    info.peaks = []
    info.shown_indexes = []
    info.shown_mz = empty
    info.shown_intensity = empty
    info.shown_residual = empty
    info.residual_mz = empty
    info.residual_intensity = empty
    window.manager.workspace.info.peak_shape_tab.func = None
    window.manager.workspace.data.calibrated_spectra.clear()


def _spectrum():
    mz = np.linspace(99.998, 100.002, 801)
    sigma = 2e-4
    intensity = np.exp(-0.5 * ((mz - 100.0) / sigma) ** 2)
    return Spectrum(
        mz=mz, intensity=intensity, path="none:",
        start_time=_START, end_time=_START + timedelta(minutes=1))


def _install_peak_fit(window):
    info = window.manager.workspace.info.peak_fit_tab
    mz = np.linspace(99.99, 100.01, 201)
    intensity = np.exp(-((mz - 100.0) / 0.002) ** 2)
    raw = Peak(mz=mz, intensity=intensity)
    fitted = FittedPeak(
        mz=mz, intensity=intensity,
        fitted_param=np.array([1.0, 100.0]),
        peak_position=100.0, peak_intensity=1.0, area=1.0,
        tags="", formulas=[])
    info.spectrum = _spectrum()
    info.raw_peaks = [raw]
    info.peaks = [fitted]
    info.original_indexes = array("i", [0])
    info.shown_indexes = array("i", [0])
    info.raw_split_num = array("i", [1])
    window.manager.workspace.info.peak_shape_tab.func = NormalDistributionFunc(
        peak_fit_sigma=_SIGMA, peak_fit_res=_RES)


def _install_shown(window):
    info = window.manager.workspace.info.peak_fit_tab
    spectrum = _spectrum()
    info.spectrum = spectrum
    info.shown_mz = spectrum.mz
    info.shown_intensity = spectrum.intensity
    info.shown_residual = spectrum.intensity * 0.5
    window.peakFitTab.plot_peaks()


# --------------------------------------------------------------------------
# Decoration: every migrated site is a ui_task bound to an async def
# --------------------------------------------------------------------------

_MIGRATED_SITES = {
    peakfit_module.Widget: [
        "showSelect",
        "ylog_toggle", "moveRight", "y_times", "rescale_clicked",
        "scale_spectrum", "timer_timeout",
        "filterClear", "filterSelected", "filterUnselected", "filterGeneral",
        "filter_tag", "filter_intensity_max", "filter_intensity_min",
        "filter_mass_defect", "filter_group_y", "filter_group_n",
        "generalAction", "step_accord_toggled", "do_step",
        "replot_within_peaks", "fit", "add_tag", "addToMassList",
        "remove_tag"],
}


def test_peakfit_all_sites_are_coroutine_tasks():
    count = 0
    for cls, names in _MIGRATED_SITES.items():
        for name in names:
            task = cls.__dict__[name]
            assert isinstance(task, task_module.ui_task), name
            assert inspect.iscoroutinefunction(task._func), name
            count += 1
    assert count == 25


def test_peakfit_helpers_are_coroutines():
    assert inspect.iscoroutinefunction(peakfit_module.Widget._general_action)
    assert inspect.iscoroutinefunction(peakfit_module.Widget.fit_formula)
    assert inspect.iscoroutinefunction(peakfit_module.Widget.fit_mass_list)
    # not counted among the 25 decorated sites
    assert not isinstance(
        peakfit_module.Widget.__dict__["_general_action"], task_module.ui_task)


# --------------------------------------------------------------------------
# The four former `mode='n'` view sites -> light: ignore busy
# --------------------------------------------------------------------------

def test_peakfit_light_sites_ignore_busy(env):
    window = env.window
    widget = window.peakFitTab
    manager = window.manager
    manager.set_busy(True)
    env.busy.clear()
    try:
        widget.ui.leftToolButton.click()               # moveRight(-1)
        widget.ui.rightToolButton.click()              # moveRight(1)
        widget.ui.yLimDoubleToolButton.click()         # y_times(2)
        widget.ui.yLimHalfToolButton.click()           # y_times(.5)
        widget.ui.stepAccordToMassCheckBox.setChecked(True)  # step_accord_toggled
        widget.timer.timeout.emit()                    # timer_timeout
        assert env.dialogs == []
        assert env.busy == []                          # light: no transition
        assert manager.busy is True
    finally:
        widget.ui.stepAccordToMassCheckBox.setChecked(False)
        manager.set_busy(False)


# --------------------------------------------------------------------------
# Default slots take and release busy
# --------------------------------------------------------------------------

def test_peakfit_default_slots_take_busy(env):
    widget = env.window.peakFitTab

    widget.ui.filterClearPushButton.click()            # filterClear
    assert env.dialogs == []
    assert env.busy == [True, False]
    assert not env.window.manager.busy
    env.reset()

    widget.ui.filterSelectYToolButton.click()          # filterSelected
    assert env.dialogs == []
    assert env.busy == [True, False]
    assert not env.window.manager.busy
    env.reset()

    widget.ui.filterIntensityMaxToolButton.click()     # filter_intensity_max
    assert env.dialogs == []
    assert env.busy == [True, False]
    assert not env.window.manager.busy


def test_peakfit_default_scale_spectrum_takes_busy(env):
    widget = env.window.peakFitTab
    widget.ui.scaleToSpectrumPushButton.click()        # default, early return
    assert env.dialogs == []
    assert env.busy == [True, False]


# --------------------------------------------------------------------------
# Signature forwarding for former withArgs=True slots (real signal emits)
# --------------------------------------------------------------------------

def test_peakfit_signature_forwarded_slots(env):
    widget = env.window.peakFitTab
    _install_shown(env.window)

    checkbox = widget.ui.yLogcheckBox
    checkbox.setChecked(True)                          # toggled(bool) -> ylog_toggle
    try:
        assert env.dialogs == []
        assert env.busy == [True, False]
    finally:
        env.reset()
        checkbox.setChecked(False)
    assert env.dialogs == []
    assert env.busy == [True, False]
    env.reset()

    widget.ui.filterTagYToolButton.click()             # lambda -> filter_tag(True)
    assert env.dialogs == []
    assert env.busy == [True, False]
    env.reset()

    accord = widget.ui.stepAccordToMassCheckBox
    accord.setChecked(True)                            # toggled(bool) -> step_accord_toggled
    try:
        assert widget.ui.stepRtolDoubleSpinBox.isEnabled() is True
        assert env.dialogs == []
        assert env.busy == []                          # light
    finally:
        accord.setChecked(False)
    assert widget.ui.stepRtolDoubleSpinBox.isEnabled() is False


def test_peakfit_light_view_args_forwarded(env):
    widget = env.window.peakFitTab
    ax = widget.plot.ax

    x0, x1 = ax.get_xlim()
    widget.ui.rightToolButton.click()                  # moveRight(1)
    new0, new1 = ax.get_xlim()
    assert new0 - x0 == pytest.approx(1.0)
    assert new1 - x1 == pytest.approx(1.0)
    assert env.busy == []
    env.reset()

    widget.ui.yLimDoubleToolButton.click()             # y_times(2)
    y0, y1 = ax.get_ylim()
    assert y0 < y1
    assert env.busy == []


# --------------------------------------------------------------------------
# Async helpers: decorated callers await the converted helpers
# --------------------------------------------------------------------------

def test_peakfit_general_action_awaits_helper(env, monkeypatch):
    widget = env.window.peakFitTab
    seen = []

    async def spy(action, msg):
        seen.append(msg)

    monkeypatch.setattr(widget, "_general_action", spy)

    widget.generalAction(lambda fp: None, "custom msg")
    assert seen == ["custom msg"]
    assert env.dialogs == []
    assert env.busy == [True, False]
    env.reset()

    widget.add_tag()
    assert seen == ["custom msg", "add tag"]
    assert env.dialogs == []
    assert env.busy == [True, False]
    env.reset()

    widget.addToMassList()
    assert seen == ["custom msg", "add tag", "add to mass list"]
    assert env.dialogs == []
    assert env.busy == [True, False]
    env.reset()

    widget.remove_tag()
    assert seen == ["custom msg", "add tag", "add to mass list", "add tag"]
    assert env.dialogs == []
    assert env.busy == [True, False]


def test_peakfit_fit_awaits_selected_helper(env, monkeypatch):
    widget = env.window.peakFitTab
    seen = []

    async def calc_spy():
        seen.append("calc")

    async def mass_spy():
        seen.append("mass list")

    monkeypatch.setattr(widget, "fit_formula", calc_spy)
    monkeypatch.setattr(widget, "fit_mass_list", mass_spy)

    widget.ui.fitComboBox.setCurrentIndex(0)
    widget.fit()
    assert seen == ["calc"]
    assert env.dialogs == []
    assert env.busy == [True, False]
    env.reset()

    widget.ui.fitComboBox.setCurrentIndex(1)
    widget.fit()
    assert seen == ["calc", "mass list"]
    assert env.dialogs == []
    assert env.busy == [True, False]


# --------------------------------------------------------------------------
# showSelect: the one MultiProcess pipeline of the batch
# --------------------------------------------------------------------------

def test_peakfit_show_select_multiprocess_pipeline(env):
    window = env.window
    widget = window.peakFitTab
    workspace = window.manager.workspace

    workspace.data.calibrated_spectra.append(_spectrum())
    window.manager.getters.spectra_list_selected_index.connect(lambda: 0)
    workspace.info.peak_shape_tab.func = NormalDistributionFunc(
        peak_fit_sigma=_SIGMA, peak_fit_res=_RES)

    widget.showSelect()

    assert env.dialogs == []
    assert env.busy == [True, False]
    assert env.msgs == [
        "read spectrum", "fit use peak shape func", "calc formula"]
    info = workspace.info.peak_fit_tab
    assert info.spectrum is not None
    assert len(info.peaks) >= 1
    assert len(info.shown_mz) == len(info.shown_intensity)
    assert len(info.raw_split_num) == len(info.original_indexes)


# --------------------------------------------------------------------------
# do_step / replot_within_peaks
# --------------------------------------------------------------------------

def test_peakfit_do_step_runs_worker(env):
    widget = env.window.peakFitTab
    widget.do_step()
    assert env.dialogs == []
    assert env.busy == [True, False]
    assert "step" in env.msgs
    assert widget.info.shown_indexes == []


def test_peakfit_replot_within_peaks_runs_worker(env):
    widget = env.window.peakFitTab
    _install_peak_fit(env.window)

    widget.replot_within_peaks()

    assert env.dialogs == []
    assert env.busy == [True, False]
    assert "calc residual" in env.msgs
    info = widget.info
    assert len(info.shown_mz) == len(info.shown_intensity)
    assert len(info.shown_mz) == len(info.shown_residual)
