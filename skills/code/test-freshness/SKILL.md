---
name: test-freshness
description: Check whether tests still detect the intended failure. Use when interfaces change, mocks may have drifted, a regression test is being added, or green tests conflict with observed behavior.
---

# Test relevance

- Trace one important assertion through its fixture or mock to the production
  behavior. Compare mocked arguments and return values with the current
  interface.
- Look for a test that would stay green if the behavior disappeared: unused
  fixtures, assertions on setup alone, mocks that bypass the changed path,
  snapshot files regenerated without review.
- When practical, show the regression test failing on the old behavior or a
  temporary controlled fault (revert the fix, flip a condition). Remove the
  fault before final verification.
- Prefer an observable outcome over source-text matching. Do not add hash
  guards merely because files changed.
- Distinguish a stale test from a product defect. Repair the relevant contract
  without relaxing the expected outcome.

## Fingerprints are bounded evidence

A hash detects only the bytes it was given; it never proves behavior or oracle
quality. Prefer a narrow, optional freshness manifest at a fragile boundary over
a mandatory hash per test. Keep the expected baseline separate from the
current computation and never regenerate it just to restore green.

Report which assertions were traced, which fault the test caught or missed,
and any test that was repaired or remains suspect.
