# -*- coding: utf-8 -*-
# Reading Thermo .RAW depends on pythonnet plus the ThermoFisher DLLs tracked next to
# this file, so it only works on Windows with a .NET runtime installed.

from datetime import datetime, timedelta
from functools import cached_property
from typing import Dict, List, Tuple, Counter, Any
import os

import numpy as np
from Orbitool import logger, setting

from ..binary_search import indexBetween
from .spectrum_filter import SpectrumFilter, SpectrumStats, StatsFilters
from . import spectrum_filter

match setting.file.dotnet_driver:
    case ".net framework":
        pass
    case ".net core":
        from pythonnet import load
        load("coreclr")
import clr


pwd = os.path.dirname(__file__)
clr.AddReference(os.path.join(pwd, 'ThermoFisher.CommonCore.Data.dll'))
clr.AddReference(os.path.join(
    pwd, 'ThermoFisher.CommonCore.RawFileReader.dll'))
clr.AddReference(os.path.join(
    pwd, 'ThermoFisher.CommonCore.BackgroundSubtraction.dll'))
clr.AddReference(os.path.join(
    pwd, 'ThermoFisher.CommonCore.MassPrecisionEstimator.dll'))

clr.AddReference('System.Collections')

from System.Collections.Generic import List as CSharpList
from System import Int32

from ThermoFisher.CommonCore.RawFileReader import RawFileReaderAdapter
from ThermoFisher.CommonCore.MassPrecisionEstimator import PrecisionEstimate
from ThermoFisher.CommonCore.Data.Interfaces import IChromatogramSettings, IScanEventBase, \
    IScanFilter, RawFileClassification
from ThermoFisher.CommonCore.Data.FilterEnums import IonizationModeType, MSOrderType, PolarityType
from ThermoFisher.CommonCore.Data.Business import ChromatogramSignal, ChromatogramTraceSettings, \
    DataUnits, Device, GenericDataTypes, SampleType, Scan, TraceType, MassOptions
from ThermoFisher.CommonCore.Data import ToleranceUnits, Extensions

TAG = "ThermoReader"

# Raw scan number -> why it cannot be averaged: the scans of one .RAW file that a read
# has proven unusable. A read hands them back with the spectrum it produced, and its
# caller keeps them only until it has shown them to the user, so nothing survives the
# read that found them.
DamagedScans = Dict[int, str]
DamagedScansByFile = Dict[str, DamagedScans]


def groupScansByReason(scans: Dict[int, str]) -> Dict[str, List[int]]:
    """Invert a {scan number: reason} mapping into {reason: [scan numbers]}.

    The one place that groups damaged scans, so the log line and the dialog cannot
    drift apart. Scan numbers come out in order.
    """
    grouped: Dict[str, List[int]] = {}
    for scan, reason in sorted(scans.items()):
        grouped.setdefault(reason, []).append(scan)
    return grouped


class NoMassSpectrometerError(Exception):
    """A .RAW holds no mass-spectrometer data, so it yields no spectrum.

    Some files carry only other devices (e.g. UV/PDA) or otherwise lack the MS
    instrument that `SelectInstrument(Device.MS, 1)` asks for; the .NET reader
    then throws `ArgumentOutOfRangeException: Instrument index not available`.
    Raised here so an import can leave such a file out instead of failing.
    """


def initRawFile(path):
    rawfile = RawFileReaderAdapter.FileFactory(str(path))
    if rawfile.GetInstrumentCountOfType(Device.MS) < 1:
        rawfile.Dispose()
        raise NoMassSpectrometerError("no MS instrument data")
    rawfile.SelectInstrument(Device.MS, 1)
    rawfile.IncludeReferenceAndExceptionData = True
    return rawfile


