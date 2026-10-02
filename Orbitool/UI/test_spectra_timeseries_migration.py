"""Executable coverage for the ticket-08 migration (Noise, PeakShape,
Spectrum, Timeseries, Timeserieses): the legacy generator tasks were
rewritten as ui_task coroutines.

The batch carries two non-default mode sites (`showSeries_CatchException`
`'e'` -> light, `rescale` `'x'` -> join), four `MultiProcess` worker steps
(Noise `ReadFromFile` in denoise/skip, Timeserieses `CalcTimeseries` /
`CalcSumTimeSeries`), and several former argument-switch slots whose
arguments are now forwarded by signature. It is also the batch where two
generator helpers (`Noise.readSelectedSpectrum`, `PeakShape.showPeak`,
`Timeserieses.showTimeseries`) became async: `showTimeseries` keeps a
synchronous table path for `restore` (which used to drain the generator
inline), and `MainUiPy.noise_tab_finish` was migrated in this ticket (the
one cross-file site) so the Noise -> PeakShape relay keeps delegating to
`await showPeak()`.

No RAW data is available, so file dialogs are answered through
`Orbitool.UI.utils.test.input` / module `savefile` stubs, user-facing
`showInfo` is recorded instead of shown, and the full main window is built
once. `thread_block_gui` makes workers run inline for deterministic busy
edges.

Placed at the batch root (all five files are top-level `Orbitool/UI`
modules) and listed in `pytest.ini`.
"""
import importlib
from array import array
from datetime import datetime, timedelta

import numpy as np
import pytest
from PyQt6 import QtWidgets

from ..models.spectrum.spectrum import Spectrum
from ..models.timeseries import TimeSeries
from ..models.workspace.timeseries import TimeSeriesInfoRow
# debug_settings is an autouse fixture re-exported for pytest
from .tests.migration_harness import MigrationEnv, debug_settings  # noqa: F401

spectrum_module = importlib.import_module("Orbitool.UI.SpectrumUiPy")
timeserieses_module = importlib.import_module("Orbitool.UI.TimeseriesesUiPy")
noise_module = importlib.import_module("Orbitool.UI.NoiseUiPy")
peakshape_module = importlib.import_module("Orbitool.UI.PeakShapeUiPy")


def _series(position: float) -> TimeSeries:
    start = datetime(2024, 1, 1, 12)
    return TimeSeries(
        position_min=position - 0.1, position_max=position + 0.1,
        times=[start, start + timedelta(minutes=1)],
        positions=array("d", [position, position]),
        intensity=array("d", [1.0, 2.0]))


@pytest.fixture(scope="module")
def env(request):
    state = MigrationEnv()
    state.build(request, extra_dialog_modules=(noise_module, peakshape_module))
    state.window.timeseriesesTab.click_series.connect(
        lambda: state.click_series.append(1))
    return state


def _reset_timeseries(window):
    data = window.manager.workspace.data
    info = window.manager.workspace.info.time_series_tab
    data.time_series.clear()
    info.timeseries_infos.clear()
    info.show_index = -1
    widget = window.timeseriesesTab
    widget.shown_series.clear()
    widget.plot.ax.clear()


@pytest.fixture(autouse=True)
def reset_state(env):
    env.reset()
    window = env.window
    _reset_timeseries(window)
    window.peakShapeTab.info.spectrum = None
    window.peakShapeTab.info.peaks_manager = None
    window.noiseTab.info.current_spectrum = None


def _install_valid_series(window, positions=(100.0, 101.0)):
    widget = window.timeseriesesTab
    info = widget.info
    for position in positions:
        series = _series(position)
        widget.timeseries.append(series)
        info.timeseries_infos.append(TimeSeriesInfoRow.FromTimeSeries(series))


# --------------------------------------------------------------------------
# Noise: default slots, signature-forwarded slots, error recovery
# --------------------------------------------------------------------------

def test_noise_default_slot_takes_and_releases_busy(env):
    window = env.window
    window.noiseTab.scaleToSpectrum()          # no spectrum -> early return
    assert env.dialogs == []
    assert env.busy == [True, False]
    assert not window.manager.busy


