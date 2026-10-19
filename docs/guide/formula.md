# Formula Calculation

The **Formula** item in the menu bar opens this calculator as a window.

## Formula format

### Input

Examples Orbitool understands:

- `H2O`
- `HH[2]O`
- `NO3-`
- `NH4+`
- `SO4-2`
- `SO4e-2`
- `Ca+2`
- `C6(H2O)6`
- `na2 s2 o 3`

`[..]` selects a specific isotope (for example `H[2]` is deuterium). `e` is the
electron.

### Output

Examples of the formulas Orbitool emits:

- `H2O`
- `HH[2]O`
- `NO3-`
- `NH4+`
- `SO4-2` (never `SO4e-2`, to avoid ambiguity with `Ne-3`)

## Settings

Formula guessing is controlled by:

- **charge**
- **mz min** / **mz max** — currently only a limit when fitting spectra.
- **tolerance(ppm)**
- **DBE limit** — **enable Nitrogen Rule** (DBE must be an integer) and
  **enable DBE limit and O H limit**.
- **global limit** — the sum of isotopes marked with "global limit" will not
  exceed this value.
- **isotopes** — the elements/isotopes used, each with **min**/**max** and
  **attrs**.
- **element infos** — per-element parameters, edited in the table.

## Calculate

You can input a **formula** or a **mass**:

- A **formula** returns its mass (including the electron).
- A **mass** returns the matching formula candidate(s) in the result window.

In the result window:

- Candidate formulas are on the left and selected as whole rows. **Show actual
  distribution of selected formula** (or double-clicking a row) fills the
  isotope table on the right. The nearest candidate is selected automatically
  when the window opens or **Calc** runs.
- The isotope table has one column per isotope. Rows are `formula` (the column
  title), `distribution`, `mass`, `tolerance(ppm)`, **theoretical ratio**
  (abundance relative to the origin formula), **actual intensity** and **actual
  ratio**. The `distribution` row plots that isotope's raw peak, cropped to the
  peak's own m/z span, and prints the theoretical and actual peak heights; the
  isotope formula is in the `formula` row. Its vertical scale is set
  independently to the taller of the raw peak and the theoretical height, so
  compare raw and theoretical heights within one column, not between columns.
- Isotopes with no peak within tolerance still get a column with their
  `formula`, `mass`, **theoretical ratio** and a theoretical-only plot; the
  `tolerance(ppm)`, **actual intensity** and **actual ratio** rows stay empty,
  and that column cannot open a peak editor.
- **Edit selected peak's formula** (or double-clicking an isotope column) writes
  that formula to the nearest peak in the whole Peak List; the matching peak may
  belong to another segment.
- Opened from the [Peak Fit window](peak-fit.md#formula-result-window), the
  window is bound to one peak: its m/z is in the title, the input is read-only,
  and **Calc** recalculates candidates after formula-setting changes.
  **Delete formula** clears the peak's assignment, **Use selected formula**
  replaces it with the selected candidates, and **Close** leaves it unchanged.
- The menu-opened calculator has no peak to accept into, so only **Close** is
  shown.

## Isotope number limit

The limit on an element's count is the sum of *element atoms + isotope atoms +
global limit*:

- **Element number limit** — the range of the total number of atoms of that
  element.
- **Isotope number limit** — the range of atoms of a *particular* isotope, such
  as `C[12]`, `C[13]`, `H[1]`, `H[3]`.
- **Global limit** — isotopes flagged "global limit" share this cap, useful to
  bound rare isotopes. If you have many rare isotopes in your experiment, do not
  flag that element with **global limit**.

## Element info and calculation method

Each element (the electron is treated as a special element) has five editable
parameters; some are fixed for some elements:

- **2*DBE** — twice the element's effect on DBE.
- **H min**, **H max** — ability to replace H.
- **O min**, **O max** — ability to replace O.

Built-in element parameters:

| | 2*DBE | H min | H max | O min | O max |
| --- | --- | --- | --- | --- | --- |
| initial | 2 | 2 | 2 | 0 | 0 |
| e | -1 | -1 | -1 | 0 | 0 |
| C | 2 | 0 | 2 | 0 | 3 |
| H | -1 | -1 | -1 | 0 | 0 |
| O | 0 | 0 | 0 | -1 | -1 |
| N | 1 | -1 | 1 | 0 | 3 |
| S | 0 | 0 | 0 | 0 | 4 |
| Li | -1 | 0 | 0 | 0 | 0 |
| Na | -1 | 0 | 0 | 0 | 0 |
| K | -1 | 0 | 0 | 0 | 0 |
| F | -1 | -1 | 0 | 0 | 0 |
| Cl | -1 | -1 | 0 | 0 | 3 |
| Br | -1 | -1 | 0 | 0 | 3 |
| I | -1 | -1 | 0 | 0 | 3 |
| P | 1 | -1 | 1 | 0 | 6 |
| Si | 2 | 0 | 2 | 0 | 3 |

Constraints:

| | min | max |
| --- | --- | --- |
| DBE | 0 | 8 |
| H | 0 | 40 |
| O | 0 | 15 |

### Example

For the partial formula `C10N-`:

- Minimum O:

$$
\max(0_{O:min},\ 0_{initial:Omin} + 10\cdot 0_{C:Omin} + 1\cdot 0_{N:Omin}) = 0
$$

- Maximum O:

$$
\min(15_{O:max},\ 0_{initial:Omax} + 10\cdot 3_{C:Omax} + 1\cdot 3_{N:Omax}) = 15
$$

The program iterates O from 0 to 15. If O is 11, the part becomes `C10O11N-`:

- Minimum H:

$$
\max(0_{H:min},\ 1\cdot(-1)_{e:Hmin} + 10\cdot 0_{C:Hmin} + 1\cdot(-1)_{N:Hmin}) = 2
$$

- Maximum H:

$$
\min(40_{H:max},\ 2_{initial:Hmax} + 1\cdot(-1)_{e:Hmax} + 10\cdot 2_{C:Hmax} + 1\cdot 1_{N:Hmax}) = 23
$$

- Current DBE:

$$
\frac{2_{initial:2DBE} + 1\cdot(-1)_{e:2DBE} + 10\cdot 2_{C:2DBE} + 1\cdot 1_{N:2DBE}}{2} = 11
$$

For DBE to lie between 0 and 8, H must be in
$[\frac{8-11}{-1/0.5}, \frac{0-11}{-1/0.5}] = [6, 22]$, so the program iterates H
from 6 to 22 for that mass guess.

Mass constraints are applied during iteration. For `C10H15O11N-`:

$$
\text{DBE} = \frac{2_{initial:2DBE} + 1\cdot(-1)_{e:2DBE} + 10\cdot 2_{C:2DBE} + 11_{N:2DBE} + 15\cdot(-1)_{H:2DBE}}{2} = 3.5
$$
