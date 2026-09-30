from typing import Optional

import h5py
import numpy as np

from Orbitool.models.formula import Formula

from .utils import create_group, move_to

# columns of the empty `timeseries_infos` table, matching the modern
# TimeSeriesInfoRow. The time-series UI rebuilds the rows from the migrated
# series on every workspace open, so migration never hand-encodes row data.
TIMESERIES_INFOS_DTYPE = np.dtype([
    ("position_min", "<f8"),
    ("position_max", "<f8"),
    ("range_sum", "?"),
    ("time_min", "<i8"),
    ("time_max", "<i8"),
    ("formulas", h5py.string_dtype("utf-8")),
])


def _formula_name(tag) -> Optional[str]:
    """
    Convert a legacy series `tag` into a formula name, or None to discard it.

    Modern formula parsing accepts charge suffixes and isotopes, so a tag that
    parses is a real formula name -- including charged ones, which the legacy
    ``"-" in tag`` rule threw away. The tags that fail to parse are numeric
    position labels and m/z range strings (the only other shapes the old UI
    could write) and fall back to the legacy discard rules: that information
    is reconstructible from the position bounds, which the time-series table
    already displays.

    Legacy's "looks like a neutral formula" branch (uppercase, no space) is
    deliberately not reproduced: keeping an unparsed string would only hand
    the modern reader a formula it cannot parse, i.e. a broken entry.
    """
    text = str(tag).strip()
    if not text:
        return None
    try:
        Formula(text)
    except Exception:
        return None
    return text


def _fill_series(series: h5py.Group):
    """
    Normalize one pre-2.4.3 series group into the layout the 2.5.0 converter
    expects. Every step is guarded, so a half-migrated copy can be re-run.
    """
    if not isinstance(series, h5py.Group):
        raise ValueError(
            f"unrecognizable time series entry '{series.name}': not a group")
    for name in ("times", "intensity"):
        if not isinstance(series.get(name), h5py.Dataset):
            raise ValueError(
                f"unrecognizable time series entry '{series.name}': "
                f"missing '{name}' dataset")

    if "positions" not in series:
        # per-point m/z values were never recorded before 2.4.3. NaN marks the
        # absence honestly instead of fabricating numbers.
        series.create_dataset(
            "positions", data=np.full(len(series["times"]), np.nan))
    if "range_sum" not in series.attrs:
        series.attrs["range_sum"] = False
    if "tag" in series.attrs:
        if "formulas" not in series.attrs:
            name = _formula_name(series.attrs["tag"])
            if name is not None:
                series.attrs["formulas"] = name
        del series.attrs["tag"]


def _assure_timeseries_infos(tab: h5py.Group):
    if "timeseries_infos" not in tab:
        tab.create_dataset(
            "timeseries_infos", shape=(0,), dtype=TIMESERIES_INFOS_DTYPE)


def _never_held_series(tab: h5py.Group) -> bool:
    """
    The 2.4.0 renamer creates `info/time_series_tab` (with an empty ui_state)
    for workspaces written before the time-series tab existed; such a tab
    carries no attributes at all. Any other tab without a series group cannot
    be interpreted and must not be migrated silently.
    """
    return not tab.attrs and set(tab.keys()) <= {"ui_state"}


def update(f: h5py.File):
    """
    to 2.4.3

    Move `info/time_series_tab/series` to `data/time_series` and rewrite each
    series in the layout the shared 2.5.0 converter expects.
    """
    tab_path = "info/time_series_tab"
    source = f"{tab_path}/series"
    target = "data/time_series"

    if tab_path not in f:
        raise ValueError(
            f"unrecognizable workspace: '{tab_path}' does not exist")
    if not isinstance(f[tab_path], h5py.Group):
        raise ValueError(f"unrecognizable workspace: '{tab_path}' is not a group")
    tab = f[tab_path]

    if source in f:
        if target in f:
            raise ValueError(
                f"unrecognizable workspace: both '{source}' and '{target}' "
                "hold time series")
        if not isinstance(f[source], h5py.Group):
            raise ValueError(f"unrecognizable workspace: '{source}' is not a group")
        move_to(f, source, target)
    elif target not in f:
        if _never_held_series(tab):
            # workspace predating the time-series feature: nothing to migrate
            create_group(f, target, 'a')
        else:
            raise ValueError(
                f"unrecognizable workspace: neither '{source}' nor '{target}' "
                "holds time series")

    group: h5py.Group = f[target]
    try:
        keys = sorted(int(key) for key in group.keys())
    except ValueError as e:
        raise ValueError(
            f"unrecognizable time series entries in '{target}': "
            f"{sorted(group.keys())}") from e

    for key in keys:
        _fill_series(group[str(key)])
    group.attrs["keys"] = keys

    _assure_timeseries_infos(tab)
