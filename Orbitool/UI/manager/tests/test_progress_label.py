from PyQt6 import QtWidgets

from ..manager import Manager

# a QApplication with no references gets destroyed mid-session; keep one alive
app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def test_progress_label_stays_unique_across_busy_transitions():
    manager = Manager()
    labels = []
    manager.tqdm.tqdm_signal.connect(
        lambda label, percent, msg: labels.append(label))

    first = manager.tqdm(msg="read", length=1)
    first.update()

    manager.set_busy(True)
    manager.set_busy(False)

    second = manager.tqdm(msg="write", length=1)
    second.update()
    third = manager.tqdm(msg="process", length=1)
    third.update()

    assert len(labels) == 3
    assert labels == sorted(set(labels))
    assert labels[0] < labels[1] < labels[2]
