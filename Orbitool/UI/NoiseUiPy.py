import csv
import math
import os
from copy import copy
from tkinter import W
from typing import Generator, Iterable, List, Optional, Tuple, Union

import matplotlib.ticker
import numpy as np
from numpy.polynomial.polynomial import polyval
from PySide6 import QtCore, QtWidgets

from Orbitool import logger, setting
from Orbitool.base.disk_structure import DiskListDirectView
from Orbitool.models.workspace.noise_tab import MzIntensity, NoiseArray, NoiseFormulaParameter
from Orbitool.models import spectrum as spectrum_func
from Orbitool.models.file import FileSpectrumInfo
from Orbitool.models.formula import Formula
from Orbitool.models.spectrum import Spectrum
from Orbitool.models.workspace import WorkSpace
from Orbitool.utils import binary_search
from Orbitool.utils.readers import thermo

from . import NoiseUi, component
from .manager import Manager, MultiProcess, ui_task, background, progress
from .utils import (TableUtils, format_noise_lod, get_tablewidget_selected_row,
                    savefile, set_header_sizes, showInfo, write_noise_lod_csv)


TAG = "NoiseUiPy"


def damagedFilesMessage(damaged: thermo.DamagedScansByFile) -> str:
    """Text describing the damaged files a read pass collected, keyed by .RAW path."""
    lines = []
    for path, scans in sorted(damaged.items()):
        grouped = thermo.groupScansByReason(scans)
        detail = ", ".join(f"{len(numbers)} x {reason}"
                           for reason, numbers in sorted(grouped.items()))
        numbers = ", ".join(str(i) for i in sorted(scans))
        lines.append(f"- {os.path.basename(path)}: {detail} (scan {numbers})")
    return ("These .RAW files contain scans that cannot be averaged. Those scans were "
            "left out of the affected windows, so those spectra use fewer scans than "
            "the rest. The files are probably damaged -- re-exporting or re-acquiring "
            "them is worth considering:\n\n" + "\n".join(lines))


def reportDamagedFiles(damaged: thermo.DamagedScansByFile):
    """Show one dialog for the damage a finished read collected, if there is any.

    Only files with at least one un-averageable scan are reported: an entry with no
    scan in it means nothing was found, and reporting it would blame a healthy file.
    The record belongs to that read: this is the only thing that displays it, and it is
    dropped as soon as the dialog closes. Everything stays in `log.txt`.
    """
    found = {path: scans for path, scans in damaged.items() if scans}
    if found:
        showInfo(damagedFilesMessage(found), "Damaged .RAW files")


