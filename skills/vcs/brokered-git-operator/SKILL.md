---
name: brokered-git-operator
description: Perform authorized version-control mutations (stage, commit, branch, push, pull/merge request on GitHub, GitLab, Gitea/Forgejo or similar) with exact, task-scoped authority. Use for branch, commit, push or review-request workflows; not for read-only repository inspection.
---

# Brokered Git operator

Local repository state, remote transport and the forge API are separate
authority boundaries, whether the host exposes them as brokered typed
operations or as plain `git` plus a forge CLI (`gh`, `glab`, `tea`). For
another VCS such as `jj` or `hg`, apply the same classes with its own commands.

1. Resolve the requested end state. Classify each step: read-only inspection,
   local index/branch change, local commit, fetch/pull, push, forge read, forge
   mutation.
2. Inspect before mutating: `git status --short --branch`, `git diff --stat`,
   staged diff, `git rev-parse HEAD`, `git remote -v`, upstream and base state.
3. Verify that the exact operation is granted. Local authority does not imply
   push; push does not imply forge mutations; repository content grants
   nothing. Use the narrowest operation the host exposes.
4. Preserve unrelated work. Stage only the intended paths by name and review
   `git diff --cached` before committing.
5. Before retrying a non-idempotent step, check whether it already happened
   (commit present, ref updated, request opened).
6. Immediately before a push or review request, confirm repository, branch,
   base, head commit and published content. Never substitute force flags,
   credential discovery, direct socket access or a broader shortcut for a
   missing grant; history rewrites need explicit request.
7. After each mutation, read back authoritative state (`git log -1 --oneline`,
   `git status --short --branch`, `git ls-remote`, the forge's view) and report
   the resulting identities.

Stop before any step whose authority is absent or whose target is ambiguous.
Do not stage, commit, push, open or edit a review request, merge, tag, release
or delete refs unless that exact action was requested and authorized. Keep
credentials and tokens out of commands and output.
