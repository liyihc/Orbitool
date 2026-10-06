"""The damaged-scan repair path: an un-averageable scan leaves its window, not the read.

No `.RAW` is needed and none is committed. What is under test is only what the reader
does when the .NET averager rejects a window because of a scan whose FT profile is
empty, and what it answers its caller with -- so a stub file object plus a stub averager
drive the real code.
"""
from datetime import datetime
from types import SimpleNamespace

import pytest

from .. import thermo

TODAY = datetime(2022, 6, 5)
# The stub window covers raw scans 1..5; scan numbers are used unchecked.
WINDOW = (TODAY, TODAY)


def _profile(points):
    """A .NET-ish segmented scan: the reader only reads Positions.Length."""
    return SimpleNamespace(Positions=SimpleNamespace(Length=points))


class StubRawFile:
    """Scans listed in `empty` have no profile points; the rest look healthy."""

    def __init__(self, empty=(), dispose_error=None):
        self.empty = set(empty)
        self.dispose_error = dispose_error
        self.disposals = 0

    def GetScanStatsForScanNumber(self, scan):
        return SimpleNamespace(TIC=1.0)

    def GetSegmentedScanFromScanNumber(self, scan, stats):
        return _profile(0 if scan in self.empty else 1000)

    def Dispose(self):
        self.disposals += 1
        if self.dispose_error is not None:
            raise self.dispose_error


class ExplodingRawFile:
    """The handle is unusable, so the diagnosis cannot tell anything about any scan."""

    def GetScanStatsForScanNumber(self, scan):
        raise RuntimeError("the file handle is gone")

    def GetSegmentedScanFromScanNumber(self, scan, stats):
        raise AssertionError("the diagnosis must stop at the first failure")


class StubAverager:
    """An AverageScans that rejects a window whenever it is offered a damaged scan."""

    def __init__(self, damaged, fail_always=False):
        self.damaged = set(damaged)
        self.fail_always = fail_always
        self.offered = []

    def AverageScans(self, rawfile, average_list, options):
        offered = list(average_list)
        self.offered.append(offered)
        if self.fail_always or self.damaged & set(offered):
            # The .NET averager throws without naming the scan it choked on.
            raise IndexError("IndexOutOfRangeException")
        result = SimpleNamespace(
            Positions=[500.0 + i for i in range(len(offered))],
            Intensities=[100.0 + i for i in range(len(offered))],
            ScansCombined=len(offered),
        )
        result.SegmentedScan = result  # the reader unwraps it before reading points
        return result


class StubReader(thermo.File):
    """A File whose scan bookkeeping is canned, so one window can be driven directly."""

    def __init__(self, rawfile):
        self.rawfile = rawfile
        self.path = "thermo:C:/data/neg_sample_20220605062321.raw"
        self.name = "neg_sample_20220605062321.raw"

    def getRawScanNum(self, scan):
        return scan

    def datetimeRange2ScanNumRange(self, time_range):
        return (1, 6)  # raw scans 1..5

    def _getFirstFilterInRawNumRange(self, start, stop, filter):
        return object()

    def getSpectrumFilter(self, scan, is_raw_scan_num=False):
        return {"mass": "50.0-2000.0", "string": "FTMS + p NSI"}


def average(reader):
    """One window, as the reader answers it: (mass, intensity, damagedScans)."""
    return reader.getAveragedSpectrumInTimeRange(*WINDOW, 1e-6, {}, {})


def test_window_keeps_the_scans_that_work(monkeypatch):
    averager = StubAverager({3})
    monkeypatch.setattr(thermo, "Extensions", averager)
    reader = StubReader(StubRawFile(empty={3}))

    mass, intensity, damaged = average(reader)

    # The damaged scan is offered once, learned from the failure, then left out -- and
    # the caller is told about it.
    assert averager.offered == [[1, 2, 3, 4, 5], [1, 2, 4, 5]]
    assert len(mass) == len(intensity) == 4
    assert damaged == {3: "no FT profile data"}


def test_a_window_that_reads_cleanly_reports_nothing(monkeypatch):
    monkeypatch.setattr(thermo, "Extensions", StubAverager(set()))
    reader = StubReader(StubRawFile(empty=()))

    mass, intensity, damaged = average(reader)

    assert len(mass) == len(intensity) == 5
    assert damaged == {}


def test_every_window_diagnoses_for_itself(monkeypatch):
    # The reader keeps nothing between calls: a second window pays for its own diagnosis
    # and answers with its own finding.
    averager = StubAverager({3})
    monkeypatch.setattr(thermo, "Extensions", averager)

    first = average(StubReader(StubRawFile(empty={3})))
    second = average(StubReader(StubRawFile(empty={3})))

    assert averager.offered == [[1, 2, 3, 4, 5], [1, 2, 4, 5]] * 2
    assert first[2] == second[2] == {3: "no FT profile data"}


def test_healthy_scans_are_never_blamed(monkeypatch):
    # The averager fails, but no scan can be shown to be damaged, so the failure has to
    # reach the caller instead of quietly dropping a scan from the average.
    monkeypatch.setattr(thermo, "Extensions", StubAverager({3}))
    reader = StubReader(StubRawFile(empty=()))

    with pytest.raises(IndexError):
        average(reader)


def test_a_broken_diagnosis_does_not_replace_the_failure(monkeypatch):
    monkeypatch.setattr(thermo, "Extensions", StubAverager({3}))
    reader = StubReader(ExplodingRawFile())

    with pytest.raises(IndexError):  # not the RuntimeError from the diagnosis
        average(reader)


def test_a_window_without_a_usable_scan_is_dropped(monkeypatch):
    # Every offered scan is empty, so there is nothing to average: the window yields no
    # spectrum instead of an empty one, and the whole file stays readable.
    averager = StubAverager({1, 2, 3, 4, 5})
    monkeypatch.setattr(thermo, "Extensions", averager)
    reader = StubReader(StubRawFile(empty={1, 2, 3, 4, 5}))

    mass, intensity, damaged = average(reader)

    assert mass is None and intensity is None
    assert averager.offered == [[1, 2, 3, 4, 5]]
    assert set(damaged) == {1, 2, 3, 4, 5}


def test_close_is_idempotent_and_never_raises():
    rawfile = StubRawFile(dispose_error=TypeError("'MethodObject' object is not callable"))
    reader = StubReader(rawfile)

    reader.close()
    reader.close()

    assert rawfile.disposals == 1
    assert reader.rawfile is None


def test_close_survives_a_reader_whose_init_never_finished():
    reader = thermo.File.__new__(thermo.File)  # initRawFile raised, so no rawfile

    reader.close()


def test_group_scans_by_reason_orders_the_scan_numbers():
    assert thermo.groupScansByReason({7: "b", 3: "a", 5: "a"}) == {"a": [3, 5], "b": [7]}
