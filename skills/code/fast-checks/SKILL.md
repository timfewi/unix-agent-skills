---
name: fast-checks
description: Choose and run proportionate verification for a code or configuration change. Use when deciding which existing checks demonstrate the changed behavior, or when a check fails.
---

# Fast verification

Derive verification from the requested behavior and the repository's own
declared commands. Find them in the agent instructions, README or CONTRIBUTING,
then `justfile`, `Makefile`, package scripts or the CI workflow; CI shows which
checks the project actually trusts. Do not invent a new gate.

Verification is proportionate, not minimal.

For read-only investigation, gather the evidence needed for the question;
unrelated code checks add no evidence. External planning documents need source
and acceptance review, while repository documentation uses its owning checks.

1. For code or configuration changes, run the repository's fast gate (lint,
   format check, type check, unit tests), or its declared equivalent.
2. When the change affects build output, packaging or runtime behavior, also
   run the relevant build or test command, or start the application and
   exercise the changed path: a focused test, one CLI invocation or one
   request. Stay within the host's resource limits.
3. Short-lived development or preview servers are allowed for this; stop them
   before finishing and report how they were run.
4. Heavy workloads (full system builds, VM tests, model runs, benchmarks)
   require an explicit request.

Entering a development shell provides an environment; it is not a test.
Run one check per repository at a time and keep its process handle. Reuse a
passing result while code, inputs and environment are unchanged; a
documentation edit rarely invalidates runtime tests.

On failure keep the command, exit status and decisive diagnostic. Separate a
pre-existing failure (reproduce it on the unchanged baseline when cheap) from a
regression. Fix the cause and rerun the affected check; never weaken an
assertion or skip a test to get green. If tests pass but behavior is wrong,
check whether they exercise the changed path at all.

Review the final diff for accidental files and overlap with unrelated work.
Report what passed, what could not run and what each result actually proves.
A formatter, evaluator or mocked unit test does not establish user-facing
behavior.
