from ..masslist import MassListItem, MassListHelper
from ...formula import Formula


def positions(rows):
    return [row.merge.position for row in rows]


def sides(rows):
    """(has_current, has_import) per aligned row."""
    return [(row.current is not None, row.imported is not None) for row in rows]


def _copy(item):
    return MassListItem(position=item.position, formulas=list(item.formulas))


def test_mergeinto():
    masslist = [MassListItem(position=i) for i in range(1, 10)]

    MassListHelper.mergeInto(masslist, [MassListItem(
        position=i + 1e-7, formulas=[]) for i in range(1, 20)], 1e-6)

    assert len(masslist) == 19


def test_formula():
    f = Formula('CH4')
    masslist = []

    MassListHelper.addMassTo(masslist, MassListItem(position=f.mass()), 1e-6)

    MassListHelper.addMassTo(masslist, MassListItem(position=f.mass(), formulas=[f]), 1e-6)
    MassListHelper.addMassTo(masslist, MassListItem(position=1), 1e-6)
    MassListHelper.addMassTo(masslist, MassListItem(position=1000), 1e-6)
    assert len(masslist) == 3
    assert masslist[0].position == 1.
    assert masslist[1].formulas[0] == f
    assert masslist[2].position == 1000.


def test_compare_empty_current():
    f = Formula('CH4')
    rows = MassListHelper.compare(
        [], [MassListItem(position=f.mass(), formulas=[f])], 1e-6)

    assert len(rows) == 1
    assert rows[0].current is None
    assert rows[0].imported.formulas[0] == f
    assert rows[0].merge.formulas[0] == f


def test_compare_empty_import():
    current = [MassListItem(position=100.0)]
    rows = MassListHelper.compare(current, [], 1e-6)

    assert len(rows) == 1
    assert rows[0].current == current[0]
    assert rows[0].imported is None
    assert rows[0].merge.position == 100.0


def test_compare_within_tolerance_joins_into_one_row():
    current = [MassListItem(position=100.0)]
    imported = [MassListItem(position=100.0000005)]  # 5e-9 relative, < 1e-6
    rows = MassListHelper.compare(current, imported, 1e-6)

    assert sides(rows) == [(True, True)]
    assert rows[0].merge.position == 100.0


def test_compare_one_sided_rows_each_way():
    current = [MassListItem(position=100.0)]
    imported = [MassListItem(position=200.0)]
    rows = MassListHelper.compare(current, imported, 1e-6)

    assert positions(rows) == [100.0, 200.0]
    assert sides(rows) == [(True, False), (False, True)]


def test_compare_formula_conflict_inserts_an_extra_row():
    # equal m/z within tolerance, both sides formula-bearing and different:
    # the merge rule inserts a second row, and so must the comparison
    current = [MassListItem(
        position=100.0, formulas=[Formula('CH4'), Formula('H2O')])]
    imported = [MassListItem(
        position=100.0000005, formulas=[Formula('CH3'), Formula('CO')])]
    rows = MassListHelper.compare(current, imported, 1e-6)

    assert sides(rows) == [(True, False), (False, True)]


def test_compare_merge_column_matches_mergeinto():
    current = [MassListItem(position=i) for i in (100.0, 300.0)]
    imported = [MassListItem(position=100.0000005),
                MassListItem(position=200.0),
                MassListItem(position=300.0,
                             formulas=[Formula('CH4'), Formula('H2O')])]
    rows = MassListHelper.compare(current, imported, 1e-6)

    expected = [_copy(item) for item in current]
    MassListHelper.mergeInto(expected, [_copy(item) for item in imported], 1e-6)

    assert positions(rows) == [item.position for item in expected]
    assert [set(row.merge.formulas) for row in rows] == \
        [set(item.formulas) for item in expected]
