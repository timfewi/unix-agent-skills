---
name: lean-code
description: Use when simplifying an implementation, consolidating duplication, or replacing an internal interface while preserving required behavior.
---

# Simplify the responsibility

Choose a concrete reduction in maintenance cost: remove a dead path,
unnecessary wrapper, repeated work, or dependency. Preserve behavior,
failure paths, ownership, and dependency direction. Fewer lines alone are not
an improvement.

Extract duplication only when callers share a stable responsibility. Prefer
existing primitives to speculative abstractions; do not trade readable code
for compressed syntax or hidden complexity.

For an internal interface replacement, migrate known callers, tests, and
affected documentation together, then remove superseded code. Keep a
compatibility path only for an identified unmigrated consumer, with a reason
and removal condition. External interfaces and persisted data need an
explicit migration strategy.

Verify observable behavior, error paths, and a migrated caller using the
owning checks. Distinguish baseline failures from regressions. Do not weaken
validation or assertions to make the smaller implementation pass. Measure
performance claims; label unmeasured benefits as expectations.

Stop when the requested simplification is checked or no worthwhile change
remains, within the agreed budget. Do not invent an iteration quota. Repair
only your own unsuccessful edits and preserve unrelated work. Refactoring
does not authorize data destruction, deployment, or host activation.
