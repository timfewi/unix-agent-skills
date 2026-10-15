---
name: lean-code
description: Use when iteratively improving code, making an implementation lighter, aligning it with existing architecture, consolidating duplication, or replacing an internal interface while preserving required behavior.
---

# Lean code improvement loop

Produce the smallest implementation a human can understand. Prefer less
code, fewer dependencies and less indirection. This is a feedback-driven agent
loop, not model training.

1. **Inspect.** Read repository instructions, affected code, known callers and
   relevant checks. Identify required behavior, failure paths, ownership,
   dependency direction and runtime constraints. Establish the baseline;
   distinguish existing failures from regressions.
2. **Choose.** Pick one concrete simplification with a benefit. Prefer
   deleting dead paths, unnecessary wrappers and repeated work. Extract duplicate
   code only when callers share a stable responsibility and the result is easier
   to read. Reuse existing primitives; avoid speculative frameworks.
3. **Change.** Make a focused edit that fits the architecture. When replacing an
   internal interface, migrate callers, tests and documentation together; remove
   superseded code. Keep compatibility only for an identified unmigrated consumer,
   with reason and removal condition.
4. **Evaluate.** Inspect the diff and run proportionate checks of observable
   behavior, error paths and a migrated caller. Keep the change only if correctness
   and security hold and maintenance becomes easier. Fewer lines
   alone earn no credit: reject compressed syntax, cryptic names, hidden complexity,
   weakened validation and weakened test assertions. Measure performance or resource
   claims; mark unmeasured expectations explicitly.
5. **Repeat or stop.** Default to at most three improvement rounds. Stop earlier
   when checks pass and no worthwhile simplification remains. Repair or discard
   only your unsuccessful edits; preserve other work. Stay within the requested
   scope. External APIs, persisted data and deployment boundaries require a migration
   strategy; refactoring does not authorize data destruction or system activation.

Report what became simpler, verification results, measured gains and remaining
limits. Claim improvement only with evidence.
