# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`GLOSSARY.md`** at the repo root, or
- **`GLOSSARY-MAP.md`** at the repo root if it exists: it points at one `GLOSSARY.md` per context. Read each one relevant to the topic.
- **`docs/adr/`**: read ADRs that touch the area you're about to work in. In multi-context repos, also check `src/<context>/docs/adr/` for context-scoped decisions.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `/domain-modeling` skill (reached via `/grill-with-docs` and `/improve-codebase-architecture`) creates them lazily when terms or decisions actually get resolved.

## File structure

Single-context repo (this repo):

```
/
├── GLOSSARY.md
├── docs/adr/
│   ├── workspace/
│   │   └── 20261009-keep-implicit-list-dataset-group-dispatch.md
│   ├── packaging/
│   │   └── 20261010-slim-release-build-by-config.md
│   └── mass-list/
│       └── 20261010-compare-preview.md
└── src/
```

Multi-context repo (presence of `GLOSSARY-MAP.md` at the root):

```
/
├── GLOSSARY-MAP.md
├── docs/adr/                          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

## ADR naming and layout

`docs/adr/` is grouped one level deep by the primary impact area of the decision
(`workspace/`, `packaging/`, `mass-list/`, …). The set of directories is open:
add one for a module or feature when its first ADR appears. Put a decision with no
clear primary area in `cross-cutting/`.

Name each ADR `YYYYMMDD-slug.md`, where the date is the day the decision was made
(the file's creation date) and carries no separators. Same-day ADRs are ordered
only by slug. Cite one as `ADR YYYYMMDD (short title)`; the date locates it, the
title disambiguates same-day entries.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `GLOSSARY.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR 20261009 (keep implicit List dispatch), but worth reopening because…_
