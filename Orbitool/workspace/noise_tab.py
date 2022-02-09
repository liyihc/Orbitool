from typing import List, Optional

import numpy as np

from .. import get_config
from ..utils.formula import Formula
from ..structures import BaseStructure, BaseRowItem, field, Row
from ..structures.HDF5 import NdArray
from ..structures.spectrum import Spectrum, SpectrumInfo


class NoiseFormulaParameter(BaseRowItem):
    item_name = "noise formula parameter"
    formula: Formula
    delta: float = 5

    useable: bool = True
    selected: bool = True
    param: NdArray[float, (2, 3)] = field(lambda: np.zeros((2, 3), float))


def default_formula_parameter():
    return [NoiseFormulaParameter(Formula(f)) for f in get_config().noise_formulas]


class NoiseGeneralSetting(BaseStructure):
    h5_type = "noise general setting"

    quantile: float = 0
    mass_dependent: bool = False
    n_sigma: float = 0
    subtract: float = True

    noise_formulas: Row[NoiseFormulaParameter] = field(
        default_formula_parameter)
    params_inited: bool = False

    spectrum_dependent: bool = True

    def get_params(self, useable: bool = False):
        """
        useable params or all params
        return params, points, deltas
        """
        params, points, deltas = [], [], []
        for param in self.noise_formulas:
            if not useable or param.selected:
                params.append(param.param)
                points.append(param.formula.mass())
                deltas.append(param.delta)
        if len(params) > 0:
            params = np.array(params)
        else:
            params = np.zeros([0, 2, 3])
        points = np.array(points)
        deltas = np.array(deltas, dtype=int)

        return params, points, deltas


class NoiseGeneralResult(BaseStructure):
    h5_type = "noise general result"

    poly_coef: np.ndarray = None
    global_noise_std: float = 0
    noise: np.ndarray = None
    LOD: np.ndarray = None


class NoiseTabInfo(BaseStructure):
    h5_type = "noise tab"

    skip: bool = False
    current_spectrum: Spectrum = None

    general_setting: NoiseGeneralSetting = field(NoiseGeneralSetting)

    general_result: NoiseGeneralResult = field(NoiseGeneralResult)

    denoised_spectrum_infos: Row[SpectrumInfo] = field(list)
