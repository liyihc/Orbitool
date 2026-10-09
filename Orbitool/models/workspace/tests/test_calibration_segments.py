"""`CalibratorInfo.add_segment` / `merge_segment` semantics.

`add_segment` splits the segment whose range contains the separator: it inserts
a copy (carrying the source's fit parameters) as the lower range and returns the
insertion position. The UI relies on both the copy-on-split behaviour and the
returned position to keep the edited segment selected.
"""
import math

import pytest

from Orbitool.models.workspace.calibration import CalibratorInfo


def _edited_info() -> CalibratorInfo:
    info = CalibratorInfo()
    seg = info.calibrate_info_segments[0]
    seg.intensity_filter = 500
    seg.degree = 3
    seg.n_ions = 4
    seg.rtol = 3e-6
    return info


def test_add_segment_splits_into_two_with_same_parameters():
    info = _edited_info()

    pos = info.add_segment(200.0)

    assert pos == 0
    assert len(info.calibrate_info_segments) == 2
    lower, upper = info.calibrate_info_segments
    assert lower.end_point == pytest.approx(200.0)
    assert math.isinf(upper.end_point)
    for seg in (lower, upper):
        assert seg.intensity_filter == 500
        assert seg.degree == 3
        assert seg.n_ions == 4
        assert seg.rtol == pytest.approx(3e-6)


def test_add_segment_inserts_in_order_and_returns_position():
    info = CalibratorInfo()
    assert info.add_segment(300.0) == 0
    assert info.add_segment(200.0) == 0
    assert info.add_segment(250.0) == 1

    assert [seg.end_point for seg in info.calibrate_info_segments] == [
        pytest.approx(200.0), pytest.approx(250.0),
        pytest.approx(300.0), pytest.approx(math.inf)]


def test_add_segment_repeat_separator_raises():
    info = CalibratorInfo()
    info.add_segment(200.0)
    with pytest.raises(ValueError):
        info.add_segment(200.0)


def test_merge_segment_keeps_last_segment():
    info = CalibratorInfo()
    info.add_segment(300.0)
    info.add_segment(200.0)
    info.add_segment(250.0)

    info.merge_segment(0, 2)

    assert [seg.end_point for seg in info.calibrate_info_segments] == [
        pytest.approx(250.0), pytest.approx(300.0), pytest.approx(math.inf)]
