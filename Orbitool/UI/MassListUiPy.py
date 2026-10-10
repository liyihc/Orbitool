import csv
from typing import Optional, Union
from functools import partial

from PySide6 import QtCore, QtWidgets

from Orbitool import logger
from Orbitool.models.peakfit import MassListItem, MassListHelper
from Orbitool.models.formula import Formula
from . import MassListUi, MassListCompareUiPy
from .manager import Manager, ui_task, background
from .utils import get_tablewidget_selected_row, openfile, savefile


class Widget(QtWidgets.QWidget):
    def __init__(self, manager: Manager) -> None:
        super().__init__()
        self.manager = manager
        self.ui = MassListUi.Ui_Form()
        self.setupUi()
        manager.getters.mass_list_selected_indexes.connect(
            self.get_selected_index)
        self.manager.init_or_restored.connect(self.restore)

    def setupUi(self):
        ui = self.ui
        ui.setupUi(self)

        ui.doubleSpinBox.valueChanged.connect(self.updateRtol)

        ui.addPushButton.clicked.connect(self.addMass)
        ui.removePushButton.clicked.connect(self.rmMass)

        ui.groupPlusPushButton.clicked.connect(lambda: self.group_plus(1))
        ui.groupMinusPushButton.clicked.connect(lambda: self.group_plus(-1))

        ui.importCompareMergePushButton.clicked.connect(self.compare_mass_list)
        ui.exportPushButton.clicked.connect(self.export)

    @property
    def info(self):
        return self.manager.workspace.info.masslist_docker

    def restore(self):
        self.showMasslist()
        self.info.ui_state.restore_state(self.ui)

    def updateState(self):
        self.info.ui_state.store_state(self.ui)

    def showMasslist(self):
        ui = self.ui
        ui.doubleSpinBox.setValue(self.info.rtol * 1e6)

        table = ui.tableWidget
        table.clearContents()
        table.setRowCount(0)
        table.setRowCount(len(self.info.masslist))
        for index, mass in enumerate(self.info.masslist):
            table.setItem(index, 0, QtWidgets.QTableWidgetItem(
                format(mass.position, '.5f')))
            table.setItem(index, 1, QtWidgets.QTableWidgetItem(
                ', '.join(str(f) for f in mass.formulas)))

    @ui_task(mode="light")
    async def showMassList_CatchException(self):
        self.showMasslist()

    @ui_task
    async def updateRtol(self):
        # ppm tooltip: see MassList.ui (label)
        self.info.rtol = self.ui.doubleSpinBox.value() * 1e-6

    @ui_task
    async def addMass(self):
        ui = self.ui
        text = ui.addItemLineEdit.text()
        rtol = self.info.rtol
        masslist = self.info.masslist
        for item in text.split(','):
            item = item.strip()
            if not item:
                continue
            try:
                mass = float(item)
                MassListHelper.addMassTo(
                    masslist, MassListItem(position=mass), rtol)
            except:
                formula = Formula(item)
                MassListHelper.addMassTo(
                    masslist, MassListItem(position=formula.mass(), formulas=[formula]), rtol)

        self.showMasslist()

    @ui_task
    async def rmMass(self):
        indexes = get_tablewidget_selected_row(self.ui.tableWidget)
        masslist = self.info.masslist
        for index in reversed(indexes):
            masslist.pop(index)
        self.showMasslist()

    @ui_task
    async def group_plus(self, times: float):
        abs_times = abs(times)
        sign = times / abs_times
        group = Formula(self.ui.groupLineEdit.text())
        group *= abs_times
        mass_delta = sign * group.mass()
        for item in self.info.masslist:
            if len(item.formulas) > 0:
                for f in item.formulas:
                    if sign > 0:
                        f += group
                    else:
                        f -= group
                if len(item.formulas) == 1:
                    item.position = item.formulas[0].mass()
                else:
                    item.position += mass_delta
            else:
                item.position += mass_delta
        self.showMasslist()

    def get_selected_index(self):
        return get_tablewidget_selected_row(self.ui.tableWidget)

    def read_masslist_from(self, f):
        rtol = self.info.rtol
        ret = []
        with open(f, "r") as file:
            reader = csv.reader(file)
            it = iter(reader)
            try:
                header = next(it)
            except StopIteration:
                header = None
            # a Mass List CSV is a two-column `position,formulas` table; anything
            # wider (e.g. the six-column comparison report) is not one
            if header is None or len(header) != 2:
                raise ValueError(
                    f'"{f}" is not a Mass List CSV: it must have a two-column'
                    f' header (position, formulas), but has '
                    f'{0 if header is None else len(header)} columns')
            for row in it:
                if not row:
                    continue
                position = row[0]
                formulas = row[1] if len(row) > 1 else ""
                formulas = [Formula(f)
                            for formula in formulas.split('/') if (f := formula.strip())]
                item = MassListItem(position=position, formulas=formulas)
                MassListHelper.addMassTo(ret, item, rtol)
        return ret

    @ui_task
    async def compare_mass_list(self):
        ret, f = openfile(
            "select mass list to import or merge", "CSV file(*.csv)")
        if not ret:
            return

        imported = await background(
            partial(self.read_masslist_from, f), "read mass list")
        logger.i(
            "MassListUiPy",
            f'compare_mass_list() path="{f}" imported={len(imported)}')
        rows = MassListHelper.compare(self.info.masslist, imported, self.info.rtol)

        dialog = MassListCompareUiPy.Dialog(self.info, rows, imported)
        dialog.exec()
        self.showMasslist()

    @ui_task
    async def export(self):
        ret, f = savefile("save mass list", "CSV file(*.csv)", "masslist.csv")
        if not ret:
            return

        masslist = self.info.masslist
        export_split = self.ui.splitFormulaCheckBox.isChecked()

        def func():
            if export_split:
                dicts = [item.formulas[0].to_dict() if len(
                    item.formulas) == 1 else {} for item in masslist]
                # use dict instead of orderedset
                header = dict.fromkeys(["e", "C", "H", "O", "N"])
                for d in dicts:
                    header.update(d)
            with open(f, 'w', newline='') as file:
                writer = csv.writer(file)
                if export_split:
                    writer.writerow(['position', 'formulas', *header])
                    for item, d in zip(masslist, dicts):
                        writer.writerow([
                            item.position,
                            '/'.join(str(formula)
                                     for formula in item.formulas),
                            *(d.get(k, 0) for k in header)])
                else:
                    writer.writerow(['position', 'formulas'])
                    for item in masslist:
                        writer.writerow(
                            [item.position, '/'.join(str(formula) for formula in item.formulas)])

        await background(func, "export mass list")
