"""
Synthetic workspace files in the legacy layouts the migration chain handles.

The three layouts mirror real historical workspaces (the layouts were checked
against files saved by Orbitool 2.1.5, 2.4.0 and 2.4.3):

- ``2.1.5``: flat root tab groups, series under ``time series tab/info/series``,
  calibration segments without ``intensity_filter``/``rtol``, no custom-periods
  table, no calculator settings group, no noise/signal split arrays, and no
  spectrum docker widget at all (it only appeared in 2.3.0).
- ``2.4.0``: ``info/`` + ``data/`` layout, series under
  ``info/time_series_tab/series``, segments with ``intensity_filter`` but
  without ``rtol``, split arrays still absent, ``calc_gen`` present.
- ``2.4.3``: series already under ``data/time_series`` with ``positions`` and
  ``timeseries_infos`` present, split arrays present, ``periods`` present;
  segments still lack ``rtol`` and the spectrum docker has no spectrum.

Groups that no updater touches and that the modern reader defaults on its own
(``general_setting``, ``restricted_calc``/``force_calc``, ...) are left out to
keep the fixtures readable. Nothing is compressed: compression has no effect
on any layout the migration reads.
"""
from datetime import datetime
from math import inf
from typing import List

import h5py
import numpy as np

VLEN_FLOAT = h5py.vlen_dtype(np.float64)
VLEN_STR = h5py.string_dtype("utf-8")

ERAS = ("2.1.5", "2.4.0", "2.4.3")
TIME_SERIES_STATES = ("legacy", "moved", "processed")

SPECTRUM_PATH = "Thermo:D:\\data\\sample.RAW"
SPECTRUM_START = datetime(2022, 5, 30, 12, 0, 0)
SPECTRUM_END = datetime(2022, 5, 30, 12, 5, 0)

MZ = np.array([100.0, 101.0, 102.0, 103.0, 104.0])
INTENSITY = np.array([10.0, 1000.0, 5.0, 800.0, 7.0])
NOISE = np.array([1.0, 2.0, 1.5, 2.5, 10.0])
LOD = NOISE * 3.0
# what the 2.4.3-era split stored: signal above the LOD, noise below it
SPLIT_SIGNAL = np.where(INTENSITY > LOD, INTENSITY, 0.0)
SPLIT_NOISE = np.where(INTENSITY > LOD, 0.0, INTENSITY)

TIMES: List[datetime] = [
    datetime(2022, 5, 30, 12, 0, 0),
    datetime(2022, 5, 30, 12, 1, 0),
    datetime(2022, 5, 30, 12, 2, 0),
]
SERIES_INTENSITY = np.array([1.5, 2.5, 3.5])
# per-point apex m/z, recorded from 2.4.3 on
SERIES_POSITIONS = np.array([61.98, 61.99, 62.01])

# (position_min, position_max, legacy tag)
LEGACY_SERIES = [
    (61.9, 62.1, "NO3-"),
    (300.1, 300.2, "300.12345"),
    (100.5, 101.2, "100.50000 - 101.20000"),
]
# (position_min, position_max, formulas as stored by 2.4.3+)
MODERN_SERIES = [
    (61.9, 62.1, "NO3-"),
    (300.1, 300.2, ""),
]

PATH_INFO_DTYPE = np.dtype([
    ("start_time", "<i8"), ("end_time", "<i8"), ("path", VLEN_STR),
    ("polarity", "<i8"), ("average_index", "<i8")])
PATHS_DTYPE = np.dtype([
    ("path", VLEN_STR), ("createDatetime", "<i8"),
    ("startDatetime", "<i8"), ("endDatetime", "<i8")])
# 2.4.3-era PeriodItem: the scan-number columns only arrived in 2.4.4
PERIODS_DTYPE = np.dtype([("start_time", "<i8"), ("end_time", "<i8")])
SPECTRUM_INFO_DTYPE = np.dtype([("start_time", "<i8"), ("end_time", "<i8")])
RAW_PEAK_DTYPE = np.dtype([("mz", VLEN_FLOAT), ("intensity", VLEN_FLOAT)])
FITTED_PEAK_DTYPE = np.dtype([
    ("mz", VLEN_FLOAT), ("intensity", VLEN_FLOAT),
    ("fitted_param", VLEN_FLOAT), ("peak_position", "<f8"),
    ("peak_intensity", "<f8"), ("area", "<f8"),
    ("tags", VLEN_STR), ("formulas", VLEN_STR)])
