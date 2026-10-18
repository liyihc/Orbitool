from pathlib import Path
import os
import shutil
import subprocess


def _output_path(ui: Path) -> Path:
    """Return the existing generated file for `ui` preserving its filename case.

    Some directories are case-sensitive (NTFS per-directory flag), so the
    default `*Ui.py` name can differ from a tracked `*Ui.Py`; look the real
    name up case-insensitively and reuse it.
    """
    wanted = (ui.stem + 'Ui.py').lower()
    for f in ui.parent.iterdir():
        if f.is_file() and f.name.lower() == wanted:
            return f
    return ui.with_name(ui.stem + 'Ui.py')


def _run_uic(ui: Path, output: Path) -> None:
    uic = shutil.which("pyside6-uic")
    if uic is None:
        raise SystemExit("pyside6-uic not found; run this through `uv run`")
    subprocess.run([uic, str(ui), "-o", str(output)], check=True)


def pyuic(path, *, check=False):
    path = Path(path)
    stale = []
    for ui in path.glob("**/*.ui"):
        uipy = _output_path(ui)
        exist = uipy.exists()
        needs_update = not exist or os.path.getmtime(ui) > os.path.getmtime(uipy)

        if check:
            if needs_update:
                stale.append((ui, uipy))
            continue

        if needs_update:
            if exist:
                print("Override old version", ui)
            else:
                print("Generate", ui)
            _run_uic(ui, uipy)

    if not check:
        return True

    for ui, uipy in stale:
        print(f"stale: {ui} -> {uipy}")
    if stale:
        print("Run `uv run python util.py pyuic` and stage the generated files.")
        return False
    return True


def clear(path):
    path = Path(path)
    for ui in path.glob("**/*.ui"):
        uipy = _output_path(ui)
        if uipy.exists():
            os.remove(uipy)
