from copy import deepcopy
import re
from typing import List, Optional

from PySide6 import QtCore, QtGui, QtWidgets
from pyteomics.mass.mass import isotopologues

from Orbitool import logger
from Orbitool.models.formula import Formula
from Orbitool.models.spectrum import FittedPeak
from Orbitool.UI.manager import Manager, ui_task
from Orbitool.UI.utils import TableUtils
from Orbitool.utils import binary_search

from . import FormulaResultUi

TAG = "FormulaResultUiPy"

_RAW_COLOR = QtGui.QColor("#1f77b4")
_THEORY_COLOR = QtGui.QColor("#d62728")


class IsotopePlot(QtWidgets.QWidget):
    """One isotope's raw peak against its theoretical height.

    The x range is the matched peak's stored m/z span, so this is that
    isotope's slice of the old overview plot. The y axis autoscales to the
    larger of that peak and the theoretical line: heights are comparable
    within one column, not across columns. Mouse events pass through so the
    enclosing table can still select the column.
    """

    def __init__(self, peak: Optional[FittedPeak], theoretical_mass: float,
                 theoretical_intensity: float, rtol: float,
                 parent=None) -> None:
        super().__init__(parent)
        self.peak = peak
        self.theoretical_mass = theoretical_mass
        self.theoretical_intensity = theoretical_intensity
        self.rtol = rtol
        self.setMinimumSize(90, 120)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                           QtWidgets.QSizePolicy.Policy.Expanding)
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def _ranges(self):
        if self.peak is not None and len(self.peak.mz):
            x_min = float(self.peak.mz.min())
            x_max = float(self.peak.mz.max())
            y_max = float(self.peak.intensity.max())
        else:
            pad = abs(self.theoretical_mass) * self.rtol
            x_min = self.theoretical_mass - pad
            x_max = self.theoretical_mass + pad
            y_max = 0.0
        if x_max <= x_min:
            pad = max(abs(self.theoretical_mass) * self.rtol, 1e-6)
            x_min = self.theoretical_mass - pad
            x_max = self.theoretical_mass + pad
        y_max = max(y_max, self.theoretical_intensity, 0.0) * 1.1
        if y_max <= 0:
            y_max = 1.0
        return x_min, x_max, y_max

    def paintEvent(self, event) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), self.palette().base())

        metrics = painter.fontMetrics()
        line_height = metrics.height()
        rect = self.rect().adjusted(2, 2 * line_height + 4, -2, -14)
        if rect.width() <= 0 or rect.height() <= 0:
            return
        x_min, x_max, y_max = self._ranges()
        span = x_max - x_min

        def x_pix(x):
            return rect.left() + (x - x_min) / span * rect.width()

        def y_pix(y):
            return rect.bottom() - y / y_max * rect.height()

        painter.setPen(_THEORY_COLOR)
        painter.drawText(
            QtCore.QPointF(2, metrics.ascent() + 1),
            f"theo {format(self.theoretical_intensity, '.2e')}")
        if self.peak is not None:
            painter.setPen(_RAW_COLOR)
            painter.drawText(
                QtCore.QPointF(2, line_height + metrics.ascent() + 1),
                f"actual {format(self.peak.peak_intensity, '.2e')}")

        if self.peak is not None and len(self.peak.mz):
            path = QtGui.QPainterPath()
            path.moveTo(x_pix(float(self.peak.mz[0])),
                        y_pix(float(self.peak.intensity[0])))
            for mz, intensity in zip(self.peak.mz, self.peak.intensity):
                path.lineTo(x_pix(float(mz)), y_pix(float(intensity)))
            pen = QtGui.QPen(_RAW_COLOR)
            pen.setWidthF(1.5)
            painter.setPen(pen)
            painter.drawPath(path)

            text = format(self.peak.peak_position, '4f')
            tx = x_pix(self.peak.peak_position) + 2
            if tx + metrics.horizontalAdvance(text) > rect.right():
                tx = x_pix(self.peak.peak_position) - \
                    metrics.horizontalAdvance(text) - 2
            painter.setPen(self.palette().text().color())
            painter.drawText(QtCore.QPointF(tx, rect.bottom() - 1), text)

        x = x_pix(self.theoretical_mass)
        y = y_pix(self.theoretical_intensity)
        pen = QtGui.QPen(_THEORY_COLOR)
        pen.setWidthF(1.2)
        pen.setStyle(QtCore.Qt.PenStyle.DashLine)
        painter.setPen(pen)
        painter.drawLine(QtCore.QPointF(x, rect.bottom()),
                         QtCore.QPointF(x, y))


