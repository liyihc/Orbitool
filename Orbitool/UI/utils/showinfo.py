from PySide6.QtWidgets import QMessageBox

from . import test

BTN = QMessageBox.StandardButton


def showInfo(content:str, cap=None):
    QMessageBox.information(None, cap or 'info', str(content))

@test.override_input
def confirm(content: str, cap=None, accept:str=None, reject:str=None) -> bool:
    box = QMessageBox()
    box.setIcon(QMessageBox.Icon.Question)
    box.setWindowTitle(cap or 'confirm')
    box.setText(str(content))
    yes = box.addButton(accept or 'Yes', QMessageBox.ButtonRole.AcceptRole)
    box.addButton(reject or 'No', QMessageBox.ButtonRole.RejectRole)
    box.setDefaultButton(yes)
    box.exec()
    return box.clickedButton() is yes
