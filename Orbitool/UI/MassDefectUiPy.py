import csv
import math
from typing import Optional, Union

import numpy as np
from matplotlib.cm import rainbow as rainbow_color_map
from matplotlib.figure import Figure
from PySide6 import QtCore, QtWidgets

from Orbitool.models.spectrum import FittedPeak
from Orbitool.models.workspace.massdefect import Clr, Gry
from . import MassDefectUi
from .component import Plot
from .manager import Manager, ui_task
from .utils import savefile


class Widget(QtWidgets.QWidget):
    def __init__(self, manager: Manager) -> None:
        super().__init__()
        self.manager = manager

        self.ui = MassDefectUi.Ui_Form()
        self.setupUi()
        self.plot = Plot(self.ui.widget)

        self.peaks: list[FittedPeak] = []
        # each window is independent and never persisted to the workspace, so
        # its plot state lives here rather than in the workspace info
        self.clr_title = ""
        self.clr = Clr()
        self.gry = Gry()

    def set_peaks(self, peaks):
        """Adopt the caller's already-deep-copied snapshot and draw it.

        The window reads only this snapshot, so it never sees later Peak Fit
        filtering; each open hands in a fresh copy.
        """
        self.peaks = peaks
        self.calculateMassDefect()
        self.plotMassDefect()

    def setupUi(self):
        ui = self.ui
        ui.setupUi(self)

        ui.calcPushButton.clicked.connect(self.calc)
        ui.exportPushButton.clicked.connect(self.export)

        ui.transparencyDoubleSpinBox.valueChanged.connect(self.replot)
        ui.logCheckBox.toggled.connect(self.replot)
        ui.showGreyCheckBox.toggled.connect(self.replot)
        ui.minSizeHorizontalSlider.valueChanged.connect(self.replot)
        ui.maxSizeHorizontalSlider.valueChanged.connect(self.replot)

    def closeEvent(self, a0) -> None:
        wins = self.manager.mass_defect_wins
        if self in wins:
            wins.remove(self)
        a0.accept()

    @ui_task
    async def calc(self):
        self.calculateMassDefect()
        self.plotMassDefect()

    def calculateMassDefect(self):
        ui = self.ui
        is_dbe = ui.dbeRadioButton.isChecked()
        is_ele = ui.elementRadioButton.isChecked()
        is_atom = ui.atomsRadioButton.isChecked()

        peaks = self.peaks

        clr_peaks = [peak for peak in peaks if len(peak.formulas) > 0]
        clr_formula = list(map(find_formula, clr_peaks))

        if is_dbe:
            clr_color = [f.dbe() for f in clr_formula]
            clr_color = np.array(clr_color, dtype=float)
            clr_labels = None
        elif is_ele:
            element = ui.elementLineEdit.text()
            clr_color = [f[element] for f in clr_formula]
            clr_color = np.array(clr_color, dtype=int)
            clr_labels = None
        elif is_atom:
            atoms = {f.atoms() for f in clr_formula}
            atoms = list(atoms)
            atoms.sort(key=lambda f: (len(f), f.mass()))
            atoms_index = {atom: ind for ind, atom in enumerate(atoms)}
            clr_color = [atoms_index[f.atoms()] for f in clr_formula]
            clr_color = np.array(clr_color, dtype=int)
            clr_labels = list(map(str, atoms))

        clr_x = [peak.peak_position for peak in clr_peaks]
        clr_x = np.array(clr_x, dtype=float)
        clr_y = clr_x - np.round(clr_x)
        clr_size = np.array(
            [peak.peak_intensity for peak in clr_peaks], dtype=float)

        gry_peaks = [peak for peak in peaks if len(peak.formulas) == 0]
        gry_x = np.array([peak.peak_position for peak in gry_peaks])
        gry_y = gry_x - np.round(gry_x)
        gry_size = np.array([peak.peak_intensity for peak in gry_peaks])

        self.clr_title = ""
        if is_dbe:
            self.clr_title = "DBE"
        elif is_ele:
            self.clr_title = element
        elif is_atom:
            self.clr_title = "atoms"

        self.clr = Clr(x=clr_x, y=clr_y, size=clr_size,
                       color=clr_color, labels=clr_labels or [])
        self.gry = Gry(x=gry_x, y=gry_y, size=gry_size)

    def plotMassDefect(self):
        plot = self.plot
        plot.clear()

        ui = self.ui
        clr = self.clr
        gry = self.gry
        show_gry = ui.showGreyCheckBox.isChecked() and len(gry.x) > 0

        if len(clr.x) == 0 and not show_gry:
            return

        if ui.minSizeHorizontalSlider.value() > ui.maxSizeHorizontalSlider.value():
            ui.minSizeHorizontalSlider.setValue(
                ui.maxSizeHorizontalSlider.value())  # will call replot
            return

        min_factor = math.exp(
            ui.minSizeHorizontalSlider.value() / 10) * 10
        max_factor = math.exp(
            ui.maxSizeHorizontalSlider.value() / 10) * 10

        is_log = ui.logCheckBox.isChecked()
        alpha = 1 - ui.transparencyDoubleSpinBox.value()

        clr_size = clr.size
        gry_size = gry.size

        if is_log:
            clr_size = np.log(clr_size + 1) - 1
            gry_size = np.log(gry_size + 1) - 1

        all_size = np.concatenate([clr_size, gry_size]) if show_gry else clr_size
        maximum = all_size.max()
        minimum = all_size.min()

        if maximum == minimum:
            # a single point (or identical sizes) would divide by zero and
            # produce NaN scatter sizes, which crashes the renderer
            maximum = minimum + 1

        # if is_log:
        #     maximum /= 70
        # else:
        #     maximum /= 200
        # maximum /= max_factor
        # minimum = 5 * min_factor

        ax = plot.ax
        if show_gry:
            gry_size = (gry_size - minimum) / (maximum - minimum) * \
                (max_factor - min_factor) + min_factor
            ax.scatter(gry.x, gry.y, s=gry_size, c='grey',
                       linewidths=0.5, edgecolors='k', alpha=alpha)

        if len(clr.x) > 0:
            clr_size = (clr_size - minimum) / (maximum - minimum) * \
                (max_factor - min_factor) + min_factor
            sc = ax.scatter(clr.x, clr.y, s=clr_size, c=clr.color,
                            cmap=rainbow_color_map, linewidths=0.5, edgecolors='k', alpha=alpha)
            clrb = plot.fig.colorbar(sc)
            clrb.ax.set_title(self.clr_title)
            if clr.labels:
                clrb.ax.set_yticklabels(clr.labels)

        ax.autoscale(True)
        plot.fig.tight_layout()

        plot.canvas.draw()

    @ui_task(mode="light")
    async def replot(self):
        ax = self.plot.ax
        x = ax.get_xlim()
        y = ax.get_ylim()
        self.plotMassDefect()
        ax = self.plot.ax
        ax.set_xlim(*x)
        ax.set_ylim(*y)
        self.plot.canvas.draw()

    @ui_task
    async def export(self):
        ret, f = savefile("Mass Defect", "CSV file(*.csv)", self.clr_title)

        if not ret:
            return

        if self.clr_title == "atoms":
            atoms = self.clr.labels

            def conv(value):
                return atoms[value]
        else:
            def conv(value):
                return value

        with open(f, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['x', 'mass defect', 'intensity', 'color'])

            writer.writerows(zip(self.clr.x, self.clr.y,
                                 self.clr.size, map(conv, self.clr.color)))
            writer.writerows(zip(self.gry.x, self.gry.y, self.gry.size))


def find_formula(peak: FittedPeak):
    tols: np.ndarray = abs(
        np.array([peak.peak_position / f.mass() - 1 for f in peak.formulas]))
    argmin = tols.argmin()
    return peak.formulas[argmin]
