"""Executable coverage for the ticket-11 migration of `MainUiPy` (the last
file still carrying the old decorator): the ten remaining task sites were
rewritten as `ui_task` coroutines, so every relay endpoint now lives in the
new mechanism.

The batch is six default sites (the four workspace/config file handlers plus
`setting_dialog` and `save`) and four `join` sites (the relay handlers
`file_tab_finish` / `peak_shape_tab_finish` / `calibration_finish` /
`noise_tab_finish`, the last ticket 08 had already moved). No site carries a
former task generator or an old error-registration rewrite.

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

import pytest

# debug_settings is an autouse fixture re-exported for pytest
from .tests.migration_harness import (  # noqa: F401
    MigrationEnv, debug_settings, task_module)

main_module = importlib.import_module("Orbitool.UI.MainUiPy")

_ALL_SITES = [
    "setting_dialog", "load", "save", "save_as", "loadConfig", "saveConfig",
    "file_tab_finish", "noise_tab_finish",
    "peak_shape_tab_finish", "calibration_finish",
]


@pytest.fixture(scope="module")
def env(request):
    return MigrationEnv().build(request)


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


# --------------------------------------------------------------------------
# Decoration: all 10 sites are ui_task coroutines, the 4 relay sites join
# --------------------------------------------------------------------------

def test_main_window_sites_are_coroutine_tasks():
    for name in _ALL_SITES:
        assert isinstance(
            main_module.Window.__dict__[name], task_module.ui_task), name
    assert len(_ALL_SITES) == 10
    # the plain method this ticket must not touch keeps its shape
    assert not isinstance(
        main_module.Window.__dict__["abort_process"], task_module.ui_task)


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
