---
name: tool-use
description: Use when choosing between available tools, bounding large output, batching independent calls, or deciding whether a failed call is safe to retry.
---

# Get the missing evidence

Choose the smallest authorized call that answers the current question.
Supplied context may already answer it; read a known path directly rather
than rediscovering it. Follow the environment's tool routing and runtime
launcher. Availability is not authority.

Consult the live schema or installed help for unfamiliar contracts and
argument errors, not as a ceremony before every established call. Use a
parser for structured data rather than inferring meaning from text matches.
Resolve version-sensitive behavior against the installed or pinned version.

## Output and dependencies

- Request the useful projection: paths, counts, selected fields, or a bounded
  excerpt. For large results, retain a source handle and inspect relevant
  ranges. On truncation, narrow the question rather than repeat the dump.
- Batch independent reads when useful. Keep dependent operations, shared
  mutations, and retries ordered so later calls use actual results.
- Account for the whole batch's output and resource cost, not just each
  call's limit. Keep running-process handles; observe existing work instead
  of launching duplicates.
- Preserve the underlying exit status when filtering output. Disable pagers
  or prompts where supported; auto-confirmation flags do not supply consent.

Retry after a relevant input, environment, or hypothesis changes. A timeout
does not establish that a mutation failed or a process stopped: inspect its
state before repeating it. Report decisive evidence and unresolved limits,
not a transcript of every call.
