"""Executable coverage for the ticket-11 migration of `MainUiPy` (the last
file carrying `@state_node`): the ten remaining task sites were rewritten as
`ui_task` coroutines, so every relay endpoint now lives in the new mechanism.

The batch is six default sites (the four workspace/config file handlers plus
`setting_dialog` and `save`) and five `join` sites (the four relay handlers
`file_tab_finish` / `peak_shape_tab_finish` / `calibration_finish` /
`show_spectrum` plus `noise_tab_finish`, which ticket 08 had already moved).
`show_spectrum` loses its `withArgs=True` and forwards its spectrum argument
by signature. No site carries a `yield` or an `except_node` rewrite.

No RAW data is available (see `.scratch/ui-state-node-refactor/baseline.md`),
so the end-to-end relay is exercised offscreen through the real signal wiring
instead of the RAW-driven E2E smoke: the four tab callbacks are emitted in
chain order while a holder keeps busy, and the tab progression plus the busy
invariant are asserted. `noise_tab_finish` awaits `peakShapeTab.showPeak()`,
which is stubbed so no peak-shape state has to be ready. `thread_block_gui`
makes workers run inline for deterministic busy edges.

Placed at the batch root (MainUiPy is a top-level `Orbitool/UI` module) and
listed in `pytest.ini`.
"""
import importlib
import inspect
from datetime import datetime, timedelta

import numpy as np
import pytest
from PyQt6 import QtWidgets

from Orbitool import setting
from ..models.spectrum import Spectrum
from .MainUiPy import Window
from .utils import test as uitest

task_module = importlib.import_module("Orbitool.UI.manager.task")
main_module = importlib.import_module("Orbitool.UI.MainUiPy")

# a QApplication with no references gets destroyed, breaking every event
# loop that runs afterwards
app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

_ALL_SITES = [
    "setting_dialog", "load", "save", "save_as", "loadConfig", "saveConfig",
    "file_tab_finish", "show_spectrum", "noise_tab_finish",
    "peak_shape_tab_finish", "calibration_finish",
]
_JOIN_SITES = [
    "file_tab_finish", "show_spectrum", "noise_tab_finish",
    "peak_shape_tab_finish", "calibration_finish",
]


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


def _stub_show_peak(window, monkeypatch):
    # `noise_tab_finish` awaits `peakShapeTab.showPeak()`; stub it so no
    # peak-shape state has to be ready. Patch the class, not the instance:
    # instance-level monkeypatch restores the original bound method into the
    # QWidget instance dict, leaving a sip self-reference that crashes a
    # later Qt test in the same process (pre-existing; recorded, not fixed).
    async def fake_show_peak(self):
        pass

    monkeypatch.setattr(type(window.peakShapeTab), "showPeak", fake_show_peak)


def _spectrum():
    start = datetime(2024, 1, 1, 12)
    return Spectrum(
        mz=np.array([100.0, 100.01, 100.02]),
        intensity=np.array([1.0, 2.0, 1.0]),
        path="none:", start_time=start, end_time=start + timedelta(minutes=1))


# --------------------------------------------------------------------------
# Decoration: all 11 sites are ui_task coroutines, the 5 relay sites join
# --------------------------------------------------------------------------

def test_main_window_sites_are_coroutine_tasks():
    for name in _ALL_SITES:
        task = Window.__dict__[name]
        assert isinstance(task, task_module.ui_task), name
        assert inspect.iscoroutinefunction(task._func), name
    assert len(_ALL_SITES) == 11
    # the plain method this ticket must not touch keeps its shape
    assert not isinstance(
        Window.__dict__["abort_process"], task_module.ui_task)


def test_main_window_modes():
    for name in _JOIN_SITES:
        assert Window.__dict__[name]._mode == "join", name
    for name in set(_ALL_SITES) - set(_JOIN_SITES):
        assert Window.__dict__[name]._mode == "default", name


# --------------------------------------------------------------------------
# join semantics: every relay handler starts while busy, no extra edge
# --------------------------------------------------------------------------