class Window(QtWidgets.QMainWindow):
    """Formula result window: a calculator, or bound to one Peak Fit peak.

    Either way it matches peaks across the whole Peak List (all segments), not
    only one segment; see `_working_targets` and the peak-fit ADR
    (`docs/adr/peak-fit/20261018-peak-fit-window-ownership-and-commit-model.md`).
    """

    acceptSignal = QtCore.Signal(list)

    ISOTOPE_ROWS = (
        "formula", "distribution", "mass", "tolerance(ppm)",
        "theoretical ratio", "actual intensity", "actual ratio")
    FORMULA_ROW, CHART_ROW, MASS_ROW, TOLERANCE_ROW, \
        THEORETICAL_RATIO_ROW, ACTUAL_INTENSITY_ROW, ACTUAL_RATIO_ROW = range(7)
    ISOTOPE_COLUMN_WIDTH = 150
    CHART_ROW_HEIGHT = 160

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
        ui.horizontalLayout.setStretch(0, 0)
        ui.horizontalLayout.setStretch(1, 1)

        isotopes = ui.isotopesTableWidget
        isotopes.setRowCount(len(self.ISOTOPE_ROWS))
        isotopes.setVerticalHeaderLabels(self.ISOTOPE_ROWS)
        header = isotopes.verticalHeader()
        header.setDefaultAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter)
        header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(
            self.CHART_ROW, QtWidgets.QHeaderView.ResizeMode.Fixed)
        header.setFixedWidth(140)
        isotopes.horizontalHeader().hide()
        isotopes.setRowHeight(self.CHART_ROW, self.CHART_ROW_HEIGHT)

        if self.peak_bound:
            ui.lineEdit.setReadOnly(True)
            self.setWindowTitle(f"Formula Calculation Result - {self.mass:.4f}")
            ui.deleteToolButton.show()
            ui.useSelectedToolButton.show()
        else:
            self.setWindowTitle("Formula Calculation Result")
            ui.deleteToolButton.hide()
            ui.useSelectedToolButton.hide()

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

    @property
    def peaks(self):
        if not self.peak_bound:
            return self.manager.workspace.info.peak_fit_tab.peaks
        return self._working_targets()[0]

    def _working_targets(self):
        """Return every peak plus the window/row each one belongs to.

        The list spans all segments, not only the owner's: a formula's isotope
        peaks usually sit in other segments, so an owner-only view would hide
        them. Pending peaks of open Peak Fit windows replace their segment.
        """
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

        if formulas:
            selected = 0
            if mass:
                selected = min(
                    range(len(formulas)),
                    key=lambda index: abs(formulas[index].mass() / mass - 1))
            table.setCurrentCell(selected, 0)
            table.selectRow(selected)
            self.plot_formula(selected)
        else:
            self._clear_isotopes()

        self._update_result_buttons()
        self._update_edit_button()

    def _clear_isotopes(self):
        table = self.ui.isotopesTableWidget
        table.clearContents()
        table.setColumnCount(0)

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

        origin_mass = formula.mass()
        if len(self.peaks) > 0:
            peak_index = self.find_peak_index(origin_mass)
            peak = self.peaks[peak_index]
            plot_peak = abs(peak.peak_position / origin_mass - 1) < rtol
        else:
            peak = None
            plot_peak = False

        if plot_peak:
            intensity = peak.peak_intensity / origin
        else:
            intensity = 1 / origin

        table = self.ui.isotopesTableWidget
        table.clearContents()
        table.setColumnCount(0)
        table.setColumnCount(len(isotopes))

        for column, (isotope, abundance) in enumerate(isotopes):
            isotope.charge = formula.charge
            isotope_mass = isotope.mass()

            iso_peak = None
            if plot_peak:
                peak_index = self.find_peak_index(isotope_mass)
                candidate = self.peaks[peak_index]
                if abs(candidate.peak_position / isotope_mass - 1) < rtol:
                    iso_peak = candidate

            iso_int = intensity * abundance

            formula_item = QtWidgets.QTableWidgetItem(str(isotope))
            font = formula_item.font()
            font.setBold(True)
            formula_item.setFont(font)
            formula_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            if iso_peak is not None:
                formula_item.setData(
                    QtCore.Qt.ItemDataRole.UserRole, iso_peak)
            table.setItem(self.FORMULA_ROW, column, formula_item)
            table.setItem(self.MASS_ROW, column, QtWidgets.QTableWidgetItem(
                format(isotope_mass, '.4f')))
            table.setItem(self.THEORETICAL_RATIO_ROW, column,
                          QtWidgets.QTableWidgetItem(
                              format(abundance / origin, '.4f')))

            if iso_peak is not None:
                table.setItem(
                    self.TOLERANCE_ROW, column, QtWidgets.QTableWidgetItem(
                        format((iso_peak.peak_position / isotope_mass - 1)
                               * 1e6, '.2f')))
                table.setItem(
                    self.ACTUAL_INTENSITY_ROW, column,
                    QtWidgets.QTableWidgetItem(
                        format(iso_peak.peak_intensity, '.2e')))
                table.setItem(
                    self.ACTUAL_RATIO_ROW, column, QtWidgets.QTableWidgetItem(
                        format(iso_peak.peak_intensity
                               / peak.peak_intensity, '.4f')))
            else:
                for empty_row in (self.TOLERANCE_ROW,
                                  self.ACTUAL_INTENSITY_ROW,
                                  self.ACTUAL_RATIO_ROW):
                    table.setItem(
                        empty_row, column, QtWidgets.QTableWidgetItem(""))

            table.setItem(self.CHART_ROW, column,
                          QtWidgets.QTableWidgetItem())
            table.setCellWidget(
                self.CHART_ROW, column,
                IsotopePlot(iso_peak, isotope_mass, iso_int, rtol))
            table.setColumnWidth(column, self.ISOTOPE_COLUMN_WIDTH)

        table.setRowHeight(self.CHART_ROW, self.CHART_ROW_HEIGHT)
        self._update_edit_button()

    @ui_task
    async def edit_peak(self, item: QtWidgets.QTableWidgetItem):
        self.edit_peak_column(item.column())

    @ui_task
    async def edit_selected_peak(self):
        column = self.ui.isotopesTableWidget.currentColumn()
        if column < 0:
            return
        logger.i(TAG, f"edit_selected_peak() column={column}")
        self.edit_peak_column(column)

    def edit_peak_column(self, column: int):
        table = self.ui.isotopesTableWidget
        item = table.item(self.FORMULA_ROW, column)
        if item is None:
            return
        formula = Formula(item.text())
        it = table.item(self.TOLERANCE_ROW, column)
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
                TAG, f"edit_peak_column() column={column} target=window:{window.original_index}:{local_index}")
            window.peaks[local_index].formulas = [formula]
            window.showPeak(local_index)
            window.raise_()
            window.show()
            window.activateWindow()
            return

        logger.i(TAG, f"edit_peak_column() column={column} target=saved:{local_index}")
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
        column = table.currentColumn()
        item = table.item(self.TOLERANCE_ROW, column) \
            if 0 <= column < table.columnCount() else None
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
