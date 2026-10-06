## Project overview

Orbitool is a Windows desktop GUI tool (PyQt6, HDF5 workspaces) for processing Thermo
Fisher mass-spec (.RAW) data — denoise → peak shape → calibration → peak fitting →
formula / mass defect / time series — aimed at atmospheric and environmental chemistry
researchers. Developed and maintained by Shanghai Jiao Tong University with
contributions from research institutions in China, France, and Finland.

## Development commands

Managed by uv (Python 3.14, locked in `uv.lock`). See `docs/dev/development.md`.

## Repository layout

- `Orbitool/` — main package: `base/` (HDF5 serialization framework), `models/`
  (domain logic: formula, spectrum, peakfit, calibration, workspace), `UI/` (PyQt6
  interface), `utils/` (runtime utilities, Thermo RAW readers)
- `utils/` — build/dev tooling (pyuic, Cython setup); unrelated to `Orbitool/utils/`
- `notebooks/` — experiments · `resources/` — icons
- `docs/` — documentation: `guide/` (user manual, entry point
  `docs/guide/index.md`), `dev/` (development + build), `agents/` (agent skill docs)
- `CONTEXT.md` / `docs/adr/` may not exist yet — see `docs/agents/domain.md`

## Notes

- Reply in the same language the user writes in
- Fresh clone has no compiled Cython extensions: run
  `uv run --group build python util.py setup` first (requires a C++ toolchain —
  MinGW-w64 or MSVC, see `docs/dev/build-environment.md`), or imports and tests fail
- Do not edit generated `*Ui.py` / `*Ui.Py` files (header says "Do not edit"); edit the
  `*.ui` source and run `util.py pyuic`; application logic lives in `*UiPy.py`
- Several generated UI files end in uppercase `.Py`; imports only work on
  case-insensitive filesystems (Windows)
- Never commit data: `*.RAW`, `data/`, `*.Orbitool` etc. are gitignored; CSVs
  are not blanket-ignored — test fixtures under `models/*/tests/` are tracked,
  and data/output CSV paths get gitignored individually as needed
- Thermo `.RAW` reading requires pythonnet + the tracked ThermoFisher DLLs
  (Windows/.NET only)
- Qt Designer requires pyside2 installed in a *separate* environment
- Running the app writes `setting.json` / `log.txt` at the repo root (gitignored);
  the test suite writes the app log to `.pytest_cache/orbitool-tests.log` (or the
  system temporary directory) instead, and only ever opens `log.txt` — it never
  writes to it (see `conftest.py`)
- Bumping `Orbitool/version.py` may need a matching updater in
  `models/workspace/updater/`, otherwise old `.Orbitool` workspaces won't open
- `test_thermo.py` hardcodes a personal data path; those tests fail on other machines
- Run the suite with `uv run --group dev pytest` and judge it by the exit code
  (`$LASTEXITCODE`); never pipe it through `Select-Object -Last N` or similar —
  that hides failure tracebacks, and the command runner already captures full output
- Code and docs land together: whenever you change code, update every doc that the
  change makes stale. A behavior work-flow change touches `docs/guide/`; a
  command/build change touches `docs/dev/`; user-visible changes get a
  `CHANGELOG.md` entry. Also update `readme.md` or `CONTEXT.md`/`docs/adr/` when
  they describe what changed — in the same change
- Writing tab background operations (`ui_task` / `background`, mode words, error and
  abort contracts): see `docs/dev/ui-tasks.md`

## Agent skills

### Issue tracker

Issues live as markdown files under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical roles: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: root `CONTEXT.md` + `docs/adr/`. See `docs/agents/domain.md`.
