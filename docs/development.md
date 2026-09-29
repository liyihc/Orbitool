# Development commands

The environment is managed by [uv](https://docs.astral.sh/uv/): Python 3.11 with the
exact dependency versions locked in `uv.lock` (direct dependencies live in
`pyproject.toml`).

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (installs Python 3.11 itself)
- A **C++ compiler** for the Cython extension build: MSVC (Visual Studio Build
  Tools, workload `VCTools`) is the route `distutils` supports out of the box on
  Windows; a standalone MinGW-w64 GCC also works with extra configuration

## Environment

- `uv sync` — install runtime dependencies (`.venv/`)
- `uv sync --group dev` — also install test dependencies (pytest, pandas)
- `uv sync --group build` — also install packaging dependencies (Cython, pyinstaller)
- `uv python install 3.11` — fetch the pinned interpreter if missing (uv does this automatically)

## Everyday

- `uv run python util.py setup` — compile the Cython extensions in place (needs a
  C++ compiler, see Prerequisites). **Required on a fresh clone**: the compiled
  `*.pyd` files are gitignored, and without
  them imports and tests fail (including `models/spectrum/_denoise.py` and
  `_functions.py`, which are PE binaries disguised as `.py`). Only scans
  `Orbitool/` (never `.venv/`).
- `uv run --group dev pytest` — run the test suite (paths are listed in `pytest.ini`)
- `uv run python Main.py [--debug] [--no_multiprocess] [--to_step file|noise|peak-fit|calibration]` —
  launch the app; exceptions are appended to `log.txt` in the repo root

## UI code generation

- Edit `*.ui` sources (Qt Designer), then `uv run python util.py pyuic` to regenerate
  the `*Ui.py` / `*Ui.Py` files. Never edit the generated files by hand.

## Packaging a release

- `uv run --group build python build.py`
  - First run creates `build-config.json` and exits — edit it, then run again
    (notably `upx_dir` must point to a valid UPX directory).
  - Pipeline: pyuic → Cython compile (deletes and rebuilds all `*.pyd`) → pytest →
    pyinstaller + UPX → zip.
  - Fails on purpose if `jedi` is importable — use a build environment without IDE
    helper packages.
- Other `util.py` subcommands: `count | setup | copy | collect | clear`.
