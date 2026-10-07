import csv
from csv import QUOTE_ALL
from datetime import datetime
from pathlib import Path
from typing import Any, Union
from typing_extensions import deprecated
import numpy as np
from PySide6 import QtWidgets, QtCore

from Orbitool import setting
from Orbitool.UI.setting.FileTabUiPy import Tab

from . import test


def set_header_sizes(header: QtWidgets.QHeaderView, sizes: list):
    list(map(header.resizeSection, range(len(sizes)), sizes))


def format_noise_lod(value: float) -> str:
    """Format a noise/LOD table cell; a blank (nan) mass reads as an empty field."""
    if value != value:  # nan
        return ""
    return format(value, ".6g")


def write_noise_lod_csv(path, rows) -> None:
    """Write a noise/LOD table: a header plus one `formula,mass,noise,LOD` row each."""
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["formula", "mass", "noise", "LOD"])
        for name, mass, noise, lod in rows:
            writer.writerow([name, format_noise_lod(mass),
                             format_noise_lod(noise), format_noise_lod(lod)])


def unique_export_subfolder(folder: Path, prefix: str) -> Path:
    """Return `folder`, or a timestamped subfolder when `folder` is non-empty, so an
    export never mixes its files with whatever is already there."""
    for _ in folder.glob("*"):
        subfolder = folder / \
            f"{prefix}-{setting.format_export_time(datetime.now())}"
        subfolder.mkdir(parents=True)
        return subfolder
    return folder


@deprecated("Use TableUtils.getSelectedRow instead")
@test.override_input
def get_tablewidget_selected_row(tableWidget: QtWidgets.QTableWidget) -> np.ndarray:
    return np.unique([index.row() for index in tableWidget.selectedIndexes()])


def sleep(second):
    if second > 0:
        loop = QtCore.QEventLoop()
        timer = QtCore.QTimer()
        timer.timeout.connect(loop.quit)
        timer.start(int(second * 1000))
        loop.exec()

class TableUtils:
    @staticmethod
    def clear(table: QtWidgets.QTableWidget):
        table.clearContents()
        table.setRowCount(0)

    @staticmethod
    def clearAndSetColumnCount(table: QtWidgets.QTableWidget, count: int):
        table.clearContents()
        table.setColumnCount(0)
        table.setColumnCount(count)
    @staticmethod
    def clearAndSetRowCount(table: QtWidgets.QTableWidget, count: int):
        table.clearContents()
        table.setRowCount(0)
        table.setRowCount(count)

    @staticmethod
    def setRow(table: QtWidgets.QTableWidget, row: int, *cells: Union[str, Any]):
        for column, cell in enumerate(cells):
            table.setItem(row, column, QtWidgets.QTableWidgetItem(str(cell)))

    @staticmethod
    def getSelectedRow(table: QtWidgets.QTableWidget):
        return np.unique([index.row() for index in table.selectedIndexes()])
