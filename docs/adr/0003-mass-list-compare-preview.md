# Mass List compare previews Import/Merge by reusing the merge rule

## Status

accepted

## Context

A Mass List is changed from a CSV two ways: **Import** replaces the whole list,
**Merge** unions the CSV into it. Neither showed its result before committing, so
"what will Import throw away?" and "what will Merge add?" were invisible until
after the fact. The three operations also sat as separate buttons.

We are adding a **Compare**: one button (`Import, Compare and Merge`) opens a
modal preview with three columns — the current list, the imported (Import) list,
and their union (Merge) — and three commit buttons (use current / use Import /
use Merge). The preview table is exportable.

The non-obvious decision is how the three lists become *aligned rows*. The union
is not a plain set union: `MassListHelper.addMassTo` joins a row within tolerance
unless the formulas differ, in which case it inserts a second row at the same
mass. A comparison row set computed by any method other than that exact rule
could disagree with what "use Merge" actually commits.

## Decision

- The **Merge column is the row set**: each row is one union entry; the current
  and Import columns show a value only where that list contributed to the row,
  blank otherwise. "Both cells present" reads as matched, "one cell present" as
  unique to that side.
- Alignment **reuses `addMassTo`'s rule, not a separate diff**: refactor
  `addMassTo` so its decision is reported (matched row / replaced row / inserted
  row), keep the existing `addMassTo` as a thin wrapper whose behavior is
  unchanged, and build `MassListHelper.compare` on the reporting variant,
  operating on a copy of the current list.
- The commit buttons use the existing semantics: use current = no change; use
  Import = replace with the parsed CSV; use Merge = replace with the union.
- Preview export is WYSIWYG: six columns
  (`current_position, current_formulas, import_position, import_formulas,
  merge_position, merge_formulas`), formulas joined by `/` to match the import
  convention, empty cells left blank.

## Consequences

The Merge column is guaranteed to equal what "use Merge" commits — including the
extra same-mass rows that formula conflicts produce — because both run the same
rule. The cost is that `addMassTo` must expose provenance without changing its
observable behavior for Add/Import caller paths.

## Considered Options

- **Independent, unaligned side-by-side columns** (three sorted lists). Rejected:
  no row correspondence, so match/unique is left to the reader's eye.
- **A separate set-based diff algorithm** for alignment. Rejected: it would drift
  from `addMassTo` (tolerance joins, formula-conflict insertions) and let the
  preview disagree with the commit.
