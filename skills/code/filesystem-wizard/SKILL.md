---
name: filesystem-wizard
description: Find the owning repository, files, symbols and verification entrypoint with bounded searches. Use when ownership is unknown, navigating a multi-repository workspace, answering structural code questions, or before editing shared code.
---

# Locate, then read narrowly

Read supplied paths directly. For unknown ownership in a multi-repository
workspace, consult an available read-only inventory and its instruction paths
before searching contents. Once scoped, read repository instructions, README
and the relevant manifest for layout and checks. Run `git status --short`
before edits or when local changes affect the answer.

| Question | Route |
| --- | --- |
| Which file? | `rg --files -g '<glob>' <dir>`; `git ls-files` for tracked paths |
| Where is this literal? | `rg -n -F -- '<text>' <dir>`; `rg -l` for names only |
| Definition or outline? | An exposed code index or LSP; else `rg -n` for the definition pattern |
| Who calls this / impact? | Index callers or impact, then confirm each hit in source |
| Why is it ignored? | `git check-ignore -v <path>` |
| When did it change? | `git log -S '<text>' --oneline -- <path>` |

- Paths before bodies: return filenames or counts, then read bounded excerpts
  around relevant hits. Follow imports only along the path the task needs.
- Scope searches to the owning tree; exclude dependencies, generated output
  and caches unless they own the question. Never scan `/`, a whole home
  directory or the Nix store.
- If expected files are absent, inspect ignore rules and hidden paths before
  concluding absence. Add `--hidden` or `--no-ignore` only to the relevant
  subtree, keeping `.git` and cache exclusions. State coverage limits.
- Use a parser for structured values or relationships; text matches alone do
  not establish configuration meaning or semantic references.
- Code-index results are leads. Check index status once; edges are resolved by
  name, so dynamic dispatch, macros, reflection and generated code are missing.
  Confirm decision-critical results with a read before editing. If the index is
  absent or stale, fall back to literal search instead of rebuilding it.

Stop when you can name the responsible files, the constraints that apply and a
command that checks the requested behavior. Return those paths with one-line
reasons plus any unresolved ownership question.
