"""Executable coverage for the ticket-07 migration (formulas dock,
MassList, SpectraList, PeakList, MassDefect): the legacy generator tasks
were rewritten as ui_task coroutines.

The batch is the one that carries the five old `a`-mode sites in the
Formula panel; that reset-on-completion mode used to clear a busy held by
someone else. They map to `light` (never touch busy),
so the tests pin that a light call during busy leaves the other holder's
busy intact.

No RAW data is available, so file dialogs are answered through
`Orbitool.UI.utils.test.input`, `os.startfile` is stubbed, and the full
main window is built offscreen. `thread_block_gui` makes workers run
inline for deterministic busy edges.

Placed next to the dominant subpackage of the batch (see `docs/ui-tasks.md`).
"""
import importlib

import pytest
from PyQt6 import QtWidgets

from Orbitool import setting
from ...models.formula import Formula
from ..MainUiPy import Window
from ..utils import test as uitest
from . import FormulaResultUiPy
from .FormulaResultUiPy import Window as FormulaResultWindow

# the package rebinds names it re-exports, so the module itself must be
# resolved through importlib, not through attribute lookup
task_module = importlib.import_module("Orbitool.UI.manager.task")
spectra_module = importlib.import_module("Orbitool.UI.SpectraListUiPy")
massdefect_module = importlib.import_module("Orbitool.UI.MassDefectUiPy")

# a QApplication with no references gets destroyed, breaking every event
# loop that runs afterwards
app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


@pytest.fixture(autouse=True)
def debug_settings(monkeypatch):
    monkeypatch.setattr(setting.debug, "thread_block_gui", True)
    monkeypatch.setattr(setting.debug, "NO_MULTIPROCESS", True)


def _drain_dialog_queue():
    while not uitest.q.empty():
        uitest.q.get_nowait()


class _Env:
    def __init__(self):
        self.dialogs = []
        self.busy = []
        self.msgs = []

    def reset(self):
        self.dialogs.clear()
        self.busy.clear()
        self.msgs.clear()
        _drain_dialog_queue()


@pytest.fixture(scope="module")
def env(request):
    state = _Env()
    original_show_info = task_module.showInfo

    def record_show_info(*args, **kwargs):
        state.dialogs.append(args)

    def teardown():
        task_module.showInfo = original_show_info
        _drain_dialog_queue()
        if state.window is not None:
            state.window.close()

    task_module.showInfo = record_show_info
    request.addfinalizer(teardown)

    state.window = window = Window()
    window.manager.busy_signal.connect(state.busy.append)
    window.manager.msg.connect(state.msgs.append)
    return state


@pytest.fixture(autouse=True)
def reset_state(env):
    env.reset()


# --------------------------------------------------------------------------
# Formula panel: five old reset-mode sites -> light
# --------------------------------------------------------------------------

def test_formula_light_sites_leave_other_busy_untouched(env):
    # this is the defect the migration fixes: the old reset mode would
    # clear busy on completion and could wipe a holder's busy; light must not
    formula = env.window.formula
    manager = env.window.manager
    manager.set_busy(True)
    env.busy.clear()
    try:
        formula.update_calc()
        formula.show_element_infos()
        formula.hide_element_infos()
        assert manager.busy is True
        assert env.busy == []        # light never emits a busy transition
        assert env.dialogs == []
    finally:
        manager.set_busy(False)


def test_formula_light_item_clicked_forwards_signal_args(env):
    formula = env.window.formula
    formula.ui.elementLineEdit.setText("C")
    formula.ui.elementAddToolButton.click()
    env.reset()

    item = formula.ui.elementTableWidget.item(0, 3)
    assert item is not None
    formula.ui.elementTableWidget.itemClicked.emit(item)   # was the old argument switch

    assert env.dialogs == []
    assert env.busy == []        # light
    assert formula.ui.elementTableWidget.cellWidget(0, 3) is not None


def test_formula_light_isotope_clicked_forwards_signal_args(env):
    # the fifth former reset-mode site: emitting the real itemClicked signal
    # forwards (item, column) and must not touch a held busy
    formula = env.window.formula
    manager = env.window.manager
    tree = formula.ui.isotopeTreeWidget
    item = tree.topLevelItem(0)
    assert item is not None

    manager.set_busy(True)
    env.busy.clear()
    try:
        tree.itemClicked.emit(item, 2)
        assert env.dialogs == []
        assert env.busy == []        # light
        assert manager.busy is True
        assert tree.itemWidget(item, 2) is not None
    finally:
        manager.set_busy(False)


