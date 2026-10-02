from typing import List, Tuple
from multiprocessing import freeze_support
from time import sleep

from PyQt6 import QtWidgets, QtCore
from .. import MultiProcess, Manager, Thread
from ..thread import EXCEPTION, RESULT
from Orbitool import setting


class p(MultiProcess):
    @staticmethod
    def func(input):
        return input

    @staticmethod
    def read(file, length):
        for i in range(length):
            yield i

    @staticmethod
    def read_len(file, length) -> int:
        return length

    @staticmethod
    def write(file, rets):
        target = []
        file["ret"] = target
        cnt = 0
        for ret in rets:
            target.append(ret)
            cnt += 1
        return cnt

    @staticmethod
    def exception(file, **kwargs):
        file.pop("ret", None)


class slow_p(p):
    @staticmethod
    def func(input):
        sleep(0.01)
        return input


class abort_p(slow_p):
    rollback_calls = 0

    @staticmethod
    def exception(file, **kwargs):
        abort_p.rollback_calls += 1
        file.pop("ret", None)


# freeze_support()


# a QApplication with no references gets destroyed mid-session; keep one alive
app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def test_single():
    old = setting.debug.NO_MULTIPROCESS
    setting.debug.NO_MULTIPROCESS = True
    try:
        file = {}
        pp = p(file, {"length": 20})
        pp.start()
        pp.wait()
        assert pp.result[0] == RESULT, pp.result
        assert pp.result[1] == 20
        assert file == {"ret": list(range(20))}
    finally:
        setting.debug.NO_MULTIPROCESS = old


def test_abort():
    old = setting.debug.NO_MULTIPROCESS
    setting.debug.NO_MULTIPROCESS = True
    try:
        abort_p.rollback_calls = 0
        file = {}
        pp = abort_p(file, {"length": 60})
        notifications = []
        pp.result_ready.connect(lambda t: notifications.append(t))

        pp.start()
        # 60 * 10ms floor keeps the run in flight for ~600ms, so aborting
        # after a short pause deterministically lands mid-run
        QtCore.QThread.msleep(50)
        pp.abort()
        pp.wait()

        assert len(notifications) == 1, notifications
        channel, payload = notifications[0]
        assert channel == EXCEPTION and isinstance(payload, RuntimeError)
        assert pp.aborted
        assert pp.result[0] == EXCEPTION
        assert abort_p.rollback_calls == 1
        assert file == {}
    finally:
        setting.debug.NO_MULTIPROCESS = old


def test_abort_sets_flag_before_notifying():
    pp = p({}, {"length": 1})
    seen = []
    pp.result_ready.connect(lambda t: seen.append(pp.aborted))
    pp.abort()
    assert seen == [True]


def test_completion_then_abort_notifies_once():
    pp = p({}, {"length": 1})
    notifications = []
    pp.result_ready.connect(lambda t: notifications.append(t))

    pp.finished_emit((RESULT, 7))
    pp.abort()

    assert notifications == [(RESULT, 7)]
    assert pp.result == (RESULT, 7)
    assert pp.aborted


def test_abort_then_completion_notifies_once():
    pp = p({}, {"length": 1})
    notifications = []
    pp.result_ready.connect(lambda t: notifications.append(t))

    pp.abort()
    pp.finished_emit((RESULT, 7))

    assert len(notifications) == 1
    channel, payload = notifications[0]
    assert channel == EXCEPTION and isinstance(payload, RuntimeError)
    assert pp.result == notifications[0]


def test_natural_completion_then_abort_does_not_roll_back():
    abort_p.rollback_calls = 0
    pp = abort_p({}, {"length": 1})

    pp.finished_emit((RESULT, 7))
    pp.abort()  # suppressed: the completion notification already won
    pp._finish_cleanup()

    assert abort_p.rollback_calls == 0


def test_abort_winning_the_notification_rolls_back():
    abort_p.rollback_calls = 0
    pp = abort_p({}, {"length": 1})

    pp.abort()
    pp.finished_emit((RESULT, 7))  # suppressed
    pp._finish_cleanup()

    assert abort_p.rollback_calls == 1


def test_abort_multiprocess_rollback():
    old_mp = setting.debug.NO_MULTIPROCESS
    old_cores = setting.general.multi_cores
    setting.debug.NO_MULTIPROCESS = False
    setting.general.multi_cores = 1
    try:
        abort_p.rollback_calls = 0
        file = {}
        pp = abort_p(file, {"length": 60})
        notifications = []
        pp.result_ready.connect(lambda t: notifications.append(t))

        pp.start()
        for _ in range(500):
            if "ret" in file:
                break
            QtCore.QThread.msleep(10)
        assert "ret" in file, "run did not reach the write stage"
        pp.abort()
        pp.wait()

        assert len(notifications) == 1, notifications
        channel, payload = notifications[0]
        assert channel == EXCEPTION and isinstance(payload, RuntimeError)
        assert abort_p.rollback_calls == 1
        assert file == {}
    finally:
        setting.debug.NO_MULTIPROCESS = old_mp
        setting.general.multi_cores = old_cores


def test_thread_emits_result_ready_with_tuple_and_qthread_finished_fires():
    thread = Thread(lambda: 0)
    ready = []
    finished = []
    thread.result_ready.connect(lambda t: ready.append(t))
    thread.finished.connect(lambda: finished.append(1))

    thread.start()
    thread.wait()
    for _ in range(100):
        app.processEvents()
        if ready and finished:
            break
        QtCore.QThread.msleep(1)

    assert ready == [(RESULT, 0)]
    assert finished == [1]

