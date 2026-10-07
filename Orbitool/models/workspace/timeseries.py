from typing import List, Union
from datetime import datetime, timedelta

from Orbitool.base import BaseRowStructure
from Orbitool.base.disk_structure import IDiskListView
from ..formula import FormulaList
from ..timeseries import TimeSeries
from .base import BaseInfo

validated_datetime = datetime(1900, 1, 1)
invalid_datetime = validated_datetime - timedelta(1000)

class TimeSeriesInfoRow(BaseRowStructure):
    position_min: float
    position_max: float
    # 0.0 = no tolerance recorded; copied from TimeSeries, defaults for old files
    rtol: float = 0.0
    range_sum: bool = False
    time_min: datetime = invalid_datetime
    time_max: datetime = invalid_datetime
    formulas: FormulaList = []

    @classmethod
    def FromTimeSeries(cls, timeseries: TimeSeries):
        return cls(
            position_min=timeseries.position_min,
            position_max=timeseries.position_max,
            rtol=timeseries.rtol,
            range_sum=timeseries.range_sum,
            time_min=timeseries.times[0] if timeseries.times else invalid_datetime,
            time_max=timeseries.times[-1] if timeseries.times else invalid_datetime,
            formulas=timeseries.formulas
        )
    
    def valid(self):
        return self.time_min > validated_datetime

    def get_name(self):
        if self.formulas:
            name = ','.join(str(f) for f in self.formulas)
        elif self.range_sum:
            return f"{self.position_min:.2f}-{self.position_max:.2f}"
        else:
            name = format((self.position_min + self.position_max) / 2, '.5f')
        # range_sum returned above: only tolerance-windowed series get ppm
        if self.rtol > 0:
            ppm = f"{self.rtol * 1e6:.2f}".rstrip('0').rstrip('.')
            name = f"{name} {ppm}ppm"
        return name


class TimeseriesInfo(BaseInfo):
    timeseries_infos: List[TimeSeriesInfoRow] = []

    def sync(self, time_series: Union[List[TimeSeries], IDiskListView[TimeSeries]]):
        if len(self.timeseries_infos) != len(time_series):
            self.timeseries_infos = [
                TimeSeriesInfoRow.FromTimeSeries(s) for s in time_series]
