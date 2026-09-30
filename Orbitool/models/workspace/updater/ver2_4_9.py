"""
Pre-2.5.0 layout normalizer.

The registered version "2.4.9" is a SEQUENCING ANCHOR, NOT A REAL RELEASE.
Updater selection picks the first registered version strictly greater than the
version stamped in the file, so anchoring here makes this updater run
immediately before the shared 2.5.0 migration for every workspace older than
2.5.0 -- including 2.4.3-2.4.5 files, which the strictly-newer-than selection
never routes through the 2.4.3 updater.

Everything in here is guarded by existence checks, so re-running it over an
already normalized copy is a no-op. The shared 2.5.0/2.5.2/2.5.3 updaters are
left untouched.
"""
from datetime import datetime
from typing import Sequence, Tuple, Type

import h5py
import numpy as np

from Orbitool.base.extra_type_handlers.column_handler import (
    get_handler as get_column_handler)
from Orbitool.models.formula import ElementState, IsotopeNum
from Orbitool.models.workspace.calibration import CalibratorInfoSegment
from Orbitool.models.workspace.formula import Factory as calc_gen_factory

from .utils import write_to

# sentinel for "no spectrum was ever shown in the spectrum docker"
EMPTY_DATETIME = datetime(1900, 1, 1)

# exactly the five attributes ver2_5_0 reads back from every calibration segment
CALIBRATION_SEGMENT_FIELDS = ("end_point", "intensity_filter",
                              "degree", "n_ions", "rtol")
CALC_GEN_SCALAR_FIELDS = ("rtol", "DBEMin", "DBEMax", "nitrogen_rule",
                          "global_limit", "dbe_limit", "debug")


def _row_columns(model) -> Tuple[Tuple[str, Type], ...]:
    """
    Column layout of a pre-2.5.0 DictRow dataset.

    Derived from the modern row model through the same column handlers the
    current serializer uses, so the names cannot drift from the fields
    ver2_5_0 reads back by name.
    """
    columns = []
    for name, field in model.model_fields.items():
        handler = get_column_handler(field.annotation)
        assert handler is not None, (
            f"no column handler for {model.__name__}.{name}")
        columns.append((name, handler.dtype))
    return tuple(columns)


ELEMENT_STATES_COLUMNS = _row_columns(ElementState)
ISOTOPE_USABLE_COLUMNS = _row_columns(IsotopeNum)


def _fill_calibration_segments(tab: h5py.Group):
    """Segments written before `intensity_filter`/`rtol` existed get the
    modern model's defaults, so the 2.5.0 converter finds every field."""
    defaults = CalibratorInfoSegment()
    for name in ("calibrate_info_segments", "last_calibrate_info_segments"):
        if name not in tab:
            continue
        segments = tab[name]
        if not isinstance(segments, h5py.Group):
            raise ValueError(
                f"unrecognizable workspace: '{segments.name}' is not a group")
        for segment in segments.values():
            if not isinstance(segment, h5py.Group):
                raise ValueError(
                    f"unrecognizable calibration segment '{segment.name}': "
                    "not a group")
            for field in CALIBRATION_SEGMENT_FIELDS:
                if field not in segment.attrs:
                    segment.attrs[field] = getattr(defaults, field)


def _rebuild_dataset(group: h5py.Group, name: str, data: np.ndarray):
    """
    Replace `group[name]` with a dataset holding `data`, keeping the original
    attributes. HDF5 cannot change a column's dtype or name in place, so both
    are rewritten through this one path.
    """
    attrs = dict(group[name].attrs.items())
    del group[name]
    dataset = group.create_dataset(name, data=data)
    for key, value in attrs.items():
        dataset.attrs[key] = value
    return dataset


def _assure_periods(file_tab: h5py.Group):
    """
    Two gaps around the custom-periods table:

    - workspaces saved before the feature have no table at all, while the
      2.5.0 converter multiplies its time columns unconditionally;
    - 2.4.4/2.4.5 named the scan-number column `end_num`, which the model
      renamed to `stop_num` before 2.5.0. `ver2_5_0` never carries the values
      across, so they would be read back as the -1 default -- a silent loss.
    """
    if "periods" not in file_tab:
        dtype = np.dtype([("start_time", "<i8"), ("end_time", "<i8"),
                          ("start_num", "<i8"), ("stop_num", "<i8")])
        file_tab.create_dataset("periods", shape=(0,), dtype=dtype)
        return

    dataset = file_tab["periods"]
    names = dataset.dtype.names or ()
    if "end_num" not in names or "stop_num" in names:
        return
    data = dataset[()]
    columns = {name: "stop_num" if name == "end_num" else name
               for name in names}
    dtype = np.dtype([(columns[name], dataset.dtype[name]) for name in names])
    new_data = np.empty(len(data), dtype=dtype)
    for name in names:
        new_data[columns[name]] = data[name]
    _rebuild_dataset(file_tab, "periods", new_data)


def _write_legacy_dict_row(group: h5py.Group, key: str, mapping: dict,
                           columns: Sequence[Tuple[str, Type]]):
    """
    Pre-2.5.0 DictRow layout: a dataset whose rows are the mapping values and
    whose `indexes` attribute holds the mapping keys. The shared 2.5.0
    converter rewrites it into the modern `_key_index` layout.
    """
    dtype = np.dtype([(name, typ) for name, typ in columns])
    rows = [tuple(getattr(mapping[k], name) for name, _ in columns)
            for k in mapping]
    dataset = group.create_dataset(key, data=np.array(rows, dtype=dtype))
    dataset.attrs["indexes"] = list(map(str, mapping.keys()))
    dataset.attrs["item_name"] = "BaseRowItem"


