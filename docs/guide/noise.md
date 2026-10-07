# Noise Tab

Calculate a noise level and LOD per spectrum, then denoise.

![Noise tab](img/noise-tab.png)

## Calculate

- **Calc noise for the selected spectrum** (`Alt + C`) computes the noise/LOD for
  the current spectrum.
- ![NO3- noise](img/nitrate-noise.png)
  Some points have larger noise (for example `NO3-`, `HN2O6-`). Add them under
  **Noise for high-intensity peaks** and calculate them independently, with a
  `delta(integer)` offset from a formula.
- The **Noise results** table is read-only: it shows the global noise/LOD and one
  row per noise mass point, exactly as the last calculation produced them. Change
  the inputs and press **Calc noise** again to update it.
- Double-click the **type** column in the results table to scale the figure to
  that noise.

### Global noise algorithm

Global noise is computed with a modified binPMF:

1. Build a *noise set* of all peaks in `[x.5 ~ x.8]`.
2. Delete peaks larger than `mean + N·σ` of the noise set.
3. Use `quantile + N·σ` of the noise set as the LOD line. (At `quantile = 0.7`
   the quantile value is close to the mean.)
4. Delete peaks below the LOD from the original spectrum to get the denoised
   spectrum.

Parameters: **quantile**, **N sigma**, and **size-dependent** handling.

**size-dependent** fits the global noise baseline as a line in m/z rather than a
single flat level. It shapes the fit only; it does not decide whether each
spectrum is fit separately.

## Denoise

- **denoise** (`Return`) reads all files and stores denoise information. The
  real denoise runs *after calibration*, because files differ.
- **Subtract noise level from peaks** removes the noise level from the kept
  peaks.
- **Spectrum-dependent params** fits each calibrated spectrum its own noise
  parameters. Untick it to reuse the parameters calculated here for every
  spectrum. Either way, unless denoise is skipped the [Calibration
  tab](calibration.md) records each spectrum's noise/LOD table for the [Spectra
  List](dockers.md) export.
- **Scale to spectrum** / **rescale** and the `×2 (↑)` / `÷2 (↓)` controls
  adjust the plot y-range (`Up`/`Down` shortcuts).

### Skipping denoise

If you do not want to denoise at all, press **skip** (`Alt + P`). If you want to
denoise only around certain mass points, set global noise and LOD to `-1`.

### Damaged files

A `.RAW` can contain a scan whose FT profile is empty — a damaged or interrupted
acquisition. Such a scan cannot be averaged, so it is left out of its window (the
window keeps its other scans) instead of failing the whole read. Nothing else about
the scan looks wrong: its TIC and every acquisition field match the healthy scans.

Every read reports what it had to repair. Each **denoise** or **skip** run ends by
listing the files it found damaged in a **Damaged .RAW files** dialog, and pressing
**show average** says so the same way — nothing is ever repaired silently. The list
belongs to that read only: it is shown once and then forgotten, so a later read repairs
the same file again and reports it again. `log.txt` is the permanent record.

## Export

All four write a CSV for the spectrum currently shown on the tab.

- **Spectrum** (`Ctrl + Alt + S`) — the raw selected/averaged spectrum.
- **Denoised spectrum** (`Ctrl + Alt + D`)
- **Noise peaks** (`Ctrl + Alt + N`)
- **Noise & LOD** (`Ctrl + Alt + L`) — the same global + per-mass-point table the
  **Noise results** table shows, as `formula, mass, noise, LOD` columns.

The per-spectrum tables for *every* calibrated spectrum are exported from the
[Spectra List](dockers.md), not here.
