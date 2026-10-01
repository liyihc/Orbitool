import logging

import pytest

from ..manager import MySignal


def test_emit_runs_remaining_handlers_after_one_fails():
    signal = MySignal()
    calls = []

    def first():
        calls.append("first")
        raise ValueError("first failed")

    def second():
        calls.append("second")

    signal.connect(first)
    signal.connect(second)

    with pytest.raises(ValueError, match="first failed"):
        signal.emit()

    assert sorted(calls) == ["first", "second"]


def test_emit_logs_the_error_it_swallows_when_several_fail(caplog):
    # handlers live in a set, so which error propagates is unspecified; both
    # must run, one propagates, the other is logged instead of vanishing
    signal = MySignal()
    calls = []

    def first():
        calls.append("first")
        raise ValueError("first failed")

    def second():
        calls.append("second")
        raise TypeError("second failed")

    signal.connect(first)
    signal.connect(second)

    with caplog.at_level(logging.ERROR, logger="Orbitool"):
        with pytest.raises((ValueError, TypeError)) as excinfo:
            signal.emit()

    assert sorted(calls) == ["first", "second"]
    messages = [record.getMessage() for record in caplog.records]
    propagated = str(excinfo.value)
    swallowed = {"first failed", "second failed"} - {propagated}
    assert messages == list(swallowed)


def test_emit_without_failures_passes_arguments_through():
    signal = MySignal()
    calls = []

    def handler(*args, **kwargs):
        calls.append((args, kwargs))

    signal.connect(handler)
    signal.emit(1, key="value")

    assert calls == [((1,), {"key": "value"})]
