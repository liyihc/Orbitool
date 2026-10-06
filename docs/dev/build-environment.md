# Build environment setup

Everything needed to compile the Cython extensions and package a release on a
fresh Windows clone, in order: uv → compiler → UPX → `build-config.json` →
compile → package. Command reference lives in
[development.md](development.md).

## 1. uv

Install [uv](https://docs.astral.sh/uv/), then from the repo root:

```powershell
uv sync --group dev     # runtime + test dependencies
uv sync --group build   # + packaging dependencies (Cython, pyinstaller)
```

uv downloads the pinned Python 3.14 interpreter automatically.

## 2. Compiler (MinGW-w64, recommended)

The extensions are compiled with MinGW-w64 GCC. Download a build from the
[MinGW-W64-builds](https://www.mingw-w64.org/downloads/) page (direct link:
<https://github.com/niXman/mingw-builds-binaries/releases>) and extract it
anywhere — no installer, no system-wide changes. Any recent build matching
these works (version number does not matter): **x86_64**, threads model
**posix**, exceptions model **seh**, runtime **ucrt**, C and C++ enabled.

Point `build-config.json`'s `mingw_dir` at the extracted directory (the one
containing `bin\gcc.exe`), see section 4. `gcc` is not expected on `PATH` —
do not use `where gcc` to check for a toolchain.

The build scripts then prepend `<mingw_dir>\bin` to `PATH` and build portable
`.pyd` files; the compile/link flags and the reasons behind them live in
`utils/setup.py` (`cythonSetup`).

### MSVC (alternative)

If `mingw_dir` is not set, the build falls back to MSVC (what distutils
discovers by default on Windows). Install it with:

```powershell
winget install --id Microsoft.VisualStudio.2022.BuildTools -e `
  --accept-source-agreements --accept-package-agreements `
  --override "--quiet --wait --norestart --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
```

When `util.py setup` fails for a missing MSVC, it prints both options and —
interactively — offers to record a MinGW-w64 directory in `build-config.json`
and retries.

## 3. UPX (packaging only)

Required only for `build.py` (release packaging), not for development
compiles. Download [UPX](https://github.com/upx/upx/releases), extract it
anywhere, and set `upx_dir` in `build-config.json` to the directory
containing `upx.exe`.

## 4. build-config.json

Created by the first `build.py` run (edit it, then rerun) or by
`util.py setup`'s MinGW prompt. Gitignored — local paths never enter the
repository. `utils/build_config.py` (`Config`) defines the fields and their
defaults.

Minimal example:

```json
{
    "mingw_dir": "D:/tools/mingw64",
    "upx_dir": "D:/tools/upx"
}
```

## 5. Compile

```powershell
uv run --group build python util.py setup          # compile extensions in place
uv run --group build python util.py setup --clear  # delete *.pyd first
```

Compiles every `.pyx` under `Orbitool/`; `compileAll` in `utils/setup.py` orders
them by dependency. Required on a fresh clone: the `*.pyd` files are gitignored,
and without them imports and tests fail.

## 6. Package a release

```powershell
uv run --group build python build.py
```

`build.py` runs the stages listed in
[development.md](development.md#packaging-a-release) and aborts with a non-zero
exit code on the first failure.

Note: `build.py` refuses to run if `jedi` is importable — build in the
project venv, not an environment with IDE helper packages.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Microsoft Visual C++ 14.0 or greater is required` | Either install MSVC (section 2) or set `mingw_dir` (section 4) |
| `cannot find "<...>\bin\gcc.exe"` | `mingw_dir` points at the wrong directory — it must contain `bin\gcc.exe` |
| `ImportError: DLL load failed` when importing a `.pyd` | Stale `.pyd` built without `-static` — recompile: `util.py setup --clear` then `util.py setup` |
| `ImportError: cannot import name '_element' ... partially initialized module ... circular import` after upgrading Python | Not a circular import — `.pyd` tagged with the old interpreter (e.g. `cp311-...` vs `cp314-...`) — recompile: `util.py setup --clear` then `util.py setup` |
| `please provide upx path` during packaging | Set `upx_dir` in `build-config.json` (section 3) |
| Collection errors in pytest mentioning missing modules | Extensions not compiled yet — run `uv run --group build python util.py setup` |
| `ModuleNotFoundError: No module named 'Cython'` | Missing build group — `uv sync --group build` (or prefix the command with `uv run --group build`) |
