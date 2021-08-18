from typing import List

from PyQt5 import QtWidgets, QtCore
from pyteomics.mass.mass import isotopologues

from ..structures.spectrum import FittedPeak
from ..functions import binary_search
from ..utils.formula import Formula
from . import FormulaResultUi
from .manager import Manager, state_node
from .component import Plot
from .utils import get_tablewidget_selected_row


class Window(QtWidgets.QMainWindow, FormulaResultUi.Ui_MainWindow):
    acceptSignal = QtCore.pyqtSignal(list)

    def __init__(self, manager: Manager, input: str, mass: float, formulas: List[Formula], peak_index: int) -> None:
        super().__init__()
        self.manager = manager
        self.setupUi(self)

        self.lineEdit.setText(input)
        self.mass = mass
        self.formulas = formulas
        self.peak_index = peak_index

        self.showResult()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.resultTableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents)
        self.isotopesTableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents)

        self.plot = Plot(self.widget)
        self.calcPushButton.clicked.connect(lambda: self.calc(False))
        self.forceCalcPushButton.clicked.connect(lambda: self.calc(True))
        self.resultTableWidget.itemDoubleClicked.connect(self.plot_row)
        self.showAllToolButton.clicked.connect(self.showResult)
        self.closeToolButton.clicked.connect(self.close)
        self.acceptToolButton.clicked.connect(self.accept)
        self.acceptEmptyToolButton.clicked.connect(self.acceptEmpty)

    @classmethod
    def FactoryCalc(cls, manager: Manager, input: str, force: bool):
        return Window(manager, *calc(manager, input, force))

    @classmethod
    def FactoryPeak(cls, manager: Manager, peak_index: int):
        peaks = manager.workspace.peakfit_tab.info.peaks
        peak = peaks[peak_index]
        return Window(manager, str(peak.peak_position), peak.peak_position, peak.formulas, peak_index)

    def find_peak_index(self, mass):
        return binary_search.indexNearest(self.peaks, mass, method=peak_position)

    @property
    def peaks(self):
        return self.manager.workspace.peakfit_tab.info.peaks

    @state_node(withArgs=True)
    def calc(self, force):
        input = self.lineEdit.text()
        _, mass, formulas, peak_index = calc(self.manager, input, force)
        self.mass = mass
        self.formulas = formulas
        self.peak_index = peak_index
        self.showResult()

    @state_node(mode='x')
    def showResult(self):
        mass = self.mass
        formulas = self.formulas

        table = self.resultTableWidget
        table.clearContents()
        table.setRowCount(0)
        table.setRowCount(len(formulas))

        def ppm(m):
            return (m / mass - 1) * 1e6

        for index, formula in enumerate(formulas):
            def setText(column, text):
                table.setItem(index, column, QtWidgets.QTableWidgetItem(text))
            setText(0, str(formula))
            setText(1, format(formula.mass(), '.4f'))
            setText(2, format(ppm(formula.mass()), '.2f'))
            setText(3, format(formula.dbe(), '.1f'))

        ax = self.plot.ax
        ax.clear()

        if self.peak_index:
            peak = self.peaks[self.peak_index]
            intensity = peak.peak_intensity
            ax.plot(peak.mz, peak.intensity)
        else:
            intensity = 1

        for f in self.formulas:
            m = f.mass()
            ax.plot([m, m], [0, intensity])
            ax.annotate(str(f), [m, intensity])

        self.plot.canvas.draw()

    @state_node(withArgs=True)
    def plot_row(self, item: QtWidgets.QTableWidgetItem):
        row = self.resultTableWidget.row(item)
        formula = self.formulas[row].findOrigin()
        origin = formula.absoluteAbundance()
        isotopes = [(Formula(isotope), abundance) for isotope, abundance in isotopologues(formula=str(formula.toStr(
            True, False)), isotope_threshold=origin * 2e-3, overall_threshold=origin * 1e-3, report_abundance=True)]

        first = isotopes.pop(0)
        isotopes.sort(key=lambda i: i[0].mass())
        isotopes.insert(0, first)

        rtol = self.manager.workspace.formula_docker.info.rtol

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

        table = self.isotopesTableWidget
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
            setText(2, format((iso_peak.peak_position / mass - 1) * 1e6, '.2f'))
            setText(4, format(iso_peak.peak_intensity, '.2e'))
            setText(5, format(iso_peak.peak_intensity /
                    peak.peak_intensity, '.4f'))

        self.plot.canvas.draw()

    @state_node
    def accept(self):
        if len(self.formulas) <= 1:
            self.acceptSignal.emit(self.formulas)
            self.close()
            return

        indexes = get_tablewidget_selected_row(self.resultTableWidget)
        if len(indexes) == 0:
            ret = QtWidgets.QMessageBox.question(
                self, "accept multi formulas?",
                "or select one formula to accept",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No)
            if ret == QtWidgets.QMessageBox.No:
                return
            formulas = self.formulas
        else:
            formulas = [self.formulas[index] for index in indexes]
        self.acceptSignal.emit(formulas)
        self.close()

    @state_node
    def acceptEmpty(self):
        self.acceptSignal.emit([])
        self.close()


def peak_position(peaks: List[FittedPeak], index):
    return peaks[index].peak_position


def calc(manager: Manager, input: str, force: bool):
    try:
        info = manager.workspace.formula_docker.info
        mass = float(input)
        if force:
            formulas = info.force_calc.get(mass)
        else:
            formulas = info.restricted_calc.get(mass)
    except ValueError:
        formula = Formula(input)
        formulas = [formula]
        mass = formula.mass()

    peaks = manager.workspace.peakfit_tab.info.peaks

    if len(peaks) > 0:
        index = binary_search.indexNearest(
            peaks, mass, method=peak_position)
        peak = peaks[index]
        peak_index = index if abs(
            peak.peak_position / mass - 1) < 3e-8 else None
    else:
        peak_index = None

    formulas.sort(key=lambda f: abs(f.mass() / mass - 1))

    return input, mass, formulas, peak_index