class File:
    def __init__(self, fullname):
        assert os.path.exists(fullname), f"File not exists: {fullname}"
        self.path = fullname
        self.name = os.path.split(fullname)[1]
        self.rawfile = initRawFile(fullname)

        # time doesn't contain time zone info
        time = self.rawfile.FileHeader.CreationDate
        self.creationDatetime = datetime(year=time.Year, month=time.Month, day=time.Day, hour=time.Hour,
                                         minute=time.Minute, second=time.Second, microsecond=time.Millisecond * 1000)
        self.startTimedelta = timedelta(
            minutes=self.rawfile.RunHeader.StartTime)
        self.endTimedelta = timedelta(
            minutes=self.rawfile.RunHeader.EndTime)
        self.firstRawScanNum = self.rawfile.RunHeader.FirstSpectrum
        self.lastRawScanNum = self.rawfile.RunHeader.LastSpectrum
        """
        include last scan num
        """
        extra_info = self.rawfile.GetTrailerExtraInformation(1)
        extra_info_dict = dict(zip(extra_info.Labels, extra_info.Values))
        self.massResolution = float(extra_info_dict.get("FT Resolution:"))

    @cached_property
    def startDatetime(self):
        return self.creationDatetime + self.startTimedelta

    @cached_property
    def endDatetime(self):
        return self.creationDatetime + self.endTimedelta

    @cached_property
    def totalScanNum(self):
        return self.lastRawScanNum - self.firstRawScanNum + 1

    def getRawScanNum(self, scan_num):
        return int(scan_num) + self.firstRawScanNum

    def getSpectrumRetentionTime(self, scanNum):
        rawScanNum = self.getRawScanNum(scanNum)
        retentionTime = timedelta(
            minutes=self.rawfile.RetentionTimeFromScanNumber(rawScanNum))
        if rawScanNum == self.lastRawScanNum:
            lastRetentionTime = self.getSpectrumRetentionTime(scanNum - 1)
            if retentionTime < lastRetentionTime:
                averageTimeDelta = (self.endTimedelta - self.startTimedelta) / \
                    (self.lastRawScanNum - self.firstRawScanNum)
                retentionTime = lastRetentionTime + averageTimeDelta
        return timedelta(minutes=self.rawfile.RetentionTimeFromScanNumber(rawScanNum))

    def getSpectrumRetentionTimes(self):
        return [self.getSpectrumRetentionTime(scan_num) for scan_num in range(self.totalScanNum)]

    def getSpectrumDatetime(self, scanNum):
        return self.creationDatetime + self.getSpectrumRetentionTime(scanNum)

    def checkFilter(self, polarity) -> bool:
        for f in self.rawfile.GetFilters():
            if convertPolarity[f.Polarity] == polarity:
                return True
        return False

    def getFilterList(self, num_range: Tuple[int, int] = None, time_range: Tuple[datetime, datetime] = None, *, raw_num_range: Tuple[int, int] = None):
        if raw_num_range is None:
            if num_range is None:
                if time_range is None:
                    num_range = (0, self.totalScanNum)
                else:
                    num_range = self.datetimeRange2ScanNumRange(time_range)
            raw_num_range = (self.getRawScanNum(
                num_range[0]), self.getRawScanNum(num_range[1]))

        f = self.rawfile
        filters = f.GetFilters()
        if len(filters) == 1:
            filter = to_spectrum_filter(filters[0])
            for i in range(*raw_num_range):
                yield filter
        else:
            for i in range(*raw_num_range):
                yield to_spectrum_filter(f.GetFilterForScanNumber(i))

    def getUniqueFilters(self):
        return list(map(to_spectrum_filter, self.rawfile.GetFilters()))

    def _getFirstFilterInRawNumRange(self, start: int, stop: int, target_filter: SpectrumFilter):
        f = self.rawfile
        filters = f.GetFilters()
        for rawfilter in filters:
            filter = to_spectrum_filter(rawfilter)
            if spectrum_filter.filter_match(filter, target_filter):
                return rawfilter
        return None

    def getSpectrumFilter(self, scan_num, is_raw_scan_num=False):
        if not is_raw_scan_num:
            scan_num = self.getRawScanNum(scan_num)
        scanfilter = self.rawfile.GetFilterForScanNumber(scan_num)
        return to_spectrum_filter(scanfilter)

    def datetimeRange2ScanNumRange(self, datetimeRange: Tuple[datetime, datetime]):
        """
            return start (inclusive), stop (exclusive)
        """
        return self.timeRange2ScanNumRange((datetimeRange[0] - self.creationDatetime, datetimeRange[1] - self.creationDatetime))

    def timeRange2ScanNumRange(self, timeRange: Tuple[timedelta, timedelta]):
        """
            return start (inclusive), end (exclusive)
        """
        s: slice = indexBetween(
            self, timeRange, (0, self.totalScanNum),
            method=(lambda _, i: self.getSpectrumRetentionTime(i)))
        return (s.start, s.stop)

    def scanNumRange2TimeRange(self, numRange: Tuple[int, int]) -> Tuple[timedelta, timedelta]:
        return self.getSpectrumRetentionTime(numRange[0]), self.getSpectrumRetentionTime(numRange[1] - 1)

    def scanNumRange2DatetimeRange(self, numRange: Tuple[int, int]):
        return self.creationDatetime + self.getSpectrumRetentionTime(numRange[0]), self.creationDatetime + self.getSpectrumRetentionTime(numRange[1])

    def checkAverageEmpty(self, filter: SpectrumFilter, timeRange: Tuple[timedelta, timedelta] = None, numRange: Tuple[int, int] = None):
        if timeRange is not None and numRange is None:
            start, end = self.timeRange2ScanNumRange(timeRange)
        elif numRange is not None and timeRange is None:
            start, end = numRange
        else:
            raise ValueError(
                "`timeRange` or `numRange` must be provided and only one can be provided")

        for i in range(start, end):
            if spectrum_filter.filter_match(self.getSpectrumFilter(i), filter):
                return False
        return True

    def getAveragedSpectrumInTimeRange(self, start: datetime, end: datetime, rtol, filter: SpectrumFilter,
                                       stats_filter: StatsFilters):
        """Average this window and say which of its scans had to be left out.

        Returns `(mass, intensity, damagedScans)`, where `damagedScans` is empty unless a
        scan could not be averaged. `mass` is None when the window produced no spectrum
        at all; `damagedScans` is returned in that case too, because the scans that
        could not be averaged are exactly what the caller needs to report.
        """
        # Due to a bug related to scan time during data acquisition, AverageScansInTimeRange should not be used
        # averaged = Extensions.AverageScansInTimeRange(self.rawfile, start, end, scanfilter, MassOptions(rtol, ToleranceUnits.ppm))
        startNum, stopNum = list(
            map(self.getRawScanNum, self.datetimeRange2ScanNumRange((start, end))))
        if self._getFirstFilterInRawNumRange(startNum, stopNum, filter) is None:
            return None, None, {}
        average_list = CSharpList[Int32]()
        cnt = 0
        accepted: List[int] = []
        for i in range(startNum, stopNum):
            i_filter = self.getSpectrumFilter(i, True)
            if not spectrum_filter.filter_match(i_filter, filter):
                continue
            if stats_filter:
                i_stats = self.get_spectrum_stats(i, True)
                if not spectrum_filter.stats_match(i_stats, stats_filter):
                    continue
            average_list.Add(i)
            cnt += 1
            accepted.append(i)

        if cnt == 0:
            logger.d(TAG, "getAveragedSpectrumInTimeRange() empty list, skip")
            return None, None, {}
        # A damaged or interrupted acquisition can leave a scan whose FT profile is
        # empty (field case: 2 of 87 scans of one acquisition). Nothing in its metadata
        # gives it away -- its TIC and every trailer field match the healthy scans, and
        # only the profile length does -- so the .NET averager throws
        # IndexOutOfRangeException from CalculateTargetSpectrumParameters without
        # naming the scan it choked on. Reading every profile up front to look for them
        # costs about as much as the averaging itself, so they are learned here, from
        # the failure.
        #
        # This is damage repair, not error handling: an empty profile cannot contribute
        # to any average, so leaving those scans out keeps the window and its point in
        # time instead of losing both.
        damaged: DamagedScans = {}
        try:
            averaged = Extensions.AverageScans(
                self.rawfile, average_list, MassOptions(rtol, ToleranceUnits.ppm))
        except Exception as e:
            # Diagnose what this window offered, and keep the scans we can prove are
            # damaged together with the reason.
            for i in accepted:
                reason = self._damageReason(i)
                if reason is not None:
                    damaged[i] = reason
            if not damaged:
                raise
            keep = [i for i in accepted if i not in damaged]
            grouped = groupScansByReason(damaged)
            detail = "; ".join(f"{reason}: {scans}"
                               for reason, scans in sorted(grouped.items()))
            outcome = (f"{len(keep)} scans averaged" if keep
                       else "no usable scan left, the window is dropped")
            logger.w(TAG, f"{self.name}: {len(damaged)} of {cnt} scans in "
                         f"{start}~{end} have no FT profile data "
                         f"(from {type(e).__name__}), {outcome} -- {detail}")
            if not keep:
                return None, None, damaged
            average_list = CSharpList[Int32]()
            for i in keep:
                average_list.Add(i)
            averaged = Extensions.AverageScans(
                self.rawfile, average_list, MassOptions(rtol, ToleranceUnits.ppm))
        if averaged is None:
            return None, None, damaged
        averaged = averaged.SegmentedScan
        mass = np.fromiter(averaged.Positions, np.float64)
        intensity = np.fromiter(averaged.Intensities, np.float64)
        return mass, intensity, damaged

    def _damageReason(self, rawScanNum: int) -> str | None:
        """Why this scan cannot go into an average, or None if nothing is wrong with it.

        The single place that knows every way a scan can be unusable, so callers record
        a diagnosis instead of guessing at one. Today there is one case: a damaged or
        interrupted acquisition can leave a scan whose SegmentedScan is empty while its
        metadata (TIC, filter, every trailer field) looks perfectly normal. Only the
        profile length reveals it, and Extensions.AverageScans throws
        IndexOutOfRangeException from CalculateTargetSpectrumParameters because of it.

        This runs while handling a failure, so it must never raise: a scan we cannot
        diagnose is reported as fine (None), which leaves the caller's original
        exception to propagate instead of replacing it with this one.
        """
        try:
            stats = self.rawfile.GetScanStatsForScanNumber(rawScanNum)
            points = int(self.rawfile.GetSegmentedScanFromScanNumber(
                rawScanNum, stats).Positions.Length)
        except Exception:
            return None
        if points == 0:
            return "no FT profile data"
        return None

    def close(self):
        """Release the reader's native file handle and mapped file.

        Holding a reader costs about 11 MB of working set and a few handles for a
        15.8 MB file, so it is worth releasing as soon as the reader is dropped;
        that is what __del__ does.

        __del__ can also run during interpreter shutdown, when pythonnet's binding
        layer is already torn down and Dispose() then raises `TypeError:
        'MethodObject' object is not callable`. A deallocator must never raise, and
        at that point the process is ending anyway, so a failure is swallowed.
        """
        rawfile = getattr(self, "rawfile", None)
        if rawfile is None:
            return
        self.rawfile = None
        try:
            rawfile.Dispose()
        except Exception:
            pass

    def __del__(self):
        self.close()

    def get_spectrum_stats(self, scan_num, is_raw_scan_num=False):
        if not is_raw_scan_num:
            scan_num = self.getRawScanNum(scan_num)
        return to_spectrum_stats(self.rawfile.GetScanStatsForScanNumber(scan_num))

    def get_stats_list(self):
        rawfile = self.rawfile
        for index in range(self.firstRawScanNum, self.lastRawScanNum + 1):
            yield to_spectrum_stats(rawfile.GetScanStatsForScanNumber(index))


def to_spectrum_filter(rawfilter) -> SpectrumFilter:
    r = rawfilter.GetMassRange(0)
    return SpectrumFilter(
        string=rawfilter.ToString(),
        polarity=str(convertPolarity[rawfilter.Polarity]),
        mass=f"{r.Low:.1f}-{r.High:.1f}",
        CiD="off" if rawfilter.HigherEnergyCiD.ToString(
        ) == "Off" else format(rawfilter.HigherEnergyCiDValue, ".2f"),
        scan=f"{rawfilter.ScanMode.ToString()} {rawfilter.ScanData.ToString()}"
    )


def to_spectrum_stats(rawstats) -> SpectrumStats:
    return SpectrumStats(
        TIC=rawstats.TIC
    )


convertPolarity = {PolarityType.Any: 0,
                   PolarityType.Positive: 1,
                   PolarityType.Negative: -1}
