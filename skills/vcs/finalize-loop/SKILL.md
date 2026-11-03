---
name: finalize-loop
description: Use when completed implementation needs final review, verification, an authorized commit, or a handoff; not for every intermediate edit.
---

# Close the evidence gaps

Compare the complete change set with the request, including staged and
untracked files. Look for unrelated edits, debug leftovers, sensitive data,
and generated artifacts. Preserve work that is not yours.

Reuse current verification results; run the owning gate and any missing
focused coverage. Review and checks may interleave as findings require.
Do not impose a fixed ceremony or rerun unchanged checks just to finish.

Before landing, establish that the request is satisfied, required checks pass,
and the intended diff is reviewed. Report baseline failures separately;
an explained failure is not permission to bypass a required gate. Repair
regressions within scope and the agreed budget. At a blocker or limit, preserve
the work and report the missing evidence.

Commit, push, or open a review request only within applicable authority.
Existing authorization need not be requested again. If publication is not
authorized, leave the result local and say so.

Read back the authoritative state after the final mutation: for example,
working-tree status and the resulting commit, remote ref, or review request.
A final report should identify that state, checks and results, and remaining
limits. The evidence must support completion; it need not be the last tool
call or force the report into a transcript format.
