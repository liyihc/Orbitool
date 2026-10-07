"""Exporting the raw spectrum shown on the Noise tab.

The Noise tab's Export group writes the currently shown (selected/averaged)
spectrum as an `mz,intensity` CSV. Before a spectrum has been read there is
nothing to export, and then nothing may be written.
"""
import csv
import importlib
from datetime import datetime, timedelta

import numpy as np
import pytest

from ...models.spectrum import Spectrum
# debug_settings is an autouse fixture re-exported for pytest
from .migration_harness import MigrationEnv, debug_settings  # noqa: F401

noise_module = importlib.import_module("Orbitool.UI.NoiseUiPy")


def _spectrum():
    start = datetime(2024, 1, 1, 12)
    return Spectrum(
        mz=np.array([100.0, 100.01, 100.02]),
        intensity=np.array([1.0, 2.0, 1.0]),
        path="none:", start_time=start, end_time=start + timedelta(minutes=1))


@pytest.fixture
def env(request):
    state = MigrationEnv().build(request, extra_dialog_modules=(noise_module,))
    state.reset()
    yield state
    state.window.noiseTab.info.current_spectrum = None


def test_export_spectrum_writes_mz_intensity_csv(env, tmp_path, monkeypatch):
    window = env.window
    window.noiseTab.info.current_spectrum = _spectrum()
    dst = tmp_path / "raw_spectrum.csv"
    monkeypatch.setattr(noise_module, "savefile",
                        lambda *a, **k: (True, str(dst)))

    window.noiseTab.exportSpectrum()

    assert env.dialogs == []
    assert env.busy == [True, False]
    with open(dst, newline="") as f:
        rows = list(csv.reader(f))
    assert rows[0] == ["mz", "intensity"]
    assert [row[0] for row in rows[1:]] == ["100.0", "100.01", "100.02"]
    assert [row[1] for row in rows[1:]] == ["1.0", "2.0", "1.0"]


def test_export_spectrum_without_selected_spectrum_writes_nothing(
        env, tmp_path, monkeypatch):
    window = env.window
    window.noiseTab.info.current_spectrum = None
    dst = tmp_path / "raw_spectrum.csv"
    calls = []
    monkeypatch.setattr(
        noise_module, "savefile",
        lambda *a, **k: (calls.append(a), (True, str(dst)))[1])

    window.noiseTab.exportSpectrum()

    assert calls == []              # the file dialog is never reached
    assert not dst.exists()
    assert len(env.dialogs) == 1    # the user is told there is nothing to save
