# Peak Fit windows are segment-scoped and own their formula window

## Status

accepted

## Context

A Peak Fit window edits one raw peak (a segment) and the fitted peaks split from
it. Several such windows can be open at once. Two things were implicit and
fragile:

- Each window cached the absolute slice of `peak_fit_tab.peaks` for its segment.
  Saving another segment changes how many fitted peaks precede it, so a later
  save (or row-to-peak mapping) in an already-open window used a stale range.
- The formula calculation result window was a single manager-wide slot. A Peak
  Fit window needs its candidates to follow that window's uncommitted `self.peaks`
  (a re-fit may not be saved yet), while the formula window opened from the menu
  is just a calculator with no peak to accept into.

The segment identity (`original_index`) is stable across saves; only the flat
range of fitted peaks moves. `Save` commits the whole segment (re-fit count,
positions, intensities, formulas), so calling it `Use new formula` would
understate what it does.

## Decision

- A Peak Fit window is segment-scoped. Resolve its fitted-peak range from
  `original_index` every time it is needed instead of caching a slice. Another
  window's save then only shifts indices, not meaning.
- Each Peak Fit window owns at most one formula result window and closes it with
  the Peak Fit window, on Save, and on Re-fit. That window reads the current
  working set of open Peak Fit windows (the owner's pending peaks plus the other
  segments' saved or pending peaks), fixes the peak's m/z in its title, and offers
  `Delete formula` / `Use selected formula` / `Close`. The menu-opened formula
  window remains the single global calculator; its accept buttons are hidden
  because it has no target.
- `Save` stays `Save` and commits the whole pending segment; `Close` discards
  it. A line under the Peaks table lists the changed categories (peak count,
  positions, intensities, formulas) and disables `Save` when nothing changed.
- Close Peak Fit windows when the workspace is loaded, when the peak set is
  regenerated, and when the main window closes — but not on Save As, which keeps
  the same data. `Fit` requires closing open Peak Fit windows first (and warns
  that uncommitted edits are discarded), because it rewrites saved peaks behind
  their working copy.

## Consequences

Concurrent edits in different segment windows no longer corrupt each other's
range, and each window can keep its uncommitted work while another saves. The
cost is that formulas are no longer edited through one shared result window, and
that a Fit while windows are open is delayed by a prompt. The global formula
window is now explicitly a read-only calculator.

## Considered Options

- **Close all other Peak Fit windows on every save.** Simple and safe, but loses
  their uncommitted edits.
- **Freeze or refresh a cached baseline when saved peaks change outside the
  window.** Either lets the summary disagree with the data or still needs the
  same dynamic range lookup.
- **Rename `Save` to `Use new formula`.** Rejected: the button also commits
  re-fit positions, intensities and peak count.
- **Keep the single global formula result window for Peak Fit.** Rejected: it
  cannot follow two windows' independent uncommitted states.
