"""Mass Defect is a pop-up opened from Peak Fit, not a central tab.

Each press of the Peak Fit Actions button opens a NEW non-modal window that
snapshots the peaks currently shown (`shown_indexes`) and receives them in
memory. The windows are independent and unpersisted, so a user can keep one
per spectrum and compare them; closing a window drops it from the manager's
list. Re-filtering Peak Fit afterwards never changes an open window.
"""
import csv
import importlib
from types import SimpleNamespace

import numpy as np
import pytest

from ...models.formula import Formula
from ...models.spectrum import FittedPeak
# debug_settings is an autouse fixture re-exported for pytest
from .migration_harness import MigrationEnv, debug_settings  # noqa: F401

massdefect_module = importlib.import_module("Orbitool.UI.MassDefectUiPy")


@pytest.fixture(scope="module")
def env(request):
    return MigrationEnv().build(request)


@pytest.fixture(autouse=True)
def reset_state(env):
    env.reset()
    info = env.window.manager.workspace.info.peak_fit_tab
    info.peaks = []
    info.shown_indexes = []
    info.spectrum = None
    for win in list(env.window.manager.mass_defect_wins):
        win.close()


def _fitted(position, formulas, intensity):
    mz = np.array([position - 1e-3, position, position + 1e-3])
    intensity_array = np.array([0.5, 1.0, 0.5]) * intensity
    return FittedPeak(
        mz=mz, intensity=intensity_array,
        fitted_param=np.array([1.0, position]),
        peak_position=position, peak_intensity=intensity, area=1.0,
        tags="", formulas=formulas)


def _install(info, shown):
    info.peaks = [_fitted(100.0, [Formula("CH4")], 2.0),
                  _fitted(101.0, [], 1.0),
                  _fitted(102.0, [Formula("CH4")], 3.0),
                  _fitted(103.0, [], 4.0)]
    info.shown_indexes = shown


# --------------------------------------------------------------------------
# Reachability: no central tab, button sits right of add-to-mass-list
# --------------------------------------------------------------------------

def test_mass_defect_is_not_a_central_tab(env):
    tab = env.window.ui.tabWidget
    titles = [tab.tabText(i) for i in range(tab.count())]
    assert "Mass Defect" not in titles


def test_actions_group_has_mass_defect_button_right_of_add_to_mass_list(env):
    ui = env.window.peakFitTab.ui
    layout = ui.groupBox_2.layout()
    sub = None
    for i in range(layout.count()):
        child = layout.itemAt(i).layout()
        if child is not None and child.indexOf(
                ui.actionAddToMassListPushButton) >= 0:
            sub = child
    assert sub is not None
    assert sub.indexOf(ui.actionMassDefectPushButton) == (
        sub.indexOf(ui.actionAddToMassListPushButton) + 1)


# --------------------------------------------------------------------------
# Multi-window snapshot semantics
# --------------------------------------------------------------------------

def test_each_open_adds_an_independent_window(env):
    window = env.window
    info = window.manager.workspace.info.peak_fit_tab
    _install(info, [0, 1, 2, 3])

    window.peakFitTab.openMassDefect()
    assert env.dialogs == []
    assert env.busy == [True, False]

    wins = window.manager.mass_defect_wins
    assert len(wins) == 1
    first = wins[0]
    assert first.isVisible()
    assert list(first.clr.x) == [100.0, 102.0]
    assert list(first.gry.x) == [101.0, 103.0]

    # re-filtering Peak Fit afterwards must not touch the open window
    info.shown_indexes = [1]
    info.peaks = [_fitted(200.0, [Formula("CH4")], 1.0)]
    assert list(first.clr.x) == [100.0, 102.0]

    # a second open is a new window with the new snapshot; the first stays
    info.peaks = [_fitted(200.0, [Formula("CH4")], 1.0),
                  _fitted(201.0, [Formula("CH4")], 2.0)]
    info.shown_indexes = [0, 1]
    window.peakFitTab.openMassDefect()
    assert len(wins) == 2
    second = wins[1]
    assert second is not first
    assert list(second.clr.x) == [200.0, 201.0]
    assert len(second.gry.x) == 0
    assert list(first.clr.x) == [100.0, 102.0]   # untouched


