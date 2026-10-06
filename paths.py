"""Filesystem roots for user files and bundled resources.

Deliberately stdlib-only (no ``Orbitool`` imports): ``Main.py``'s crash handler
imports this module, and importing anything under ``Orbitool`` would run
``Orbitool/__init__.py`` — which constructs the settings model and, worse, opens
the log file — and could mask the original traceback with a secondary failure.

In a PyInstaller onedir bundle the bootloader sets ``sys.frozen`` and
``sys._MEIPASS`` (the ``_internal`` folder): bundled data goes there, but
``setting.json`` / ``log.txt`` stay next to the executable, outside ``_internal``.
"""
from pathlib import Path
import sys

if getattr(sys, "frozen", False):
    ROOT_PATH = Path(sys.executable).parent
    RESOURCE_PATH = Path(sys._MEIPASS) / "resources"
    # Older frozen builds treated _internal as ROOT_PATH and wrote setting.json
    # there; read it once so upgrades do not lose the user's settings.
    LEGACY_CONFIG_PATH = Path(sys._MEIPASS) / "setting.json"
else:
    ROOT_PATH = Path(__file__).parent
    RESOURCE_PATH = ROOT_PATH / "resources"
    LEGACY_CONFIG_PATH = None

CONFIG_PATH = ROOT_PATH / "setting.json"
LOG_PATH = ROOT_PATH / "log.txt"
