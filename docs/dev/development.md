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
  `pytest.ini` turns on pytest's live logging (`log_cli`, level `INFO`), so the
  application's own `INFO`-and-above records show up on the console as the tests
  run, with pytest's format; `DEBUG` is not shown live. Every test that
  deliberately logs an error (the `ui_task` error contract) is therefore expected
  output, not a failure — the verdict is the pytest summary line.
  The repository-root `conftest.py` keeps the process-wide `Orbitool` logger out of
  the way: during tests the app's file log is `.pytest_cache/orbitool-tests.log`,
  falling back to the system temporary directory and, failing that, to dropping the
  records — never to the `log.txt` a user sends to support. The logger's
  handlers/level/`propagate` are also snapshotted around every test: a test that
  leaves them changed gets a `PytestWarning` and the old configuration back.
  For a concise run with no live `INFO` chatter — `-q` trims pytest's own progress
  and `-o log_cli=false` turns off the live logging; failing tests still print their
  captured logs and tracebacks — use
  `uv run --group dev pytest -q -o log_cli=false`.
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

## UI code generation

- Edit `*.ui` sources (Qt Designer), then `uv run python util.py pyuic` to regenerate
  the `*Ui.py` / `*Ui.Py` files. Never edit the generated files by hand; application
  logic lives in the hand-written `*UiPy.py` siblings.
- A few generated files end in uppercase `.Py`; those imports only resolve on
  case-insensitive filesystems (Windows).

## Packaging a release

- `uv run --group build python build.py`
  - First run creates `build-config.json` and exits — edit it (notably `upx_dir`
    must point to a valid UPX directory, `mingw_dir` the MinGW-w64 directory;
    see [build-environment.md](build-environment.md)), then run again.
  - Pipeline: pyuic → Cython compile (deletes and rebuilds all `*.pyd`) → pytest →
    pyinstaller + UPX → zip.
  - The pytest step prints the app's `ERROR`/`WARNING` records as they happen (see
    [Everyday](#everyday)) and ends with one verdict line: `pytest: OK (exit 0)`, or
    `pytest FAILED (exit N) - packaging stopped`, which aborts the build before the
    PyInstaller step.
  - Fails on purpose if `jedi` is importable — use a build environment without IDE
    helper packages.
- Other `util.py` subcommands: `count | setup | copy | collect | clear`.