def _assure_calc_gen(formula_docker: h5py.Group):
    """Workspaces predating the calculator settings group get the default
    tables, so the formula tab opens."""
    if "calc_gen" in formula_docker:
        return
    calc = calc_gen_factory()
    group = formula_docker.create_group("calc_gen")
    group.attrs["h5_type"] = "calculator generator"
    for name in CALC_GEN_SCALAR_FIELDS:
        group.attrs[name] = getattr(calc, name)
    _write_legacy_dict_row(
        group, "element_states", calc.element_states, ELEMENT_STATES_COLUMNS)
    _write_legacy_dict_row(
        group, "isotope_usable", calc.isotope_usable, ISOTOPE_USABLE_COLUMNS)


def _assure_noise_splits(noise_tab: h5py.Group):
    """
    Workspaces older than 2.4.3 never stored the noise/signal split arrays the
    2.5.0 converter requires. Rebuild them from the stored current spectrum
    and the stored per-point noise array: the spectrum replays as the signal
    side, the noise array replays as the noise side, both over the same m/z
    axis (the two arrays have the same length, verified against real files).
    """
    if "general_result" not in noise_tab:
        return
    result = noise_tab["general_result"]
    if "spectrum_mz" in result or "spectrum_split" in result:
        return

    current = noise_tab.get("current_spectrum")
    if not isinstance(current, h5py.Group):
        raise ValueError(
            "cannot rebuild the noise/signal split: "
            "info/noise_tab/current_spectrum is missing or not a group")
    if "noise" not in result:
        raise ValueError(
            "cannot rebuild the noise/signal split: "
            "info/noise_tab/general_result has no 'noise' array")
    for name in ("mz", "intensity"):
        if not isinstance(current.get(name), h5py.Dataset):
            raise ValueError(
                "cannot rebuild the noise/signal split: "
                f"current_spectrum has no '{name}' dataset")

    mz = current["mz"][()]
    intensity = current["intensity"][()]
    noise = result["noise"][()]
    if not (len(mz) == len(intensity) == len(noise)):
        raise ValueError(
            "cannot rebuild the noise/signal split: current spectrum and noise "
            f"array lengths differ ({len(mz)}, {len(intensity)}, {len(noise)})")

    write_to(result, "spectrum_mz", mz)
    write_to(result, "spectrum_intensity", intensity)
    write_to(result, "noise_mz", mz)
    write_to(result, "noise_intensity", noise)


def _rename_mass_detect_tab(f_info: h5py.Group):
    """The 2.4.0-era renamer produces `mass_detect_tab` for pre-2.4.0
    workspaces; the current model field is `mass_defect_tab`."""
    legacy = "mass_detect_tab"
    if legacy in f_info and "mass_defect_tab" not in f_info:
        f_info.move(legacy, "mass_defect_tab")


def _assure_spectrum(spectrum_docker: h5py.Group):
    """A workspace whose spectrum panel was never opened has no spectrum
    group; the 2.5.0 converter reads it unconditionally. An empty spectrum
    with the attributes the model requires degrades to an empty value instead
    of a broken entry."""
    if "spectrum" in spectrum_docker:
        return
    group = spectrum_docker.create_group("spectrum")
    group.attrs["h5_type"] = "Spectrum"
    group.attrs["path"] = ""
    group.attrs["start_time"] = str(EMPTY_DATETIME)
    group.attrs["end_time"] = str(EMPTY_DATETIME)
    group.create_dataset("mz", data=np.empty(0, float))
    group.create_dataset("intensity", data=np.empty(0, float))


def _assure_fixed_width_paths(file_tab: h5py.Group):
    """
    Old files store the spectrum-info `path` column as HDF5 variable-length
    strings; the 2.5.2 migration copies that dtype into a new compound dtype,
    which is only constructible for fixed-width bytes. Convert first (this is
    what the historical flow only avoided via an intermediate save).
    """
    if "spectrum_infos" not in file_tab:
        return
    dataset = file_tab["spectrum_infos"]
    names = dataset.dtype.names
    if names is None or "path" not in names:
        return
    if dataset.dtype["path"].char != "O":
        return

    data = dataset[()]
    paths = data["path"]
    if len(paths):
        converted = np.array([
            p if isinstance(p, bytes) else str(p).encode("utf-8")
            for p in paths])
    else:
        converted = np.empty(0, dtype="S1")
    dtype = np.dtype([
        (name, converted.dtype if name == "path" else dataset.dtype[name])
        for name in names])
    new_data = np.empty(len(data), dtype=dtype)
    for name in names:
        new_data[name] = converted if name == "path" else data[name]
    _rebuild_dataset(file_tab, "spectrum_infos", new_data)


def _fill_file_tab(file_tab: h5py.Group):
    _assure_periods(file_tab)
    _assure_fixed_width_paths(file_tab)


#: (tab name, filler); every filler is existence-guarded and idempotent
TAB_FILLERS = (
    ("calibration_tab", _fill_calibration_segments),
    ("file_tab", _fill_file_tab),
    ("formula_docker", _assure_calc_gen),
    ("noise_tab", _assure_noise_splits),
    ("spectrum_docker", _assure_spectrum),
)


def update(f: h5py.File):
    """
    to 2.4.9 (sequencing anchor, not a real release)

    Fill in everything the shared 2.5.0 converter requires but files older
    than 2.5.0 may lack.
    """
    if "info" not in f:
        raise ValueError("unrecognizable workspace: missing 'info' group")
    f_info = f["info"]

    for name, filler in TAB_FILLERS:
        if name in f_info:
            filler(f_info[name])
    # the rename acts on `info` itself, so it sits outside the table
    _rename_mass_detect_tab(f_info)
