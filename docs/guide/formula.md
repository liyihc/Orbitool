# Formula Calculation

The [Formula docker](dockers.md#formula) hides and shows this calculator.

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
- **element infos** — per-element parameters, shown with **show infos**.

## Calculate

You can input a **formula** or a **mass**:

- A **formula** returns its mass (including the electron).
- A **mass** returns the matching formula candidate(s) in the result window.

In the result window:

- **Double-click** a row to display its natural isotope distribution.
- **Double-click** an isotope row to save that formula to a peak.
- **show all**, **Accept**, and **Accept empty list** finalize the assignment.

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
