"""Reading one spectrum info: the reader it opens, reuses and releases, and the damage
record it fills in for the read it belongs to.

No `.RAW` is needed: the reader class is stubbed, so only the bookkeeping in
`FileSpectrumInfo.get_spectrum_from_info` is under test.
"""
from datetime import datetime, timedelta

import pytest

from .. import file as file_module
from ..file import FileSpectrumInfo

START = datetime(2022, 6, 5, 6, 23, 21)
END = START + timedelta(minutes=1)


class StubReader:
    """A ThermoFile that answers the way the real one does: (mass, intensity, damaged)."""

    def __init__(self, realpath, damaged=None, yields_spectrum=True):
        self.path = realpath
        self.damaged = damaged or {}
        self.yields_spectrum = yields_spectrum
        self.closed = 0

    def getAveragedSpectrumInTimeRange(self, start, end, rtol, filter, stats_filter):
        if not self.yields_spectrum:
            return None, None, self.damaged
        return [1.0, 2.0], [3.0, 4.0], self.damaged

    def close(self):
        self.closed += 1


class ReaderFactory:
    """Stands in for ThermoFile: every reader the info opens, in order."""

    def __init__(self):
        self.made = []
        self.damaged = {5: "no FT profile data"}
        self.yields_spectrum = True

    def __call__(self, realpath):
        reader = StubReader(realpath, self.damaged, self.yields_spectrum)
        self.made.append(reader)
        return reader


@pytest.fixture
def readers(monkeypatch):
    factory = ReaderFactory()
    monkeypatch.setattr(file_module, "ThermoFile", factory)
    return factory


def info(path):
    return FileSpectrumInfo(start_time=START, end_time=END, path=path,
                            filter={}, stats_filter={}, average_index=0)


def test_the_damage_of_a_window_reaches_the_read(readers):
    damaged = {}

    info("Thermo:C:/data/a.raw").get_spectrum_from_info(1e-6, damaged=damaged)

    # Keyed by the workspace path of the file, which all of its windows share.
    assert damaged == {"Thermo:C:/data/a.raw": {5: "no FT profile data"}}


def test_every_read_is_given_a_record(readers):
    # `damaged` is required, so a read cannot quietly repair without a place to say so.
    with pytest.raises(TypeError):
        info("Thermo:C:/data/a.raw").get_spectrum_from_info(1e-6)

    assert readers.made == []


def test_a_window_that_reads_cleanly_files_nothing(readers):
    # The record must only ever hold real findings. A file that was merely read used to
    # leave an empty entry behind, and an empty entry reads as damage.
    readers.damaged = {}
    damaged = {}

    info("Thermo:C:/data/a.raw").get_spectrum_from_info(1e-6, damaged=damaged)

    assert damaged == {}


def test_windows_of_one_file_share_one_entry(readers):
    damaged = {}
    info("Thermo:C:/data/a.raw").get_spectrum_from_info(1e-6, damaged=damaged)

    readers.damaged = {6: "no FT profile data"}
    info("Thermo:C:/data/a.raw").get_spectrum_from_info(1e-6, damaged=damaged)

    assert damaged == {"Thermo:C:/data/a.raw": {5: "no FT profile data",
                                               6: "no FT profile data"}}


def test_a_window_without_a_spectrum_still_files_its_damage(readers):
    # The window produced nothing, but the scans it could not average still have to be
    # reported, so the record is written before the reader is released.
    readers.yields_spectrum = False
    damaged = {}

    assert info("Thermo:C:/data/a.raw").get_spectrum_from_info(
        1e-6, damaged=damaged) == (None, None)

    assert damaged == {"Thermo:C:/data/a.raw": {5: "no FT profile data"}}
    assert readers.made[0].closed == 1


def test_the_reader_is_reused_while_the_path_matches(readers):
    damaged = {}
    _, last_reader = info("Thermo:C:/data/a.raw").get_spectrum_from_info(1e-6, damaged=damaged)

    info("Thermo:C:/data/a.raw").get_spectrum_from_info(
        1e-6, last_reader=last_reader, damaged=damaged)

    assert len(readers.made) == 1
    assert readers.made[0].closed == 0


def test_a_superseded_reader_is_closed(readers):
    damaged = {}
    _, last_reader = info("Thermo:C:/data/a.raw").get_spectrum_from_info(1e-6, damaged=damaged)

    info("Thermo:C:/data/b.raw").get_spectrum_from_info(
        1e-6, last_reader=last_reader, damaged=damaged)

    assert [reader.closed for reader in readers.made] == [1, 0]
    assert set(damaged) == {"Thermo:C:/data/a.raw", "Thermo:C:/data/b.raw"}
