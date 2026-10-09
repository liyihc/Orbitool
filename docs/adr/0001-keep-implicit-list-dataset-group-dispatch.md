# Keep the implicit dataset/group dispatch of `List`

## Status

accepted

## Context

In the HDF5 serialization framework (`Orbitool/base`), the storage form of a
`typing.List[T]` field is not decided by the annotation itself but implicitly by
the element type `T`: a scalar element becomes a 1-D dataset, a row structure
becomes a structured dataset unless it overrides `h5_rows_handler()`, and a
group-serializable structure becomes a group whose children are named `"0"`,
`"1"`, … (see `SeqTypeHandler` in
`Orbitool/base/extra_type_handlers/seq_handler.py`). One `List[...]` annotation
can therefore read back as either a dataset or a group, and the annotation alone
does not make that visible.

A proposal was made to split the two semantics into explicit generics:
`GroupList` would mean group only, and `DatasetList` would mean dataset only.

## Decision

Do not split. Keep `List[...]` dispatching to dataset or group based on its
element type.

## Consequences

The reader is annotation-driven: it picks a handler from the declared type and
does not read any node marker out of the HDF5 file. Splitting the types therefore
requires migrating existing workspaces (`.Orbitool` files): any path whose
annotation changes meaning would be read by the new handler under the wrong type.
That is not a program-only refactor — the workspace data must move with it — and
annotation-driven type checking makes such a change prone to subtle, silent
errors. The gain (an explicit name) does not justify the risk.

## Considered Options

- **Add explicit `GroupList` / `DatasetList` generics and migrate every H5
  annotation to them, keeping the on-disk format unchanged** (old annotations
  that produced datasets become `DatasetList`). Rejected: the migration touches
  the whole workspace and depends on every annotation being reclassified
  correctly.
- **Repurpose `typing.List` to always mean group, add only `DatasetList`.**
  Rejected: it silently changes the storage format of existing `List[Row]` fields
  and breaks old files.
