from array import array
from datetime import datetime, timedelta

from PySide6 import QtWidgets

from ...models.timeseries import TimeSeries
from ..MainUiPy import Window

# one QApplication for the whole session, alive until interpreter exit:
# destroying it mid-suite while Qt objects still exist crashes the next test
_app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def _series(position: float) -> TimeSeries:
    start = datetime(2024, 1, 1, 12)
    return TimeSeries(
        position_min=position - 0.1, position_max=position + 0.1,
        times=[start, start + timedelta(minutes=1)],
        positions=array("d", [position, position]),
        intensity=array("d", [1.0, 2.0]))


def test_restore_syncs_legacy_infos_without_error():
    # a migrated workspace opens with an empty timeseries_infos table;
    # restore must sync the infos without raising (the old docker table used
    # to raise IndexError here)
    window = Window()
    try:
        workspace = window.manager.workspace
        for i in range(5):
            workspace.data.time_series.append(_series(100.0 + i))
        info = workspace.info.time_series_tab
        assert info.timeseries_infos == []

        window.timeseriesesTab.restore()

        assert len(info.timeseries_infos) == 5
        assert window.timeseriesesTab.ui.tableWidget.rowCount() == 5
    finally:
        window.close()
