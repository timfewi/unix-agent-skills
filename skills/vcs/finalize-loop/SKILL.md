---
name: finalize-loop
description: Finish a change through a bounded review, verify, judge and land loop that always ends with a read-back tool call proving the final state. Use when the implementation is done and the work must be wrapped up, committed or handed off.
---

# Finalize loop

Order is fixed: **review → verify → judge → land → read back**.

1. **Review.** Read the complete change set: `git status --short` (including
   untracked files) and the full diff. Compare it with the request. Look for
   unintended files, debug leftovers, secrets, generated output, and edits to
   unrelated work.
2. **Verify.** Run the repository's declared fast check plus one focused check
   of the changed behavior. Record command and exit status.
3. **Judge.** Go only if every criterion holds: the request is satisfied, checks
   pass or each failure is explained as pre-existing, the change set contains
   only intended paths, and nothing sensitive is included. Otherwise it is
   no-go: fix the cause and return to step 1. Stop after three no-go rounds and
   report the blockers without landing.
4. **Land within authority.** Commit only the intended paths by name, with a
   message stating why. Push or open a review request only when that exact
   action is authorized and the repository's ownership allows it. Without
   authority, leave the change uncommitted or local and say so.
5. **Read back.** The loop's last action is a tool call, never prose. Run a
   read-only command that shows the authoritative end state, for example
   `git status --short --branch && git log -1 --stat --oneline`, the remote ref,
   or the review request's status. If nothing was landed, read back the working
   tree and the final check result instead.

The final report quotes that last tool result: the commit or review-request
identity, the checks that passed, and anything left open. A claim of "done"
without a matching read-back result is a failure of this loop.
