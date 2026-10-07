"""Spectra List Select export maps the selected row back to its spectrum.

When averaged windows are on, the table shows fewer rows than the underlying
spectrum collection: everything after the first scan of an average
(`average_index != 0`) is folded into the displayed row above it. A selected
table row is therefore an index into the displayed rows, and Select export
must translate it through `shown_indexes` before indexing the spectra.
"""
import csv
import importlib
from datetime import datetime, timedelta

import numpy as np
import pytest

from ...models.file import FileSpectrumInfo
from ...models.spectrum import Spectrum
# debug_settings is an autouse fixture re-exported for pytest
from .migration_harness import MigrationEnv, debug_settings  # noqa: F401

spectra_list_module = importlib.import_module("Orbitool.UI.SpectraListUiPy")

BASE = datetime(2024, 1, 1, 12)


def _spectrum(minute, intensity):
    start = BASE + timedelta(minutes=minute)
    return Spectrum(
        mz=np.array([100.0, 101.0]),
        intensity=np.array([intensity, intensity + 0.5]),
        path="none:", start_time=start, end_time=start + timedelta(minutes=1))


def _info(minute, average_index=0):
    start = BASE + timedelta(minutes=minute)
    return FileSpectrumInfo(
        start_time=start, end_time=start + timedelta(minutes=1),
        path="none:", average_index=average_index)


@pytest.fixture
def env(request):
    state = MigrationEnv().build(
        request, extra_dialog_modules=(spectra_list_module,))
    state.reset()
    yield state


def test_select_exports_the_selected_shown_row(env, tmp_path, monkeypatch):
    window = env.window
    widget = window.spectraList
    data = window.manager.workspace.data
    data.raw_spectra.clear()
    for minute, intensity in enumerate((10.0, 20.0, 30.0)):
        data.raw_spectra.append(_spectrum(minute, intensity))
    file_tab = window.manager.workspace.info.file_tab
    file_tab.spectrum_infos.clear()
    # rows 0 and 2 start an average; row 1 is folded into row 0
    file_tab.spectrum_infos.extend([
        _info(0), _info(0, average_index=1), _info(2)])

    monkeypatch.setattr(
        spectra_list_module, "openfolder",
        lambda *a, **k: (True, str(tmp_path)))
    monkeypatch.setattr(
        spectra_list_module.os, "startfile", lambda *a, **k: None)

    widget.show_file_infos()
    assert list(widget.info.shown_indexes) == [0, 2]
    widget.ui.tableWidget.selectRow(1)
    widget.export("select")

    assert env.dialogs == []
    files = list(tmp_path.glob("*.csv"))
    assert len(files) == 1
    with open(files[0], newline="") as f:
        rows = list(csv.reader(f))
    assert rows[0] == ["mz", "intensity"]
    assert [row[1] for row in rows[1:]] == ["30.0", "30.5"]
