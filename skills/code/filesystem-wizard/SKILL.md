---
name: filesystem-wizard
description: Use when repository ownership, implementing files, callers, or change impact are unknown; not to rediscover supplied paths.
---

# Find the owning source

Read supplied paths directly. When ownership is unknown in a multi-repository
workspace, use its available read-only inventory before searching contents.
Apply the owning repository's guidance and inspect local changes before
editing. A routine edit does not need a new whole-repository map.

| Missing evidence | Useful route |
| --- | --- |
| Filename | Scoped file glob or tracked-path inventory |
| Literal | Bounded literal search in the owning tree |
| Definition or references | Available language server or code index |
| Ignore behavior | `git check-ignore -v <path>` |
| History of a change | `git log -S '<text>' --oneline -- <path>` |

Follow imports and callers only as needed for the question. Prefer paths or
counts before large excerpts, but do not add a discovery pass for a file
already known.

If expected files are absent, inspect ignore rules and the relevant hidden
subtree. Do not turn a missing match into an unbounded scan of dependencies,
caches, a home directory, the filesystem root, or the Nix store.

Use parsers for structured meaning. Index results are leads: stale data,
unresolved edges, dynamic dispatch, macros, and generated code limit coverage.
Confirm decision-critical references in source; fall back to scoped text
search where semantic navigation is unavailable.

Return the owning paths, evidence for the relationship, the relevant check
entrypoint, and any coverage gap.
