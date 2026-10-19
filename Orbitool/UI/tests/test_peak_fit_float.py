"""Offscreen coverage for the Peak Fit float window changes: row selection,
segment lookup that survives another window's save, the per-window formula
result window, and the Fit guard.

No RAW data is used; the window is built through the shared migration harness.
"""
from array import array
from datetime import datetime, timedelta

import numpy as np
import pytest
from PySide6 import QtCore, QtWidgets
from pyteomics.mass.mass import isotopologues

from ...models.formula import Formula
from ...models.peakfit.normal_distribution import NormalDistributionFunc
from ...models.spectrum import FittedPeak, Peak, Spectrum
from .. import PeakFitFloatUiPy
from ..formulas.FormulaResultUiPy import Window as FormulaResultWindow
# debug_settings is an autouse fixture re-exported for pytest
from ..tests.migration_harness import MigrationEnv, debug_settings  # noqa: F401

_START = datetime(2024, 1, 1, 12)

_SIGMA = 2.852197450904393e-06
_RES = 148889.02590153966


@pytest.fixture(scope="module")
def env(request):
    return MigrationEnv().build(request)


@pytest.fixture(autouse=True)
def reset_state(env):
    env.reset()
    env.window.manager.close_peak_float_wins()
    info = env.window.manager.workspace.info.peak_fit_tab
    empty = np.empty(0, float)
    info.spectrum = None
    info.raw_peaks = []
    info.raw_split_num = array("i")
    info.original_indexes = array("i")
    info.peaks = []
    info.shown_indexes = array("i")
    info.shown_mz = empty
    info.shown_intensity = empty
    info.shown_residual = empty
    env.window.manager.workspace.info.peak_shape_tab.func = None


def _spectrum():
    mz = np.linspace(99.99, 200.01, 801)
    intensity = np.exp(-0.5 * ((mz - 100.0) / 2e-4) ** 2)
    return Spectrum(
        mz=mz, intensity=intensity, path="none:",
        start_time=_START, end_time=_START + timedelta(minutes=1))


def _raw(center):
    mz = np.linspace(center - 0.01, center + 0.01, 201)
    intensity = np.exp(-((mz - center) / 0.002) ** 2)
    return Peak(mz=mz, intensity=intensity)


def _fitted(center, formula):
    mz = np.linspace(center - 0.01, center + 0.01, 201)
    intensity = np.exp(-((mz - center) / 0.002) ** 2)
    return FittedPeak(
        mz=mz, intensity=intensity,
        fitted_param=np.array([1.0, center]),
        peak_position=center, peak_intensity=1.0, area=1.0,
        tags="", formulas=[Formula(formula)] if formula else [])


def _install_two_segments(window):
    info = window.manager.workspace.info.peak_fit_tab
    info.spectrum = _spectrum()
    info.raw_peaks = [_raw(100.0), _raw(200.0)]
    info.peaks = [
        _fitted(100.0, "CH4"), _fitted(100.001, "CH4"),
        _fitted(200.0, "C2H6"), _fitted(200.001, "C2H6"),
    ]
    info.original_indexes = array("i", [0, 0, 1, 1])
    info.shown_indexes = array("i", [0, 1, 2, 3])
    info.raw_split_num = array("i", [2, 2])
    window.manager.workspace.info.peak_shape_tab.func = NormalDistributionFunc(
        peak_fit_sigma=_SIGMA, peak_fit_res=_RES)


def _install_isotopes(window):
    info = window.manager.workspace.info.peak_fit_tab
    origin = Formula("CH4")
    entries = [(Formula(isotope), abundance) for isotope, abundance in isotopologues(
        formula=str(origin.toStr(True, False)), isotope_threshold=1e-8,
        overall_threshold=1e-8, report_abundance=True)]
    peaks = []
    for formula, abundance in entries:
        mass = formula.mass()
        mz = np.linspace(mass - 0.001, mass + 0.001, 11)
        intensity = np.exp(-((mz - mass) / 0.0002) ** 2) * abundance
        peaks.append(FittedPeak(
            mz=mz, intensity=intensity,
            fitted_param=np.array([abundance, mass]),
            peak_position=mass, peak_intensity=abundance, area=abundance,
            tags="", formulas=[formula]))
    peaks.sort(key=lambda peak: peak.peak_position)

    info.spectrum = _spectrum()
    info.raw_peaks = [_raw(peaks[0].peak_position),
                      _raw(peaks[1].peak_position)]
    info.peaks = peaks
    info.original_indexes = array("i", [0] + [1] * (len(peaks) - 1))
    info.shown_indexes = array("i", list(range(len(peaks))))
    info.raw_split_num = array("i", [1, len(peaks) - 1])
    window.manager.workspace.info.peak_shape_tab.func = NormalDistributionFunc(
        peak_fit_sigma=_SIGMA, peak_fit_res=_RES)


