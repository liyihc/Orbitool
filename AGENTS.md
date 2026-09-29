## Project overview

Orbitool is a Windows desktop GUI tool (PyQt6, HDF5 workspaces) for processing Thermo
Fisher mass-spec (.RAW) data — denoise → peak shape → calibration → peak fitting →
formula / mass defect / time series — aimed at atmospheric and environmental chemistry
researchers. Developed and maintained by Shanghai Jiao Tong University with
contributions from research institutions in China, France, and Finland.

## Development commands

Managed by uv (Python 3.11, locked in `uv.lock`). See `docs/development.md`.

## Repository layout

- `Orbitool/` — main package: `base/` (HDF5 serialization framework), `models/`
  (domain logic: formula, spectrum, peakfit, calibration, workspace), `UI/` (PyQt6
  interface), `utils/` (runtime utilities, Thermo RAW readers)
- `utils/` — build/dev tooling (pyuic, Cython setup); unrelated to `Orbitool/utils/`
- `notebooks/` — experiments · `resources/` — icons · `docs/` — documentation
- `CONTEXT.md` / `docs/adr/` may not exist yet — see `docs/agents/domain.md`

## Notes

- Fresh clone has no compiled Cython extensions: run `uv run python util.py setup`
  first (requires a C++ toolchain), or imports and tests fail
- Do not edit generated `*Ui.py` / `*Ui.Py` files (header says "Do not edit"); edit the
  `*.ui` source and run `util.py pyuic`; application logic lives in `*UiPy.py`
- Several generated UI files end in uppercase `.Py`; imports only work on
  case-insensitive filesystems (Windows)
- Never commit data: `*.RAW`, `data/`, `*.Orbitool`, `*.csv` etc. are gitignored;
  test fixtures under `models/*/tests/` are the tracked exception
- Thermo `.RAW` reading requires pythonnet + the tracked ThermoFisher DLLs
  (Windows/.NET only)
- Qt Designer requires pyside2 installed in a *separate* environment
- Running the app writes `setting.json` / `log.txt` at the repo root (gitignored)
- Bumping `Orbitool/version.py` may need a matching updater in
  `models/workspace/updater/`, otherwise old `.Orbitool` workspaces won't open
- `test_thermo.py` hardcodes a personal data path; those tests fail on other machines

## Agent skills

### Issue tracker

Issues live as markdown files under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical roles: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: root `CONTEXT.md` + `docs/adr/`. See `docs/agents/domain.md`.
