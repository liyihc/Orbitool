from datetime import datetime
from pathlib import Path
import shutil
from typing import Dict, Union

from matplotlib.pyplot import get
from PySide6 import QtCore, QtGui, QtWidgets

from Orbitool import setting
from Orbitool.base.structure import broken_entries as h5_brokens
from Orbitool.models.workspace import WorkSpace, updater
from ..version import VERSION
from . import (CalibrationUiPy, file_tab, formulas, MainUi, MassDefectUiPy,
               MassListUiPy, NoiseUiPy, PeakFitUiPy, PeakListUiPy,
               PeakShapeUiPy, SpectraListUiPy, TimeseriesesUiPy)
from . import utils as UiUtils
from .manager import Manager, MultiProcess, ui_task


class Window(QtWidgets.QMainWindow):

    def setupUi(self):
        ui = self.ui
        ui.setupUi(self)

        manager = self.manager
        self.setWindowTitle(f"Orbitool {manager.workspace.info.version}")

        dock_opt = self.DockOption

        self.setDockOptions(dock_opt.AllowNestedDocks|dock_opt.AllowTabbedDocks|dock_opt.AnimatedDocks|dock_opt.GroupedDragging|dock_opt.VerticalTabs)
        ui.settingAction.triggered.connect(self.setting_dialog)
        ui.workspaceLoadAction.triggered.connect(self.load)
        ui.workspaceSaveAction.triggered.connect(self.save)
        ui.workspaceSaveAsAction.triggered.connect(self.save_as)

        ui.configLoadAction.triggered.connect(self.loadConfig)
        ui.configSaveAction.triggered.connect(self.saveConfig)

        ui.formulaAction.triggered.connect(self.open_formula)

        # tab widgets
        ui.abortPushButton.clicked.connect(self.abort_process)

        self.fileTab: file_tab.Widget = self.add_tab(
            file_tab.Widget(manager), "File")
        self.fileTab.callback.connect(self.file_tab_finish)

        self.noiseTab: NoiseUiPy.Widget = self.add_tab(
            NoiseUiPy.Widget(manager), "Noise")
        self.noiseTab.callback.connect(self.noise_tab_finish)

        self.peakShapeTab: PeakShapeUiPy.Widget = self.add_tab(
            PeakShapeUiPy.Widget(manager), "Peak Shape")
        self.peakShapeTab.callback.connect(self.peak_shape_tab_finish)

        self.calibrationTab = self.add_tab(
            CalibrationUiPy.Widget(manager), "Calibration")
        self.calibrationTab.callback.connect(
            self.calibration_finish)

        self.peakFitTab = self.add_tab(PeakFitUiPy.Widget(manager), "Peak Fit")
        self.peakFitTab.show_mass_defect.connect(self.open_mass_defect)

        self.timeseriesesTab = self.add_tab(
            TimeseriesesUiPy.Widget(manager), "Timeseries")

        # window widgets

        self.formula = formulas.FormulaWidget(manager)
        self.formula.setWindowTitle("Formula")

        # docker widgets — three fixed dockers, stacked as tabs in the left
        # area. The tab order is Spectra List, Peak List, Mass List (each
        # tabified after the previous), and navigation never changes it.

        self.spectraList = SpectraListUiPy.Widget(manager)
        self.spectraListDw = self.add_dock_widget(
            "Spectra List", self.spectraList)

        self.peakList = PeakListUiPy.Widget(manager)
        self.peakListDw = self.add_dock_widget(
            "Peak List", self.peakList, self.spectraListDw)
        self.peakFitTab.filter_selected.connect(self.peakList.filterSelected)

        self.masslist = MassListUiPy.Widget(manager)
        self.massListDw = self.add_dock_widget(
            "Mass List", self.masslist, self.peakListDw)
        self.peakFitTab.show_masslist.connect(self.masslist.showMassList_CatchException)

        self.spectraListDw.raise_()

        ui.tabWidget.setCurrentIndex(0)

    def __init__(self, workspacefile=None) -> None:
        super().__init__()
        self.manager = Manager()
        self.manager.workspace = WorkSpace()

        self.ui = MainUi.Ui_MainWindow()
        self.setupUi()

        self.manager.busy_signal.connect(self.set_busy)

        self.progress_bars: Dict[int, QtWidgets.QProgressBar] = {}
        self.manager.msg.connect(self.showMsg)
        self.manager.tqdm.tqdm_signal.connect(self.showBarLabelMessage)
        self.set_busy(False)
        if workspacefile is not None:
            self._load_workspace(workspacefile)
        else:
            self.manager.init_or_restored.emit()

    @property
    def workspace(self):
        return self.manager.workspace

    def set_busy(self, value):
        self.ui.menuWorkspace.setDisabled(value)
        self.ui.menuOrbitool.setDisabled(value)
        self.ui.tabWidget.setDisabled(value)
        self.ui.processWidget.setHidden(not value)

        if not value:
            for bar in self.progress_bars.values():
                bar.deleteLater()
            self.progress_bars.clear()

    def add_dock_widget(self, title, widget, after=None):
        dw = QtWidgets.QDockWidget(title)
        dw.setWidget(widget)
        dw.setAllowedAreas(QtCore.Qt.DockWidgetArea.AllDockWidgetAreas)
        dw.setFeatures(dw.DockWidgetFeature.DockWidgetMovable | dw.DockWidgetFeature.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dw)
        if after is not None:
            self.tabifyDockWidget(after, dw)
        return dw

    def add_tab(self, widget, title):
        self.ui.tabWidget.addTab(widget, title)
        return widget

    def open_formula(self):
        self.formula.show()
        self.formula.raise_()
        self.formula.activateWindow()

    def open_mass_defect(self, peaks, title):
        win = MassDefectUiPy.Widget(self.manager)
        win.setWindowTitle(title)
        win.set_peaks(peaks)
        self.manager.mass_defect_wins.append(win)
        win.show()
        win.raise_()
        win.activateWindow()

    def closeEvent(self, e: QtGui.QCloseEvent) -> None:
        self.formula.close()
        for win in list(self.manager.mass_defect_wins):
            win.close()
        if self.manager.formulas_result_win is not None:
            self.manager.formulas_result_win.close()
        self.manager.save.emit()
        self.workspace.close()
        e.accept()

    @ui_task
    async def setting_dialog(self):
        from .setting import Dialog as SettingDialog
        dialog = SettingDialog()
        dialog.exec()

    @ui_task
    async def load(self):
        ret, f = UiUtils.openfile(
            "Load workspace", "Orbitool Workspace file(*.Orbitool)")
        if not ret:
            return
        self._load_workspace(f)

    def _load_workspace(self, f: str):
        version = updater.get_version(f)
        if updater.need_update(version):
            ret, n = UiUtils.savefile("Update workspace and save as a new file", "Orbitool Workspace file(*.Orbitool)")
            if not ret:
                return
            shutil.copy(f, n)
            n = Path(n)
            if n.with_suffix(".orbt-tmp").exists():
                n.with_suffix(".orbt-tmp").unlink()
            n.chmod(0o666)
            updater.update(n)
            f = n
        workspace = WorkSpace(f)
        if h5_brokens:
            UiUtils.showInfo("I have try to save more data, but below data is lost\n" +
                             "\n".join(h5_brokens), "file broken, please save as a new file")
            h5_brokens.clear()
        self.manager.workspace = workspace
        self.manager.init_or_restored.emit()

    @ui_task
    async def save(self):
        self.manager.save.emit()
        self.manager.workspace.save()

    @ui_task
    async def save_as(self):
        ret, f = UiUtils.savefile(
            "Save workspace", "Orbitool Workspace file(*.Orbitool)")
        if not ret:
            return
        self.manager.save.emit()
        self.manager.workspace.close_as(f)
        if h5_brokens:
            UiUtils.showInfo("\n".join(h5_brokens), "below data was broken")
        self.manager.workspace = WorkSpace(f)

    @ui_task
    async def loadConfig(self):
        ret, f = UiUtils.openfile(
            "Load config from workspace file", "Orbitool Workspace file(*.Orbitool)")
        if not ret:
            return

        self.manager.workspace.load_config_from_file(f)
        self.manager.init_or_restored.emit()

    @ui_task
    async def saveConfig(self):
        ret, f = UiUtils.savefile(
            "Save config", "Orbitool Workspace file(*.Orbitool)")
        if not ret:
            return
        self.manager.save.emit()
        config = WorkSpace()
        config.load_config(self.manager.workspace)
        config.close_as(f)

    def showMsg(self, msg):
        self.ui.statusbar.showMessage(
            f"{setting.format_time(datetime.now())} | {msg}")

    def showBarLabelMessage(self, label: int, percent: int, msg: str):
        if (bar := self.progress_bars.get(label, None)) is None:
            bar = QtWidgets.QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(1)
            bar.setFormat("")
            self.ui.progressBarLayout.addWidget(bar)
            self.progress_bars[label] = bar
        bar.setValue(percent)
        bar.setFormat(msg)

    @ui_task(mode="join")
    async def file_tab_finish(self):
        self.spectraList.ui.comboBox.setCurrentIndex(-1)
        self.spectraList.ui.comboBox.setCurrentIndex(0)
        self.ui.tabWidget.setCurrentWidget(self.noiseTab)

    @ui_task(mode="join")
    async def noise_tab_finish(self, result):
        self.workspace.info.peak_shape_tab.spectrum = result[0]
        self.ui.tabWidget.setCurrentWidget(self.peakShapeTab)
        await self.peakShapeTab.showPeak()

    @ui_task(mode="join")
    async def peak_shape_tab_finish(self):
        self.ui.tabWidget.setCurrentWidget(self.calibrationTab)

    @ui_task(mode="join")
    async def calibration_finish(self):
        self.ui.tabWidget.setCurrentWidget(self.peakFitTab)
        self.spectraList.ui.comboBox.setCurrentIndex(1)

    def abort_process(self):
        thread: MultiProcess = self.manager.running_thread
        if isinstance(thread, MultiProcess):
            thread.abort()
