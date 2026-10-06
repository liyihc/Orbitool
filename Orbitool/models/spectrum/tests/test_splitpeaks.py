import numpy as np

from .._functions import splitPeaks as _splitPeaks
from ..functions import splitPeaks


def test_splitpeaks_both_edges_zero():
    mz = np.array([1., 2., 3., 4., 5.])
    intensity = np.array([0., 1., 0., 1., 0.])
    ranges = _splitPeaks(mz, intensity)
    assert ranges.dtype == np.int32
    assert ranges.tolist() == [[0, 3], [2, 5]]


def test_splitpeaks_rising_left_edge():
    # Intensity starts above the threshold, so there is no left valley and the
    # first index is prepended (`len(l) < len(r)`). This branch raised
    # "Buffer dtype mismatch, expected 'int32' but got 'long long'" on numpy 2.x.
    mz = np.array([1., 2., 3., 4.])
    intensity = np.array([3., 2., 1., 0.])
    peaks = splitPeaks(mz, intensity)
    assert len(peaks) == 1
    assert list(peaks[0].mz) == [1., 2., 3., 4.]


def test_splitpeaks_rising_right_edge():
    # Intensity ends above the threshold, so there is no right valley and the
    # stop index is appended (`len(l) > len(r)`). This branch raised
    # "Buffer dtype mismatch, expected 'int32' but got 'long long'" on numpy 2.x.
    mz = np.array([1., 2., 3., 4.])
    intensity = np.array([0., 1., 2., 3.])
    peaks = splitPeaks(mz, intensity)
    assert len(peaks) == 1
    assert list(peaks[0].mz) == [1., 2., 3., 4.]
