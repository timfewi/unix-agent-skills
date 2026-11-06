---
name: fast-checks
description: Use when selecting checks for changed behavior or diagnosing a failed check; not for unrelated read-only investigation.
---

# Verify the changed contract

Use the repository's declared gate and supported environment. Select
additional checks from the behavior at risk, not a generic list of tools.
Entering a development shell is setup, not verification.

- For code or configuration changes, run the owning fast gate or declared
  equivalent.
- For runtime, packaging, or build-output changes, also exercise the affected
  path: a focused test, CLI invocation, build, or request. Reuse coverage
  already supplied by the gate instead of rerunning the same check by habit.
- Read-only questions need source evidence, not unrelated builds. Repository
  documentation uses its applicable checks; external plans need source and
  acceptance review.

Keep one check running per repository, preserve its handle, and reuse passing
results while inputs remain unchanged. Stay within authorized workload and
resource limits. Stop owned preview servers when finished.
Use workload authorization from the current request or trusted environment
policy. Reuse standing grants within their scope and budgets; do not infer
permission for unrelated builds, VM tests, model runs or benchmarks.

On failure, retain the command, exit status, and decisive diagnostic.
Distinguish baseline failures from regressions when practical. Repair task-caused
failures and rerun affected checks. Keep publication paused until required
checks pass; a failure does not end authorized diagnosis. Fix the cause, not
the assertion; never skip or weaken a check for green output.

State what each result proves and what remains untested. A formatter,
evaluator, or mocked unit test does not establish user-facing behavior.