def test_join_handlers_start_while_busy(env, monkeypatch):
    window = env.window
    manager = window.manager
    _stub_show_peak(window, monkeypatch)

    manager.set_busy(True)
    env.busy.clear()
    try:
        # non-chain order: each join handler must start on its own
        window.fileTab.callback.emit()
        window.peakShapeTab.callback.emit(())
        window.calibrationTab.callback.emit()
        window.noiseTab.callback.emit((object(),))

        assert env.dialogs == []          # no "Wait for process"
        assert env.busy == []             # busy already held -> no new edge
        assert manager.busy is True       # each join released only its own count
    finally:
        manager.set_busy(False)

    assert manager.busy is False
    assert env.busy == [False]


# --------------------------------------------------------------------------
# Relay chain: file -> noise -> peak shape -> calibration -> peak fit
# --------------------------------------------------------------------------

def test_relay_chain_tab_progression_keeps_busy(env, monkeypatch):
    window = env.window
    manager = window.manager
    _stub_show_peak(window, monkeypatch)

    manager.set_busy(True)
    env.busy.clear()
    try:
        window.fileTab.callback.emit()
        assert manager.busy is True
        assert window.ui.tabWidget.currentWidget() is window.noiseTab

        window.noiseTab.callback.emit((object(),))
        assert manager.busy is True
        assert window.ui.tabWidget.currentWidget() is window.peakShapeTab

        window.peakShapeTab.callback.emit(())
        assert manager.busy is True
        assert window.ui.tabWidget.currentWidget() is window.calibrationTab

        window.calibrationTab.callback.emit()
        assert manager.busy is True
        assert window.ui.tabWidget.currentWidget() is window.peakFitTab

        assert env.busy == []             # the whole chain adds no busy edge
        assert env.dialogs == []
    finally:
        manager.set_busy(False)

    assert manager.busy is False


# --------------------------------------------------------------------------
# show_spectrum: signature forwarding (the deleted withArgs=True)
# --------------------------------------------------------------------------

def test_show_spectrum_forwards_signature(env, monkeypatch):
    window = env.window
    seen = []
    # patch the class, not the instance: an instance-level monkeypatch restores
    # the original bound method into the QWidget instance dict, leaving a sip
    # self-reference that can crash a later Qt test in the same process
    monkeypatch.setattr(
        type(window.spectrum), "show_spectrum", lambda self, s: seen.append(s))
    window.spectrumDw.hide()

    spectrum = _spectrum()
    window.peakFitTab.show_spectrum.emit(spectrum)      # wired endpoint 1
    assert seen == [spectrum]             # forwarded by signature, not withArgs
    assert env.busy == [True, False]
    assert not window.spectrumDw.isHidden()
    env.reset()

    window.noiseTab.selected_spectrum_average.emit(spectrum)  # wired endpoint 2
    assert seen == [spectrum, spectrum]
    assert env.busy == [True, False]
    assert env.dialogs == []


# --------------------------------------------------------------------------
# Default sites: take/release busy, and are refused while busy
# --------------------------------------------------------------------------

def test_save_default_task_emits_and_persists(env, monkeypatch):
    window = env.window
    manager = window.manager
    saved = []
    saves = []
    saver = lambda: saves.append(1)          # MySignal is weak: keep it alive
    manager.save.connect(saver)
    monkeypatch.setattr(manager.workspace, "save", lambda: saved.append(1))

    window.save()

    assert saves == [1]
    assert saved == [1]
    assert env.dialogs == []
    assert env.busy == [True, False]
    assert not manager.busy


def test_load_default_task_dialog_cancel(env, monkeypatch):
    window = env.window
    monkeypatch.setattr(
        main_module.UiUtils, "openfile", lambda *a, **k: (False, ""))

    window.load()                             # cancelled before any file work

    assert env.dialogs == []
    assert env.busy == [True, False]
    assert not window.manager.busy


def test_default_site_refused_while_busy(env, monkeypatch):
    window = env.window
    manager = window.manager
    saved = []
    monkeypatch.setattr(manager.workspace, "save", lambda: saved.append(1))

    manager.set_busy(True)                    # disables the tree -> call directly
    try:
        window.save()
    finally:
        manager.set_busy(False)

    assert env.dialogs == [("Wait for process", 'busy')]
    assert saved == []                        # refused before running
    assert not manager.busy
