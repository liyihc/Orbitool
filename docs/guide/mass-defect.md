# Mass Defect Window

Reached from the [Peak Fit tab](peak-fit.md): the **mass defect** button in the
**Actions** group opens a non-modal window for the peaks currently shown there.
Each press opens a **new** window, so you can keep one per spectrum and compare
them side by side.

![Mass defect tab](img/mass-defect-tab.png)

The window works on a **snapshot**: it plots the peaks that were shown in Peak
Fit at the moment it opened, and filtering Peak Fit again afterwards leaves it
unchanged. Its window is named after the source spectrum's time range (or
`Mass Defect Untitled` when there is none), and closing it discards it.

- **Color** — color points by **DBE** or by a specific **Element**'s atom count.
- **show peak without formula** — include unassigned peaks (grey).
- **log intensity** — size points by log intensity instead of intensity.
- **transparency**, **min size**, **max size** — tune the bubble plot.
- **Atoms type** selects which atom count the color scale represents.
- **calc mass defect** recomputes, and **Export** writes the data.

![Mass defect plot](img/massdefect.png)
