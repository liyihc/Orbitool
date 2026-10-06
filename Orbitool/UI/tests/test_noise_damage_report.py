"""The damaged-file report: only files with a scan that could not be averaged are named.

A read records the damage it finds in a record its caller owns (see the noise tab's
read passes), so this is about what the interface does with that record: one dialog,
and never a file that had nothing wrong with it.
"""
import pytest

from .. import NoiseUiPy


@pytest.fixture
def dialogs(monkeypatch):
    """Every dialog the report shows, as (content, caption)."""
    shown = []
    monkeypatch.setattr(NoiseUiPy, "showInfo",
                        lambda content, cap=None: shown.append((content, cap)))
    return shown


def test_a_file_that_was_only_read_is_not_reported(dialogs):
    # An entry with no scan in it means nothing was found for that file.
    NoiseUiPy.reportDamagedFiles({"Thermo:C:/data/healthy.raw": {}})

    assert dialogs == []


def test_a_read_that_found_nothing_reports_nothing(dialogs):
    NoiseUiPy.reportDamagedFiles({})

    assert dialogs == []


def test_only_the_damaged_files_are_named(dialogs):
    NoiseUiPy.reportDamagedFiles({
        "Thermo:C:/data/a.raw": {3: "no FT profile data"},
        "Thermo:C:/data/b.raw": {},
    })

    assert len(dialogs) == 1
    content, cap = dialogs[0]
    assert cap == "Damaged .RAW files"
    assert "- a.raw:" in content
    assert "b.raw" not in content
