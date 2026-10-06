import logging
import os
from PySide6 import QtWidgets, QtCore
import tempfile
# from pytestqt import qtbot
from ..MainUiPy import Window
from ...models.workspace import WorkSpace

from .routine import init, fileui, file_spectra, noise, qt_exit


# def test_precedure(qtbot: qtbot.QtBot):
def test_precedure(caplog):
    # caplog instead of a hand-attached handler: the routine must not log an
    # error, and a handler added here would have to be removed again by hand
    # (conftest.py restores the logger afterwards anyway).
    with caplog.at_level(logging.ERROR, logger="Orbitool"):
        app = QtWidgets.QApplication([])
        window = Window()
        init(window)
        window.show()
        print("show window")
        fileui(window)
        print("finish test file tab")
        file_spectra(window)
        print("finish test file spectra")
        noise(window)
        print("finish test noise")
        print("ui test finished")

        window.close()        

    assert not any(
        r.name.startswith("Orbitool") and r.levelno >= logging.ERROR
        for r in caplog.records)


def test_export_load():
    with tempfile.TemporaryDirectory(prefix="orbitool_test") as tmpdir:
        tmppath = os.path.join(tmpdir, "tmp.Orbitool")

        app = QtWidgets.QApplication([])
        window = Window()

        window.manager.save.emit()
        window.manager.workspace.close_as(tmppath)
        window.manager.workspace = WorkSpace(tmppath)
        window.manager.init_or_restored.emit()
        window.close()
