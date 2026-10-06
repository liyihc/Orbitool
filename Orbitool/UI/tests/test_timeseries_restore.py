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


def test_show_series_after_legacy_migration():
    # a migrated workspace opens with an empty timeseries_infos table and a
    # show_index saved by the old version; restore used to raise IndexError
    window = Window()
    try:
        workspace = window.manager.workspace
        for i in range(5):
            workspace.data.time_series.append(_series(100.0 + i))
        info = workspace.info.time_series_tab
        info.show_index = 2
        assert info.timeseries_infos == []

        window.timeseries.restore()

        assert len(info.timeseries_infos) == 5
        assert info.show_index == 2
        assert window.timeseries.ui.tableWidget.rowCount() == 2
        assert window.timeseries.ui.tableWidget.item(0, 1) is not None
    finally:
        window.close()