def test_noise_signature_forwarded_slots(env):
    window = env.window
    noise = window.noiseTab

    noise.moveToTableClickedNoise(QtWidgets.QTableWidgetItem("x"))
    assert env.busy == [True, False]
    assert env.dialogs == []
    env.reset()

    noise.y_times(2.0)                          # was the old argument switch
    assert env.busy == [True, False]
    assert env.dialogs == []
    env.reset()

    checkbox = noise.ui.yLogCheckBox
    checkbox.setChecked(True)                   # real toggled(bool) -> yLogToggle
    try:
        assert env.dialogs == []
        assert env.busy == [True, False]
    finally:
        checkbox.setChecked(False)


def test_noise_add_formula_recovers_before_dialog(env, monkeypatch):
    window = env.window
    noise = window.noiseTab
    info = noise.info
    info.general_setting.noise_formulas.clear()
    original = noise.showNoiseFormula

    def spy():
        env.timeline.append(("showNoiseFormula",))
        original()

    def boom(text):
        raise ValueError("bad formula")

    monkeypatch.setattr(noise, "showNoiseFormula", spy)
    monkeypatch.setattr(noise_module, "Formula", boom)
    noise.ui.lineEdit.setText("whatever")

    noise.addFormula()                          # replaces the old recovery hook

    assert [entry[0] for entry in env.timeline] == ["showNoiseFormula", "dialog"]
    assert env.dialogs == [("bad formula",)]    # str(e), once
    assert env.busy == [True, False]            # counting rule releases on error
    assert not window.manager.busy
    noise.ui.lineEdit.setText("")


# --------------------------------------------------------------------------
# PeakShape: generator helper became an async helper
# --------------------------------------------------------------------------

def test_peakshape_show_peak_early_return_is_async(env):
    window = env.window
    window.peakShapeTab.showButtonClicked()     # spectrum None -> showInfo + return
    assert ("please denoise first",) in [
        (args[0],) for args in env.dialogs]
    assert env.busy == [True, False]
    assert not window.manager.busy


def test_peakshape_finish_emits_callback(env):
    window = env.window
    hits = []
    window.peakShapeTab.callback.connect(lambda result: hits.append(result))
    window.peakShapeTab.finishPeakShape()
    assert hits == [()]
    assert env.busy == [True, False]


# --------------------------------------------------------------------------
# Spectrum: msgless background step -> default message
# --------------------------------------------------------------------------

def test_spectrum_export_worker_and_default_message(env, tmp_path, monkeypatch):
    window = env.window
    spectrum = Spectrum(
        mz=np.array([1.0, 2.0]), intensity=np.array([3.0, 4.0]),
        path="none:", start_time=datetime(2024, 1, 1),
        end_time=datetime(2024, 1, 1, 1))
    window.spectrum.info.spectrum = spectrum
    dst = tmp_path / "spectrum.csv"
    monkeypatch.setattr(spectrum_module, "savefile", lambda *a, **k: (True, str(dst)))

    window.spectrum.export()

    assert env.dialogs == []
    assert env.busy == [True, False]
    assert "processing" in env.msgs             # msgless background -> default msg
    assert dst.exists() and dst.stat().st_size > 0


# --------------------------------------------------------------------------
# Timeseries: one former single-letter light site
# --------------------------------------------------------------------------

def test_timeseries_light_show_series_leaves_busy_untouched(env):
    window = env.window
    manager = window.manager
    manager.set_busy(True)
    env.busy.clear()
    try:
        window.timeseries.showSeries_CatchException()   # was a light letter mode
        assert env.dialogs == []
        assert env.busy == []                            # light: no transition
        assert manager.busy is True
    finally:
        manager.set_busy(False)


# --------------------------------------------------------------------------
# Timeserieses: MultiProcess pipeline, join, async helper + sync restore
# --------------------------------------------------------------------------

