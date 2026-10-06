# Changelog

All notable changes to Orbitool are documented in this file. The format is based
on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed

- The Qt binding moved from `PyQt6` to `PySide6-Essentials` (LGPLv3, and slimmer:
  the Addons — QtWebEngine, Charts, 3D, Multimedia, … — are not pulled in). All
  `PyQt6` imports are now `PySide6`, `pyqtSignal`/`pyqtSlot` are `Signal`/`Slot`,
  and the generated `*Ui.py` / `*Ui.Py` files were regenerated with `pyside6-uic`.
  Qt Designer now ships with PySide6 (`pyside6-designer`), so the separate pyside2
  environment is no longer needed. Three switch-over follow-ups ride along:
  `util.py pyuic` preserves the existing case of generated `*Ui.py` / `*Ui.Py`
  filenames, so `--clear` no longer fails on case-sensitive directories; the
  file/folder pickers use PySide6's `dir=` keyword (PyQt6's `directory=` is
  rejected), so **Open**, **Save** and **Select folder** work again; and background
  workers are kept referenced until Qt reports them finished, so a step that starts
  the next worker from its result no longer destroys a still-running `QThread`
  (`QThread: Destroyed while thread '' is still running`, seen after **Denoise**).
- The packaged release no longer ships `StartOrbitool.bat`; run
  `Orbitool/Orbitool.exe` directly. `setting.json` and `log.txt` are now written
  next to that executable — outside the `_internal` folder PyInstaller 6 uses for
  bundled dependencies — so they stay where the readme says they are. A
  `setting.json` left inside `_internal` by an older build is read once and
  migrated to the new location, so settings survive the upgrade.

### Added

- A theme option in **Settings → General** with three choices: **Follow system**,
  **Light** and **Dark**. It selects the Qt color scheme; **Light** stays the
  default. The choice takes effect when the dialog is accepted, with no restart.

### Fixed

- Peak splitting no longer aborts calibration or peak fitting with `ValueError:
  Buffer dtype mismatch, expected 'int32' but got 'long long'`. When a cut
  spectrum did not fall back to zero at its right edge (or did not rise from zero
  at its left), the boundary index appended to the peak range was built as a
  64-bit integer and rejected by the function's 32-bit index array on numpy 2.x;
  it now keeps the array's `int32` type.
- Importing files or a folder no longer fails for the whole batch when one `.RAW`
  has no mass-spectrometer data — the .NET reader raises
  `ArgumentOutOfRangeException: Instrument index not available` on such a file.
  The file is skipped, the rest are imported, and the skipped files are listed in
  one **Unreadable .RAW files** dialog (and in `log.txt`) when the import ends.

## [2.6.0]

### Changed

- Documentation is now kept in the repository: the user manual lives under
  `docs/guide/` and developer/build docs under `docs/dev/`. The external Notion
  links have been removed.

### Fixed

- Averaging no longer kills the denoise read when a `.RAW` contains a scan whose FT
  profile is empty (a damaged or interrupted acquisition). The .NET averager throws
  `IndexOutOfRangeException` on such a scan without naming it, so the unusable scans
  are now detected on the first failure and left out of that window, which is averaged
  again instead of aborting the whole file. A read reports the scans it had to repair
  to whoever started it, so every denoise, skip or show-average read lists the files it
  found damaged in one dialog (as well as in `log.txt`) and forgets them with that read;
  nothing is repaired silently. Such a scan looks normal otherwise — its TIC and every
  trailer field match the healthy scans.
- A raw file reader now releases its file handle through an explicit `File.close()`,
  which `__del__` calls without ever raising, and which the spectrum read path calls
  as soon as a reader is superseded or yields no spectrum. The previous `__del__`
  called `Dispose()` unguarded and raised `TypeError: 'MethodObject' object is not
  callable` whenever it ran during interpreter shutdown.

## [2.5.4]

- First tracked release. Changes before this version were not recorded in the
  repository; the current version lives in `Orbitool/version.py`.