class Widget(QtWidgets.QWidget):
    callback = QtCore.Signal(tuple)

    def __init__(self, manager: Manager) -> None:
        super().__init__()
        self.manager = manager

        self.ui = NoiseUi.Ui_Form()
        self.setupUi()

        manager.init_or_restored.connect(self.restore)
        manager.save.connect(self.updateState)

    def setupUi(self):
        ui = self.ui
        ui.setupUi(self)

        set_header_sizes(ui.paramTableWidget.horizontalHeader(), [
                         150, 150, 150])
        self.plot = component.Plot(ui.widget)
        ui.toolBox.setCurrentIndex(0)
        ui.showAveragePushButton.clicked.connect(self.showSelectedSpectrum)
        ui.addPushButton.clicked.connect(self.addFormula)
        ui.delPushButton.clicked.connect(self.delFormula)
        ui.calculateNoisePushButton.clicked.connect(self.calcNoise)
        ui.exportSpectrumPushButton.clicked.connect(self.exportSpectrum)
        ui.exportDenoisedSpectrumPushButton.clicked.connect(
            self.exportDenoise)
        ui.exportNoisePeaksPushButton.clicked.connect(self.exportNoisePeaks)
        ui.exportNoiseLODPushButton.clicked.connect(self.exportNoiseLOD)
        ui.denoisePushButton.clicked.connect(self.denoise)
        ui.skipPushButton.clicked.connect(self.skip)

        ui.paramTableWidget.itemDoubleClicked.connect(
            self.moveToTableClickedNoise)
        ui.spectrumPushButton.clicked.connect(self.scaleToSpectrum)
        ui.yLogCheckBox.toggled.connect(self.yLogToggle)
        ui.yAxisPushButton.clicked.connect(self.y_rescale_click)
        ui.yLimDoubleToolButton.clicked.connect(lambda: self.y_times(2))
        ui.yLimHalfToolButton.clicked.connect(lambda: self.y_times(.5))

    @property
    def info(self):
        return self.manager.workspace.info.noise_tab

    def restore(self):
        self.showNoiseFormula()
        self.plotSelectSpectrum()
        self.showNoise()
        self.info.ui_state.restore_state(self.ui)

    def updateState(self):
        self.info.ui_state.store_state(self.ui)

    def showNoiseFormula(self):
        widget = self.ui.tableWidget
        widget.clearContents()
        widget.setRowCount(0)
        formulas = self.info.general_setting.noise_formulas
        widget.setRowCount(len(formulas))
        for i, formula in enumerate(formulas):
            widget.setItem(i, 0, QtWidgets.QTableWidgetItem(
                str(formula.formula)))
            dsb = QtWidgets.QSpinBox()
            dsb.setMinimum(1)
            dsb.setMaximum(50)
            dsb.setValue(int(formula.delta))
            widget.setCellWidget(i, 1, dsb)
            widget.setItem(i, 2, QtWidgets.QTableWidgetItem(
                format(formula.formula.mass(), ".6f")))

    @ui_task
    async def showSelectedSpectrum(self):
        # Reading for the plot repairs damaged windows too, and a spectrum built from
        # fewer scans than the file has must never be shown without saying so.
        damaged: thermo.DamagedScansByFile = {}
        await self.readSelectedSpectrum(damaged)
        self.ui.toolBox.setCurrentIndex(0)
        reportDamagedFiles(damaged)

    async def readSelectedSpectrum(self, damaged: thermo.DamagedScansByFile):
        """Read the selected spectrum, recording what it cannot average in `damaged`.

        The caller owns the record and reports it once its own read is over.
        """
        workspace = self.manager.workspace
        index = self.manager.getters.spectra_list_selected_index.get()
        info_list = workspace.info.file_tab.spectrum_infos

        left = index
        right = left + 1
        while right < len(info_list) and info_list[right].average_index != 0:
            right += 1

        rtol = workspace.info.file_tab.rtol
        infos: List[FileSpectrumInfo] = list(info_list[left:right])
        logger.d(TAG, f"readSelectedSpectrum() info[{left},{right}] {len(infos)=}")

        def read_and_average():
            spectra: List[Tuple[np.ndarray, np.ndarray, float]] = []
            for info in infos:
                spectrum, _ = info.get_spectrum_from_info(rtol, True, damaged=damaged)
                if spectrum is not None:
                    spectra.append(spectrum)
            if len(spectra) > 0:
                spectra = [(*spectrum_func.removeZeroPositions(
                    spectrum[0], spectrum[1]), spectrum[2]) for spectrum in spectra]
                mz, intensity = spectrum_func.averageSpectra(
                    spectra, rtol, True)
                spectrum = Spectrum(
                    mz=mz, intensity=intensity, path='none:',
                    start_time=infos[0].start_time, end_time=infos[-1].end_time)
                return True, spectrum
            else:
                return False, None

        success, spectrum = await background(read_and_average, "read & average")

        if success:
            self.info.current_spectrum = spectrum
            self.plotSelectSpectrum()
            self.ui.denoisePushButton.setEnabled(False)
        else:
            showInfo("Spectra all may be filtered", "Empty spectra")

    def plotSelectSpectrum(self):
        spectrum = self.info.current_spectrum
        if spectrum is not None:
            self.plot.ax.clear()
            self.plot.ax.plot(spectrum.mz, spectrum.intensity)
            self.plot.canvas.draw()
            self.y_rescale(self.ui.yLogCheckBox.isChecked())

    @ui_task
    async def addFormula(self):
        try:
            formula = Formula(self.ui.lineEdit.text())
            self.info.general_setting.noise_formulas.append(
                NoiseFormulaParameter(formula=formula))
        finally:
            self.showNoiseFormula()

    @ui_task
    async def delFormula(self):
        try:
            indexes = TableUtils.getSelectedRow(self.ui.tableWidget)
            for index in reversed(indexes):
                del self.info.general_setting.noise_formulas[index]
        finally:
            self.showNoiseFormula()

    @ui_task
    async def calcNoise(self):
        info = self.info
        spectrum = info.current_spectrum

        if spectrum is None:
            showInfo("Please show a spectrum first")
            return

        ui = self.ui
        quantile = ui.quantileDoubleSpinBox.value()
        n_sigma = ui.nSigmaDoubleSpinBox.value()

        mass_dependent = ui.sizeDependentCheckBox.isChecked()

        noise_setting = info.general_setting
        mass_points = np.array([f.formula.mass()
                                for f in noise_setting.noise_formulas])
        mass_point_deltas = np.array([ui.tableWidget.cellWidget(
            i, 1).value() for i in range(ui.tableWidget.rowCount())], dtype=np.int32)

        def func():
            poly, std, slt, params = spectrum_func.getNoiseParams(
                spectrum.mz, spectrum.intensity, quantile, mass_dependent, mass_points, mass_point_deltas)
            noise, LOD = spectrum_func.noiseLODFunc(
                spectrum.mz, poly, std, params, mass_points, mass_point_deltas, n_sigma)
            if setting.denoise.plot_noise_in_diff_color:
                noise_split = spectrum_func.splitNoise(
                    spectrum.mz, spectrum.intensity, poly, std, params,
                    mass_points, mass_point_deltas, n_sigma)
            else:
                noise_split = (None,) * 4

            return (poly, std, slt, params), (noise, LOD), noise_split

        result = info.general_result

        rets, noises, noise_split = await background(func, "get noise infomations")

        result.poly_coef, result.global_noise_std, slt, params = rets
        result.noise = NoiseArray(noise=noises[0], LOD=noises[1])
        result.spectrum_split = MzIntensity(
            mz=noise_split[0], intensity=noise_split[1])
        result.noise_split = MzIntensity(
            mz=noise_split[2], intensity=noise_split[3])

        noise_setting = info.general_setting

        noise_setting.params_inited = True
        noise_setting.quantile, noise_setting.mass_dependent, noise_setting.n_sigma = quantile, mass_dependent, n_sigma

        ind: np.ndarray = slt.cumsum() - 1
        formula_params = noise_setting.noise_formulas
        for index, (i, s, d) in enumerate(zip(ind, slt, mass_point_deltas)):
            p = formula_params[index]
            p.useable = bool(s)
            if s:
                p.param = params[i]
            p.delta = d

        self.showNoise()

    def noiseLODTable(self):
        """The Noise results table as (name, mass, noise, LOD) rows.

        Row 0 is `global` (mass blank); the rest follow `noise_formulas`. A mass
        point the fit could not use reads 0, matching the old editable table and
        the exported CSV. This is read-only: the values are whatever the last
        calculation produced.
        """
        info = self.info
        noise_setting = info.general_setting
        result = info.general_result
        n_sigma = noise_setting.n_sigma
        global_noise, global_lod = spectrum_func.getGlobalShownNoise(
            result.poly_coef, n_sigma, result.global_noise_std)
        rows = [("global", math.nan, global_noise, global_lod)]
        for param in noise_setting.noise_formulas:
            if param.useable:
                noise, lod = spectrum_func.getNoiseLODFromParam(
                    param.param, n_sigma)
            else:
                noise, lod = 0.0, 0.0
            rows.append((str(param.formula), param.formula.mass(), noise, lod))
        return rows

    def showNoise(self):
        ui = self.ui
        noise_setting = self.info.general_setting

        if not noise_setting.params_inited:
            return

        rows = self.noiseLODTable()
        table = ui.paramTableWidget
        table.clearContents()
        table.setRowCount(0)
        table.setRowCount(len(rows))

        for i, (name, mass, noise, lod) in enumerate(rows):
            table.setItem(i, 0, QtWidgets.QTableWidgetItem(name))
            table.setItem(i, 1, QtWidgets.QTableWidgetItem(
                format_noise_lod(noise)))
            table.setItem(i, 2, QtWidgets.QTableWidgetItem(
                format_noise_lod(lod)))

        ui.toolBox.setCurrentWidget(ui.paramTool)
        self.plotNoise()
        ui.denoisePushButton.setEnabled(True)

    def plotNoise(self):
        info = self.info
        spectrum = info.current_spectrum
        if spectrum is None:
            return
        result = info.general_result
        if not len(result.noise.LOD) or spectrum.mz.shape != result.noise.LOD.shape:
            return  # show another spectrum after calc noise

        is_log = self.ui.yLogCheckBox.isChecked()
        plot = self.plot
        ax = plot.ax
        ax.clear()

        ax.set_yscale('log' if is_log else 'linear')

        ax.axhline(color='k', linewidth=0.5)
        ax.yaxis.set_tick_params(rotation=45)

        if not is_log:
            ax.yaxis.set_major_formatter(
                matplotlib.ticker.FormatStrFormatter(r"%.1e"))

        ax.plot(spectrum.mz, result.noise.LOD, zorder=2.5,
                linewidth=1, color='k', label='LOD')
        ax.plot(spectrum.mz, result.noise.noise, zorder=2.5,
                linewidth=1, color='b', label='noise')
        spectrum_split = result.spectrum_split
        noise_split = result.noise_split
        if setting.denoise.plot_noise_in_diff_color and spectrum_split.mz is not None:
            ax.plot(spectrum_split.mz, spectrum_split.intensity,
                    linewidth=1, color="#1f77b4", label="Spectrum")
            ax.plot(noise_split.mz, noise_split.intensity,
                    linewidth=1, color="#BF2138", label="Noise")
        else:
            ax.plot(spectrum.mz, spectrum.intensity,
                    linewidth=1, color="#BF2138", label="Spectrum")
        ax.legend(loc='upper right')

        self.moveToGlobalNoise()
        plot.canvas.draw()

    @ui_task
    async def exportSpectrum(self):
        spectrum = self.info.current_spectrum
        if spectrum is None:
            showInfo("Please show a spectrum first")
            return

        ret, f = savefile("Save Spectrum", "CSV file(*.csv)",
                          f"raw_spectrum {spectrum.start_time.strftime(setting.general.export_time_format)}"
                          f"-{spectrum.end_time.strftime(setting.general.export_time_format)}.csv")
        if not ret:
            return

        def export():
            with open(f, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["mz", "intensity"])
                writer.writerows(progress.tqdm(
                    zip(spectrum.mz, spectrum.intensity), length=len(spectrum.mz)))

        await background(export, "export")

    @ui_task
    async def exportDenoise(self):
        info = self.info
        subtract = self.ui.substractCheckBox.isChecked()
        spectrum = info.current_spectrum
        noise_setting = info.general_setting

        ret, f = savefile("Save Denoise Spectrum", "CSV file(*.csv)",
                          f"denoise_spectrum {spectrum.start_time.strftime(setting.general.export_time_format)}"
                          f"-{spectrum.end_time.strftime(setting.general.export_time_format)}.csv")
        if not ret:
            return

        def func():
            params, points, deltas = noise_setting.get_params(True)
            mz, intensity = spectrum_func.denoiseWithParams(
                spectrum.mz, spectrum.intensity, info.general_result.poly_coef,
                info.general_result.global_noise_std, params, points, deltas,
                noise_setting.n_sigma, subtract)

            s = Spectrum(
                mz=mz, intensity=intensity, path=spectrum.path,
                start_time=spectrum.start_time, end_time=spectrum.end_time)

            return s

        s: Spectrum = await background(func, "doing denoise")

        def export():
            with open(f, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["mz", "intensity"])
                writer.writerows(progress.tqdm(
                    zip(s.mz, s.intensity), length=len(s.mz)))

        await background(export, "export")

    @ui_task
    async def exportNoisePeaks(self):
        info = self.info
        spectrum = info.current_spectrum
        noise_setting = info.general_setting
        ret, f = savefile("Save Noise Peak", "CSV file(*.csv)",
                          f"noise_peak {spectrum.start_time.strftime(setting.general.export_time_format)}"
                          f"-{spectrum.end_time.strftime(setting.general.export_time_format)}.csv")
        if not ret:
            return

        def func():
            params, points, deltas = noise_setting.get_params(True)
            mz, intensity = spectrum_func.getNoisePeaks(
                spectrum.mz, spectrum.intensity, info.general_result.poly_coef,
                info.general_result.global_noise_std, params, points, deltas, noise_setting.n_sigma)
            return mz, intensity

        mz, intensity = await background(func, "get noise peak")

        def export():
            with open(f, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["peak position", "peak intensity"])
                writer.writerows(progress.tqdm(
                    zip(mz, intensity), length=len(mz)))
        await background(export, "export")

    @ui_task
    async def exportNoiseLOD(self):
        info = self.info
        spectrum = info.current_spectrum
        if spectrum is None:
            showInfo("Please show a spectrum first")
            return
        if not info.general_setting.params_inited:
            showInfo("Please calculate noise first")
            return

        ret, f = savefile(
            "Save Noise results", "CSV file(*.csv)",
            f"noise_results {spectrum.start_time.strftime(setting.general.export_time_format)}"
            f"-{spectrum.end_time.strftime(setting.general.export_time_format)}.csv")
        if not ret:
            return

        rows = self.noiseLODTable()
        await background(lambda: write_noise_lod_csv(f, rows), "export")

    @ui_task
    async def denoise(self):
        info = self.info
        subtract = self.ui.substractCheckBox.isChecked()
        spectrum = info.current_spectrum
        noise_setting = info.general_setting

        def func():
            params, points, deltas = noise_setting.get_params(True)
            mz, intensity = spectrum_func.denoiseWithParams(
                spectrum.mz, spectrum.intensity, info.general_result.poly_coef,
                info.general_result.global_noise_std, params, points, deltas,
                noise_setting.n_sigma, subtract)

            s = Spectrum(
                mz=mz, intensity=intensity, path=spectrum.path,
                start_time=spectrum.start_time, end_time=spectrum.end_time)

            return s

        s = await background(func, "doing denoise")

        # The record of this whole denoise: the read pass fills it, the report below
        # shows it once, and it is dropped with this call.
        damaged: thermo.DamagedScansByFile = {}
        read_from_file = ReadFromFile(self.manager.workspace, read_kwargs={"damaged": damaged})
        await background(read_from_file, "read and average all spectra")
        reportDamagedFiles(damaged)

        noise_setting.subtract = subtract
        noise_setting.spectrum_dependent = self.ui.dependentCheckBox.isChecked()
        info.skip = False

        self.callback.emit((s,))

    @ui_task
    async def skip(self):
        # One record for this whole skip, shared by both reads below, so the dialog
        # shows each damaged file once and only what this skip found.
        damaged: thermo.DamagedScansByFile = {}
        await background(ReadFromFile(self.manager.workspace, read_kwargs={"damaged": damaged}),
                         "read and average all spectra")
        info = self.info
        info.skip = True
        if info.current_spectrum is None:
            await self.readSelectedSpectrum(damaged)
        reportDamagedFiles(damaged)
        self.callback.emit((info.current_spectrum,))

    @ui_task
    async def moveToTableClickedNoise(self, item: QtWidgets.QTableWidgetItem):
        row = item.row()
        info = self.info
        if info.current_spectrum is None:
            return
        if not info.general_setting.params_inited:
            return
        is_log = self.ui.yLogCheckBox.isChecked()

        noise_setting = info.general_setting
        result = info.general_result

        plot = self.plot
        if row == 0:  # noise
            self.moveToGlobalNoise()
        else:
            param = noise_setting.noise_formulas[row - 1]

            point = param.formula.mass()
            x_min = point - param.delta * 2
            x_max = point + param.delta * 2
            xrange = [x_min, x_max]
            global_range = polyval(xrange, result.poly_coef)
            global_lod_max = global_range.max() + noise_setting.n_sigma * result.global_noise_std
            if param.useable:
                y_min, y_max = spectrum_func.getNoiseLODFromParam(
                    param.param, noise_setting.n_sigma)
                y_min = min(global_range.min(), y_min)
                y_max = max(global_lod_max, y_max)
            else:  # global noise
                y_min = global_range.min() / 2
                y_max = global_lod_max
            
            if is_log:
                y_min = max(y_min, 0) * 0.5
                y_max *= 10
            else:
                y_min = min(y_min, 0)
                y_max *= 1.5

            plot.ax.set_xlim(x_min, x_max)
            plot.ax.set_ylim(y_min, y_max)
        plot.canvas.draw()

    def moveToGlobalNoise(self):
        ui = self.ui
        is_log = ui.yLogCheckBox.isChecked()
        ax = self.plot.ax

        info = self.info
        spectrum = info.current_spectrum
        result = info.general_result

        x_min = spectrum.mz[0]
        x_max = spectrum.mz[-1]
        yrange = polyval([x_min, x_max], result.poly_coef)
        y_min = yrange.min()
        y_max = abs(yrange.max() + info.general_setting.n_sigma *
                    result.global_noise_std)
        if is_log:
            if y_min > 0:
                y_min *= 0.5
            else:
                y_min = 0
            y_max *= 10
        else:
            if y_min > 0:
                y_min = 0
            else:
                y_min *= 2

            y_max *= 5
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

    @ui_task
    async def scaleToSpectrum(self):
        info = self.info
        if info.current_spectrum is None:
            return

        is_log = self.ui.yLogCheckBox.isChecked()

        spectrum = info.current_spectrum
        self.plot.ax.set_xlim(spectrum.mz.min(), spectrum.mz.max())

        self.y_rescale(is_log)

        self.plot.canvas.draw()

    @ui_task
    async def yLogToggle(self, is_log: bool):
        ax = self.plot.ax
        ax.set_yscale('log' if is_log else 'linear')

        if not is_log:
            ax.yaxis.set_major_formatter(
                matplotlib.ticker.FormatStrFormatter(r"%.1e"))

        if self.info.current_spectrum is None:
            return

        self.y_rescale(is_log)
        self.plot.canvas.draw()

    @ui_task
    async def y_rescale_click(self):
        is_log = self.ui.yLogCheckBox.isChecked()
        self.y_rescale(is_log)
        self.plot.canvas.draw()

    def y_rescale(self, is_log: bool):
        plot = self.plot
        ax = plot.ax
        spectrum = self.info.current_spectrum

        x_min, x_max = ax.get_xlim()
        id_x_min, id_x_max = binary_search.indexBetween_np(
            spectrum.mz, (x_min, x_max))

        y_max = spectrum.intensity[id_x_min:id_x_max].max()

        if is_log:
            info = self.info
            if info.general_setting.params_inited:
                y_min = polyval(
                    [x_min, x_max], info.general_result.poly_coef).min() / 10
            else:
                y_min = 0.1
            y_max *= 2
        else:
            dy = 0.05 * y_max
            y_min = -dy
            y_max = y_max + dy

        ax.set_ylim(y_min, y_max)

    @ui_task
    async def y_times(self, times: float):
        plot = self.plot
        ax = plot.ax
        y_min, y_max = ax.get_ylim()
        y_max *= times
        if not self.ui.yLogCheckBox.isChecked():
            y_min = - 0.025 * y_max
        ax.set_ylim(y_min, y_max)
        plot.canvas.draw()


