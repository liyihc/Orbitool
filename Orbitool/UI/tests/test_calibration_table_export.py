"""Calibration Table sub-tab export: a CSV mirror of the on-screen deviation
matrix, one `ppm`/`used` column pair per ion, files sorted by start time.

The table itself shows ppm with the used ions highlighted; a CSV has no
background, so each ion gets an explicit `used` companion column (1/0). Missing
ions (`rtol` is NaN) write an empty ppm cell but keep `used` as 0. The button is
enabled only once calibration info has been computed.
"""
import csv
import importlib
from datetime import datetime, timedelta

import numpy as np
import pytest

from ...models.calibration import Calibrator, Ion, PathIonInfo
# debug_settings is an autouse fixture re-exported for pytest
from .migration_harness import MigrationEnv, debug_settings  # noqa: F401
from ..utils import test as uitest

calibration_module = importlib.import_module("Orbitool.UI.CalibrationUiPy")

BASE = datetime(2024, 1, 1, 12)


@pytest.fixture
def env(request):
    state = MigrationEnv().build(
        request, extra_dialog_modules=(calibration_module,))
    state.reset()
    yield state


def _ion_info(rtol):
    return PathIonInfo(
        raw_position=np.array([100.0]), raw_intensity=np.array([1.0]),
        position=100.0, rtol=rtol)


def _calibrator(ions):
    formulas = [ion.formula for ion in ions]
    return Calibrator(
        formulas=formulas,
        used_indexes=np.array([0]),
        unused_indexes=np.array(list(range(1, len(ions)))),
        poly_coef=np.array([0.0]))


def _setup_info(info):
    ion0 = Ion.fromText("NO3-")
    ion1 = Ion.fromText("HNO3NO3-")
    info.last_ions = [ion0, ion1]
    # path "early" starts before path "late": export must sort by time
    info.path_times = {"late": BASE + timedelta(minutes=5), "early": BASE}
    info.path_ion_infos = {
        "late": {ion0.formula: _ion_info(1.23456e-6),
                 ion1.formula: _ion_info(float("nan"))},
        "early": {ion0.formula: _ion_info(-0.5e-6),
                  ion1.formula: _ion_info(2e-6)},
    }
    info.calibrator_segments = {
        path: [_calibrator(info.last_ions)]
        for path in info.path_ion_infos}
    return ion0, ion1


def _export(env, tmp_path, widget, filename="calibration_table.csv"):
    target = tmp_path / filename
    uitest.input((True, str(target)))
    widget.exportCalibrationTable()
    assert env.dialogs == []
    with open(target, newline="") as f:
        return list(csv.reader(f))


def test_export_writes_one_ppm_used_pair_per_ion(env, tmp_path):
    widget = env.window.calibrationTab
    ion0, ion1 = _setup_info(widget.info)
    widget.showAllInfo()

    rows = _export(env, tmp_path, widget)

    assert rows[0] == [
        "Time",
        f"{ion0.shown_text} ppm", f"{ion0.shown_text} used",
        f"{ion1.shown_text} ppm", f"{ion1.shown_text} used",
    ]
    # rows sorted by start time: "early" first, then "late"
    assert len(rows) == 3
    assert rows[1] == ["2024-01-01 12:00", "-0.50000", "1", "2.00000", "0"]
    assert rows[2] == ["2024-01-01 12:05", "1.23456", "1", "", "0"]


def test_cancelled_savefile_writes_nothing(env, tmp_path):
    widget = env.window.calibrationTab
    _setup_info(widget.info)
    widget.showAllInfo()

    uitest.input((False, ""))
    widget.exportCalibrationTable()

    assert env.dialogs == []
    assert list(tmp_path.iterdir()) == []


def test_export_without_info_is_blocked(env):
    widget = env.window.calibrationTab
    widget.info.calibrator_segments = {}

    widget.exportCalibrationTable()

    assert env.dialogs == [("please calculate calibration info first",)]
