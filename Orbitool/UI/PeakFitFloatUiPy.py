from copy import deepcopy
from typing import List, Optional

import matplotlib.ticker
import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets

from Orbitool import logger
from Orbitool.models import peakfit
from Orbitool.models.formula import Formula
from Orbitool.models.spectrum import FittedPeak
from Orbitool.utils import binary_search

from . import PeakFitFloatUi
from .component import Plot
from .formulas import FormulaResultWindow
from .manager import Manager, ui_task
from .utils import set_header_sizes

TAG = "PeakFitFloatUiPy"


class Window(QtWidgets.QMainWindow):
    """One segment's Peak Fit window; it owns at most one formula result window."""

    callback = QtCore.Signal()

    @classmethod
    def get_or_create(cls, manager: Manager, peak_index: int):
        info = manager.workspace.info.peak_fit_tab
        original_index = info.original_indexes[peak_index]
        wins = manager.peak_float_wins
        if original_index in wins:
            win = wins[original_index]
        else:
            win = cls(manager, original_index)
            wins[original_index] = win
        return win

    def __init__(self, manager: Manager, original_index: int) -> None:
        """Build a window without registering it; use `get_or_create` to share."""
        super().__init__()
        self.manager = manager
        self.ui = PeakFitFloatUi.Ui_MainWindow()
        self.setupUi()

        self.original_index = original_index
        self.formulas_result_win: Optional[FormulaResultWindow] = None
        self.peaks: List[FittedPeak] = deepcopy(self._saved_peaks())

        self.showPeak()
        self.plotPeak()

    def setupUi(self):
        ui = self.ui
        ui.setupUi(self)
        self.plot = Plot(ui.widget)
        ui.refitPushButton.clicked.connect(self.refit)
        ui.savePushButton.clicked.connect(self.save)
        ui.closePushButton.clicked.connect(self.close)
        ui.editSelectedPushButton.clicked.connect(self.editSelected)

        ui.sumCheckBox.clicked.connect(self.replotPeak)
        ui.idealCheckBox.clicked.connect(self.replotPeak)
        ui.legendCheckBox.clicked.connect(self.replotPeak)
        ui.originCheckBox.clicked.connect(self.replotPeak)
        ui.residualCheckBox.clicked.connect(self.replotPeak)
        set_header_sizes(ui.peaksTableWidget.horizontalHeader(),
                         [120, 200, 150, 110, 90, 100, 110])
        ui.peaksTableWidget.currentCellChanged.connect(
            self._update_edit_button)

        ui.peaksTableWidget.itemDoubleClicked.connect(self.finetuneFormula)

    def _segment_slice(self) -> slice:
        return binary_search.indexBetween(
            self.info.original_indexes, (self.original_index, self.original_index))

    def _saved_peaks(self) -> List[FittedPeak]:
        return self.info.peaks[self._segment_slice()]

    def _saved_formulas(self) -> List[str]:
        formulas = []
        for peak in self._saved_peaks():
            for formula in peak.formulas:
                text = str(formula)
                if text and text not in formulas:
                    formulas.append(text)
        return formulas

    def set_formulas(self, peak_index: int, formulas: List[Formula]):
        local_index = peak_index - self._segment_slice().start
        if 0 <= local_index < len(self.peaks):
            self.peaks[local_index].formulas = formulas
            self.showPeak(local_index)

    @property
    def info(self):
        return self.manager.workspace.info.peak_fit_tab

    def _close_formula_window(self):
        win = self.formulas_result_win
        self.formulas_result_win = None
        if win is not None:
            win.close()

    def open_formula_window(self, row: int):
        if not 0 <= row < len(self.peaks):
            return
        logger.i(TAG, f"open_formula_window() row={row}")
        self._close_formula_window()
        win = FormulaResultWindow.fromPeakFitWindow(self, row)
        self.formulas_result_win = win
        win.acceptSignal.connect(
            lambda formulas, row=row: self.finetuneFinish(row, formulas))
        win.show()
        win.raise_()

    @ui_task
    async def editSelected(self):
        row = self.ui.peaksTableWidget.currentRow()
        if row < 0:
            return
        logger.i(TAG, f"editSelected() row={row}")
        self.open_formula_window(row)

    @ui_task
    async def finetuneFormula(self, item: QtWidgets.QTableWidgetItem):
        logger.i(TAG, f"finetuneFormula() row={item.row()}")
        self.open_formula_window(item.row())

    def finetuneFinish(self, local_index: int, formulas: List[Formula]):
        if 0 <= local_index < len(self.peaks):
            logger.i(
                TAG, f"finetuneFinish() row={local_index} formulas={len(formulas)}")
            self.peaks[local_index].formulas = formulas
            self.showPeak(local_index)

    def updateTitle(self):
        peak = self.info.raw_peaks[self.original_index]
        mz = peak.mz[peak.intensity.argmax()]
        formulas = self._saved_formulas()
        title = f"Peak Fit - {mz:.4f}"
        if formulas:
            title += " - " + ", ".join(formulas)
        self.setWindowTitle(title)

    def _change_categories(self) -> List[str]:
        saved = self._saved_peaks()
        current = self.peaks
        changes = []
        if len(saved) != len(current):
            changes.append(f"peaks {len(saved)} \u2192 {len(current)}")

        positions = intensities = formulas = False
        for old, new in zip(saved, current):
            if old.peak_position != new.peak_position:
                positions = True
            if old.peak_intensity != new.peak_intensity:
                intensities = True
            if [str(f) for f in old.formulas] != [str(f) for f in new.formulas]:
                formulas = True

        if len(current) > len(saved):
            if any(new.formulas for new in current[len(saved):]):
                formulas = True
        elif len(saved) > len(current):
            if any(old.formulas for old in saved[len(current):]):
                formulas = True

        if positions:
            changes.append("positions")
        if intensities:
            changes.append("intensities")
        if formulas:
            changes.append("formulas")
        return changes

    def _update_summary(self):
        changes = self._change_categories()
        self.ui.peaksTableWidget.setColumnHidden(2, "formulas" not in changes)
        if changes:
            self.ui.summaryLabel.setStyleSheet("")
            self.ui.summaryLabel.setText(
                "Unsaved changes: " + ", ".join(changes))
        else:
            self.ui.summaryLabel.setStyleSheet("color: gray;")
            self.ui.summaryLabel.setText("No unsaved changes")
        self.ui.savePushButton.setEnabled(bool(changes))
        self._update_edit_button()

    def _update_edit_button(self, *_):
        table = self.ui.peaksTableWidget
        self.ui.editSelectedPushButton.setEnabled(
            table.rowCount() > 0 and table.currentRow() >= 0)

    def showPeak(self, current_row: Optional[int] = None):
        self.updateTitle()
        origin_peak = self.info.raw_peaks[self.original_index]
        peaks = self.info.peaks
        saved_peaks = self._saved_peaks()
        show_peaks = self.peaks

        ui = self.ui
        ui.spinBox.setValue(len(show_peaks))

        table = ui.peaksTableWidget
        if current_row is None:
            current_row = table.currentRow()
        table.clearContents()
        table.setRowCount(0)
        table.setRowCount(len(show_peaks))

        rtol = self.manager.workspace.info.formula_docker.calc_gen.rtol

        for index, peak in enumerate(show_peaks):
            def setText(column, msg):
                table.setItem(
                    index, column, QtWidgets.QTableWidgetItem(str(msg)))

            setText(0, format(peak.peak_position, '.5f'))
            if saved_peaks:
                setText(1, ', '.join(str(f) for f in saved_peaks[binary_search.indexNearest(
                    saved_peaks, peak.peak_position, method=peakfit.get_peak_position)].formulas))
            else:
                setText(1, "")
            setText(2, ', '.join(str(f) for f in peak.formulas))
            setText(3, format(peak.peak_intensity, '.3e'))
            setText(5, format(peak.area, '.3e'))
            if len(peak.formulas) == 1:
                setText(4,
                        format((peak.peak_position / peak.formulas[0].mass() - 1) * 1e6, '.5f'))
                formula = peak.formulas[0]
                if formula.isIsotope:
                    origin = formula.findOrigin()
                    mass = origin.mass()
                    d = mass * rtol
                    s = binary_search.indexBetween(
                        peaks, (mass - d, mass + d), method=(lambda peaks, index: peaks[index].peak_position))
                    for p in peaks[s]:
                        for f in p.formulas:
                            if f == origin:
                                setText(6, format(peak.peak_intensity /
                                                  p.peak_intensity, '5f'))
                                setText(
                                    7, format(formula.relativeAbundance(), '.5f'))
                                break
                        else:
                            continue
                        break

        table = ui.intensityTableWidget
        table.clearContents()
        table.setRowCount(0)
        table.setRowCount(len(origin_peak.mz))
        for index, (mz, intensity) in enumerate(zip(origin_peak.mz, origin_peak.intensity)):
            table.setItem(
                index, 0, QtWidgets.QTableWidgetItem(format(mz, '.5f')))
            table.setItem(index, 1, QtWidgets.QTableWidgetItem(
                format(intensity, '.5f')))

        if 0 <= current_row < len(show_peaks):
            ui.peaksTableWidget.setCurrentCell(current_row, 0)
        elif show_peaks:
            ui.peaksTableWidget.setCurrentCell(0, 0)
        self._update_summary()

    def plotPeak(self):
        ui = self.ui
        show_origin = ui.originCheckBox.isChecked()
        show_sum = ui.sumCheckBox.isChecked()
        show_id = ui.idealCheckBox.isChecked()
        show_residual = ui.residualCheckBox.isChecked()
        show_legend = ui.legendCheckBox.isChecked()

        origin_peak = self.info.raw_peaks[self.original_index]
        show_peaks = self.peaks

        func = self.manager.workspace.info.peak_shape_tab.func

        ax = self.plot.ax
        ax.clear()
        ax.axhline(color='k', linewidth=.5)

        if show_origin:
            ax.plot(origin_peak.mz, origin_peak.intensity,
                    label='origin', linewidth=2, color='k')

        id_mz = not show_id or np.arange(
            origin_peak.mz.min(), origin_peak.mz.max(), 2e-5)
        id_int = not show_id or np.zeros_like(id_mz)
        intensity_sum = not show_sum or np.zeros_like(origin_peak.intensity)
        intensity_diff = not show_residual or origin_peak.intensity.copy()

        for index, peak in enumerate(show_peaks):
            ax.plot(peak.mz, peak.intensity,
                    label=f"fitted peak {index}", linewidth=1.5)

            if show_id:
                id_int += func.getIntensity(id_mz, peak)

            if show_sum or show_residual:
                tmp_intensity = func.getIntensity(origin_peak.mz, peak)
                if show_sum:
                    intensity_sum += tmp_intensity
                if show_residual:
                    intensity_diff -= tmp_intensity

        if show_id:
            ax.plot(id_mz, id_int, label="ideal", color='g')

        if len(show_peaks) > 1:
            if show_sum:
                ax.plot(origin_peak.mz, intensity_sum,
                        label="fitted peak sum", linewidth=1.5)

        if show_residual:
            ax.plot(origin_peak.mz, intensity_diff,
                    label="peak residual", color='r', linewidth=1.5)

        ax.xaxis.set_tick_params(rotation=15)
        ax.yaxis.set_tick_params(rotation=60)
        ax.yaxis.set_major_formatter(
            matplotlib.ticker.FormatStrFormatter(r"%.1e"))
        if show_legend:
            ax.legend()

        ax.set_xlim(origin_peak.mz.min(), origin_peak.mz.max())
        self.plot.canvas.draw()

    @ui_task(mode="light")
    async def replotPeak(self):
        self.plotPeak()

    @ui_task
    async def refit(self):
        self._close_formula_window()
        num = self.ui.spinBox.value()
        func = self.manager.workspace.info.peak_shape_tab.func
        info = self.info
        fittedpeaks = func.splitPeak(
            info.raw_peaks[self.original_index], num, True)

        calc_get = self.manager.workspace.info.formula_docker.get_calcer()
        for peak in fittedpeaks:
            peak.formulas = calc_get(peak.peak_position)

        self.peaks = fittedpeaks

        self.showPeak()
        self.plotPeak()

    @ui_task
    async def save(self):
        self._close_formula_window()
        new_peaks = self.peaks

        self.info.raw_split_num[self.original_index] = len(new_peaks)

        peaks = self.info.peaks
        original_indexes = self.info.original_indexes
        shown_indexes = self.info.shown_indexes

        segment = self._segment_slice()
        start, stop = segment.start, segment.stop
        delta = len(new_peaks) - stop + start

        del peaks[start:stop]
        for peak in reversed(new_peaks):
            peaks.insert(start, peak)

        del original_indexes[start:stop]
        for _ in range(len(new_peaks)):
            original_indexes.insert(start, self.original_index)

        i = binary_search.indexFirstNotSmallerThan(shown_indexes, start)
        j = binary_search.indexFirstNotSmallerThan(shown_indexes, stop)
        del shown_indexes[i:j]

        for j in range(len(new_peaks)):
            shown_indexes.insert(i + j, start + j)
        for j in range(i + len(new_peaks), len(shown_indexes)):
            shown_indexes[j] += delta

        self.manager.signals.peak_refit_finish.emit()
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self._close_formula_window()
        self.manager.peak_float_wins.pop(self.original_index, None)
        a0.accept()
