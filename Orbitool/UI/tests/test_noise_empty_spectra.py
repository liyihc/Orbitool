"""Empty-spectrum feedback on the Noise tab.

Reading the selected spectrum can produce nothing for three different reasons,
and the tab must name the right one: the spectra list was never built, the
filter excluded every scan, or the scans were all damaged -- the last is left
to the damaged-file report, which already says which files and scans.

The read path is stubbed, so no `.RAW` is needed.
"""
import importlib
from datetime import datetime, timedelta

import pytest

from ...models.file import FileSpectrumInfo
# debug_settings is an autouse fixture re-exported for pytest
from .migration_harness import MigrationEnv, debug_settings  # noqa: F401

noise_module = importlib.import_module("Orbitool.UI.NoiseUiPy")

START = datetime(2024, 1, 1, 12)
END = START + timedelta(minutes=1)


def _info():
    return FileSpectrumInfo(
        start_time=START, end_time=END, path="Thermo:C:/data/a.raw",
        filter={}, stats_filter={}, average_index=0)


@pytest.fixture
def env(request):
    state = MigrationEnv().build(request, extra_dialog_modules=(noise_module,))
    state.reset()
    state.window.manager.getters.spectra_list_selected_index.connect(lambda: 0)
    yield state


def test_a_missing_spectra_list_names_the_file_tab_step(env):
    env.window.manager.workspace.info.file_tab.spectrum_infos = []

    env.window.noiseTab.showSelectedSpectrum()

    assert env.dialogs == [(
        'Build the list first: File tab → "All file(s)".', "No spectra list")]


def test_a_selection_past_the_list_falls_back_to_the_same_hint(env):
    env.window.manager.workspace.info.file_tab.spectrum_infos = [_info()]
    env.window.manager.getters.spectra_list_selected_index.connect(lambda: 5)

    env.window.noiseTab.showSelectedSpectrum()

    assert env.dialogs == [(
        'Build the list first: File tab → "All file(s)".', "No spectra list")]


def test_a_window_whose_scans_are_all_filtered_out_says_so(env, monkeypatch):
    env.window.manager.workspace.info.file_tab.spectrum_infos = [_info()]
    monkeypatch.setattr(FileSpectrumInfo, "get_spectrum_from_info",
                        lambda self, *a, **k: (None, None))

    env.window.noiseTab.showSelectedSpectrum()

    assert env.dialogs == [(
        "Every scan here is excluded by the filter."
        " Adjust it on the File tab and rebuild.",
        "No spectra in this window")]


def test_a_window_lost_to_damage_only_reports_the_damage(env, monkeypatch):
    env.window.manager.workspace.info.file_tab.spectrum_infos = [_info()]

    def read(self, *a, **k):
        k["damaged"].setdefault(self.path, {}).update({3: "no FT profile data"})
        return None, None

    monkeypatch.setattr(FileSpectrumInfo, "get_spectrum_from_info", read)

    env.window.noiseTab.showSelectedSpectrum()

    assert [cap for _, cap in env.dialogs] == ["Damaged .RAW files"]
