## Project overview

Orbitool is a Windows desktop GUI tool (PySide6, HDF5 workspaces) for processing Thermo
Fisher mass-spec (.RAW) data — denoise → peak shape → calibration → peak fitting →
formula / mass defect / time series — aimed at atmospheric and environmental chemistry
researchers. Developed and maintained by Shanghai Jiao Tong University with
contributions from research institutions in China, France, and Finland.

## Development commands

Managed by uv (Python 3.14, locked in `uv.lock`). `docs/dev/development.md` is the
single source for the setup build (compiled Cython extensions, required on a fresh
clone before imports or tests work), the test command, launching the app, UI code
generation, and packaging. Read it before running any of them.

## Repository layout

- `Orbitool/` — main package: `base/` (HDF5 serialization framework), `models/`
  (domain logic: formula, spectrum, peakfit, calibration, workspace), `UI/` (PySide6
  interface), `utils/` (runtime utilities, Thermo RAW readers)
- `tools/` — build/dev tooling (pyuic, Cython setup); unrelated to `Orbitool/utils/`
- `notebooks/` — experiments · `resources/` — icons
- `docs/` — documentation: `guide/` (user manual, entry point
  `docs/guide/index.md`), `dev/` (development + build), `agents/` (agent skill docs)

## Notes

- Reply in the same language the user writes in
- A pitfall that lives in a single file belongs in that file's comments/docstring,
  not here; keep AGENTS.md to cross-cutting traps and pointers
- Never commit data: `*.RAW`, `data/`, `*.Orbitool` etc. are gitignored; test
  fixtures under `models/*/tests/` are tracked, so add data/output CSV paths to
  `.gitignore` individually rather than blanket-ignoring all CSVs
- Judge a test run by its exit code (`$LASTEXITCODE`); never pipe `pytest` through
  `Select-Object -Last N` — that hides failure tracebacks
- Code and docs land together: whenever you change code, update every doc that the
  change makes stale. A behavior work-flow change touches `docs/guide/`; a
  command/build change touches `docs/dev/`. Also update `readme.md` or
  `GLOSSARY.md`/`docs/adr/` when they describe what changed — in the same change. But `docs/dev/` states
  contracts and entry points, not implementation mechanics: don't restate what the
  code already carries (path resolution, migration fallbacks, volatile
  tables/defaults). To keep it findable, point to the authoritative `file`/`symbol`
  — a relative link or backticked path, never a line number — and leave the reason
  and the mechanics in the code's comments/docstring. This holds even for a dev doc
  that explains a framework (`docs/dev/ui-tasks.md`). The user guide
  (`docs/guide/`) is exempt: it keeps its own account of the workflow and
  algorithms, for users who do not read the code
- Every UI operation must be reachable through a visible control; purely implicit
  gestures (double-click magic, hotkey-only, or otherwise hidden actions) are not
  allowed
- Writing tab background operations (`ui_task` / `background`, mode words, error and
  abort contracts): see `docs/dev/ui-tasks.md`
- Logging user actions (level, TAG, what to log): see `docs/dev/logging.md`

## Agent skills

### Issue tracker

Issues live as markdown files under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: root `GLOSSARY.md` + `docs/adr/`. See `docs/agents/domain.md`.
