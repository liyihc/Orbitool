import csv
from typing import List, Optional

from PySide6 import QtWidgets

from Orbitool import logger
from Orbitool.models.peakfit import CompareRow, MassListItem
from Orbitool.models.workspace.masslist import MassListInfo
from . import MassListCompareUi
from .utils import savefile


def _cells(item: Optional[MassListItem]):
    """Display pair (mz, formulas) for one cell, empty when the side is absent."""
    if item is None:
        return "", ""
    return format(item.position, '.5f'), ', '.join(str(f) for f in item.formulas)


def _export_cells(item: Optional[MassListItem]):
    """Export pair (position, formulas); formulas joined by '/' like the CSV import."""
    if item is None:
        return "", ""
    return item.position, '/'.join(str(f) for f in item.formulas)


class Dialog(QtWidgets.QDialog):
    """Modal preview of a Mass List comparison: current vs imported vs merge.

    Holds no workspace state of its own; the opener hands in the aligned rows,
    the parsed imported list and the Mass List info to commit onto.
    """

    def __init__(self, info: MassListInfo, rows: List[CompareRow],
                 imported: List[MassListItem]) -> None:
        super().__init__()
        self.info = info
        self.rows = rows
        self.imported = imported

        self.ui = MassListCompareUi.Ui_Dialog()
        self.ui.setupUi(self)
        self._show_rows()

        self.ui.useCurrentPushButton.clicked.connect(self.use_current)
        self.ui.useImportPushButton.clicked.connect(self.use_import)
        self.ui.useMergePushButton.clicked.connect(self.use_merge)
        self.ui.exportPushButton.clicked.connect(self.export)

    def _show_rows(self):
        table = self.ui.tableWidget
        table.setRowCount(0)
        table.setRowCount(len(self.rows))
        for r, row in enumerate(self.rows):
            for c, text in enumerate((*_cells(row.current), *_cells(row.imported),
                                      *_cells(row.merge))):
                table.setItem(r, c, QtWidgets.QTableWidgetItem(text))

    def use_current(self):
        self.reject()

    def use_import(self):
        self._commit("import", self.imported)

    def use_merge(self):
        self._commit("merge", [row.merge for row in self.rows])

    def _commit(self, choice: str, masslist: List[MassListItem]):
        logger.i("MassListCompareUiPy",
                 f'_commit() use={choice} count={len(masslist)}')
        self.info.masslist = masslist
        self.accept()

    def export(self):
        ret, f = savefile(
            "Export mass list comparison", "CSV file(*.csv)", "masslist-compare.csv")
        if not ret:
            return
        logger.i("MassListCompareUiPy", f'export() path="{f}"')
        with open(f, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["current_position", "current_formulas",
                             "import_position", "import_formulas",
                             "merge_position", "merge_formulas"])
            for row in self.rows:
                writer.writerow([*_export_cells(row.current),
                                 *_export_cells(row.imported),
                                 *_export_cells(row.merge)])
