# -*- mode: python ; coding: utf-8 -*-
import re

block_cipher = None


a = Analysis(['Main.py'],
             pathex=[],
             binaries=[],
             datas=[
                ('Orbitool/utils/readers/*.dll','Orbitool/utils/readers'),
                ('resources/icons/*', 'resources/icons') ],
            hiddenimports=[
                # scipy.optimize.curve_fit (called from the denoise .pyx) and
                # scipy.integrate (imported by the _ellip_harm_2 C extension via
                # scipy.special) are resolved from C code, which PyInstaller's
                # static analysis cannot see.
                'scipy.special._ufuncs_cxx',
                'scipy.linalg.cython_blas',
                'scipy.linalg.cython_lapack',
                'scipy.integrate'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[
                # Leaked in through guarded/optional imports; no runtime path
                # needs them. pandas is only used by the test suite (dev group)
                # and arrives via pyteomics' optional `try: import pandas`
                # (file_helpers.py), Cython only by tools/setup.py (build group).
                'pandas', 'Cython',
                # matplotlib is forced onto QtAgg (Main.py `mpl.use("QtAgg")`);
                # nothing imports its Tk backend.
                'tkinter',
                # NOTE: do not add scipy subpackages here — scipy loads them
                # lazily from C extensions and excluding one crashes startup
                # (see docs/adr/0002-slim-release-build-by-config.md).
                # Guard against a stray PyQt6 in the build environment.
                'PyQt6'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)


# Hooks over-collect. Everything matched below backs a feature the app never
# touches, so dropping the files is behavior-preserving:
#  - Qt: only QtCore/QtGui/QtWidgets are used (QtNetwork/QtSvg are also
#    imported unconditionally by PySide6/__init__.py and matplotlib qt_compat,
#    so they stay). No QTranslator, no non-PNG image I/O, no SVG icons, no
#    network information, no touch input.
#  - Pillow: only PNG is ever decoded; the app never touches AVIF/WebP/color
#    management/Tk (matplotlib needs _imaging/_imagingft, which stay).
#  - matplotlib: sample_data feeds the bundled examples only.
#
# Deliberately NOT dropped: opengl32sw.dll, qdirect2d.dll and the Qt tls
# plugins. They cannot be proven unused from the source (Qt may fall back to
# them), so they stay until the bundle is smoke-tested against them.
_DROP = [re.compile(pattern) for pattern in (
    r'PySide6[\\/]translations[\\/]',
    r'PySide6[\\/]plugins[\\/]imageformats[\\/]',
    r'PySide6[\\/]plugins[\\/]networkinformation[\\/]',
    r'PySide6[\\/]plugins[\\/]iconengines[\\/]',
    r'PySide6[\\/]plugins[\\/]generic[\\/]',
    r'PIL[\\/]_avif\.',
    r'PIL[\\/]_webp\.',
    r'PIL[\\/]_imagingcms\.',
    r'PIL[\\/]_imagingtk\.',
    r'matplotlib[\\/]mpl-data[\\/]sample_data[\\/]',
)]


def _drop(entries):
    return [entry for entry in entries
            if not any(pattern.search(entry[0]) for pattern in _DROP)]


a.binaries = _drop(a.binaries)
a.datas = _drop(a.datas)


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Orbitool',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[
                    "pydantic_core/*.pyd",
                    # Windows Defender false positive (Trojan:Win32/Commando.A!ml)
                    # on the UPX-packed scipy binary; it quarantines the file and
                    # the build dies during COLLECT.
                    "scipy/special/cython_special*"
               ],
               name='Orbitool')
