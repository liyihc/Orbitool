import h5py
import numpy as np
import pytest

from Orbitool.base.structure import broken_entries
from Orbitool.models.formula import Formula
from Orbitool.models.workspace import WorkSpace, updater
from Orbitool.models.workspace.tests import legacy_workspace as legacy


def _open(path) -> WorkSpace:
    broken_entries.clear()
    return WorkSpace(path, False)


def _assert_time_series(workspace: WorkSpace, era: str):
    series = list(workspace.data.time_series)
    if era == "2.4.3":
        specs = legacy.MODERN_SERIES
        expected_formulas = [[Formula("NO3-")], []]
    else:
        specs = legacy.LEGACY_SERIES
        expected_formulas = [[Formula("NO3-")], [], []]

    assert len(series) == len(specs)
    for item, spec in zip(series, specs):
        assert item.position_min == pytest.approx(spec[0])
        assert item.position_max == pytest.approx(spec[1])
        # time unit conversion is part of the shared migration
        assert list(item.times) == legacy.TIMES
        np.testing.assert_array_equal(item.intensity, legacy.SERIES_INTENSITY)

    assert [[f for f in item.formulas] for item in series] == expected_formulas

    for item in series:
        # pre-existing files carry no `rtol`: the reader must default it, so the
        # tag stays unchanged instead of gaining a fabricated ppm
        assert item.rtol == 0.0
        if era == "2.4.3":
            np.testing.assert_array_equal(
                item.positions, legacy.SERIES_POSITIONS)
        else:
            # never recorded before 2.4.3: absent, not fabricated
            assert len(item.positions) == len(legacy.TIMES)
            assert np.isnan(item.positions).all()

    rows = workspace.info.time_series_tab.timeseries_infos
    if era == "2.4.3":
        assert len(rows) == len(series)
        assert rows[0].time_min == legacy.TIMES[0]
        assert rows[0].time_max == legacy.TIMES[-1]
        assert rows[0].formulas == [Formula("NO3-")]
        # the row was written before `rtol` existed: default it, keep the old tag
        assert rows[0].rtol == 0.0
        assert rows[0].get_name() == "O3N-"
    else:
        # an empty table: the time-series UI rebuilds the rows on open
        assert rows == []


def _assert_workspace(workspace: WorkSpace, era: str):
    info = workspace.info
    _assert_time_series(workspace, era)

    assert len(workspace.data.raw_spectra) == 1
    assert len(workspace.data.calibrated_spectra) == 1

    spectrum_infos = info.file_tab.spectrum_infos
    assert len(spectrum_infos) == 2
    assert spectrum_infos[0].path == legacy.SPECTRUM_PATH
    assert spectrum_infos[0].filter == {"polarity": "1"}
    if era == "2.4.3":
        assert len(info.file_tab.periods) == 1
        assert info.file_tab.periods[0].use_time()
    else:
        assert info.file_tab.periods == []

    segment = info.calibration_tab.calibrate_info_segments[0]
    assert segment.intensity_filter == 100
    assert segment.rtol == pytest.approx(2e-6)
    assert segment.degree == 2
    assert segment.n_ions == 3

    calc_gen = info.formula_docker.calc_gen
    if era == "2.1.5":
        # settings group supplied by the normalizer
        assert "C" in calc_gen.element_states
        assert "C[13]" in calc_gen.isotope_usable
    else:
        # settings group from the file preserved as-is
        assert list(calc_gen.element_states) == list(legacy.ELEMENT_STATES)
        assert list(calc_gen.isotope_usable) == list(legacy.ISOTOPE_USABLE)

    result = info.noise_tab.general_result
    np.testing.assert_array_equal(result.spectrum_split.mz, legacy.MZ)
    np.testing.assert_array_equal(result.noise_split.mz, legacy.MZ)
    if era == "2.4.3":
        # existing split arrays are untouched
        np.testing.assert_array_equal(
            result.spectrum_split.intensity, legacy.SPLIT_SIGNAL)
        np.testing.assert_array_equal(
            result.noise_split.intensity, legacy.SPLIT_NOISE)
    else:
        # rebuilt from the stored current spectrum and noise array
        np.testing.assert_array_equal(
            result.spectrum_split.intensity, legacy.INTENSITY)
        np.testing.assert_array_equal(
            result.noise_split.intensity, legacy.NOISE)
    np.testing.assert_array_equal(
        info.noise_tab.current_spectrum.mz, legacy.MZ)

    # state with no UI left: the 2.6.0 updater strips the stale spectrum
    # docker, mass-defect tab and time-series show index from the file itself
    assert "info/spectrum_docker" not in workspace.file
    assert "info/mass_defect_tab" not in workspace.file
    time_series_tab = workspace.file.get_h5group("info/time_series_tab")
    assert "show_index" not in time_series_tab.attrs

    assert len(info.peak_fit_tab.peaks) == 1
    assert len(info.peak_fit_tab.raw_peaks) == 1
    assert len(info.peak_shape_tab.peaks_manager.peaks) == 1


def test_too_new_is_the_mirror_of_need_update():
    assert updater.too_new("99.0.0")
    assert not updater.too_new("2.6.0")
    assert not updater.too_new("1.0.0")
    assert not updater.need_update("99.0.0")
    assert updater.need_update("1.0.0")


