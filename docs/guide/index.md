# Orbitool User Guide

Orbitool processes Thermo Fisher Orbitrap `.RAW` mass spectra: spectrum averaging,
denoising, calibration, peak fitting, formula calculation, mass defect and time
series. The workflow runs left to right through the tabs.

New here? Start with the [quick start in the README](../../readme.md). This guide
goes tab by tab; screenshots live in [`img/`](img/).

## Workflow

```
Files ─▶ Noise ─▶ Peak Shape ─▶ Calibration ─▶ Peak Fit ─▶ Timeseries
 (average)  (denoise)            (per-file)     (fit)         (analysis)
```

Each tab's **Finish and continue** button hands the result to the next tab. After
Calibration the analysis tabs are independent; the Mass Defect window is opened
from Peak Fit.

## Pages

| Page | What it covers |
| --- | --- |
| [Files Tab](file-tab.md) | Import RAW files, average them, build a spectra list |
| [Noise Tab](noise.md) | Calculate noise/LOD, denoise, skip denoising |
| [Peak Shape Tab](peak-shape.md) | Estimate peak width from selected peaks |
| [Calibration Tab](calibration.md) | Calibrate each file, optionally by mass segment |
| [Peak Fit Tab](peak-fit.md) | Fit peaks, filter them, tag them |
| [Mass Defect Window](mass-defect.md) | Mass-defect plots colored by DBE/element (opened from Peak Fit) |
| [Timeseries Tab](timeseries.md) | Extract intensity time series |
| [Formula Calculation](formula.md) | Formula input/output and search settings |
| [Dockers](dockers.md) | The Spectra List / Peak List / Mass List panels |
| [Workspace & Options](workspace.md) | Save/load workspaces and configuration |
| [FAQ](faq.md) | Common problems |

Developer and build documentation lives in [`../dev/`](../dev/).
