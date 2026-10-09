"""Separating a calibration segment must not discard edited parameters.

`separate` (`Widget.addSegment`) mutates the segment list, so the widget must
commit the current spin-box values first -- as `changeSegment` and `calcInfo`
already do -- and then keep `current_segment_index` pointing at the logical
segment the user was editing.
"""
import importlib

import pytest

# debug_settings is an autouse fixture re-exported for pytest
from .migration_harness import MigrationEnv, debug_settings  # noqa: F401

calibration_module = importlib.import_module("Orbitool.UI.CalibrationUiPy")


@pytest.fixture
def env(request):
    state = MigrationEnv().build(
        request, extra_dialog_modules=(calibration_module,))
    state.reset()
    yield state


def _separator(widget, fraction):
    info = widget.manager.workspace.info.formula_docker
    return info.mz_min + (info.mz_max - info.mz_min) * fraction


def test_separate_keeps_edited_parameters(env):
    widget = env.window.calibrationTab
    assert len(widget.info.calibrate_info_segments) == 1
    assert widget.info.current_segment_index == 0

    widget.ui.degreeSpinBox.setValue(4)
    widget.ui.separatorDoubleSpinBox.setValue(_separator(widget, 0.5))
    widget.addSegment()

    segments = widget.info.calibrate_info_segments
    assert [seg.degree for seg in segments] == [4, 4]
    assert widget.ui.degreeSpinBox.value() == 4
    assert widget.info.current_segment_index == 1


def test_separate_before_current_keeps_current_segment(env):
    widget = env.window.calibrationTab
    first = _separator(widget, 0.66)
    second = _separator(widget, 0.33)

    widget.ui.separatorDoubleSpinBox.setValue(first)
    widget.addSegment()
    widget.ui.degreeSpinBox.setValue(5)

    widget.ui.separatorDoubleSpinBox.setValue(second)
    widget.addSegment()

    info = widget.info
    segments = info.calibrate_info_segments
    assert [seg.end_point for seg in segments] == pytest.approx(
        [second, first, float("inf")])
    assert info.current_segment_index == 2
    assert segments[info.current_segment_index].degree == 5
    assert widget.ui.degreeSpinBox.value() == 5
