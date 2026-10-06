import typing
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget
from Orbitool.config import _Setting

class BaseTab(QtWidgets.QWidget):
    def stash_setting(self, setting: _Setting):
        pass