# Slim the release build by pruning runtime-unreachable files in PyInstaller

## Status

accepted

## Context

A release package weighed ~138 MB, essentially all of it the PyInstaller/PySide6
bundle. Swapping the Qt binding (PyQt6 → PySide6) changed the number by nothing.
The bulk is over-collection: Qt ships every module, plugin and translation it
has; Pillow ships every image codec; matplotlib ships its sample data;
`pyteomics` drags in `pandas` through a guarded optional import. The app reaches
only a fraction of it. Dependency versions are frozen (`pyproject.toml` /
`uv.lock`), so the reduction has to happen in the packaging configuration, not by
changing dependencies.

The obvious first cut — also excluding the scipy subpackages that
`scipy.optimize.curve_fit` "does not import" — silently broke startup. The
imports exist but are made from C extensions, which static analysis and
`builtins.__import__` monkeypatching both miss (see Consequences).

## Decision

Reduce the bundle in `Main.spec`, dropping only what no runtime path reaches:

- `hiddenimports` is trimmed to the modules that are genuinely resolved from C
  code and therefore invisible to PyInstaller: `scipy.special._ufuncs_cxx`,
  `scipy.linalg.cython_blas`, `scipy.linalg.cython_lapack`, plus
  `scipy.integrate` (imported by the `scipy.special._ellip_harm_2` C extension).
  The old list's remaining entries — the non-existent `scipy.integrate.*` names
  and `pkg_resources.py2_warn` — were dead; PyInstaller reported them "not found".
- `excludes` drops packages that only leak in through guarded/optional imports,
  or through an import that should not be there: `pandas`, `Cython`, `tkinter`,
  `PyQt6`. `tkinter` became removable once the accidental
  `from tkinter import W` (an unused constant) was deleted from
  `Orbitool/UI/NoiseUiPy.py` — before that, `Main.py` pulled it in at startup.
- `a.binaries`/`a.datas` are filtered to remove Qt files backing features the app
  never uses (translations, `imageformats`/`iconengines`/`networkinformation`/
  `generic` plugins), unused Pillow codecs
  (`_avif`/`_webp`/`_imagingcms`/`_imagingtk`) and matplotlib `sample_data`.

Deliberately **not** dropped, because they cannot be proven unreachable from the
source:

- **Any scipy subpackage.** scipy loads subpackages lazily from C extensions:
  `_denoise.pyx → scipy.optimize → scipy.linalg.interpolative → scipy.fft` and
  `scipy.special._ellip_harm_2 → scipy.integrate`. Excluding either crashes at
  import. PyInstaller's `hook-scipy.*` hooks exist exactly to bundle them.
- **`opengl32sw.dll`, `qdirect2d.dll`, the Qt tls plugins.** Qt may fall back to
  them; keeping them costs little and removes the risk.

`Qt6Network`/`Qt6Svg` and Pillow are kept too: `PySide6/__init__.py` and
matplotlib's `qt_compat` import them unconditionally.

## Consequences

Installed size drops from ~138 MB to ~113 MB and the release zip from ~100 MB to
~82 MB, with behavior unchanged — every pruned item is unreachable from the UI.
The cost is coupling to third-party hooks: the drop list is correct only while
the app ships no Qt translations, no non-PNG image I/O, no SVG icons and no
Pillow codec beyond PNG; a future feature that adds any of those must remove the
matching entry from `Main.spec`.

A debugging trap worth remembering: `Main.py` catches startup exceptions and
writes them to `log.txt` next to the exe (see `paths.py`) and then exits with code
0, so "the process stayed alive" and "exit code 0" are both misleading. Check
`dist/Orbitool/log.txt` for a `Traceback`. Relatedly, monkeypatching
`builtins.__import__` to simulate an absent package does **not** intercept
imports issued by C extensions, so source-level "block the import" tests give
false confidence; verify against the frozen build.

## Considered Options

- **Trim at the dependency level** (drop scipy/matplotlib, replace `curve_fit`
  with numpy). Rejected: changes runtime behavior and the frozen dependency set;
  out of scope for a packaging-only change.
- **Remove matplotlib's bundled fonts** (~8.5 MB). Rejected: the default font set
  is load-bearing for any plot text; not worth the risk for the payoff.
- **Exclude scipy subpackages** (would shave a few more MB). Rejected: crashes
  startup, as above.