def test_formula_default_element_add_takes_and_releases_busy(env):
    formula = env.window.formula
    formula.ui.elementLineEdit.setText("C")
    formula.ui.elementAddToolButton.click()   # default ui_task

    assert env.dialogs == []
    assert env.busy == [True, False]
    assert not env.window.manager.busy
    assert "C" in formula.info.calc_gen.element_states


def test_formula_calc_opens_result_window(env, monkeypatch):
    formula = env.window.formula
    captured = {}

    class _StubResultWin:
        @classmethod
        def fromInputStr(cls, manager, text):
            return cls()

        def show(self):
            captured["opened"] = True

    monkeypatch.setattr(FormulaResultUiPy, "Window", _StubResultWin)
    formula.calc()

    assert captured.get("opened") is True
    assert env.busy == [True, False]
    assert env.dialogs == []


# --------------------------------------------------------------------------
# FormulaResultWindow: old relay mode -> join
# --------------------------------------------------------------------------

def test_formula_result_join_starts_while_busy(env):
    manager = env.window.manager
    win = FormulaResultWindow(
        manager, "CH4", 16.0313, [Formula("CH4")], None)
    try:
        manager.set_busy(True)
        env.busy.clear()
        try:
            win.showResult()      # join: must not be refused with a dialog
            assert env.dialogs == []
            assert manager.busy is True   # only its own count was returned
            assert env.busy == []         # busy already held -> no new edge
        finally:
            manager.set_busy(False)
    finally:
        win.close()


# --------------------------------------------------------------------------
# MassList
# --------------------------------------------------------------------------

def test_masslist_light_and_default_modes(env):
    masslist = env.window.masslist

    masslist.showMassList_CatchException()      # was a light letter mode
    assert env.busy == []

    masslist.updateRtol()                       # default
    assert env.busy == [True, False]

    env.reset()
    masslist.ui.addItemLineEdit.setText("100.0")
    masslist.ui.addPushButton.click()           # addMass
    assert env.busy == [True, False]
    assert len(masslist.info.masslist) == 1
    assert env.dialogs == []


def test_masslist_import_and_export_background(env, tmp_path):
    masslist = env.window.masslist

    src = tmp_path / "in.csv"
    src.write_text("position,formulas\n100.0,CH4\n")
    env.reset()
    uitest.input((True, str(src)))
    masslist.import_masslist()                  # worker background step
    assert env.dialogs == []
    assert env.busy == [True, False]
    assert len(masslist.info.masslist) == 1

    dst = tmp_path / "out.csv"
    env.reset()
    uitest.input((True, str(dst)))
    masslist.export()                           # worker background step
    assert env.dialogs == []
    assert env.busy == [True, False]
    assert dst.exists() and dst.stat().st_size > 0


# --------------------------------------------------------------------------
# SpectraList
# --------------------------------------------------------------------------

def test_spectralist_light_combo_and_export_worker(env, tmp_path, monkeypatch):
    spectra = env.window.spectraList

    spectra.comboBox_changed()                  # was a light letter mode
    assert env.busy == []

    monkeypatch.setattr(spectra_module.os, "startfile", lambda *a: None)
    env.reset()
    uitest.input((True, str(tmp_path)))
    spectra.export("select")                    # worker background step
    assert env.dialogs == []
    assert env.busy == [True, False]
    assert "processing" in env.msgs             # msgless background -> default msg


# --------------------------------------------------------------------------
# PeakList
# --------------------------------------------------------------------------

def test_peaklist_light_and_default_modes(env):
    peaklist = env.window.peakList

    peaklist.scrolled(0)                        # was a light letter mode
    assert env.busy == []

    env.reset()
    peaklist.goto_mass()                        # default (was argument-less)
    assert env.busy == [True, False]
    assert env.dialogs == []


# --------------------------------------------------------------------------
# MassDefect
# --------------------------------------------------------------------------

def test_massdefect_light_and_default_modes(env, monkeypatch):
    massdefect = env.window.massDefectTab

    massdefect.replot()                         # was a light letter mode
    assert env.busy == []

    env.reset()
    massdefect.calc()                           # default
    assert env.busy == [True, False]
    assert env.dialogs == []

    env.reset()
    monkeypatch.setattr(massdefect_module, "savefile", lambda *a, **k: (False, ""))
    massdefect.export()                         # default, early return
    assert env.busy == [True, False]
    assert env.dialogs == []