def test_timeserieses_calc_peak_multiprocess_pipeline(env):
    window = env.window
    widget = window.timeseriesesTab
    widget.ui.mzRadioButton.setChecked(True)
    widget.ui.mzDoubleSpinBox.setValue(100.0)
    widget.ui.rtolDoubleSpinBox.setValue(5.0)

    widget.calc_peak()                          # empty calibrated_spectra

    assert env.dialogs == []
    assert env.busy == [True, False]
    assert "calculate time series" in env.msgs
    assert "write to disk" in env.msgs
    assert len(widget.info.timeseries_infos) == 1
    assert widget.ui.tableWidget.rowCount() == 1


def test_timeserieses_calc_sum_multiprocess_pipeline(env):
    window = env.window
    widget = window.timeseriesesTab
    widget.ui.rangeMinDoubleSpinBox.setValue(99.0)
    widget.ui.rangeMaxDoubleSpinBox.setValue(101.0)

    widget.calc_sum()

    assert env.dialogs == []
    assert env.busy == [True, False]
    assert "calculate mz range sum series" in env.msgs
    assert len(widget.info.timeseries_infos) == 1


def test_timeserieses_join_rescale_starts_while_busy(env):
    window = env.window
    manager = window.manager
    manager.set_busy(True)
    env.busy.clear()
    try:
        window.timeseriesesTab.rescale()        # was join-mode
        assert env.dialogs == []                # not refused
        assert env.busy == []                   # busy already held -> no new edge
        assert manager.busy is True
    finally:
        manager.set_busy(False)


def test_timeserieses_restore_syncs_without_busy(env):
    window = env.window
    widget = window.timeseriesesTab
    info = widget.info
    window.manager.workspace.data.time_series.append(_series(100.0))
    assert info.timeseries_infos == []

    widget.restore()                            # used to drain showTimeseries()

    assert len(info.timeseries_infos) == 1
    assert widget.ui.tableWidget.rowCount() == 1
    assert env.busy == []                       # the sync path never touches busy


def test_timeserieses_signature_forwarded_slots(env):
    window = env.window
    widget = window.timeseriesesTab
    _install_valid_series(window)
    widget._show_timeseries_table()
    table = widget.ui.tableWidget

    checkbox = table.cellWidget(0, 0)
    assert checkbox is not None
    checkbox.setChecked(True)                   # toggled -> showTimeseriesAt(index, checked)
    assert env.dialogs == []
    assert env.busy == [True, False]
    assert 0 in widget.shown_series             # a line was plotted
    env.reset()

    item = table.item(0, 1)
    assert item is not None
    table.itemDoubleClicked.emit(item)          # -> seriesClicked(item)
    assert widget.info.show_index == 0
    assert env.click_series == [1]
    assert env.busy == [True, False]


def test_timeserieses_export_worker(env, tmp_path, monkeypatch):
    window = env.window
    widget = window.timeseriesesTab
    _install_valid_series(window)
    widget.info.show_index = 0
    dst = tmp_path / "timeseries.csv"
    monkeypatch.setattr(
        timeserieses_module, "savefile", lambda *a, **k: (True, str(dst)))

    widget.export("intensity")                  # worker background step

    assert env.dialogs == []
    assert env.busy == [True, False]
    assert dst.exists() and dst.stat().st_size > 0


# --------------------------------------------------------------------------
# Cross-file: MainUiPy.noise_tab_finish relay (the ticket-08 dependency)
# --------------------------------------------------------------------------

def test_noise_tab_finish_join_relay_awaits_show_peak(env, monkeypatch):
    window = env.window
    manager = window.manager
    spent = []

    async def fake_show_peak():
        spent.append(manager.busy)

    monkeypatch.setattr(window.peakShapeTab, "showPeak", fake_show_peak)
    manager.set_busy(True)
    env.busy.clear()
    try:
        window.noise_tab_finish((object(),))
        assert spent == [True]                  # awaited while the outer holder is busy
        assert env.dialogs == []
        assert env.busy == []                   # join releases only its own count
        assert manager.busy is True
    finally:
        manager.set_busy(False)
