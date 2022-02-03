import heapq
from datetime import datetime
from typing import List

import numpy as np

from ...structures import BaseStructure, BaseRowItem, Row
from ...structures.spectrum import Spectrum
from ...utils.formula import Formula


class Ion(BaseRowItem):
    item_name = "calibration ion"

    shown_text: str
    formula: Formula

    @classmethod
    def fromText(cls, text):
        return Ion(shown_text=text, formula=Formula(text))


class Calibrator(BaseStructure):
    """
        ions_raw_position: shape (len(spectrum), len(ions))
        ions_raw_intensity: shape (len(spectrum), len(ions))

        ions_position: shape (len(ions))
        ions_rtol: shape (len(ions))
    """
    h5_type = "calibrator"

    time: datetime
    ions: Row[Ion]
    ions_raw_position: np.ndarray
    ions_raw_intensity: np.ndarray

    ions_position: np.ndarray
    ions_rtol: np.ndarray
    min_indexes: np.ndarray
    max_indexes: np.ndarray

    @classmethod
    def fromMzInt(cls, time: datetime, ions: List[Ion], ions_raw_position: np.ndarray, ions_raw_intensity: np.ndarray, rtol: float = 5e-6, use_N_ions=None):
        """
        ions_raw_position: shape (len(spectrum), len(ions))
        ions_raw_intensity: shape (len(spectrum), len(ions))
        """
        ions_mz = np.fromiter([ion.formula.mass()
                               for ion in ions], dtype=float)
        ions_position = []
        for index, ion in enumerate(ions_mz):
            position: np.ndarray = ions_raw_position[:, index]
            select: np.ndarray = abs(ion / position - 1) < rtol
            select &= ~np.isnan(position)
            if select.sum():
                ions_position.append(position[select].mean())
            else:
                ions_position.append(np.nan)

        ions_position = np.array(ions_position, dtype=float)

        ions_rtol: np.ndarray = 1 - ions_mz / ions_position

        length = len(ions_rtol)
        if use_N_ions is None or length < use_N_ions:
            use_N_ions = length

        abs_rtol_minarg = abs(ions_rtol).argsort()
        min_indexes = abs_rtol_minarg[:use_N_ions]
        max_indexes = abs_rtol_minarg[use_N_ions:][::-1]

        if np.isnan(ions_rtol[min_indexes]).sum():
            missing = [ion.shown_text for ion, slt in zip(
                ions, np.isnan(ions_rtol)) if slt]
            raise ValueError(
                f"Cannot find enough ions to fit, missing ions: {missing}")

        return Calibrator(time, ions, ions_raw_position, ions_raw_intensity, ions_position,
                          ions_rtol, min_indexes, max_indexes)

    def regeneratCalibrator(self, rtol: float = 5e-6, use_N_ions=None):
        return self.fromMzInt(self.time, self.ions, self.ions_raw_position, self.ions_raw_intensity, rtol, use_N_ions)
