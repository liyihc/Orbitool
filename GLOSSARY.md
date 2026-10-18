# Orbitool

Orbitool is a Windows desktop GUI tool for processing Thermo Fisher mass-spec
(`.RAW`) data: denoise → peak shape → calibration → peak fitting → formula /
mass defect / time series.

## Mass List

**Mass List**:
The workspace's ordered list of m/z rows, each carrying an optional formula, used
to fit peaks and build time series.
_Avoid_: mass table, peak list

**Import** (mass list):
Replace the current Mass List with the rows read from a CSV.
_Avoid_: load, open

**Merge** (mass list):
Union a CSV's rows into the current Mass List; within tolerance an entry joins an
existing row, otherwise it is inserted.
_Avoid_: append, combine

**Compare** (mass list):
Preview Import and Merge against the current Mass List side by side, then commit
one of the three as the new Mass List.
_Avoid_: diff, versus

**Tolerance** (mass list):
The relative m/z window in which two rows are considered the same mass;
entered in ppm. Governs Add, Import, Merge and Compare alike.
_Avoid_: precision, resolution

## Peak Fit

**Segment** (Peak Fit):
A raw peak from the fit input. Its split fitted peaks form one contiguous group
in the Peak List, and one Peak Fit window edits that group.
_Avoid_: big peak, cluster

**Peak Fit window**:
The window for one segment: re-fit its fitted peaks, assign their formulas, and
commit the result with **Save**.
_Avoid_: popup, peak editor

**Formula** (Peak Fit window):
A fitted peak's saved formula assignment, as stored in the Peak List.
_Avoid_: old formula, original formula

**New formula**:
A fitted peak's uncommitted formula assignment in a Peak Fit window; it replaces
**Formula** for that peak on **Save**.
_Avoid_: edited formula, pending formula

**Theoretical ratio**:
The natural isotope abundance of an isotope relative to the origin formula,
shown in the isotope table.
_Avoid_: abundance
