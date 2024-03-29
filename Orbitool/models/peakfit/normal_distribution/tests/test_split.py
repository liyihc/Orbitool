from ..normal_distribution import NormalDistributionFunc
from .....models.spectrum import Peak
import pandas as pd
import pathlib

root = pathlib.Path(__file__).parent


def test_split():
    func = NormalDistributionFunc(
        peak_fit_sigma=2.852197450904393e-06,
        peak_fit_res=148889.02590153966)
    data = pd.read_csv(root.joinpath("peak_1.csv"))
    peak = Peak(mz=data["mz"], intensity=data["intensity"])
    peaks = func.splitPeak(peak)