@pytest.mark.parametrize("era", legacy.ERAS)
def test_migrate_legacy_workspace(tmp_path, era):
    path = tmp_path / "legacy.Orbitool"
    legacy.build(path, era)
    assert updater.get_version(str(path)) == era

    updater.update(str(path))

    assert updater.get_version(str(path)) == "2.6.0"
    assert not updater.need_update(updater.get_version(str(path)))

    workspace = _open(path)
    try:
        assert broken_entries == []
        _assert_workspace(workspace, era)
    finally:
        workspace.close()
    assert broken_entries == []


@pytest.mark.parametrize("state", ["moved", "processed"])
def test_migration_resumes_a_half_migrated_copy(tmp_path, state):
    path = tmp_path / "half.Orbitool"
    legacy.build(path, "2.4.0", time_series_state=state)
    assert updater.get_version(str(path)) == "2.4.0"

    updater.update(str(path))

    assert updater.get_version(str(path)) == "2.6.0"
    workspace = _open(path)
    try:
        assert broken_entries == []
        _assert_workspace(workspace, "2.4.0")
    finally:
        workspace.close()
    assert broken_entries == []


def test_migration_fails_loudly_when_the_time_series_tab_is_gone(tmp_path):
    path = tmp_path / "unrecognizable.Orbitool"
    legacy.build(path, "2.4.0")
    with h5py.File(path, "r+") as f:
        del f["info/time_series_tab"]

    with pytest.raises(ValueError, match="time_series_tab"):
        updater.update(str(path))

    # the version is stamped only after the whole chain succeeds, so the copy
    # stays retryable and can never look like a successful migration
    assert updater.get_version(str(path)) == "2.4.0"


def test_migration_fails_loudly_on_a_malformed_series(tmp_path):
    path = tmp_path / "malformed.Orbitool"
    legacy.build(path, "2.4.0")
    with h5py.File(path, "r+") as f:
        del f["info/time_series_tab/series/0/times"]

    with pytest.raises(ValueError, match="'times' dataset"):
        updater.update(str(path))

    assert updater.get_version(str(path)) == "2.4.0"


def test_migration_fails_loudly_when_the_series_group_is_gone(tmp_path):
    # the tab itself was written by an app version that had the feature, so a
    # missing `series` group is damage, not "this workspace never had any"
    path = tmp_path / "damaged.Orbitool"
    legacy.build(path, "2.4.0")
    with h5py.File(path, "r+") as f:
        del f["info/time_series_tab/series"]

    with pytest.raises(ValueError, match="holds time series"):
        updater.update(str(path))

    assert updater.get_version(str(path)) == "2.4.0"


def test_migration_fails_loudly_when_the_split_cannot_be_rebuilt(tmp_path):
    # pre-2.4.3 files have no noise/signal split; without a current spectrum
    # there is nothing honest to rebuild it from, so refuse loudly
    path = tmp_path / "no_split_source.Orbitool"
    legacy.build(path, "2.4.0")
    with h5py.File(path, "r+") as f:
        del f["info/noise_tab/current_spectrum"]

    with pytest.raises(ValueError, match="noise/signal split"):
        updater.update(str(path))

    assert updater.get_version(str(path)) == "2.4.0"


def test_migration_carries_the_legacy_period_end_column(tmp_path):
    # 2.4.4/2.4.5 stored the scan-number range as start_num/end_num; the model
    # renamed the second column to stop_num and ver2_5_0 never follows it, so
    # without the normalizer the values would read back as the -1 default
    path = tmp_path / "scan_numbers.Orbitool"
    legacy.build(path, "2.4.3")
    legacy.use_scan_number_periods(path, 100, 200)
    assert updater.get_version(str(path)) == "2.4.5"

    updater.update(str(path))

    assert updater.get_version(str(path)) == "2.6.0"
    workspace = _open(path)
    try:
        assert broken_entries == []
        periods = workspace.info.file_tab.periods
        assert len(periods) == 1
        assert periods[0].start_num == 100
        assert periods[0].stop_num == 200
        assert not periods[0].use_time()
        assert periods[0].length() == 100
        # the rest of the workspace still migrates
        assert len(workspace.data.time_series) == len(legacy.MODERN_SERIES)
    finally:
        workspace.close()
    assert broken_entries == []


def test_migration_accepts_a_tab_that_never_held_series(tmp_path):
    # a tab the 2.4.0 renamer created for a workspace predating the
    # time-series feature: no attributes, no series -- nothing to migrate
    path = tmp_path / "no_series_feature.Orbitool"
    legacy.build(path, "2.4.0")
    with h5py.File(path, "r+") as f:
        tab = f["info/time_series_tab"]
        del tab["series"]
        for name in list(tab.attrs):
            del tab.attrs[name]

    updater.update(str(path))

    assert updater.get_version(str(path)) == "2.6.0"
    workspace = _open(path)
    try:
        assert broken_entries == []
        assert len(workspace.data.time_series) == 0
        # the rest of the workspace still migrates
        assert workspace.info.file_tab.spectrum_infos[0].path == \
            legacy.SPECTRUM_PATH
    finally:
        workspace.close()
    assert broken_entries == []
