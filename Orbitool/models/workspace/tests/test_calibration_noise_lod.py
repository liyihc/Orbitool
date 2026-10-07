"""The per-spectrum noise/LOD tables calibration records.

They live in `info/calibration_tab/noise_lod`, parallel to
`calibrated_spectrum_infos` / `data/calibrated_spectra`. A workspace that was
calibrated before the tables existed simply has no such dataset: the field must
default to empty without raising, so no migration is needed.
"""
import h5py
import pytest

from Orbitool.base.structure import broken_entries
from Orbitool.models.spectrum import Spectrum
from Orbitool.models.workspace import WorkSpace
from Orbitool.models.workspace.calibration import CalibratedNoiseLOD
from Orbitool.models.workspace.tests import legacy_workspace as legacy


def _spectrum() -> Spectrum:
    return Spectrum(
        mz=legacy.MZ, intensity=legacy.INTENSITY,
        path=legacy.SPECTRUM_PATH,
        start_time=legacy.SPECTRUM_START, end_time=legacy.SPECTRUM_END)


def _rows():
    return [
        CalibratedNoiseLOD(spectrum_index=0, formula="global", mass=float("nan"),
                           noise=2.0, LOD=3.0),
        CalibratedNoiseLOD(spectrum_index=0, formula="NO3-", mass=61.9884,
                           noise=0.4, LOD=0.8),
        CalibratedNoiseLOD(spectrum_index=1, formula="global", mass=float("nan"),
                           noise=2.5, LOD=3.5),
    ]


def test_noise_lod_round_trips(tmp_path):
    path = tmp_path / "workspace.Orbitool"
    workspace = WorkSpace(str(path), False)
    workspace.data.calibrated_spectra.append(_spectrum())
    workspace.data.calibrated_spectra.append(_spectrum())
    workspace.info.calibration_tab.noise_lod = _rows()
    workspace.save()
    workspace.close()

    broken_entries.clear()
    reopened = WorkSpace(str(path), False)
    try:
        assert broken_entries == []
        rows = reopened.info.calibration_tab.noise_lod
        assert len(rows) == 3
        assert [row.spectrum_index for row in rows] == [0, 0, 1]
        assert [row.formula for row in rows] == ["global", "NO3-", "global"]
        assert rows[1].mass == pytest.approx(61.9884)
        assert rows[1].noise == pytest.approx(0.4)
        assert rows[1].LOD == pytest.approx(0.8)
    finally:
        reopened.close()


def test_missing_noise_lod_defaults_empty(tmp_path):
    path = tmp_path / "old.Orbitool"
    workspace = WorkSpace(str(path), False)
    workspace.info.calibration_tab.noise_lod = _rows()
    workspace.save()
    workspace.close()

    # an old file predates the field: drop the dataset, then read it back
    with h5py.File(path, "r+") as f:
        del f["info/calibration_tab/noise_lod"]

    broken_entries.clear()
    reopened = WorkSpace(str(path), False)
    try:
        assert reopened.info.calibration_tab.noise_lod == []
        assert broken_entries == []
    finally:
        reopened.close()
