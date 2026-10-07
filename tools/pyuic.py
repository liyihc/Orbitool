from pathlib import Path
import os


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


def pyuic(path):
    path = Path(path)
    for ui in path.glob("**/*.ui"):
        uipy = _output_path(ui)

        exist = uipy.exists()
        if not exist or os.path.getmtime(ui) > os.path.getmtime(uipy):
            if exist:
                print("Override old version", ui)
            else:
                print("Generate", ui)
            os.system(f'pyside6-uic "{ui}" -o "{uipy}"')


def clear(path):
    path = Path(path)
    for ui in path.glob("**/*.ui"):
        uipy = _output_path(ui)
        if uipy.exists():
            os.remove(uipy)