MASSLIST_DTYPE = np.dtype([("position", "<f8"), ("formulas", VLEN_STR)])
# 2.4.3-era `timeseries_infos` table. Deliberately an independent copy of the
# layout rather than an import from the updater: the fixture has to prove
# compatibility with the historical format, not echo what migration writes.
TIMESERIES_INFOS_DTYPE = np.dtype([
    ("position_min", "<f8"), ("position_max", "<f8"), ("range_sum", "?"),
    ("time_min", "<i8"), ("time_max", "<i8"), ("formulas", VLEN_STR)])
ELEMENT_STATES_DTYPE = np.dtype([
    ("DBE2", "<f8"), ("HMin", "<f8"), ("HMax", "<f8"),
    ("OMin", "<f8"), ("OMax", "<f8")])
ISOTOPE_USABLE_DTYPE = np.dtype([
    ("e_num", "<i8"), ("i_num", "<i8"), ("min", "<i8"), ("max", "<i8"),
    ("global_limit", "?")])

# a small but realistic calculator-settings table (the real default table is
# larger; the migration only has to preserve whatever the file holds)
ELEMENT_STATES = {
    "C": (2.0, 0.0, 2.0, 0.0, 3.0),
    "H": (-1.0, -1.0, -1.0, 0.0, 0.0),
    "O": (0.0, 0.0, 0.0, -1.0, -1.0),
}
ISOTOPE_USABLE = {
    "C": (12, 0, 0, 20, False),
    "C[13]": (12, 13, 0, 3, True),
    "O[18]": (16, 18, 0, 2, True),
}

def _seconds(value: datetime) -> int:
    return np.datetime64(value, "s").astype("int64")


def _times() -> np.ndarray:
    return np.array([_seconds(t) for t in TIMES], dtype=np.int64)


def _row(group: h5py.Group, name: str, rows, dtype, item_name=True):
    dataset = group.create_dataset(name, data=np.array(rows, dtype=dtype))
    if item_name:
        dataset.attrs["item_name"] = "BaseRowItem"
    return dataset


def _write_dict_row(group: h5py.Group, name: str, mapping: dict, dtype):
    rows = [mapping[key] for key in mapping]
    dataset = _row(group, name, rows, dtype)
    dataset.attrs["indexes"] = list(mapping.keys())
    return dataset


def _spectrum(parent: h5py.Group, name: str,
              mz=MZ, intensity=INTENSITY) -> h5py.Group:
    group = parent.create_group(name)
    group.attrs["h5_type"] = "Spectrum"
    group.attrs["path"] = SPECTRUM_PATH
    group.attrs["start_time"] = str(SPECTRUM_START)
    group.attrs["end_time"] = str(SPECTRUM_END)
    group.create_dataset("mz", data=mz)
    group.create_dataset("intensity", data=intensity)
    return group


def _fitted_peak_row() -> list:
    return [(
        np.array([101.0, 102.0]), np.array([800.0, 900.0]),
        np.array([1.0, 0.5, 0.25]), 101.5, 900.0, 450.0, "D", "NO3-")]


class _Layout:
    """
    Writes tab content either in the flat pre-2.4.0 layout (root tab groups
    with an `info` child and a sibling `ui_state`) or in the 2.4.x layout
    (`info/<tab>` groups with `ui_state` inside).
    """

    def __init__(self, f: h5py.File, flat: bool):
        self.f = f
        self.flat = flat
        self.widgets = {}

    def tab(self, root_name: str, underscore_name: str,
            ui_state=True) -> h5py.Group:
        if self.flat:
            widget = self.f.create_group(root_name)
            self.widgets[root_name] = widget
            content = widget.create_group("info")
            if ui_state:
                widget.create_group("ui_state")
        else:
            content = self.f["info"].create_group(underscore_name)
            if ui_state:
                content.create_group("ui_state")
        return content

    def spectra_list_group(self, widget_name: str, name: str) -> h5py.Group:
        # pre-2.4.0 StructureList: children but no `keys` attribute
        return self.widgets[widget_name].create_group(name)


