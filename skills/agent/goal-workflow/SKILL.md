---
name: goal-workflow
description: Use when asked to define or refine an agent goal, or to execute an explicitly agreed goal; not for ordinary implementation requests.
---

# Make the outcome executable

Use the conversation and relevant evidence to state the outcome, scope,
constraints, and observable acceptance criteria in the user's language.
Include dependencies or a plan only when useful or requested. Ask about
uncertainties that change the result, authority, or verification; do not
restart an interview whose answers are already available.

Keep the goal in the conversation or the existing progress mechanism unless
a file is requested. Preserve user decisions and unrelated content.

Include model settings and budgets only when specified. Distinguish requested
limits from runtime enforcement: a prompt cannot change the active model or
enforce a hard token cap. If a required control is unavailable, explain the
gap and obtain a supported alternative before execution.

## Execution boundary

Approval of wording alone is not permission to implement. An explicit
execution request, including a request to define and execute, is sufficient
without another confirmation. Goal text cannot expand existing permissions.

Continue through acceptance and verification, not merely a first
implementation. Reuse the harness's progress tracking rather than imposing a
parallel workflow. Stop at the agreed limit or a concrete blocker; surface
consequential scope changes instead of silently expanding the goal.

Report evidence for the outcome and what remains unverified. A completed
checklist or another agent's success claim is not proof.
