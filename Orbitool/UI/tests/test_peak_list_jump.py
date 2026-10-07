"""Right-clicking a Peak List row offers "Jump to peak".

The menu selects the row under the cursor and acts on the current selection
(single row today). Choosing the action centers the Peak Fit plot on that peak
(±5 m/z), rescales y to the new window, and switches to the Peak Fit tab.
"""
from array import array
from types import SimpleNamespace

import numpy as np
import pytest
from PySide6 import QtCore

from ...models.spectrum import FittedPeak
# debug_settings is an autouse fixture re-exported for pytest
from .migration_harness import MigrationEnv, debug_settings  # noqa: F401


@pytest.fixture(scope="module")
def env(request):
    return MigrationEnv().build(request)


@pytest.fixture(autouse=True)
def reset_state(env):
    env.reset()
    info = env.window.manager.workspace.info.peak_fit_tab
    info.peaks = []
    info.shown_indexes = []
    info.raw_peaks = []
    info.original_indexes = []
    info.raw_split_num = array("i")
    info.shown_mz = None
    info.shown_intensity = None
    info.spectrum = None
    env.window.peakList.ui.tableWidget.setRowCount(0)
    env.window.ui.tabWidget.setCurrentWidget(env.window.peakFitTab)


def _fitted(position, intensity):
    mz = np.array([position - 1e-3, position, position + 1e-3])
    return FittedPeak(
        mz=mz, intensity=np.array([0.5, 1.0, 0.5]) * intensity,
        fitted_param=np.array([1.0, position]),
        peak_position=position, peak_intensity=intensity, area=1.0,
        tags="", formulas=[])


def _install(info, shown=None):
    peaks = [_fitted(100.0, 1000.0), _fitted(101.0, 1.0),
             _fitted(102.0, 300.0), _fitted(103.0, 4000.0)]
    info.peaks = peaks
    info.shown_indexes = (list(range(len(peaks)))
                          if shown is None else shown)
    info.original_indexes = list(range(len(peaks)))
    info.raw_split_num = array("i", [1] * len(peaks))
    info.shown_mz = np.concatenate([p.mz for p in peaks])
    info.shown_intensity = np.concatenate([p.intensity for p in peaks])
    info.spectrum = SimpleNamespace()


def test_table_uses_custom_context_menu(env):
    table = env.window.peakList.ui.tableWidget
    assert table.contextMenuPolicy() == (
        QtCore.Qt.ContextMenuPolicy.CustomContextMenu)


def test_jump_centers_plot_and_switches_tab(env):
    window = env.window
    info = window.manager.workspace.info.peak_fit_tab
    _install(info, shown=[1, 2, 3])   # display rows are offset from true indexes
    info.spectrum = None              # menu must be enabled only with a spectrum
    window.manager.signals.peak_list_show.emit()
    info.spectrum = SimpleNamespace()

    table = window.peakList.ui.tableWidget
    assert table.rowCount() == 3
    table.selectRow(1)                # display row 1 -> true index 2 (m/z 102)

    window.ui.tabWidget.setCurrentWidget(window.noiseTab)
    window.peakList.jump_to_selected_peak()

    x_min, x_max = window.peakFitTab.plot.ax.get_xlim()
    assert x_min == pytest.approx(97.0)
    assert x_max == pytest.approx(107.0)
    # y follows the target peak (300) even though a neighbour is 4000
    y_min, y_max = window.peakFitTab.plot.ax.get_ylim()
    assert y_min == pytest.approx(-15.0)
    assert y_max == pytest.approx(315.0)
    assert window.ui.tabWidget.currentWidget() is window.peakFitTab


def test_jump_action_disabled_without_spectrum(env):
    window = env.window
    info = window.manager.workspace.info.peak_fit_tab
    _install(info)
    info.spectrum = None
    action = window.peakList.build_context_menu().actions()[0]
    assert not action.isEnabled()

    info.spectrum = SimpleNamespace()
    action = window.peakList.build_context_menu().actions()[0]
    assert action.isEnabled()


def test_right_click_outside_rows_opens_no_menu(env, monkeypatch):
    window = env.window
    calls = []
    monkeypatch.setattr(
        window.peakList, "build_context_menu",
        lambda: calls.append(True))

    # an empty table has no item at any position
    pos = window.peakList.ui.tableWidget.viewport().rect().center()
    window.peakList.show_context_menu(pos)
    assert calls == []