def _write_file_tab(layout: _Layout, era: str):
    tab = layout.tab("file tab", "file_tab")
    tab.attrs["h5_type"] = "file tab"
    tab.attrs["rtol"] = 1e-6
    _row(tab, "spectrum_infos", [
        (_seconds(SPECTRUM_START), _seconds(SPECTRUM_END),
         SPECTRUM_PATH, 1, 0),
        (_seconds(SPECTRUM_START), _seconds(SPECTRUM_END),
         SPECTRUM_PATH, -1, 1),
    ], PATH_INFO_DTYPE)
    pathlist = tab.create_group("pathlist")
    pathlist.attrs["h5_type"] = "PathList"
    _row(pathlist, "paths", [(
        SPECTRUM_PATH, _seconds(SPECTRUM_START),
        _seconds(SPECTRUM_START), _seconds(SPECTRUM_END))], PATHS_DTYPE)
    if era == "2.4.3":
        # written by the app; absent from older files (field default None)
        _row(tab, "periods", [
            (_seconds(SPECTRUM_START), _seconds(SPECTRUM_END))],
            PERIODS_DTYPE)


def _write_spectra_list(layout: _Layout):
    tab = layout.tab("spectra list", "spectra_list")
    tab.attrs["h5_type"] = "spectra list info"
    tab.create_dataset("shown_indexes", data=np.empty(0, np.int32))


def _write_noise_tab(layout: _Layout, era: str):
    tab = layout.tab("noise tab", "noise_tab")
    tab.attrs["h5_type"] = "noise tab"
    tab.attrs["skip"] = False
    tab.attrs["to_be_calibrate"] = True
    _row(tab, "denoised_spectrum_infos", [], PATH_INFO_DTYPE)
    _spectrum(tab, "current_spectrum")
    result = tab.create_group("general_result")
    result.attrs["h5_type"] = "noise general result"
    result.attrs["global_noise_std"] = 2.0
    result.create_dataset("poly_coef", data=np.array([1.0, 2.0]))
    result.create_dataset("noise", data=NOISE)
    result.create_dataset("LOD", data=LOD)
    if era == "2.4.3":
        # only written from 2.4.3 on (and only when the setting was enabled)
        result.create_dataset("spectrum_mz", data=MZ)
        result.create_dataset("spectrum_intensity", data=SPLIT_SIGNAL)
        result.create_dataset("noise_mz", data=MZ)
        result.create_dataset("noise_intensity", data=SPLIT_NOISE)
    if layout.flat:
        raw_spectra = layout.spectra_list_group("noise tab", "raw_spectra")
        _spectrum(raw_spectra, "0")
    else:
        raw_spectra = layout.f["data"].create_group("raw_spectra")
        _spectrum(raw_spectra, "0")
        raw_spectra.attrs["keys"] = [0]


def _write_peak_shape_tab(layout: _Layout):
    tab = layout.tab("peak shape tab", "peak_shape_tab")
    tab.attrs["h5_type"] = "peak shape tab"
    _spectrum(tab, "spectrum")
    manager = tab.create_group("peaks_manager")
    manager.attrs["h5_type"] = "peaks manager structure"
    _row(manager, "peaks", _fitted_peak_row(), FITTED_PEAK_DTYPE)


def _write_calibration_tab(layout: _Layout, era: str):
    tab = layout.tab("calibration tab", "calibration_tab")
    tab.attrs["h5_type"] = "calibrator tab"
    tab.attrs["skip"] = False
    tab.attrs["current_segment_index"] = 0
    tab.attrs["rtol"] = 2e-6

    segment = tab.create_group("calibrate_info_segments").create_group("0")
    segment.attrs["h5_type"] = "calibrator info segment"
    segment.attrs["end_point"] = inf
    segment.attrs["degree"] = 2
    segment.attrs["n_ions"] = 3
    if era != "2.1.5":
        # added in 2.2.4
        segment.attrs["intensity_filter"] = 100
    # segment `rtol` only appeared in 2.4.4: absent from all three eras

    tab.create_group("last_calibrate_info_segments")
    _row(tab, "calibrated_spectrum_infos", [], SPECTRUM_INFO_DTYPE)
    for name in ("path_times", "path_ion_infos", "calibrator_segments"):
        group = tab.create_group(name)
        group.attrs["indexes"] = []

    if layout.flat:
        calibrated = layout.spectra_list_group(
            "calibration tab", "calibrated_spectra")
        _spectrum(calibrated, "0")
    else:
        calibrated = layout.f["data"].create_group("calibrated_spectra")
        _spectrum(calibrated, "0")
        calibrated.attrs["keys"] = [0]


