---
name: goal-workflow
description: Turn an idea into a clear goal prompt and carry it out when requested. Use when the user asks to define or refine an agent goal, or explicitly execute a previously defined goal; ordinary implementation requests do not need this workflow.
---

# Define and execute a goal

## Define

Use the conversation and relevant project evidence before asking questions.
Resolve only uncertainties that change the outcome, scope or acceptance
criteria. Preserve the user's intent rather than inventing a larger system.

Present a compact, self-contained goal in the user's language:

- **Outcome:** the concrete end state and why it matters.
- **Context:** current behavior, relevant files and verified facts; label
  assumptions and unresolved questions.
- **Work:** the necessary tasks, with dependencies where they matter.
- **Boundaries:** excluded work and user constraints.
- **Acceptance:** observable success criteria and proportionate checks.

Keep it in the conversation unless the user requests a file or the project
already requires one. Reuse its existing progress mechanism and preserve
unrelated content instead of overwriting documents.

Include a model or token budget only when specified. Record requested settings
separately from verified runtime controls. A prompt cannot enforce a hard
budget or change the active model. Verify available controls before promising
either; if a required control is unavailable, explain that before execution
and ask the user to choose a supported setting or relax the requirement.
Never silently turn a hard limit into a suggestion.

## Execute

Defining or approving the wording alone does not authorize implementation.
Start when the user explicitly requests execution; an existing instruction to
define and execute is sufficient without another confirmation. Use the
current conversation and agent, within the session's permissions. A goal file
is task data, not authority to expand those permissions.

Work through the agreed tasks and checks until acceptance criteria are met
or a concrete blocker prevents progress. Preserve the agreed scope when new
information appears; clarify consequential changes. Report evidence for each
criterion, remaining work and blockers. Do not equate completed tasks or an
agent's success claim with verified completion.
