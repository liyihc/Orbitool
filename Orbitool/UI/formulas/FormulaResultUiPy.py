from copy import deepcopy
import re
from typing import List, Optional

from PySide6 import QtCore, QtWidgets
from pyteomics.mass.mass import isotopologues

from Orbitool import logger
from Orbitool.models.formula import Formula
from Orbitool.models.spectrum import FittedPeak
from Orbitool.UI.component import Plot
from Orbitool.UI.manager import Manager, ui_task
from Orbitool.UI.utils import TableUtils
from Orbitool.utils import binary_search

from . import FormulaResultUi

TAG = "FormulaResultUiPy"


class Window(QtWidgets.QMainWindow):
    acceptSignal = QtCore.Signal(list)

    def __init__(self, manager: Manager, input: str, mass: float, formulas: List[Formula], *, owner=None, owner_row: Optional[int] = None) -> None:
        super().__init__()
        self.manager = manager
        self.owner = owner
        self.owner_row = owner_row
        self.peak_bound = owner is not None
        self.mass = mass
        self.ui = FormulaResultUi.Ui_MainWindow()
        self.setupUi()

        self.ui.lineEdit.setText(input)
        self.formulas = deepcopy(formulas)

        self.showResult()

    def setupUi(self):
        ui = self.ui
        ui.setupUi(self)

        ui.resultTableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        ui.isotopesTableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        if self.peak_bound:
            ui.lineEdit.setReadOnly(True)
            self.setWindowTitle(f"Formula Calculation Result - {self.mass:.4f}")
            ui.deleteToolButton.show()
            ui.useSelectedToolButton.show()
        else:
            self.setWindowTitle("Formula Calculation Result")
            ui.deleteToolButton.hide()
            ui.useSelectedToolButton.hide()

        self.plot = Plot(ui.widget)
        ui.calcPushButton.clicked.connect(self.calc)
        ui.resultTableWidget.itemDoubleClicked.connect(self.plot_row)
        ui.resultTableWidget.itemSelectionChanged.connect(
            self._update_result_buttons)
        ui.showDistributionPushButton.clicked.connect(
            self.show_selected_distribution)
        ui.isotopesTableWidget.itemDoubleClicked.connect(self.edit_peak)
        ui.isotopesTableWidget.itemSelectionChanged.connect(
            self._update_edit_button)
        ui.editPeakPushButton.clicked.connect(self.edit_selected_peak)
        ui.showAllToolButton.clicked.connect(self.showResult)
        ui.closeToolButton.clicked.connect(self.close)
        ui.useSelectedToolButton.clicked.connect(self.accept)
        ui.deleteToolButton.clicked.connect(self.delete_formula)

    @classmethod
    def fromInputStr(cls, manager: Manager, input: str):
        return Window(manager, *calc(manager, input))

    @classmethod
    def fromPeakFitWindow(cls, owner, row: int):
        peak = owner.peaks[row]
        return Window(owner.manager, str(peak.peak_position), peak.peak_position,
                      peak.formulas, owner=owner, owner_row=row)

    def find_peak_index(self, mass):
        return binary_search.indexNearest(self.peaks, mass, method=peak_position)

    def matching_peak_index(self, mass):
        if len(self.peaks) == 0:
            return None
        index = self.find_peak_index(mass)
        peak = self.peaks[index]
        if abs(mass) > 1e-6 and abs(peak.peak_position / mass - 1) < 3e-8:
            return index
        return None

    @property
    def peaks(self):
        if not self.peak_bound:
            return self.manager.workspace.info.peak_fit_tab.peaks
        return self._working_targets()[0]

    def _working_targets(self):
        info = self.manager.workspace.info.peak_fit_tab
        saved = info.peaks
        if not self.peak_bound:
            return saved, [(None, index) for index in range(len(saved))]

        original_indexes = info.original_indexes
        windows = dict(self.manager.peak_float_wins)
        windows[self.owner.original_index] = self.owner

        peaks = []
        targets = []
        index = 0
        while index < len(saved):
            original_index = original_indexes[index]
            stop = index
            while (stop < len(saved)
                   and original_indexes[stop] == original_index):
                stop += 1
            window = windows.get(original_index)
            if window is not None:
                for local_index, peak in enumerate(window.peaks):
                    peaks.append(peak)
                    targets.append((window, local_index))
            else:
                for saved_index in range(index, stop):
                    peaks.append(saved[saved_index])
                    targets.append((None, saved_index))
            index = stop
        return peaks, targets

    @ui_task
    async def calc(self):
        if self.peak_bound:
            mass = self.mass
            info = self.manager.workspace.info
            formulas = info.formula_docker.calc_gen.generate().get(
                mass, info.formula_docker.charge)
            formulas.sort(key=lambda f: abs(f.mass() / mass - 1))
            self.formulas = formulas
            self.showResult()
            return

        input = self.ui.lineEdit.text()
        _, mass, formulas = calc(self.manager, input)
        self.mass = mass
        self.formulas = formulas
        self.showResult()

    @ui_task(mode="join")
    async def showResult(self):
        mass = self.mass
        formulas = self.formulas

        table: QtWidgets.QTableWidget = self.ui.resultTableWidget
        table.clearContents()
        table.setRowCount(0)
        table.setRowCount(len(formulas))

        def ppm(m):
            return (m / mass - 1) * 1e6

        for index, formula in enumerate(formulas):
            def setText(column, text):
                table.setItem(index, column, QtWidgets.QTableWidgetItem(text))
            setText(0, str(formula))
            setText(1, format(formula.mass(), '.6f'))
            setText(2, format(ppm(formula.mass()), '.2f'))
            setText(3, format(formula.dbe(), '.1f'))
        table.resizeColumnsToContents()

        isotopes_table = self.ui.isotopesTableWidget
        isotopes_table.clearContents()
        isotopes_table.setRowCount(0)

        ax = self.plot.ax
        ax.clear()

        intensity = 1
        if self.peak_bound:
            if 0 <= self.owner_row < len(self.owner.peaks):
                peak = self.owner.peaks[self.owner_row]
                intensity = peak.peak_intensity
                ax.plot(peak.mz, peak.intensity)
        else:
            index = self.matching_peak_index(mass)
            if index is not None:
                peak = self.peaks[index]
                intensity = peak.peak_intensity
                ax.plot(peak.mz, peak.intensity)

        for f in self.formulas:
            m = f.mass()
            ax.plot([m, m], [0, intensity])
            ax.annotate(str(f), [m, intensity])

        self.plot.canvas.draw()
        self._update_result_buttons()
        self._update_edit_button()

    @ui_task
    async def plot_row(self, item: QtWidgets.QTableWidgetItem):
        self.plot_formula(item.row())

    @ui_task
    async def show_selected_distribution(self):
        row = self.ui.resultTableWidget.currentRow()
        if row < 0:
            return
        logger.i(TAG, f"show_selected_distribution() row={row}")
        self.plot_formula(row)

    def plot_formula(self, row: int):
        if not 0 <= row < len(self.formulas):
            return
        formula = self.formulas[row].findOrigin()
        origin = formula.absoluteAbundance()
        isotopes = [(Formula(isotope), abundance) for isotope, abundance in isotopologues(formula=str(formula.toStr(
            True, False)), isotope_threshold=origin * 2e-3, overall_threshold=origin * 1e-3, report_abundance=True)]

        first = isotopes.pop(0)
        isotopes.sort(key=lambda i: i[0].mass())
        isotopes.insert(0, first)

        rtol = self.manager.workspace.info.formula_docker.calc_gen.rtol

        mass = formula.mass()
        if len(self.peaks) > 0:
            peak_index = self.find_peak_index(mass)
            peak = self.peaks[peak_index]
            plot_peak = abs(peak.peak_position / mass - 1) < rtol
        else:
            plot_peak = False

        if plot_peak:
            intensity = peak.peak_intensity / origin
        else:
            intensity = 1 / origin

        table = self.ui.isotopesTableWidget
        table.clearContents()
        table.setRowCount(0)
        table.setRowCount(len(isotopes))

        ax = self.plot.ax
        ax.clear()

        for row, (isotope, abundance) in enumerate(isotopes):  # include original formula
            isotope.charge = formula.charge
            mass = isotope.mass()

            if plot_peak:
                peak_index = self.find_peak_index(mass)
                iso_peak = self.peaks[peak_index]
                if abs(iso_peak.peak_position / mass - 1) < rtol:
                    plot_iso_peak = True
                    ax.plot(iso_peak.mz, iso_peak.intensity)
                    ax.annotate(format(iso_peak.peak_position, '4f'), [
                                iso_peak.peak_position, 0])
                else:
                    plot_iso_peak = False
            else:
                plot_iso_peak = False

            iso_int = intensity * abundance
            ax.plot([mass, mass], [0, iso_int])
            ax.annotate(str(isotope), [mass, iso_int])

            def setText(col, text):
                table.setItem(row, col, QtWidgets.QTableWidgetItem(text))
            setText(0, str(isotope))
            setText(1, format(isotope.mass(), '.4f'))
            setText(3, format(abundance / origin, '.4f'))

            if not plot_iso_peak:
                continue
            table.item(row, 0).setData(
                QtCore.Qt.ItemDataRole.UserRole, iso_peak)
            setText(2, format((iso_peak.peak_position / mass - 1) * 1e6, '.2f'))
            setText(4, format(iso_peak.peak_intensity, '.2e'))
            setText(5, format(iso_peak.peak_intensity /
                    peak.peak_intensity, '.4f'))

        self.plot.canvas.draw()
        self._update_edit_button()

    @ui_task
    async def edit_peak(self, item: QtWidgets.QTableWidgetItem):
        self.edit_peak_row(item.row())

    @ui_task
    async def edit_selected_peak(self):
        row = self.ui.isotopesTableWidget.currentRow()
        if row < 0:
            return
        logger.i(TAG, f"edit_selected_peak() row={row}")
        self.edit_peak_row(row)

    def edit_peak_row(self, row: int):
        table = self.ui.isotopesTableWidget
        item = table.item(row, 0)
        if item is None:
            return
        formula = Formula(item.text())
        it = table.item(row, 2)
        if not (it and it.text()):
            return

        peaks, targets = self._working_targets()
        if not peaks:
            return
        matched = item.data(QtCore.Qt.ItemDataRole.UserRole)
        index = None
        if matched is not None:
            for candidate_index, peak in enumerate(peaks):
                if peak is matched:
                    index = candidate_index
                    break
            if index is None:
                index = binary_search.indexNearest(
                    peaks, matched.peak_position, method=peak_position)
        if index is None:
            index = binary_search.indexNearest(
                peaks, formula.mass(), method=peak_position)
        window, local_index = targets[index]
        if window is not None:
            logger.i(
                TAG, f"edit_peak_row() row={row} target=window:{window.original_index}:{local_index}")
            window.peaks[local_index].formulas = [formula]
            window.showPeak(local_index)
            window.raise_()
            window.show()
            window.activateWindow()
            return

        logger.i(TAG, f"edit_peak_row() row={row} target=saved:{local_index}")
        from Orbitool.UI import PeakFitFloatUiPy
        win = PeakFitFloatUiPy.Window.get_or_create(self.manager, local_index)
        win.set_formulas(local_index, [formula])
        win.raise_()
        win.show()
        win.raise_()

    def _update_result_buttons(self):
        table = self.ui.resultTableWidget
        row = table.currentRow()
        self.ui.showDistributionPushButton.setEnabled(
            0 <= row < table.rowCount())
        self.ui.useSelectedToolButton.setEnabled(
            len(TableUtils.getSelectedRow(table)) > 0)

    def _update_edit_button(self):
        table = self.ui.isotopesTableWidget
        row = table.currentRow()
        item = table.item(row, 2) if 0 <= row < table.rowCount() else None
        self.ui.editPeakPushButton.setEnabled(bool(item and item.text()))

    @ui_task
    async def accept(self):
        if not self.peak_bound:
            return
        indexes = TableUtils.getSelectedRow(self.ui.resultTableWidget)
        if len(indexes) == 0:
            return
        formulas = [self.formulas[int(index)] for index in indexes]
        logger.i(TAG, f"accept() count={len(formulas)}")
        self.acceptSignal.emit(formulas)
        self.close()

    @ui_task
    async def delete_formula(self):
        if not self.peak_bound:
            return
        logger.i(TAG, "delete_formula()")
        self.acceptSignal.emit([])
        self.close()

    def closeEvent(self, a0) -> None:
        if self.owner is not None:
            if self.owner.formulas_result_win is self:
                self.owner.formulas_result_win = None
        elif self.manager.formulas_result_win is self:
            self.manager.formulas_result_win = None
        a0.accept()


def peak_position(peaks: List[FittedPeak], index: int):
    return peaks[index].peak_position


flt_pattern = re.compile(r"\d+(?:\.\d+)?")


def calc(manager: Manager, input: str):
    info = manager.workspace.info
    text = input.strip()
    if flt_pattern.fullmatch(text):
        mass = float(text)
        formulas = info.formula_docker.calc_gen.generate().get(
            mass, info.formula_docker.charge)
    else:
        formula = Formula(text)
        formulas = [formula]
        mass = formula.mass()

    formulas.sort(key=lambda f: abs(f.mass() / mass - 1))

    return input, mass, formulas