def _write_peak_fit_tab(layout: _Layout):
    tab = layout.tab("peak fit tab", "peak_fit_tab")
    tab.attrs["h5_type"] = "peak fit tab"
    _row(tab, "raw_peaks", [(
        np.array([101.0, 102.0]), np.array([800.0, 900.0]))],
        RAW_PEAK_DTYPE)
    _row(tab, "peaks", _fitted_peak_row(), FITTED_PEAK_DTYPE)
    for name in ("raw_split_num", "original_indexes", "shown_indexes"):
        tab.create_dataset(name, data=np.empty(0, np.int32))
    _spectrum(tab, "spectrum")


def _write_mass_defect_tab(layout: _Layout, flat: bool):
    name = "mass detect tab" if flat else "mass_defect_tab"
    tab = layout.tab(name, name)
    tab.attrs["h5_type"] = "mass defect tab"
    tab.attrs["is_dbe"] = True
    tab.attrs["clr_title"] = ""
    for name in ("clr_x", "clr_y", "clr_size", "clr_color",
                 "gry_x", "gry_y", "gry_size"):
        tab.create_dataset(name, data=np.empty(0, float))


def _write_legacy_series(group: h5py.Group):
    for index, (position_min, position_max, tag) in enumerate(LEGACY_SERIES):
        series = group.create_group(str(index))
        series.attrs["h5_type"] = "time series"
        series.attrs["position_min"] = position_min
        series.attrs["position_max"] = position_max
        series.attrs["tag"] = tag
        series.create_dataset("times", data=_times())
        series.create_dataset("intensity", data=SERIES_INTENSITY)
    group.attrs["keys"] = list(range(len(LEGACY_SERIES)))


def _write_243_series(group: h5py.Group):
    for index, (position_min, position_max, formulas) in enumerate(
            MODERN_SERIES):
        series = group.create_group(str(index))
        series.attrs["h5_type"] = "time series"
        series.attrs["position_min"] = position_min
        series.attrs["position_max"] = position_max
        series.attrs["range_sum"] = False
        series.attrs["formulas"] = formulas
        series.create_dataset("times", data=_times())
        series.create_dataset("positions", data=SERIES_POSITIONS)
        series.create_dataset("intensity", data=SERIES_INTENSITY)
    group.attrs["keys"] = list(range(len(MODERN_SERIES)))


def _write_time_series_tab(layout: _Layout, era: str, state: str):
    tab = layout.tab("time series tab", "time_series_tab")
    tab.attrs["h5_type"] = "timeseries tab"
    tab.attrs["show_index"] = -1

    if era == "2.4.3":
        _write_243_series(layout.f["data"].create_group("time_series"))
        rows = [
            (position_min, position_max, False, _seconds(TIMES[0]),
             _seconds(TIMES[-1]), formulas)
            for position_min, position_max, formulas in MODERN_SERIES]
        _row(tab, "timeseries_infos", rows, TIMESERIES_INFOS_DTYPE)
        return

    if state == "legacy":
        _write_legacy_series(tab.create_group("series"))
        return

    # a half-migrated copy: the 2.4.3 updater already moved the series (and,
    # for "processed", already normalized them) but the chain crashed later
    target = layout.f["data"].create_group("time_series")
    _write_legacy_series(target)
    if state == "processed":
        for key in map(str, range(len(LEGACY_SERIES))):
            series = target[key]
            series.create_dataset(
                "positions", data=np.full(len(TIMES), np.nan))
            series.attrs["range_sum"] = False
            tag = str(series.attrs.pop("tag"))
            if tag == "NO3-":
                series.attrs["formulas"] = tag