def test_title_uses_spectrum_time_then_untitled(env):
    window = env.window
    info = window.manager.workspace.info.peak_fit_tab
    _install(info, [0, 2])

    window.peakFitTab.openMassDefect()
    assert window.manager.mass_defect_wins[-1].windowTitle() == (
        "Mass Defect Untitled")

    info.spectrum = SimpleNamespace(
        start_time="10:23:45", end_time="10:24:00")
    window.peakFitTab.openMassDefect()
    assert window.manager.mass_defect_wins[-1].windowTitle() == (
        "Mass Defect 10:23:45-10:24:00")


def test_closing_a_window_drops_it_from_the_list(env):
    window = env.window
    info = window.manager.workspace.info.peak_fit_tab
    _install(info, [0, 1, 2])
    window.peakFitTab.openMassDefect()
    win = window.manager.mass_defect_wins[-1]
    win.close()
    assert win not in window.manager.mass_defect_wins


def test_single_point_snapshot_does_not_crash(env):
    # one colored peak (or several of equal size) makes max == min; the plot
    # must still draw instead of dividing by zero into NaN sizes
    window = env.window
    info = window.manager.workspace.info.peak_fit_tab
    info.peaks = [_fitted(100.0, [Formula("CH4")], 2.0)]
    info.shown_indexes = [0]

    window.peakFitTab.openMassDefect()
    assert env.dialogs == []
    win = window.manager.mass_defect_wins[-1]
    assert list(win.clr.x) == [100.0]


def test_only_grey_peaks_snapshot_does_not_crash(env):
    # no peak carries a formula, so there is nothing colored to normalise;
    # opening and then showing the grey points must not fail on empty arrays
    window = env.window
    info = window.manager.workspace.info.peak_fit_tab
    info.peaks = [_fitted(100.0, [], 2.0), _fitted(101.0, [], 3.0)]
    info.shown_indexes = [0, 1]

    window.peakFitTab.openMassDefect()
    assert env.dialogs == []
    win = window.manager.mass_defect_wins[-1]
    assert len(win.clr.x) == 0
    assert list(win.gry.x) == [100.0, 101.0]

    env.reset()
    win.ui.showGreyCheckBox.setChecked(True)   # triggers replot
    assert env.busy == []
    assert env.dialogs == []


# --------------------------------------------------------------------------
# Colouring/display controls and Export still work off the snapshot
# --------------------------------------------------------------------------

def test_calc_button_recomputes_from_snapshot(env):
    window = env.window
    info = window.manager.workspace.info.peak_fit_tab
    _install(info, [0, 1, 2, 3])
    window.peakFitTab.openMassDefect()
    assert env.busy == [True, False]
    env.reset()
    win = window.manager.mass_defect_wins[-1]

    win.ui.dbeRadioButton.setChecked(True)
    win.ui.calcPushButton.click()
    assert env.busy == [True, False]
    assert env.dialogs == []
    assert win.clr_title == "DBE"


def test_export_writes_snapshot(env, tmp_path, monkeypatch):
    window = env.window
    info = window.manager.workspace.info.peak_fit_tab
    _install(info, [0, 1, 2, 3])
    window.peakFitTab.openMassDefect()
    assert env.busy == [True, False]
    env.reset()
    win = window.manager.mass_defect_wins[-1]

    dst = tmp_path / "mass_defect.csv"
    monkeypatch.setattr(
        massdefect_module, "savefile", lambda *a, **k: (True, str(dst)))
    win.export()

    assert env.dialogs == []
    assert env.busy == [True, False]
    with open(dst, newline="") as f:
        rows = list(csv.reader(f))
    assert rows[0] == ["x", "mass defect", "intensity", "color"]
    # colored rows first, then grey rows
    assert [row[0] for row in rows[1:]] == ["100.0", "102.0", "101.0", "103.0"]
