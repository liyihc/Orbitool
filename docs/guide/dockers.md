# Dockers

The panels around the main tabs are dock widgets. They can be dragged out into
floating windows or stacked:

<img src="img/dockers-draged-out.png" alt="A docker dragged out" width="45%"> <img src="img/dockers-stack.png" alt="Dockers stacked" width="45%">

## Formula

The single formula calculator. **Double-clicking** the result table shows the
natural isotope distribution; double-clicking an isotope row saves that formula
to a peak. See [Formula Calculation](formula.md).

## Mass List

Orbitool uses the mass list to fit peaks and calculate time series.

- Each row is an **mz** and an optional **formula**. If a row has a formula, its
  mz is ignored.
- **group**, **plus**, **minus** — add or subtract a chemical group across the
  whole list.
- **tolerance(ppm)**, **split formula**, **Merge**, **Remove selected**.
- **Import** / **Export** a CSV in this shape:

  | mz | formulas |
  | --- | --- |
  | mz1 | formula1 |
  | mz2 | formula2 |
  | ... | ... |

- **add to mass list** from the [Peak Fit tab](peak-fit.md) (`Alt + A`) fills it.

## Spectra List

The averaged spectra produced by the [Files tab](file-tab.md). **show spectra
after** filters by time; **Select** / **All** export them.

## Spectrum

Plots the currently selected spectrum.

## Peak List

The fitted peaks for the current spectrum.

- Untick **bind to plot** to navigate independently of the [Peak Fit
  plot](peak-fit.md).
- **Double-click** a row to edit the peak; type in **goto** to jump to the
  nearest mass.
- Columns: position, formula, intensity, ppm, area, tag, peaks num.
- **Export**: **Spectrum**, **peaks**, **isotope**.

## Timeseries

Plots the selected time series and exports a single one
(**Export this time series**). See [Timeseries](timeseries.md).
