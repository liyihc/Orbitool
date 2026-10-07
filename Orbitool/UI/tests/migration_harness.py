"""Shared scaffolding for the `ui_task` migration regression tests.

Each of the six `test_*_migration.py` modules builds one real `Window` per
module, records `showInfo` dialogs instead of showing them, and observes the
busy and progress-message signals. This module holds the pieces they all
repeat (the QApplication pin, the dialog recorder, the per-test reset) so the
migration tests only declare what is specific to their tab batch.
"""
import importlib

import pytest
from PySide6 import QtWidgets

from Orbitool import setting
from ..MainUiPy import Window
from ..utils import test as uitest

# the package rebinds names it re-exports, so resolve the module itself
task_module = importlib.import_module("Orbitool.UI.manager.task")

# a QApplication with no references gets destroyed, breaking every event
# loop that runs afterwards
app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


@pytest.fixture(autouse=True)
def debug_settings(monkeypatch):
    monkeypatch.setattr(setting.debug, "thread_block_gui", True)
    monkeypatch.setattr(setting.debug, "NO_MULTIPROCESS", True)


def drain_dialog_queue():
    """Drop a leftover `uitest.input()` answer so it cannot leak later."""
    while not uitest.q.empty():
        uitest.q.get_nowait()


class MigrationEnv:
    """Recorded dialogs, busy edges, progress messages and a real Window."""

    def __init__(self):
        self.window = None
        self.dialogs = []
        self.busy = []
        self.msgs = []
        self.timeline = []
        self.callback_hits = []
        self.startup_dialogs = []

    def reset(self):
        self.dialogs.clear()
        self.busy.clear()
        self.msgs.clear()
        self.timeline.clear()
        self.callback_hits.clear()
        drain_dialog_queue()

    def _record_show_info(self, *args, **kwargs):
        self.dialogs.append(args)
        self.timeline.append(("dialog", args))

    def build(self, request, *, extra_dialog_modules=()):
        """Patch `showInfo`, build the Window, wire the signals, and restore
        everything on teardown. Returns self so a fixture can `return
        MigrationEnv().build(request)`."""
        modules = [task_module, *extra_dialog_modules]
        originals = [(module, module.showInfo) for module in modules]
        for module in modules:
            module.showInfo = self._record_show_info

        def teardown():
            for module, original in originals:
                module.showInfo = original
            drain_dialog_queue()
            if self.window is not None:
                self.window.close()
        request.addfinalizer(teardown)

        self.window = window = Window()
        self.startup_dialogs = list(self.dialogs)
        window.manager.busy_signal.connect(self.busy.append)
        window.manager.msg.connect(self.msgs.append)
        return self
