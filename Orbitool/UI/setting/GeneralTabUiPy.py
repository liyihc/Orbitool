from multiprocessing import cpu_count
import typing
from PySide6 import QtCore, QtWidgets
from .GeneralTabUi import Ui_Form
from Orbitool.config import _Setting
from .common import BaseTab
from datetime import datetime


COLOR_SCHEMES = ("system", "light", "dark")
COLOR_SCHEME_LABELS = ("Follow system", "Light", "Dark")


class Tab(BaseTab):
    def __init__(self, parent: QtWidgets.QWidget, setting: _Setting) -> None:
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.init(setting)

    def init(self, setting: _Setting):
        ui = self.ui

        general = setting.general

        def revert(line_edit: QtWidgets.QLineEdit, field: str):
            line_edit.setText(type(general).model_fields[field].get_default())

        ui.themeComboBox.addItems(COLOR_SCHEME_LABELS)
        ui.themeComboBox.setCurrentIndex(
            COLOR_SCHEMES.index(general.color_scheme))

        ui.defaultSelectCheckBox.setChecked(general.default_select)

        ui.multiCoresSpinBox.setMinimum(1)
        ui.multiCoresSpinBox.setMaximum(cpu_count())
        ui.multiCoresSpinBox.setValue(general.multi_cores)

        ui.timeFormatLineEdit.textChanged.connect(self.change_time_format)
        ui.timeFormatLineEdit.setText(general.time_format)
        ui.timeFormatRevertButton.clicked.connect(
            lambda: revert(ui.timeFormatLineEdit, "time_format"))

        ui.exportTimeFormatLineEdit.textChanged.connect(
            self.change_export_time_format)
        ui.exportTimeFormatLineEdit.setText(general.export_time_format)
        ui.exportTimeFormatRevertButton.clicked.connect(
            lambda: revert(ui.exportTimeFormatLineEdit, "export_time_format"))

    def stash_setting(self, setting: _Setting):
        ui = self.ui
        general = setting.general
        general.color_scheme = COLOR_SCHEMES[ui.themeComboBox.currentIndex()]
        general.multi_cores = ui.multiCoresSpinBox.value()
        general.default_select = ui.defaultSelectCheckBox.isChecked()
        general.time_format = ui.timeFormatLineEdit.text()
        general.export_time_format = ui.exportTimeFormatLineEdit.text()

    def change_time_format(self, text: str):
        try:
            s = f"example: {datetime.now().strftime(text)}"
        except Exception as e:
            s = f"example: {e}"
        self.ui.timeFormatShowLabel.setText(s)

    def change_export_time_format(self, text: str):
        try:
            s = f"example: {datetime.now().strftime(text)}"
        except Exception as e:
            s = f"example: {e}"
        self.ui.exportTimeFormatShowLabel.setText(s)
