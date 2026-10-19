from .workspace import WorkSpace
from ...version import VERSION
from . import noise_tab, spectra_list, base
from .base import UiNameGetter, UiState
from .ui_state_handlers import init_handlers

init_handlers()

from .updater import update, need_update, get_version
