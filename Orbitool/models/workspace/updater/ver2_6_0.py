import h5py

from .utils import delete


def update(f: h5py.File):
    """
    to 2.6.0

    Drop the workspace state that no longer has a UI: the spectrum docker
    panel, the mass-defect tab (its windows are now independent and
    unpersisted) and the time-series tab's selected-row index.
    """
    info = f["info"]
    delete(info, "spectrum_docker")
    delete(info, "mass_defect_tab")
    tab = info.get("time_series_tab")
    if tab is not None and "show_index" in tab.attrs:
        del tab.attrs["show_index"]
