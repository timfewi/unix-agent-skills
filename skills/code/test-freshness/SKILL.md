---
name: test-freshness
description: Use when a regression test is added, mocks may have drifted, interfaces change, or green tests conflict with observed behavior.
---

# Would the test catch the failure?

Trace an important assertion through its fixture or mock to the production
behavior. Compare the mocked interface with the real caller's arguments,
return values, and failure modes.

Look for false reassurance: assertions on setup alone, unused fixtures,
mocks that bypass the changed path, or snapshots regenerated without review.
Prefer observable outcomes to matching source text.

Where practical, demonstrate that the regression test fails on the old
behavior or a controlled fault. Remove the fault before final verification.
Distinguish a stale test from a product defect; repair the contract without
relaxing the expected outcome.

A fingerprint proves only that selected bytes match, not that a test detects
a bug. Use freshness manifests only at boundaries that need them; keep the
expected baseline separate and never regenerate it merely to restore green.

Report the assertion traced, the fault caught or missed, and any remaining
coverage gap. Do not present structural fixture validation as an executed
end-to-end test.
