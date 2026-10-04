
# Orbitool

Orbitool is a Windows desktop tool for processing Thermo Fisher Orbitrap mass
spectrometry (`.RAW`) data. It covers the whole workflow from raw spectra to
interpretable results:

> spectrum averaging → denoising → peak shape → calibration → peak fitting →
> formula / mass defect / time series

It is built with PyQt6 and stores its data in HDF5 workspaces (`.Orbitool`
files). It is aimed at atmospheric and environmental chemistry researchers.

## Get started

Download and open `Orbitool.exe` from the
[download page](https://orbitrap.catalyse.cnrs.fr/download-link/). If you have
never used Orbitool or an online MS instrument for atmospheric work, follow the
steps below.

![Drag and drop files](docs/guide/img/dragdrop-files.gif)

1. **Files** — drag in one or more `.RAW` files (or a folder) and choose the
   polarity of your spectra.
2. **All file(s)** (`Return`) to build the spectra list, or **Selected file(s)**
   (`Alt + S`) for just the highlighted rows. Configure averaging first if you
   want it (every N time/scan periods, or a custom set).
3. **Noise** — select a spectrum, **Calc noise for the selected spectrum**
   (`Alt + C`), then **denoise** (`Return`).
4. **Peak Shape** — review the peaks used to estimate width, remove outliers,
   then **Finish and continue** (`Return`).
5. **Calibration** — add reference ions, **Calc calibrate info** (`Alt + C`),
   then **Calibrate and continue** (`Return`).
6. **Peak Fit** — filter the peaks, **Fit**, and tag the results.
7. **Mass Defect** / **Timeseries** — explore and export the final data.

Full details, tab by tab, are in the [user guide](docs/guide/index.md). Common
problems are in the [FAQ](docs/guide/faq.md).

## Tips

- When processing large files, save the workspace to disk early
  (**Workspace → Save as**) to save memory.
- Running Orbitool writes `setting.json` and `log.txt` next to the executable.

## Documentation

- [User guide](docs/guide/index.md) — the interface and each processing step.
- [Development](docs/dev/development.md) — build, run and test.
  [Build environment](docs/dev/build-environment.md) — toolchain setup.
- [Changelog](CHANGELOG.md).

## Maintain

### Maintainer

The program is developed and maintained by students of Shanghai Jiao Tong
University. Runlong acts as a chemical advisor during program development.

- Developer: Yihao Li <liyihc@outlook.com>
- Chemical advisor: Runlong Cai

### Contributors

- State Environmental Protection Key Laboratory of Formation and Prevention of
  Urban Air Pollution Complex, Shanghai Academy of Environmental Sciences,
  Shanghai, 200233, China
- Univ. Lyon, Université Claude Bernard Lyon 1, CNRS, IRCELYON, F-69626,
  Villeurbanne, France.
- Institute for Atmospheric and Earth System Research / Physics, Faculty of
  Science, University of Helsinki, Helsinki, 00140, Finland.

### Bug reports and feature requests

If you meet any bugs, please let us know. Send the `log.txt` file that sits next
to `Orbitool.exe`, and a description of the issue, to:

- "Matthieu Riva" <matthieu.riva@ircelyon.univ-lyon1.fr>
- "Cheng Huang" <huangc@saes.sh.cn>
