import os
from functools import partial
from typing import DefaultDict, Dict, Iterable, List, Optional, Tuple, Union, cast

from PySide6 import QtCore, QtGui, QtWidgets

from Orbitool import logger, utils
from Orbitool.models.file import FileSpectrumInfo, Path, PathList
from Orbitool.UI.utils.utils import TableUtils
from Orbitool.utils.readers import NoMassSpectrometerError

from .. import utils as UiUtils
from ..manager import Manager, Thread, ui_task, background, progress
from ..utils import DragHelper, set_header_sizes, showInfo
from . import FileUi
from .table_filter_helper import TableFilterHelper
from .utils import str2timedelta

TAG = "FileUiPy"


class Widget(QtWidgets.QWidget):
    callback = QtCore.Signal()

    def __init__(self, manager: Manager, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent=parent)
        self.manager: Manager = manager
        self.ui = FileUi.Ui_Form()
        self.drag_helper = DragHelper(("file",))
        self.setupUi()

        manager.init_or_restored.connect(self.init_or_restore)
        manager.save.connect(self.updateState)

    def setupUi(self):
        self.ui.setupUi(self)

        ui = self.ui

        ui.tableWidget.itemDoubleClicked.connect(self.showFileDetail)
        ui.tableWidget.dragEnterEvent = self.tableDragEnterEvent
        ui.tableWidget.dragMoveEvent = self.tableDragMoveEvent
        ui.tableWidget.dropEvent = self.tableDropEvent

        ui.addFilePushButton.clicked.connect(self.addThermoFile)
        ui.addFolderPushButton.clicked.connect(self.addFolder)
        ui.removeFilePushButton.clicked.connect(self.removePath)

        ui.timeAdjustPushButton.clicked.connect(self.adjust_time)

        ui.periodToolButton.clicked.connect(self.edit_period)

        self.filter_helper = TableFilterHelper(self.manager, self.ui.filterTableWidget)
        ui.refreshFilterPushButton.clicked.connect(self.filter_helper.refresh_filter)
        ui.addFilterToolButton.clicked.connect(self.filter_helper.add_filter)
        ui.delFilterToolButton.clicked.connect(self.filter_helper.del_filter)

        ui.selectedPushButton.clicked.connect(self.processSelected)
        ui.allPushButton.clicked.connect(self.processAll)

    @property
    def info(self):
        return self.manager.workspace.info.file_tab

    @property
    def pathlist(self) -> PathList:
        return self.info.pathlist

    def init_or_restore(self):
        self.showPaths()
        self.info.ui_state.restore_state(self.ui)
        self.filter_helper.show_filter()

    def updateState(self):
        ui = self.ui
        self.info.ui_state.store_state(ui)

    def _refresh_paths(self, *, refresh_filters: bool = True):
        """Repaint the path table (and, unless a bare table refresh is
        wanted, the filter table). Shared by the task success tails and
        their recovery handlers."""
        self.showPaths()
        if refresh_filters:
            self.filter_helper.show_filter()

    def _importRawFiles(self, filepaths: Iterable[str]) -> List[Tuple[str, str]]:
        """Import each readable file, collecting the rest instead of aborting.

        One unusable `.RAW` -- e.g. a file with no MS data -- must not sink a
        whole batch or folder, so the files that could not be read are returned
        with their reason for the caller to report once the import is over.
        """
        pathlist = self.pathlist
        info = self.info
        skipped: List[Tuple[str, str]] = []
        for filepath in filepaths:
            try:
                path = pathlist.addThermoFile(filepath)
                for f in path.getFileHandler().getUniqueFilters():
                    info.add_filter(f)
            except NoMassSpectrometerError as e:
                skipped.append((filepath, str(e)))
                logger.w(TAG, f"skipping unreadable .RAW {filepath}: {e}")
        pathlist.sort()
        self.filter_helper.refresh_filter_polarity()
        return skipped

    def _reportSkippedFiles(self, skipped: List[Tuple[str, str]]):
        """Show one dialog for the files an import could not read, if any."""
        if not skipped:
            return
        lines = "\n".join(f"- {os.path.basename(filepath)}: {reason}"
                          for filepath, reason in skipped)
        showInfo("These .RAW files could not be read and were left out of the "
                 "import:\n\n" + lines, "Unreadable .RAW files")

    @ui_task
    async def edit_period(self):
        from .CustomPeriodUiPy import Dialog
        ui = self.ui
        start_time = ui.startDateTimeEdit.dateTime().toPython()
        end_time = ui.endDateTimeEdit.dateTime().toPython()
        time_interval = ui.nMinutesLineEdit.text()
        dialog = Dialog(
            self.manager, start_time, end_time,
            ui.nSpectraSpinBox.value(), time_interval)
        dialog.init_periods(start_time, end_time, time_interval)
        dialog.show_periods()
        dialog.exec()

    @ui_task
    async def addThermoFile(self):
        try:
            files = UiUtils.openfiles(
                "Select one or more files", "RAW files(*.RAW)")

            skipped = await background(
                lambda: self._importRawFiles(files), "read files")

            self._refresh_paths()
            self._reportSkippedFiles(skipped)
        except Exception:
            self._refresh_paths(refresh_filters=False)
            raise

    @ui_task
    async def addFolder(self):
        try:
            ret, folder = UiUtils.openfolder("Select one folder")
            if not ret:
                return
            recurrent = self.ui.recursionCheckBox.isChecked()

            def func():
                return self._importRawFiles(progress.tqdm(
                    utils.files.FolderTraveler(
                        folder, ext=".RAW", recurrent=recurrent)))

            skipped = await background(func, "read folders")

            self._refresh_paths()
            self._reportSkippedFiles(skipped)
        except Exception:
            self._refresh_paths()
            raise

    @ui_task
    async def showFileDetail(self, item: QtWidgets.QTableWidgetItem):
        from .FileDetailUiPy import Dialog
        Dialog(self.manager, item.row()).exec()

    def tableDragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if self.drag_helper.accept(event.mimeData()):
            event.setDropAction(QtCore.Qt.DropAction.LinkAction)
            event.accept()

    def tableDragMoveEvent(self, event: QtGui.QDragMoveEvent):
        event.accept()

    @ui_task
    async def tableDropEvent(self, event: QtGui.QDropEvent):
        data = event.mimeData()
        paths = list(self.drag_helper.yield_file(data))
        recurrent = self.ui.recursionCheckBox.isChecked()

        def rawFiles():
            for p in paths:
                if p.is_dir():
                    yield from progress.tqdm(utils.files.FolderTraveler(
                        str(p), ext=".RAW", recurrent=recurrent))
                elif p.suffix.lower() == ".raw":
                    yield str(p)

        skipped = await background(
            lambda: self._importRawFiles(rawFiles()), "read files")

        self._refresh_paths()
        self._reportSkippedFiles(skipped)

    @ui_task
    async def removePath(self):
        try:
            indexes = TableUtils.getSelectedRow(self.ui.tableWidget)
            paths = self.pathlist.rmPath(indexes)
            info = self.info

            def func():
                for path in paths:
                    for f in path.getFileHandler().getUniqueFilters():
                        info.rm_filter(f)
            await background(func)

            self._refresh_paths()
        except Exception:
            self._refresh_paths()
            raise

    def showPaths(self):
        ui = self.ui
        table = ui.tableWidget
        pathlist = self.pathlist
        table.setRowCount(0)
        table.setRowCount(len(pathlist))

        for i, f in enumerate(pathlist):
            v = [f.get_show_name(), f.startDatetime.replace(microsecond=0),
                 f.endDatetime.replace(microsecond=0), f.scanNum, f.path]
            for j, vv in enumerate(v):
                table.setItem(i, j, QtWidgets.QTableWidgetItem(str(vv)))
        table.resizeColumnsToContents()
        table.setColumnWidth(0, 150)

        if ui.autoTimeCheckBox.isChecked():
            time_start, time_end = pathlist.timeRange
            if time_start is None:
                return
            ui.startDateTimeEdit.setDateTime(time_start)
            ui.endDateTimeEdit.setDateTime(time_end)

    @ui_task
    async def adjust_time(self):
        ui = self.ui
        slt = TableUtils.getSelectedRow(ui.tableWidget)
        paths = self.pathlist.subList(slt)
        start, end = paths.timeRange
        if start is None:
            return
        ui.startDateTimeEdit.setDateTime(start)
        ui.endDateTimeEdit.setDateTime(end)


    @ui_task
    async def processSelected(self):
        indexes = TableUtils.getSelectedRow(self.ui.tableWidget)
        if len(indexes) == 0:
            return None

        paths = self.pathlist.subList(indexes)
        self.info.spectrum_infos = await background(self._process_paths(paths.paths), "get infomations from selected spectra")

        self.callback.emit()

    @ui_task
    async def processAll(self):
        self.info.spectrum_infos = await background(self._process_paths(self.pathlist.paths), "get infomations from spectra")

        self.callback.emit()

    def _process_paths(self, paths: List[Path]):
        ui = self.ui
        time_range = (ui.startDateTimeEdit.dateTime().toPython(),
                      ui.endDateTimeEdit.dateTime().toPython())

        # ppm tooltip: see File.ui (rtolLabel)
        self.info.rtol = ui.rtolDoubleSpinBox.value() * 1e-6

        filters = self.info.getCastedUsedSpectrumFilters()
        stats_filters = self.info.getCastedScanstatsFilters()
        if ui.averageGroupBox.isChecked():
            if ui.nSpectraRadioButton.isChecked():
                num = ui.nSpectraSpinBox.value()
                func = partial(FileSpectrumInfo.infosFromNumInterval,
                               paths, num, filters, stats_filters, time_range)
            elif ui.nMinutesRadioButton.isChecked():
                interval = str2timedelta(ui.nMinutesLineEdit.text())
                func = partial(FileSpectrumInfo.infosFromTimeInterval,
                               paths, interval, filters, stats_filters, time_range)
            elif ui.periodRadioButton.isChecked():
                func = partial(FileSpectrumInfo.infosFromPeriods,
                               paths, filters, stats_filters, self.info.periods)
        else:
            func = partial(FileSpectrumInfo.infosFromPath_withoutAveraging,
                           paths, filters, stats_filters, time_range)

        return func
