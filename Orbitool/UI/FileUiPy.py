from typing import Union, Optional
from . import FileUi
from PyQt5 import QtWidgets, QtCore


class Widget(QtWidgets.QWidget, FileUi.Ui_Form):
    def __init__(self, parent: Optional['QWidget'] = None) -> None:
        super().__init__(parent=parent)
        self.setupUi(self)