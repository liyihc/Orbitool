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

uv downloads the pinned Python 3.11 interpreter automatically.

## 2. Compiler (MinGW-w64, recommended)

The extensions are compiled with MinGW-w64 GCC. Download a build from the
[MinGW-W64-builds](https://www.mingw-w64.org/downloads/) page (the "MinGW-W64
builds" project, winlibs-style release archives, direct link:
<https://github.com/niXman/mingw-builds-binaries/releases>) and extract it
anywhere — no installer, no system-wide changes.

When choosing a build, use these principles:

- architecture **x86_64** (64-bit)
- threads model **posix**
- exceptions model **seh**
- runtime **ucrt**
- C and C++ languages enabled

Any recent build matching the above works; the version number itself does not
matter.

Enable it by pointing `build-config.json` at the extracted directory (the one
containing `bin\gcc.exe`), see section 4.

What the build scripts do with it (handled automatically, for reference):

- prepend `<mingw_dir>\bin` to `PATH` for the compile
- compile with `--compiler=mingw32`
- define `MS_WIN64`: the MSVC-flavoured `pyconfig.h` shipped with Python only
  defines it under `_MSC_VER`; without it gcc computes `SIZEOF_VOID_P = 4` and
  Cython's static assert fails (or worse, silently mis-sizes types)
- link with `-static` so the `.pyd` files do not depend on
  `libstdc++`/`libgcc`/`libwinpthread` DLLs and load on machines without a
  MinGW runtime

### MSVC (alternative)

If `mingw_dir` is not set, the build falls back to MSVC (what distutils
discovers by default on Windows). Install it with:

```powershell
winget install --id Microsoft.VisualStudio.2022.BuildTools -e `
  --accept-source-agreements --accept-package-agreements `
  --override "--quiet --wait --norestart --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
```

When `uv run python util.py setup` fails because MSVC is missing, it prints
both options and — in an interactive terminal — offers to take a MinGW-w64
directory directly, saves it to `build-config.json`, and retries.

## 3. UPX (packaging only)

Required only for `build.py` (release packaging), not for development
compiles. Download [UPX](https://github.com/upx/upx/releases), extract it
anywhere, and set `upx_dir` in `build-config.json` to the directory
containing `upx.exe`.

## 4. build-config.json

Created on the first `build.py` run (it then asks you to edit the file and
rerun), or created by `util.py setup` when you answer its MinGW prompt. It is
gitignored — local paths never enter the repository. Full reference:

| field | default | meaning |
|---|---|---|
| `not_compile_once` | `false` | one-shot: compile once, then this flips itself off |
| `compile` | `true` | run pyuic + Cython compile stage in `build.py` |
| `test` | `true` | run pytest stage (build aborts on failure) |
| `build` | `true` | run pyinstaller + UPX stage |
| `zip_file` | `true` | zip `dist/` output |
| `upx_dir` | `""` | directory containing `upx.exe` (empty → packaging stage fails) |
| `mingw_dir` | `""` | MinGW-w64 root (containing `bin\gcc.exe`); empty → MSVC fallback |

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

Scans `Orbitool/` for `.pyx` files and builds them in dependency order.
Required on a fresh clone: the `*.pyd` files are gitignored, and without them
imports and tests fail.

## 6. Package a release

```powershell
uv run --group build python build.py
```

Pipeline: pyuic → Cython compile (deletes and rebuilds all `*.pyd`) → pytest
→ pyinstaller + UPX → zip in `dist/`. Any stage failing aborts with a
non-zero exit code.

Note: `build.py` refuses to run if `jedi` is importable — build in the
project venv, not an environment with IDE helper packages.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Microsoft Visual C++ 14.0 or greater is required` | Either install MSVC (section 2) or set `mingw_dir` (section 4) |
| `cannot find "<...>\bin\gcc.exe"` | `mingw_dir` points at the wrong directory — it must contain `bin\gcc.exe` |
| `ImportError: DLL load failed` when importing a `.pyd` | Stale `.pyd` built without `-static` — recompile: `util.py setup --clear` then `util.py setup` |
| `please provide upx path` during packaging | Set `upx_dir` in `build-config.json` (section 3) |
| Collection errors in pytest mentioning missing modules | Extensions not compiled yet — run `uv run --group build python util.py setup` |
| `ModuleNotFoundError: No module named 'Cython'` | Missing build group — `uv sync --group build` (or prefix the command with `uv run --group build`) |
