from array import array
from datetime import datetime, timedelta

import pytest

from Orbitool.models.timeseries import TimeSeries
from Orbitool.models.workspace.timeseries import TimeseriesInfo


def _series(position: float) -> TimeSeries:
    start = datetime(2024, 1, 1, 12)
    return TimeSeries(
        position_min=position - 0.1, position_max=position + 0.1,
        times=[start, start + timedelta(minutes=1)],
        positions=array("d", [position, position]),
        intensity=array("d", [1.0, 2.0]))


def test_sync_rebuilds_rows_for_migrated_workspace():
    # ver2_4_3 opens with an empty infos table while the series exist
    info = TimeseriesInfo()
    info.show_index = 2

    info.sync([_series(100.0 + i) for i in range(5)])

    assert len(info.timeseries_infos) == 5
    assert info.show_index == 2
    row = info.timeseries_infos[2]
    assert row.valid()
    assert row.position_min == pytest.approx(101.9)
    assert row.time_min == datetime(2024, 1, 1, 12)


def test_sync_clamps_stale_show_index():
    info = TimeseriesInfo()
    info.show_index = 7

    info.sync([_series(100.0)])

    assert len(info.timeseries_infos) == 1
    assert info.show_index == -1


def test_sync_drops_orphan_rows_and_their_index():
    info = TimeseriesInfo()
    info.sync([_series(100.0), _series(200.0), _series(300.0)])
    info.show_index = 2

    info.sync([_series(100.0)])

    assert len(info.timeseries_infos) == 1
    assert info.show_index == -1


def test_sync_keeps_matching_rows_untouched():
    info = TimeseriesInfo()
    series = [_series(100.0), _series(200.0)]
    info.sync(series)
    rows = info.timeseries_infos
    info.show_index = 1

    info.sync(series)

    assert info.timeseries_infos is rows
    assert info.show_index == 1


def test_sync_empty_workspace():
    info = TimeseriesInfo()
    info.show_index = 3

    info.sync([])

    assert info.timeseries_infos == []
    assert info.show_index == -1
