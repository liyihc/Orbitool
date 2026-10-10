---
name: release-notes
description: Draft an English, user-facing GitHub release description for a new Orbitool version.
disable-model-invocation: true
---

Draft the GitHub release description for a new Orbitool version. Title it
`# Orbitool <version>`, reading the version from `Orbitool/version.py`. Write it
for end users, in English, and output it in the conversation — never run
`gh release create` or write a file.

Range: `<previous release tag>..<target ref>`. Establish the target ref
explicitly — it is the branch or tag the user names, which is often **not** the
current checkout; never assume `HEAD`. Use the tags the user gives; otherwise
find the latest tag before the target with `git tag --sort=-v:refname` and
confirm the previous tag, the target ref, and the commit list with the user
before writing.

Collect with `git log <prev>..<target> --format="%h %s%n%b"` (the message bodies
carry the user-visible rationale) and `git diff --stat`. Ignore generated and
non-source noise (Cython `.html`, `*.pyd`, `uv.lock`, data files).

Write exactly three sections, in this order:

- **## Feature changes** — how behavior differs for the user. Each bullet must
  state the **previous behavior**, the **new behavior**, and **why** it changed.
  Use the concept names from `docs/guide/` and `GLOSSARY.md`, and say what the
  thing used to be (e.g. "Formula used to be a dock panel; it is now a
  menu-opened window because it is a settings tool, not a processing step").
- **## Bug fixes** — user-visible bugs that are now resolved.
- **## Under the hood** — changes to the code itself: language and dependency
  versions, architecture, build tooling. Keep it to short bullets.

Keep internal work (Python/Qt/build/refactors/docs) out of the first two
sections — it belongs under **Under the hood**, and is never framed as a breaking
change. Keep sentences short and plain, one idea per bullet, in a user's words —
no paths or hashes. No preamble. Output Markdown.