def test_peak_list_selects_rows(env):
    table = env.window.peakList.ui.tableWidget
    assert table.selectionBehavior() == \
        QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
    assert table.selectionMode() == \
        QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection


def test_peak_fit_window_title_columns_and_summary(env):
    window = env.window
    _install_two_segments(window)
    win = PeakFitFloatUiPy.Window(window.manager, 0)
    try:
        table = win.ui.peaksTableWidget
        assert win.windowTitle() == "Peak Fit - 100.0000 - CH4"
        assert table.selectionBehavior() == \
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        assert table.selectionMode() == \
            QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection
        assert table.horizontalHeaderItem(1).text() == "formula"
        assert table.horizontalHeaderItem(2).text() == "new formula*"
        assert table.isColumnHidden(2)
        assert win.ui.summaryLabel.text() == "No unsaved changes"
        assert not win.ui.savePushButton.isEnabled()

        win.set_formulas(0, [Formula("C2H6")])

        assert table.item(0, 1).text() == "CH4"
        assert table.item(0, 2).text() == "C2H6"
        assert not table.isColumnHidden(2)
        assert win.ui.summaryLabel.text() == "Unsaved changes: formulas"
        assert win.ui.savePushButton.isEnabled()

        win.set_formulas(1, [Formula("C3H8")])

        assert table.currentRow() == 1
        assert table.item(1, 2).text() == "C3H8"
    finally:
        win.close()


def test_new_formula_column_shows_for_added_peak_formula(env):
    window = env.window
    _install_two_segments(window)
    win = PeakFitFloatUiPy.Window(window.manager, 0)
    try:
        win.peaks = win.peaks + [_fitted(100.002, "C3H8")]
        win.showPeak()

        assert not win.ui.peaksTableWidget.isColumnHidden(2)
        summary = win.ui.summaryLabel.text()
        assert "peaks 2 \u2192 3" in summary
        assert "formulas" in summary
    finally:
        win.close()


def test_new_formula_column_stays_hidden_for_a_peaks_only_change(env):
    window = env.window
    _install_two_segments(window)
    win = PeakFitFloatUiPy.Window(window.manager, 0)
    try:
        win.peaks = win.peaks + [_fitted(100.002, None)]
        win.showPeak()

        assert win.ui.peaksTableWidget.isColumnHidden(2)
        summary = win.ui.summaryLabel.text()
        assert "peaks 2 \u2192 3" in summary
        assert "formulas" not in summary
    finally:
        win.close()


def test_segment_lookup_survives_another_window_save(env):
    window = env.window
    _install_two_segments(window)
    info = window.manager.workspace.info.peak_fit_tab
    first = PeakFitFloatUiPy.Window(window.manager, 0)
    second = PeakFitFloatUiPy.Window(window.manager, 1)
    try:
        first.peaks = first.peaks[:1]
        first.save()
        assert list(info.original_indexes) == [0, 1, 1]

        second.set_formulas(2, [Formula("C3H8")])

        assert [str(p.formulas[0]) if p.formulas else "" for p in second.peaks] \
            == ["C2H6", "C3H8"]
        assert second._segment_slice() == slice(1, 3)

        second.save()
        assert [str(p.formulas[0]) for p in info.peaks] \
            == ["CH4", "C2H6", "C3H8"]
    finally:
        first.close()
        second.close()


def test_formula_result_peak_bound_and_global_modes(env):
    window = env.window
    _install_two_segments(window)
    peak_fit = PeakFitFloatUiPy.Window(window.manager, 0)
    peak_fit.open_formula_window(0)
    bound = peak_fit.formulas_result_win
    global_win = FormulaResultWindow.fromInputStr(window.manager, "CH4")
    try:
        assert bound.peak_bound
        assert bound.windowTitle() == "Formula Calculation Result - 100.0000"
        assert bound.ui.lineEdit.isReadOnly()
        assert bound.ui.calcPushButton.isEnabled()
        assert not bound.ui.deleteToolButton.isHidden()
        assert not bound.ui.useSelectedToolButton.isHidden()
        assert bound.ui.resultTableWidget.selectionBehavior() == \
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        assert bound.ui.resultTableWidget.selectionMode() == \
            QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection
        assert bound.ui.isotopesTableWidget.selectionMode() == \
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        assert bound.ui.isotopesTableWidget.selectionBehavior() == \
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectColumns
        assert bound.ui.isotopesTableWidget.verticalHeaderItem(4).text() \
            == "theoretical ratio"
        # the first candidate is selected on open, so its distribution is shown
        assert bound.ui.showDistributionPushButton.isEnabled()

        bound.ui.resultTableWidget.setCurrentIndex(QtCore.QModelIndex())
        assert not bound.ui.showDistributionPushButton.isEnabled()

        bound.ui.resultTableWidget.setCurrentCell(0, 0)
        assert bound.ui.showDistributionPushButton.isEnabled()

        assert not global_win.peak_bound
        assert global_win.windowTitle() == "Formula Calculation Result"
        assert global_win.ui.deleteToolButton.isHidden()
        assert global_win.ui.useSelectedToolButton.isHidden()
        assert not global_win.ui.closeToolButton.isHidden()
    finally:
        bound.close()
        global_win.close()
        peak_fit.close()