class ReadFromFile(MultiProcess):
    @staticmethod
    def func(data: Tuple[FileSpectrumInfo, Tuple[np.ndarray, np.ndarray, float]], **kwargs):
        info, (mz, intensity) = data
        mz, intensity = spectrum_func.removeZeroPositions(mz, intensity)
        spectrum = Spectrum(
            mz=mz, intensity=intensity, path=info.path,
            start_time=info.start_time, end_time=info.end_time)
        return info, spectrum

    @staticmethod
    def read(file: WorkSpace, damaged: thermo.DamagedScansByFile, **kwargs) -> Generator:
        rtol = file.info.file_tab.rtol
        cnt = 0
        last_reader = None
        for info in file.info.file_tab.spectrum_infos:
            data, last_reader = info.get_spectrum_from_info(
                rtol, last_reader=last_reader, damaged=damaged)
            if info.average_index and info.average_index != cnt:
                info = copy(info)
                info.average_index = cnt
            if data is not None:
                yield info, data
                cnt = info.average_index + 1
            else:
                cnt = info.average_index

    @staticmethod
    def read_len(file: WorkSpace, **kwargs) -> int:
        return len(file.info.file_tab.spectrum_infos)

    @staticmethod
    def write(file: WorkSpace, rets: Iterable[Tuple[FileSpectrumInfo, Spectrum]], **kwargs):
        obj = (file.proxy_file or file.file)._obj
        tmp = DiskListDirectView(Spectrum, obj, "tmp")
        infos = []

        def it():
            for info, spectrum in rets:
                infos.append(info)
                yield spectrum
        tmp.extend(it())

        file.info.noise_tab.denoised_spectrum_infos = infos
        file.info.noise_tab.to_be_calibrate = True
        path = file.data.raw_spectra.obj.name
        del obj[path]
        obj.move(tmp.obj.name, path)

    @staticmethod
    def exception(file: WorkSpace, **kwargs):
        obj = (file.proxy_file or file.file)._obj
        if "tmp" in obj:
            del obj["tmp"]
