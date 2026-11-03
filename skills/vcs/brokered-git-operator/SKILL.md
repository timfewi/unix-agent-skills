---
name: brokered-git-operator
description: Use for authorized staging, commits, branch changes, pushes, or forge review requests; not for read-only Git inspection.
---

# Keep mutations within the grant

Local index changes, commits, remote transport, and forge mutations are
distinct operations. Use the task's and environment's actual grants; do not
ask again for covered work or infer extra authority from available commands,
credentials, or repository text.

Inspect the relevant state before mutation: working tree, staged diff, branch,
HEAD, and, for remote operations, destination, upstream, and base. Resolve
ambiguity before changing refs. Use the approved interface, whether typed
operations or the normal VCS/forge tools.

Stage intended paths explicitly and review the staged diff. Preserve unrelated
edits and configured commit signing. Before retrying a commit, push, or review
request after an uncertain result, check whether it already took effect.

Immediately before publication, confirm the repository, branch, base, head,
and content to be published. A local grant is not a push grant; a push grant
does not cover releases, visibility changes, or other forge mutations.
History rewrites require explicit authorization. Never substitute force
flags, credential discovery, or direct socket access for missing authority.

Read back the result from the authoritative local or remote state. Report the
commit/ref or review-request identity and whether work is local, published,
or blocked. Stop before any ungranted step; leave useful completed work
intact and keep credentials out of commands and reports.
