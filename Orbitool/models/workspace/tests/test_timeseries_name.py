import pytest

from Orbitool.models.formula import Formula
from Orbitool.models.timeseries import TimeSeries
from Orbitool.models.workspace.timeseries import TimeSeriesInfoRow


def _row(**kwargs) -> TimeSeriesInfoRow:
    return TimeSeriesInfoRow(position_min=100.0, position_max=100.0, **kwargs)


def test_formula_tag_has_no_ppm_without_tolerance():
    # old / range / hand-built series carry rtol == 0 and keep the legacy tag
    assert _row(formulas=[Formula("C3HO5-")]).get_name() == "C3HO5-"


@pytest.mark.parametrize("ppm, expected", [
    (5.0, "C3HO5- 5ppm"),
    (5.5, "C3HO5- 5.5ppm"),
    (5.25, "C3HO5- 5.25ppm"),
    (10.0, "C3HO5- 10ppm"),
    (0.01, "C3HO5- 0.01ppm"),
    (99.99, "C3HO5- 99.99ppm"),
])
def test_formula_tag_shows_ppm(ppm, expected):
    row = _row(rtol=ppm * 1e-6, formulas=[Formula("C3HO5-")])
    assert row.get_name() == expected


def test_ppm_is_rounded_to_two_decimals():
    row = _row(rtol=5.3333e-6, formulas=[Formula("C3HO5-")])
    assert row.get_name() == "C3HO5- 5.33ppm"


def test_multiple_formulas_share_one_suffix():
    row = _row(rtol=5e-6, formulas=[Formula("C3HO5-"), Formula("C2H4O2")])
    assert row.get_name() == "C3HO5-,C2H4O2 5ppm"


def test_range_sum_series_never_shows_ppm():
    # even with a tolerance set, a range-sum series has no ppm window
    row = TimeSeriesInfoRow(
        position_min=100.5, position_max=101.2, range_sum=True, rtol=5e-6)
    assert row.get_name() == "100.50-101.20"


def test_mz_tag_shows_ppm():
    row = TimeSeriesInfoRow(
        position_min=99.9995, position_max=100.0005, rtol=1e-6)
    assert row.get_name() == "100.00000 1ppm"


def test_from_timeseries_carries_rtol():
    series = TimeSeries.FactoryPositionRtol(100.0, 5e-6, [Formula("C3HO5-")])
    assert series.rtol == pytest.approx(5e-6)
    row = TimeSeriesInfoRow.FromTimeSeries(series)
    assert row.rtol == pytest.approx(5e-6)
    assert row.get_name() == "C3HO5- 5ppm"
