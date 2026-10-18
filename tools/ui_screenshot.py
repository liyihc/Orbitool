"""Render a Qt widget to a PNG without opening a desktop window.

Usage (from the repo root):

    $env:QT_QPA_PLATFORM = "offscreen"
    uv run python tools/ui_screenshot.py BUILDER.py OUT.png [--size 1000x700]

`BUILDER.py` defines `build() -> QWidget`. It may import `Orbitool` as usual;
this script puts the repo root on `sys.path`. A minimal builder:

    from Orbitool.UI.MainUiPy import Window

    def build():
        return Window()

For a window that needs workspace data, reuse the setup from the offscreen
tests (`Orbitool/UI/tests/migration_harness.py` and the `_install_*` helpers in
`Orbitool/UI/tests/test_peak_fit_float.py`). This is an opt-in debugging tool:
no test runs it and no image is written unless it is invoked explicitly.
"""
import argparse
import importlib.util
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6 import QtWidgets  # noqa: E402


def _load_builder(path: Path):
    spec = importlib.util.spec_from_file_location("ui_screenshot_builder", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load builder: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    build = getattr(module, "build", None)
    if not callable(build):
        raise SystemExit(f"{path} must define build() -> QWidget")
    return build


def _parse_size(text: str):
    width, _, height = text.partition("x")
    return int(width), int(height)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("builder", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--size", type=_parse_size,
                        help="resize the widget before grabbing, e.g. 1000x700")
    args = parser.parse_args()

    build = _load_builder(args.builder)
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    widget = build()
    widget.show()
    app.processEvents()
    if args.size is not None:
        widget.resize(*args.size)
        app.processEvents()
    pixmap = widget.grab()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if not pixmap.save(str(args.output)):
        raise SystemExit(f"failed to save {args.output}")
    print(f"saved {args.output} ({pixmap.width()}x{pixmap.height()})")
    widget.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
