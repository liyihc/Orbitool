from __future__ import annotations

import heapq
from datetime import datetime
from typing import List

import numpy as np

from ...structures.base import BaseStructure, BaseTableItem
from ...structures.spectrum import Spectrum
from ...utils.formula import Formula


class Ion(BaseTableItem):
    item_name = "calibration ion"

    shown_text: str
    formula: Formula


class Calibrator(BaseStructure):
    h5_type = "calibrator"

    time: datetime
    ions: List[Ion]
    ions_raw_position: np.ndarray
    ions_raw_intensity: np.ndarray

    ions_position: np.ndarray
    ions_rtol: np.ndarray
    min_indexes: np.ndarray
    max_indexes: np.ndarray

    @classmethod
    def FactoryFromMzInt(cls, time: datetime, ions: List[Ion], ions_raw_position: np.ndarray, ions_raw_intensity: np.ndarray, rtol: float = 5e-6, use_N_ions=None):
        """
        ions_position: shape (len(spectrum), len(ion))
        ions_intensity: shape (len(spectrum), len(ion))
        """
        ions_mz = np.fromiter([ion.formula.mass()
                               for ion in ions], dtype=float)
        ions_position = []
        for index, ion in enumerate(ions_mz):
            position: np.ndarray = ions_raw_position[:, index]
            select: np.ndarray = abs(ion / position - 1) < rtol
            if select.sum():
                position = position[select]
            ions_position.append(position.mean())

        ions_position = np.array(ions_position, dtype=float)

        ions_rtol: np.ndarray = 1 - ions_mz / ions_position

        length = len(ions_rtol)
        if use_N_ions is None or length < use_N_ions:
            use_N_ions = length

        abs_rtol_minarg = abs(ions_rtol).argsort()
        min_indexes = abs_rtol_minarg[:use_N_ions]
        max_indexes = abs_rtol_minarg[use_N_ions:][::-1]

        return Calibrator(time=time, ions=ions, ions_raw_position=ions_raw_position, ions_raw_intensity=ions_raw_intensity, ions_position=ions_position,
                          ions_rtol=ions_rtol, min_indexes=min_indexes, max_indexes=max_indexes)

    def regeneratCalibrator(self, rtol: float = 5e-6, use_N_ions=None) -> Calibrator:
        return self.FactoryFromMzInt(self.time, self.ions, self.ions_raw_position, self.ions_raw_intensity, rtol, use_N_ions)