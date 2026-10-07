"""Retention-time lookup across the scan range, including the boundaries.

No `.RAW` is needed and none is committed. `getSpectrumRetentionTime` works only from
the scan-number bookkeeping and one .NET call (`RetentionTimeFromScanNumber`), so a stub
raw file plus the real `File` methods drive the code: the last-scan correction, and the
single-scan file that is also its own last scan.
"""
from datetime import timedelta

from .. import thermo


class StubRawFile:
    """Maps raw scan number -> retention time in minutes, as the .NET reader does."""

    def __init__(self, retention_minutes):
        self.retention_minutes = retention_minutes

    def RetentionTimeFromScanNumber(self, scan):
        return self.retention_minutes[scan]


class StubReader(thermo.File):
    """A File with only the bookkeeping `getSpectrumRetentionTime` reads."""

    def __init__(self, retention_minutes, first_raw, last_raw, start, end):
        self.rawfile = StubRawFile(retention_minutes)
        self.firstRawScanNum = first_raw
        self.lastRawScanNum = last_raw
        self.startTimedelta = start
        self.endTimedelta = end


def test_single_scan_file_keeps_its_own_time():
    # The single scan is its own last scan. The correction has no predecessor to compare
    # against, so it must be skipped instead of recursing into scan -1.
    reader = StubReader({1: 1.5}, first_raw=1, last_raw=1,
                        start=timedelta(0), end=timedelta(minutes=1.5))

    assert reader.totalScanNum == 1
    assert reader.getSpectrumRetentionTime(0) == timedelta(minutes=1.5)


def test_single_scan_range_still_selects_the_scan():
    reader = StubReader({1: 1.5}, first_raw=1, last_raw=1,
                        start=timedelta(0), end=timedelta(minutes=1.5))

    assert reader.timeRange2ScanNumRange((timedelta(0), timedelta(minutes=2))) == (0, 1)
    # A window that does not cover the scan still comes back empty, not out of range.
    assert reader.timeRange2ScanNumRange((timedelta(0), timedelta(minutes=1))) == (0, 0)


def test_last_scan_time_going_backwards_is_corrected():
    # Raw scans 1..3 hold 1, 2 and 1.5 minutes: the last scan predates the one before it,
    # so the correction spaces it one average step past its predecessor.
    reader = StubReader({1: 1.0, 2: 2.0, 3: 1.5}, first_raw=1, last_raw=3,
                        start=timedelta(0), end=timedelta(minutes=6))

    assert reader.getSpectrumRetentionTime(0) == timedelta(minutes=1.0)
    assert reader.getSpectrumRetentionTime(1) == timedelta(minutes=2.0)
    assert reader.getSpectrumRetentionTime(2) == timedelta(minutes=5.0)


def test_healthy_scans_are_left_untouched():
    reader = StubReader({1: 1.0, 2: 2.0, 3: 3.0}, first_raw=1, last_raw=3,
                        start=timedelta(0), end=timedelta(minutes=6))

    assert [reader.getSpectrumRetentionTime(i) for i in range(3)] == [
        timedelta(minutes=1.0), timedelta(minutes=2.0), timedelta(minutes=3.0)]
