from array import array

import h5py
import numpy as np
import pytest

from Orbitool.base.structure import broken_entries
from Orbitool.models.formula import Formula
from Orbitool.models.spectrum import Spectrum
from Orbitool.models.timeseries import TimeSeries
from Orbitool.models.workspace import WorkSpace
from Orbitool.models.workspace.tests import legacy_workspace as legacy


def _spectrum() -> Spectrum:
    return Spectrum(
        mz=legacy.MZ, intensity=legacy.INTENSITY,
        path=legacy.SPECTRUM_PATH,
        start_time=legacy.SPECTRUM_START, end_time=legacy.SPECTRUM_END)


def _series() -> TimeSeries:
    return TimeSeries(
        position_min=61.9, position_max=62.1, range_sum=False,
        formulas=[Formula("NO3-")],
        times=list(legacy.TIMES),
        positions=array("d", legacy.SERIES_POSITIONS),
        intensity=array("d", legacy.SERIES_INTENSITY))


def _build(path):
    workspace = WorkSpace(path, False)
    workspace.data.raw_spectra.append(_spectrum())
    workspace.data.calibrated_spectra.append(_spectrum())
    workspace.data.time_series.append(_series())
    workspace.save()
    workspace.close()


def _assert_copy(path):
    broken_entries.clear()
    workspace = WorkSpace(path, False)
    try:
        assert broken_entries == []
        assert len(workspace.data.raw_spectra) == 1
        assert len(workspace.data.calibrated_spectra) == 1
        series = list(workspace.data.time_series)
        assert len(series) == 1
        item = series[0]
        assert item.position_min == pytest.approx(61.9)
        assert item.position_max == pytest.approx(62.1)
        assert item.formulas == [Formula("NO3-")]
        assert list(item.times) == legacy.TIMES
        np.testing.assert_array_equal(item.positions, legacy.SERIES_POSITIONS)
        np.testing.assert_array_equal(item.intensity, legacy.SERIES_INTENSITY)
    finally:
        workspace.close()
    assert broken_entries == []


def test_close_as_copies_time_series(tmp_path):
    source = tmp_path / "source.Orbitool"
    _build(source)

    destination = tmp_path / "destination.Orbitool"
    workspace = WorkSpace(str(source))
    workspace.close_as(str(destination))

    _assert_copy(destination)


def test_close_as_still_reports_broken_entries(tmp_path):
    source = tmp_path / "broken_source.Orbitool"
    _build(source)
    # make one spectrum unreadable: its `0` entry is no longer a spectrum
    # dataset but a group whose mz is not a dataset either
    with h5py.File(source, "r+") as f:
        del f["data/raw_spectra/0"]
        f["data/raw_spectra"].create_group("0").create_group("mz")

    broken_entries.clear()
    workspace = WorkSpace(str(source))
    destination = tmp_path / "destination.Orbitool"
    workspace.close_as(str(destination))

    assert broken_entries, "partial data loss must stay disclosed"
    assert any(entry.startswith("/data/raw_spectra")
               for entry in broken_entries)

    # the time series are copied regardless of the broken spectrum
    broken_entries.clear()
    reopened = WorkSpace(destination, False)
    try:
        assert broken_entries == []
        assert len(reopened.data.time_series) == 1
        assert reopened.data.time_series[0].formulas == [Formula("NO3-")]
    finally:
        reopened.close()
