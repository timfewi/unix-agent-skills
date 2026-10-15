---
name: context-management
description: Keep a long, resumed or compacted task focused on current evidence. Use when a session resumes, the context window fills with tool output, or earlier findings may be stale after edits.
---

# Keep a small, current working state

Retain only what the next decision needs:

```text
Goal:        requested end state and acceptance criteria
Constraints: authority limits, scope, user decisions
Evidence:    verified facts with path:line or command + exit status
Assumptions: unverified beliefs, marked as such
Changed:     files edited so far
Running:     live process handles or jobs
Next:        the single next action
```

- After an edit, a changed requirement or a resume, recheck the affected
  evidence. Mark superseded notes stale and replace them; never reason from an
  old excerpt or an old test result.
- Keep paths and short failure signatures instead of repeated listings, full
  logs or abandoned plans. Reopen the smallest source range when needed.
- Before compaction or a handoff, write the checkpoint above into the
  project's existing progress mechanism when the task spans sessions. Include
  why a failed attempt failed, so the next session does not repeat it.
- Use only the context controls the harness actually exposes. A summary does
  not erase history. Never delete project files, transcripts or user notes to
  save context.
