from functools import wraps
from multiprocessing.pool import Pool
from typing import Callable

from PyQt5.QtCore import QThread, pyqtSignal, QObject

from ...structures import WorkSpace
from ..utils import showInfo


class Manager(QObject):
    inited = pyqtSignal()
    busy_signal = pyqtSignal(bool)
    __slots__ = ["node_thread", "pool", "workspace", "_busy"]

    def __init__(self) -> None:
        super().__init__()
        self.node_thread: QThread = None
        self.pool: Pool = None
        self.workspace: WorkSpace = None
        self._busy: bool = True

    def set_busy(self, busy: bool):
        if busy ^ self._busy:
            self._busy = busy
            self.busy_signal.emit(busy)

    @property
    def busy(self):
        return self._busy
