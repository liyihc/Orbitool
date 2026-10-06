from datetime import datetime, timedelta
from multiprocessing import cpu_count
from typing import List, Literal, Set
import weakref
from pydantic import BaseModel, Field
from paths import CONFIG_PATH, LEGACY_CONFIG_PATH, RESOURCE_PATH, ROOT_PATH
from .version import VERSION


class TempFile:
    prefixTimeFormat = r"orbitool_%Y%m%d%H%M%S_"
    tempPath = None


config_path = CONFIG_PATH

multi_cores = cpu_count() - 1
if multi_cores < 1:
    multi_cores = 1


class General(BaseModel):
    default_select: bool = True
    color_scheme: Literal["system", "light", "dark"] = "light"
    time_format: str = r"%Y-%m-%d %H:%M:%S"
    export_time_format: str = r"%Y%m%d_%H%M%S"
    multi_cores: int = multi_cores


class File(BaseModel):
    dotnet_driver: Literal[".net framework", ".net core"] = ".net framework"


class Denoise(BaseModel):
    plot_noise_in_diff_color: bool = True
    noise_formulas: List[str] = ["NO3-", "HNO3NO3-"]


class Calibration(BaseModel):
    dragdrop_ion_replace: bool = False

class Peakfit(BaseModel):
    plot_show_formulas: int = 5

class TimeSeries(BaseModel):
    mz_sum_target: Literal["peak_intensity", "area"] = "peak_intensity"
    mz_sum_func: Literal["nofit", "norm"] = "nofit"

    export_time_formats: Set[Literal[
        "iso", "igor", "matlab", "excel"]] = {"iso"}


class Debug(BaseModel):
    thread_block_gui: bool = False
    NO_MULTIPROCESS: bool = False


class _Setting(BaseModel):
    general: General = General()
    file: File = File()
    denoise: Denoise = Denoise()
    calibration: Calibration = Calibration()
    peakfit: Peakfit = Peakfit()
    timeseries: TimeSeries = TimeSeries()

    debug: Debug = Debug()

    test_timeout: int = 1
    # directory scanned by Orbitool/UI/tests; empty -> <repo parent>/data
    test_data_path: str = ""
    time_delta: timedelta = timedelta(seconds=1)

    plot_refresh_interval: float = 1

    version: str = VERSION

    def load_setting(self):
        """Read setting.json into this object, if it exists.

        A pre-PyInstaller-6-layout build wrote setting.json inside `_internal`
        (the then-ROOT_PATH); if the file is missing at its new home next to the
        exe, fall back to that legacy copy. ``save_setting`` then persists it in
        the new location, completing the migration.
        """
        source = config_path
        if (not source.exists() and LEGACY_CONFIG_PATH is not None
                and LEGACY_CONFIG_PATH.exists()):
            source = LEGACY_CONFIG_PATH
        if source.exists():
            self.update_from(self.model_validate_json(source.read_text()))

    def save_setting(self):
        config_path.write_text(self.model_dump_json(indent=4))

    def apply_color_scheme(self, app):
        from PySide6 import QtCore
        schemes = {
            "system": QtCore.Qt.ColorScheme.Unknown,
            "light": QtCore.Qt.ColorScheme.Light,
            "dark": QtCore.Qt.ColorScheme.Dark,
        }
        app.styleHints().setColorScheme(schemes[self.general.color_scheme])

    def update_from(self, new_config: "_Setting"):
        for key in type(new_config).model_fields.keys():
            setattr(self, key, getattr(new_config, key))

    def format_time(self, dt: datetime):
        return dt.strftime(self.general.time_format)
    
    def parse_time(self, s: str):
        return datetime.strptime(s,self.general.time_format)

    def format_export_time(self, dt: datetime):
        return dt.strftime(self.general.export_time_format)

    def parse_export_time(self, s: str):
        return datetime.strptime(s,self.general.export_time_format)

    def get_global_var(self, key: str, default=None):
        if key in vars:
            try:
                return vars[key]()
            except:
                pass
        return default

    def pop_global_var(self, key: str, default=None):
        if key in vars:
            try:
                return vars.pop(key)()
            except:
                pass
        return default

    def set_global_var(self, key: str, variable):
        vars[key] = weakref.ref(variable)

    def get_global_val(self, key: str, default=None):
        return vals.get(key, default)

    def pop_global_val(self, key: str, default=None):
        return vals.pop(key, default)

    def set_global_val(self, key: str, value):
        vals[key] = value

vars = {}
vals = {}

setting = _Setting()
