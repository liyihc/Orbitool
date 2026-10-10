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
