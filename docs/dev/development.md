# Development commands

The environment is managed by [uv](https://docs.astral.sh/uv/): Python 3.14 with the
exact dependency versions locked in `uv.lock` (direct dependencies live in
`pyproject.toml`).

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (installs Python 3.14 itself)
- A **C++ compiler** for the Cython extension build: MinGW-w64 GCC (recommended)
  or MSVC — full setup, including UPX and `build-config.json`, is documented in
  [build-environment.md](build-environment.md)

## Environment

- `uv sync` — install runtime dependencies (`.venv/`)
- `uv sync --group dev` — also install test dependencies (pytest, pandas)
- `uv sync --group build` — also install packaging dependencies (Cython, pyinstaller)
- `uv python install 3.14` — fetch the pinned interpreter if missing (uv does this automatically)

## Everyday

- `uv run --group build python util.py setup` — compile the Cython extensions in
  place (needs a C++ compiler and the build dependency group, see
  [build-environment.md](build-environment.md)). **Required on a fresh clone**: the compiled
  `*.pyd` files are gitignored, and without
  them imports and tests fail (including `models/spectrum/_denoise.py` and
  `_functions.py`, which are PE binaries disguised as `.py`). Only scans
  `Orbitool/` (never `.venv/`).
- `uv run --group dev pytest` — run the test suite (paths are listed in `pytest.ini`).
  A passing run is silent: `pytest.ini` sets `log_cli = false`, so no application
  log records reach the console. pytest still captures them, so a failing test
  prints its logs and traceback in the report as usual; tests that deliberately
  log an error (the `ui_task` error contract) pass, so their records stay hidden
  too. `pytest.ini` also sets `filterwarnings = error`, with a single `ignore` for
  matplotlib's deprecated Qt enum, so any other warning fails the test that raised
  it. `-q` trims pytest's own progress; there is no live chatter to turn off.
  `logger.py` detects pytest (`"pytest" in sys.modules`) and skips the file
  handler, so a test run never writes the `log.txt` a user sends to support;
  pytest's `log_file` keeps the run's `WARNING`-and-above records in
  `.pytest_cache/orbitool-tests.log` instead.
- `uv run python Main.py [--debug] [--no_multiprocess] [--to_step file|noise|peak-fit|calibration]` —
  launch the app; exceptions are appended to `log.txt` in the repo root
- Ad-hoc scripts that `import Orbitool` must run with the repo root on
  `sys.path`: `python` adds the *script's* own directory, not the repo root, so
  `uv run python C:\elsewhere\probe.py` raises `ModuleNotFoundError`. Keep the
  script at the repo root, or set `PYTHONPATH=.` just for that command
  (PowerShell: `$env:PYTHONPATH="."; uv run python ...`). `uv run pytest` needs
  none of this — `pytest.ini`'s rootdir handles it.

## UI tests

`Orbitool/UI/tests` mostly holds the real-GUI suite (`test_ui.py`), which drives
the GUI against real `.RAW` files that are not committed; `pytest.ini` excludes
that suite from the default run. Offscreen tests that need no RAW data are
listed explicitly in `pytest.ini` `testpaths`, so they do run with the default
suite: `test_timeseries_restore.py` in this folder and the `test_*_migration.py`
regression tests for the `ui_task` migration (under `Orbitool/UI/`,
`Orbitool/UI/file_tab/`, and `Orbitool/UI/formulas/`).

To run the real-GUI suite:

- put `test_data_path` (a folder scanned for `.RAW`) and, if processing is slow,
  a larger `test_timeout` (seconds, default `1`) in `setting.json` at the repo
  root; the tests read it the same way `Main.py` does. `test_data_path` defaults
  to `<repo parent>/data`.
- `uv run --group dev pytest Orbitool/UI/tests`
- set `QT_QPA_PLATFORM=offscreen` to run without a visible window.
- To drive the real `Window` offscreen from an ad-hoc script, build it the way
  `Orbitool/UI/tests/migration_harness.py` does — it pins a `QApplication`
  (constructing `Window()` without one aborts the process) and disables
  multiprocessing/threading for determinism.

## UI code generation

- Edit `*.ui` sources (Qt Designer), then `uv run python util.py pyuic` to regenerate
  the `*Ui.py` / `*Ui.Py` files. Never edit the generated files by hand; application
  logic lives in the hand-written `*UiPy.py` siblings.
- A few generated files end in uppercase `.Py`; those imports only resolve on
  case-insensitive filesystems (Windows).

## UI tooltips

Explanatory tooltips describe **what the code actually does at run time** — the
concrete effect on the data — not a restatement of the widget's label. For a
mass-tolerance (ppm) box that means the operation it feeds (e.g. "a new mass joins
an existing mass-list entry if within this ±ppm"), never just "tolerance(ppm)".

Tooltip text lives in the `.ui` source (`toolTip` property), so regeneration keeps
it. The hand-written `*UiPy.py` that reads the value carries a one-line pointer,
`# ppm tooltip: see <X.ui> (<widget>)`, so editing the logic surfaces the tooltip
that must change with it.

## UI structure

The main window is `MainUiPy.Window` (hand-written) over the generated
`MainUi.Ui_MainWindow` from `Main.ui`. The `QTabWidget` holds the left-to-right
workflow tabs; the side panels (Spectra List, Peak List, Mass List) are
`QDockWidget`s, not tabs.

## Packaging a release

- `uv run --group build python build.py`
  - First run creates `build-config.json` and exits — edit it (notably `upx_dir`
    must point to a valid UPX directory, `mingw_dir` the MinGW-w64 directory;
    see [build-environment.md](build-environment.md)), then run again.
  - Pipeline: pyuic → Cython compile (deletes and rebuilds all `*.pyd`) → pytest →
    pyinstaller + UPX → zip.
  - The zip root holds `Orbitool.exe` plus its `_internal/` dependency bundle
    (PyInstaller 6 layout), with no launcher `.bat`. Settings and logs live next to
    the exe, outside `_internal`: settings save to `setting.json` via
    `Orbitool/config.py`, paths resolved in `paths.py`.
  - The bundle is pruned to what the UI can actually reach — unused Qt files,
    Pillow codecs, matplotlib sample data and dev-only packages that hooks
    over-collect are dropped in `Main.spec`. That spec is the single source for
    the drop lists and the reason each entry exists. scipy subpackages are
    deliberately kept: they are imported from C extensions, so excluding them
    crashes the app. See
    [ADR 0002](../adr/0002-slim-release-build-by-config.md).
  - The pytest step is silent while tests pass; a failure prints the offending
    test's captured logs and traceback (see [Everyday](#everyday)). It ends with one
    verdict line: `pytest: OK (exit 0)`, or
    `pytest FAILED (exit N) - packaging stopped`, which aborts the build before the
    PyInstaller step.
  - Fails on purpose if `jedi` is importable — use a build environment without IDE
    helper packages.
- Other `util.py` subcommands: `count | setup | copy | collect | clear`.
