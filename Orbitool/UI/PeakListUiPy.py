import csv
from typing import Dict, List, Optional, Tuple, Union
import contextlib

from PyQt5 import QtCore, QtWidgets, QtGui

from .. import get_config
from ..functions import binary_search
from ..structures.spectrum import FittedPeak, PeakTags
from ..utils.formula import Formula
from . import PeakListUi
from .manager import Manager, state_node
from .PeakFitFloatUiPy import Window as PeakFloatWin
from .utils import get_tablewidget_selected_row, savefile

colors = {
    PeakTags.Done: QtGui.QColor(0xD9FFC9),
    PeakTags.Noise: QtGui.QColor(0xC6C6C6),
    PeakTags.Fail: QtGui.QColor(0xFFBBB1)}


class Widget(QtWidgets.QWidget, PeakListUi.Ui_Form):

    def __init__(self, manager: Manager) -> None:
        super().__init__()
        self.manager = manager
        manager.init_or_restored.connect(self.restore)
        manager.save.connect(self.updateState)

        manager.signals.peak_list_show.connect(self.showPeaks)
        manager.getters.peak_list_selected_true_index.connect(self.getSelected)
        self.setupUi(self)

    def setupUi(self, Form):
        super().setupUi(Form)

        self.doubleSpinBox.setKeyboardTracking(False)
        self.doubleSpinBox.valueChanged.connect(self.goto_mass)
        self.gotoToolButton.clicked.connect(self.goto_mass)
        self.tableWidget.itemDoubleClicked.connect(self.openPeakFloatWin)
        self.tableWidget.verticalScrollBar().valueChanged.connect(self.scrolled)

        self.manager.bind.peak_fit_left_index.connect(
            "peaklist", self.scroll_to_index)

        self.exportSpectrumPushButton.clicked.connect(self.exportSpectrum)
        self.exportPeaksPushButton.clicked.connect(self.exportPeaks)
        self.exportIsotopePushButton.clicked.connect(self.exportIsotopes)

    def restore(self):
        self.manager.workspace.peaklist_docker.ui_state.set_state(self)

    def updateState(self):
        self.manager.workspace.peaklist_docker.ui_state.fromComponents(self, [
            self.bindPlotCheckBox,
            self.doubleSpinBox])

    @property
    def peaks_info(self):
        return self.manager.workspace.peakfit_tab.info

    def showPeaks(self):
        table = self.tableWidget
        peaks = self.peaks_info.peaks
        original_indexes = self.peaks_info.original_indexes
        raw_split_num = self.peaks_info.raw_split_num
        indexes = self.peaks_info.shown_indexes

        peaks = [peaks[index] for index in indexes]

        bar = table.verticalScrollBar()
        item = table.verticalHeaderItem(bar.value())
        if item:
            current_index = int(item.text())
        else:
            current_index = 0

        with self.no_send_slider():
            table.clearContents()
            table.setRowCount(0)
            table.setRowCount(len(peaks))
            table.setVerticalHeaderLabels(map(str, indexes))
            ind = binary_search.indexNearest(indexes, current_index)
            bar.setRange(0, len(indexes))
            bar.setSliderPosition(ind)

        for index, peak in enumerate(peaks):
            tag = peak.tags
            if tag:
                tag = PeakTags(tag[0])
            c = colors.get(tag, None)

            def setItem(column, msg):
                item = QtWidgets.QTableWidgetItem(str(msg))
                if c is not None:
                    item.setBackground(c)
                table.setItem(
                    index, column, item)

            setItem(0, format(peak.peak_position, '.5f'))
            setItem(1, ', '.join(str(f) for f in peak.formulas))
            setItem(2, format(peak.peak_intensity, '.3e'))
            setItem(3,
                    format((peak.peak_position / peak.formulas[0].mass() - 1) * 1e6, '.5f') if len(peak.formulas) == 1 else "")
            setItem(4, format(peak.area, '.3e'))
            setItem(5, ','.join(tag.name for tag in map(PeakTags, peak.tags)))

            setItem(6, raw_split_num[original_indexes[indexes[index]]])

    @contextlib.contextmanager
    def no_send_slider(self):
        bar = self.tableWidget.verticalScrollBar()
        box = self.bindPlotCheckBox
        value = box.isChecked()
        box.setChecked(False)
        yield
        box.setChecked(value)

    def filterSelected(self, select: bool):
        """
            filter selected or filter unselected
        """
        selectedindex = get_tablewidget_selected_row(self.tableWidget)
        info = self.peaks_info
        indexes = info.shown_indexes
        if select:
            info.shown_indexes = [indexes[index] for index in selectedindex]
        else:
            for index in reversed(selectedindex):
                indexes.pop(index)

    def getSelected(self):
        selectedindex = get_tablewidget_selected_row(self.tableWidget)
        info = self.peaks_info
        indexes = info.shown_indexes
        return [indexes[index] for index in selectedindex]

    @state_node
    def goto_mass(self):
        mass = self.doubleSpinBox.value()
        peaks = self.peaks_info.peaks
        indexes = self.peaks_info.shown_indexes
        index = binary_search.indexNearest(
            indexes, mass, method=lambda indexes, ind: peaks[indexes[ind]].peak_position)
        self.scroll_to_index(index)
        self.manager.bind.peak_fit_left_index.emit_except("peaklist", index)

    @state_node(mode='n', withArgs=True)
    def scrolled(self, index):
        if self.bindPlotCheckBox.isChecked():
            self.manager.bind.peak_fit_left_index.emit_except(
                "peaklist", index)

    def scroll_to_index(self, index):
        if self.bindPlotCheckBox.isChecked():
            with self.no_send_slider():
                self.tableWidget.verticalScrollBar().setSliderPosition(index)

    @state_node(withArgs=True)
    def openPeakFloatWin(self, item: QtWidgets.QTableWidgetItem):
        row = item.row()
        win = PeakFloatWin.get_or_create(
            self.manager, self.peaks_info.shown_indexes[row])
        win.show()
        win.raise_()

    @state_node
    def exportSpectrum(self):
        spectrum = self.peaks_info.spectrum
        ret, f = savefile("Save Spectrum", "CSV file(*.csv)",
                          f"fitted_spectrum {spectrum.start_time.strftime(get_config().format_export_time)}-"
                          f"{spectrum.end_time.strftime(get_config().format_export_time)}")

        if not ret:
            return

        with open(f, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['mz', 'intensity'])
            writer.writerows(zip(spectrum.mz, spectrum.intensity))

    @state_node
    def exportPeaks(self):
        spectrum = self.peaks_info.spectrum

        ret, f = savefile("Save Peak List", "CSV file(*.csv)",
                          f"peak_list {spectrum.start_time.strftime(get_config().format_export_time)}"
                          f"-{spectrum.end_time.strftime(get_config().format_export_time)}")
        if not ret:
            return

        peaks = self.peaks_info.peaks
        indexes = self.peaks_info.shown_indexes
        peaks: List[FittedPeak] = [peaks[index] for index in indexes]
        raw_split_num = self.peaks_info.raw_split_num
        orginal_indexes = self.peaks_info.original_indexes

        with open(f, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['mz', 'intensity', 'area',
                             'formula', 'DBE', 'rtol', 'peaks num'])
            for index, peak in enumerate(peaks):
                writer.writerow([
                    peak.peak_position,
                    peak.peak_intensity,
                    peak.area,
                    '/'.join([str(formula) for formula in peak.formulas]),
                    '/'.join([str(formula.dbe())
                              for formula in peak.formulas]),
                    (peak.peak_position /
                     peak.formulas[0].mass() - 1) if len(peak.formulas) == 1 else '',
                    raw_split_num[orginal_indexes[indexes[index]]]])

    @state_node
    def exportIsotopes(self):
        spectrum = self.peaks_info.spectrum

        ret, f = savefile("Save Isotopes", "CSV file(*.csv)",
                          f"isotope {spectrum.start_time.strftime(get_config().format_export_time)}"
                          f"-{spectrum.end_time.strftime(get_config().format_export_time)}")
        if not ret:
            return

        peaks = self.peaks_info.peaks
        shown_indexes = self.peaks_info.shown_indexes

        formula_map: Dict[Formula, List[Tuple[int, Formula]]] = {}
        for index, peak in enumerate(peaks):
            for formula in peak.formulas:
                if formula.isIsotope:
                    formula_map.setdefault(
                        formula.findOrigin(), []).append((index, formula))

        with open(f, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['formula', 'measured mz', 'intensity',
                             'intensity ratio', 'theoretic ratio'])

            for index in shown_indexes:
                peak = peaks[index]

                formulas = [f for f in peak.formulas if not f.isIsotope]
                if not formulas:
                    continue

                isotopes = [formula_map.get(formula, [])
                            for formula in formulas]
                isotopes = sum(isotopes, [])
                writer.writerow(['/'.join(str(f) for f in formulas),
                                 peak.peak_position, peak.peak_intensity, 1, 1])

                for i, isotope in isotopes:
                    i_peak = peaks[i]
                    writer.writerow([str(isotope), i_peak.peak_position, i_peak.peak_intensity,
                                     i_peak.peak_intensity / peak.peak_intensity, isotope.relativeAbundance()])

                writer.writerow([''])
