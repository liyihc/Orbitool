"""Workspace open prompts: the too-new refusal and the pre-upgrade explanation.

Two prompts sit on top of `updater`'s version checks, both exercised through the
real `Window` so the whole `_load_workspace` path runs. An older workspace must
be explained before it is copied and migrated, and the user can cancel; a
workspace from a newer build is refused outright. The dialogs are recorded rather
than shown.
"""
import importlib

import h5py
import pytest

# debug_settings is an autouse fixture re-exported for pytest
from .migration_harness import (  # noqa: F401
    MigrationEnv, debug_settings)

main_module = importlib.import_module("Orbitool.UI.MainUiPy")
ui_utils = importlib.import_module("Orbitool.UI.utils")


def _write_version(path, version):
    with h5py.File(path, "w") as f:
        f.create_group("info").attrs["version"] = version


@pytest.fixture(scope="module")
def env(request):
    return MigrationEnv().build(request)


def test_too_new_workspace_is_refused(env, tmp_path, monkeypatch):
    path = tmp_path / "future.Orbitool"
    _write_version(path, "99.0.0")
    dialogs = []
    monkeypatch.setattr(
        ui_utils, "showInfo",
        lambda content, cap=None: dialogs.append((content, cap)))
    saves = []
    monkeypatch.setattr(
        ui_utils, "savefile",
        lambda *a, **k: saves.append((a, k)) or (False, ""))
    before = env.window.manager.workspace

    env.window._load_workspace(str(path))

    assert len(dialogs) == 1
    content, cap = dialogs[0]
    assert "99.0.0" in content
    assert saves == []                        # never offered an upgrade
    assert env.window.manager.workspace is before


def test_old_workspace_cancel_aborts_before_saving(env, tmp_path, monkeypatch):
    path = tmp_path / "old.Orbitool"
    _write_version(path, "1.0.0")
    asked = []
    monkeypatch.setattr(
        ui_utils, "confirm",
        lambda content, cap=None, accept=None, reject=None:
        asked.append((content, cap, accept, reject)) or False)
    saves = []
    monkeypatch.setattr(
        ui_utils, "savefile",
        lambda *a, **k: saves.append((a, k)) or (False, ""))
    before = env.window.manager.workspace

    env.window._load_workspace(str(path))

    assert len(asked) == 1
    content, cap, accept, reject = asked[0]
    assert "1.0.0" in content
    assert accept == "Upgrade and Save…"
    assert saves == []                        # cancel means no save dialog
    assert env.window.manager.workspace is before


def test_old_workspace_confirm_prefills_name_and_prompts_save(env, tmp_path, monkeypatch):
    path = tmp_path / "old.Orbitool"
    _write_version(path, "1.0.0")
    monkeypatch.setattr(ui_utils, "confirm", lambda *a, **k: True)
    saves = []
    monkeypatch.setattr(
        ui_utils, "savefile",
        lambda *a, **k: saves.append((a, k)) or (False, ""))
    before = env.window.manager.workspace

    env.window._load_workspace(str(path))

    assert len(saves) == 1
    args, kwargs = saves[0]
    assert kwargs.get("prefer_name") == "old.Orbitool"
    assert env.window.manager.workspace is before   # save dialog cancelled
