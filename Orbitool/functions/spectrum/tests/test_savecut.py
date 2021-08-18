import pathlib

import pandas as pd
import pytest


from .._spectrum import safeCutSpectrum
from Orbitool.functions import binary_search

data_path = pathlib.Path(__file__).absolute(
).parent.joinpath("savecut_test.csv")


@pytest.fixture
def spectrum():
    spectrum = pd.read_csv(data_path)
    mz = spectrum["mz"].to_numpy()
    intensity = spectrum["intensity"].to_numpy()
    return mz, intensity


def test_safecut_casual(spectrum):
    mz, intensity = spectrum
    mz_, intensity_ = safeCutSpectrum(
        mz, intensity, 50.04741654, 50.05157275)
    assert abs(mz_[0] - 50.0472906) < 1e-9
    assert abs(mz_[-1] - 50.05174069) < 1e-9


def test_safecut_right_zero(spectrum):
    mz, intensity = spectrum
    mz_, intensity_ = safeCutSpectrum(
        mz, intensity, 50.0472906, 50.05174069)
    assert abs(mz_[0] - 50.0472906) < 1e-9
    assert abs(mz_[-1] - 50.05174069) < 1e-9


def test_safecut_wrong_zero(spectrum):
    mz, intensity = spectrum
    mz_, intensity_ = safeCutSpectrum(
        mz, intensity, 50.02991577, 50.06337248)
    assert abs(mz_[0] - 50.0472906) < 1e-9
    assert abs(mz_[-1] - 50.06379248) < 1e-9
