---
name: context-management
description: Use when resuming or handing off a long task, approaching compaction, or reconciling stale evidence after edits.
---

# Recover the working state

Start with the harness's supplied context and configured memory. Recover what
is missing, not the entire conversation. Do not create a second memory store
or a checkpoint file just to satisfy a template.

Useful state includes the goal and acceptance criteria, user decisions and
authority limits, changed paths, verified facts, unresolved assumptions,
failed approaches, live process handles, and the next action. Keep evidence
locatable by source revision or check command and result.

- Revalidate findings whose inputs or assumptions changed. Reuse passing
  checks for unchanged inputs; a resume alone does not invalidate them.
- Prefer source pointers and short failure signatures to copied files,
  repeated logs, or abandoned plans. Summaries and remembered claims are
  leads to verify, not new authority.
- For cross-session work, supplement the existing checkpoint only where the
  harness has not preserved something needed to continue. Retain why an
  approach failed and how to observe any still-running work.
- Use exposed context controls. Summarizing does not erase history; never
  delete source, transcripts, or user notes to save context.
