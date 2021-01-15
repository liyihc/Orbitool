from . import HDF5


class Peak(HDF5.Group):
    h5_type = HDF5.RegisterType("Peak")
    mz = HDF5.SmallNumpy()
    intensity = HDF5.SmallNumpy()
    splitNum = HDF5.Int()


class FittedPeak(Peak):
    h5_type = HDF5.RegisterType("FittedPeak")

    fitted_param = HDF5.SmallNumpy()
    peak_position = HDF5.SmallNumpy()
    peak_intensity = HDF5.SmallNumpy()
    formula_list = HDF5.SmallNumpy()


class Spectrum(HDF5.Group):
    h5_type = HDF5.RegisterType("Spectrum")
    fileTime = HDF5.Datetime()
    mz = HDF5.BigNumpy()
    intensity = HDF5.BigNumpy()
    startTime = HDF5.Datetime()
    endTime = HDF5.Datetime()