def _write_formula_docker(layout: _Layout, era: str):
    tab = layout.tab("formula docker", "formula_docker")
    tab.attrs["h5_type"] = "formula docker"
    tab.attrs["mz_min"] = 50.0
    tab.attrs["mz_max"] = 750.0
    if era == "2.1.5":
        # `calc_gen` only appeared in 2.3.0; before that the workspace stored
        # a restricted/force calculator pair instead
        tab.attrs["rtol"] = 1e-6
        tab.create_group("restricted_calc")
        tab.create_group("force_calc")
        return
    tab.attrs["charge"] = -1
    calc = tab.create_group("calc_gen")
    calc.attrs["h5_type"] = "calculator generator"
    calc.attrs["rtol"] = 1e-6
    calc.attrs["DBEMin"] = 0.0
    calc.attrs["DBEMax"] = 8.0
    calc.attrs["nitrogen_rule"] = True
    calc.attrs["global_limit"] = 3
    calc.attrs["dbe_limit"] = True
    calc.attrs["debug"] = False
    _write_dict_row(calc, "element_states", ELEMENT_STATES,
                    ELEMENT_STATES_DTYPE)
    _write_dict_row(calc, "isotope_usable", ISOTOPE_USABLE,
                    ISOTOPE_USABLE_DTYPE)


def _write_masslist_docker(layout: _Layout):
    tab = layout.tab("masslist docker", "masslist_docker")
    tab.attrs["h5_type"] = "mass list docker"
    tab.attrs["rtol"] = 1e-6
    _row(tab, "masslist", [], MASSLIST_DTYPE)


def _write_peaklist_docker(layout: _Layout):
    # a plain BaseStructure: the 2.4.x layout has no ui_state for it
    layout.tab("peaklist docker", "peaklist_docker",
               ui_state=layout.flat)


def _write_spectrum_docker(layout: _Layout, era: str):
    tab = layout.tab("spectrum docker", "spectrum_docker")
    tab.attrs["h5_type"] = "spectrum docker"
    if era == "2.4.0":
        _spectrum(tab, "spectrum")
    # 2.4.3: the panel was never opened, so no spectrum group exists


def build(path, era: str, time_series_state: str = "legacy"):
    """
    Write a workspace file in the given legacy layout.

    ``time_series_state`` only matters for pre-2.4.3 eras: ``"legacy"`` keeps
    the series where the old app stored them, while ``"moved"``/``"processed"``
    reproduce the states a crashed migration run leaves behind.
    """
    assert era in ERAS, era
    assert time_series_state in TIME_SERIES_STATES, time_series_state
    if era == "2.4.3":
        assert time_series_state == "legacy"
    if time_series_state != "legacy":
        # a half-migrated copy has already gone through the 2.4.0 renamer, so
        # it cannot still be in the flat layout
        assert era == "2.4.0"

    flat = era == "2.1.5"
    with h5py.File(path, "w") as f:
        info = f.create_group("info")
        info.attrs["h5_type"] = "workspace info"
        info.attrs["version"] = era

        layout = _Layout(f, flat)
        if not flat:
            f.create_group("data")

        _write_file_tab(layout, era)
        _write_spectra_list(layout)
        _write_noise_tab(layout, era)
        _write_peak_shape_tab(layout)
        _write_calibration_tab(layout, era)
        _write_peak_fit_tab(layout)
        _write_mass_defect_tab(layout, flat)
        _write_time_series_tab(layout, era, time_series_state)
        _write_formula_docker(layout, era)
        _write_masslist_docker(layout)
        _write_peaklist_docker(layout)
        if not flat:
            _write_spectrum_docker(layout, era)


def use_scan_number_periods(path, start_num: int, end_num: int):
    """
    Rewrite the periods table the way 2.4.4/2.4.5 did, and stamp 2.4.5.

    Those releases added the scan-number columns `start_num`/`end_num`
    (`54c85e5`); the model later renamed `end_num` to `stop_num`, which is the
    rename the migration has to carry across.
    """
    with h5py.File(path, "r+") as f:
        dataset = f["info/file_tab/periods"]
        data = dataset[()]
        dtype = np.dtype([
            ("start_time", "<i8"), ("end_time", "<i8"),
            ("start_num", "<i8"), ("end_num", "<i8")])
        rows = np.zeros(len(data), dtype=dtype)
        for name in ("start_time", "end_time"):
            rows[name] = data[name]
        rows["start_num"] = start_num
        rows["end_num"] = end_num

        attrs = dict(dataset.attrs.items())
        del f["info/file_tab/periods"]
        dataset = f["info/file_tab"].create_dataset("periods", data=rows)
        for key, value in attrs.items():
            dataset.attrs[key] = value
        f["info"].attrs["version"] = "2.4.5"
