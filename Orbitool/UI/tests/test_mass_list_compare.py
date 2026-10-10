"""The Import, Compare and Merge preview shows the current Mass List, the
imported CSV, and their merge side by side, then commits one of the three.

Driven offscreen through the shared migration harness (like the Mass Defect
popup test). The dialog is a modal QDialog, so tests build it directly and
click its buttons rather than going through `exec()`.
"""
import csv
import importlib

import pytest

from ...models.formula import Formula
from ...models.peakfit import MassListHelper, MassListItem
from ..utils import test as uitest
# debug_settings is an autouse fixture re-exported for pytest
from .migration_harness import MigrationEnv, debug_settings  # noqa: F401

compare_module = importlib.import_module("Orbitool.UI.MassListCompareUiPy")


@pytest.fixture(scope="module")
def env(request):
    return MigrationEnv().build(request)


@pytest.fixture(autouse=True)
def reset_state(env):
    env.reset()
    env.window.manager.workspace.info.masslist_docker.masslist = []


def _open(env, current, imported, rtol=1e-6):
    rows = MassListHelper.compare(current, imported, rtol)
    info = env.window.manager.workspace.info.masslist_docker
    return compare_module.Dialog(info, rows, imported)


def _committed(env):
    return [item.position for item in
            env.window.manager.workspace.info.masslist_docker.masslist]


def test_shows_six_columns_for_the_three_lists(env):
    dlg = _open(env, [], [])
    table = dlg.ui.tableWidget
    headers = [table.horizontalHeaderItem(i).text()
               for i in range(table.columnCount())]
    assert headers == ["current mz", "current formula", "import mz",
                       "import formula", "merge mz", "merge formula"]


def test_aligned_rows_leave_absent_side_blank(env):
    dlg = _open(env, [MassListItem(position=100.0)],
                [MassListItem(position=200.0)])
    table = dlg.ui.tableWidget
    assert table.rowCount() == 2
    assert table.item(0, 0).text() == "100.00000"
    assert table.item(0, 2).text() == ""
    assert table.item(0, 4).text() == "100.00000"
    assert table.item(1, 0).text() == ""
    assert table.item(1, 2).text() == "200.00000"
    assert table.item(1, 4).text() == "200.00000"


def test_within_tolerance_match_sits_on_one_row_with_both_sides(env):
    dlg = _open(env, [MassListItem(position=100.0)],
                [MassListItem(position=100.0000005)])
    table = dlg.ui.tableWidget
    assert table.rowCount() == 1
    assert table.item(0, 0).text() == "100.00000"
    assert table.item(0, 2).text() == "100.00000"


def test_use_current_leaves_the_mass_list_unchanged(env):
    env.window.manager.workspace.info.masslist_docker.masslist = [
        MassListItem(position=100.0)]
    dlg = _open(env, [MassListItem(position=100.0)],
                [MassListItem(position=200.0)])
    dlg.ui.useCurrentPushButton.click()
    assert _committed(env) == [100.0]


def test_use_import_replaces_the_mass_list(env):
    imported = [MassListItem(position=200.0)]
    dlg = _open(env, [MassListItem(position=100.0)], imported)
    dlg.ui.useImportPushButton.click()
    assert _committed(env) == [200.0]


def test_use_merge_replaces_the_mass_list_with_the_union(env):
    dlg = _open(env, [MassListItem(position=100.0)],
                [MassListItem(position=200.0)])
    dlg.ui.useMergePushButton.click()
    assert _committed(env) == [100.0, 200.0]


def test_export_writes_the_six_on_screen_columns(env, tmp_path, monkeypatch):
    current = [MassListItem(position=100.0, formulas=[Formula('CH4')])]
    imported = [MassListItem(position=200.0)]
    dlg = _open(env, current, imported)

    dst = tmp_path / "compare.csv"
    monkeypatch.setattr(
        compare_module, "savefile", lambda *a, **k: (True, str(dst)))
    dlg.export()

    with open(dst, newline="") as f:
        rows = list(csv.reader(f))
    assert rows[0] == ["current_position", "current_formulas",
                       "import_position", "import_formulas",
                       "merge_position", "merge_formulas"]
    assert rows[1] == ["100.0", "CH4", "", "", "100.0", "CH4"]
    assert rows[2] == ["", "", "200.0", "", "200.0", ""]


# --------------------------------------------------------------------------
# The import chooser reads only the two-column Mass List CSV; the six-column
# comparison report is a deliverable, not a Mass List, and must be refused.
# --------------------------------------------------------------------------

def test_read_accepts_a_two_column_mass_list(env, tmp_path):
    src = tmp_path / "masslist.csv"
    src.write_text("position,formulas\n100.0,\n200.0,CH4\n")
    items = env.window.masslist.read_masslist_from(str(src))
    assert len(items) == 2


def test_read_refuses_a_comparison_report(env, tmp_path):
    src = tmp_path / "compare.csv"
    src.write_text(
        "current_position,current_formulas,import_position,import_formulas,"
        "merge_position,merge_formulas\n100.0,,200.0,,100.0,\n")
    with pytest.raises(ValueError):
        env.window.masslist.read_masslist_from(str(src))


def test_compare_mass_list_reports_a_non_mass_list_file(env, tmp_path):
    src = tmp_path / "compare.csv"
    src.write_text("a,b,c\n1,2,3\n")
    env.window.manager.workspace.info.masslist_docker.masslist = [
        MassListItem(position=100.0)]

    env.reset()
    uitest.input((True, str(src)))
    env.window.masslist.compare_mass_list()

    assert env.dialogs != []            # the uniform error dialog fired
    assert _committed(env) == [100.0]   # and the Mass List is untouched