def test_formula_result_finds_isotopes_across_segments(env):
    window = env.window
    _install_isotopes(window)
    peak_fit = PeakFitFloatUiPy.Window(window.manager, 0)
    peak_fit.open_formula_window(0)
    bound = peak_fit.formulas_result_win
    try:
        bound.plot_formula(0)
        table = bound.ui.isotopesTableWidget
        assert table.columnCount() > 1
        assert table.item(bound.TOLERANCE_ROW, 1) is not None
        assert table.item(bound.TOLERANCE_ROW, 1).text() != ""
        assert table.item(bound.FORMULA_ROW, 1).data(
            QtCore.Qt.ItemDataRole.UserRole) is not None
        assert table.cellWidget(bound.CHART_ROW, 1) is not None
    finally:
        bound.close()
        peak_fit.close()


def test_bound_formula_accept_and_delete(env):
    window = env.window
    _install_two_segments(window)
    peak_fit = PeakFitFloatUiPy.Window(window.manager, 0)
    try:
        peak_fit.open_formula_window(0)
        bound = peak_fit.formulas_result_win
        accepted = bound.formulas[0]
        bound.ui.resultTableWidget.selectRow(0)
        bound.accept()

        assert [str(f) for f in peak_fit.peaks[0].formulas] \
            == [str(accepted)]
        assert peak_fit.formulas_result_win is None
        assert not bound.isVisible()

        peak_fit.open_formula_window(0)
        bound = peak_fit.formulas_result_win
        bound.delete_formula()

        assert peak_fit.peaks[0].formulas == []
        assert peak_fit.formulas_result_win is None
    finally:
        peak_fit.close()


def test_owner_save_closes_formula_window(env):
    window = env.window
    _install_two_segments(window)
    peak_fit = PeakFitFloatUiPy.Window(window.manager, 0)
    try:
        peak_fit.open_formula_window(0)
        bound = peak_fit.formulas_result_win
        peak_fit.save()

        assert peak_fit.formulas_result_win is None
        assert not bound.isVisible()
    finally:
        peak_fit.close()


def test_bound_edit_targets_open_segment_pending_peaks(env):
    window = env.window
    _install_isotopes(window)
    info = window.manager.workspace.info.peak_fit_tab
    target = PeakFitFloatUiPy.Window.get_or_create(window.manager, 2)
    target_formula = target.peaks[0].formulas[0]
    target.peaks = target.peaks[:1]
    target.peaks[0].formulas = []
    info.peaks[1].formulas = []

    owner = PeakFitFloatUiPy.Window(window.manager, 0)
    owner.open_formula_window(0)
    bound = owner.formulas_result_win
    try:
        bound.plot_formula(0)
        table = bound.ui.isotopesTableWidget
        target_mass = target.peaks[0].peak_position
        column = next(
            column for column in range(table.columnCount())
            if table.item(bound.TOLERANCE_ROW, column) is not None
            and table.item(bound.TOLERANCE_ROW, column).text()
            and abs(Formula(table.item(bound.FORMULA_ROW, column).text()).mass()
                    / target_mass - 1) < 1e-6)
        bound.edit_peak_column(column)

        assert [str(f) for f in target.peaks[0].formulas] \
            == [str(target_formula)]
        assert info.peaks[1].formulas == []
    finally:
        bound.close()
        owner.close()
        target.close()


def test_fit_requires_closing_float_windows(env, monkeypatch):
    window = env.window
    _install_two_segments(window)
    peak_fit = PeakFitFloatUiPy.Window.get_or_create(window.manager, 0)
    seen = []

    async def calc_spy():
        seen.append("calc")

    monkeypatch.setattr(window.peakFitTab, "fit_formula", calc_spy)
    monkeypatch.setattr(
        QtWidgets.QMessageBox, "question",
        lambda *args, **kwargs: QtWidgets.QMessageBox.StandardButton.No)

    window.peakFitTab.fit()
    assert seen == []
    assert peak_fit.original_index in window.manager.peak_float_wins

    monkeypatch.setattr(
        QtWidgets.QMessageBox, "question",
        lambda *args, **kwargs: QtWidgets.QMessageBox.StandardButton.Yes)

    window.peakFitTab.fit()
    assert seen == ["calc"]
    assert window.manager.peak_float_wins == {}
