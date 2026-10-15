---
name: filesystem-wizard
description: Find the files, symbols and verification entrypoint that own a task, and answer structural questions (where is X defined, who calls it, what breaks if it changes) with bounded searches. Use when the owning files are not yet known, in an unfamiliar repository, or before editing shared code.
---

# Locate, then read narrowly

Start from what is known: read supplied paths directly. Otherwise read the
repository's agent instructions and README, then its manifests (`flake.nix`,
`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`,
`justfile`, CI config) for layout and check commands. Run `git status --short`
before edits or when local changes affect the answer.

| Question | Route |
| --- | --- |
| Which file? | `rg --files -g '<glob>' <dir>` or `git ls-files '<pattern>'` |
| Where is this literal? | `rg -n -F -- '<text>' <dir>`; `rg -l` for names only |
| Definition or outline? | An exposed code index or LSP; else `rg -n` for the definition pattern |
| Who calls this / impact? | Index callers or impact, then confirm each hit in source |
| Why is it ignored? | `git check-ignore -v <path>` |
| When did it change? | `git log -S '<text>' --oneline -- <path>` |

- Paths before bodies: filenames and manifests usually establish ownership.
  Then read a bounded excerpt around the hit (`sed -n 'A,Bp'`) and follow
  imports only along the path the task needs.
- Scope every search to a directory. Never scan `/`, a whole home directory or
  the Nix store. Skip generated, vendored and cache trees (`node_modules`,
  `dist`, `target`, `.direnv`, `result*`) unless they own the behavior.
- State coverage: `.gitignore`, hidden files and binary filters can hide the
  answer (`rg -uu` widens). Text matches are not semantic references.
- Code-index results are leads. Check index status once; edges are resolved by
  name, so dynamic dispatch, macros, reflection and generated code are missing.
  Confirm decision-critical results with a read before editing. If the index is
  absent or stale, fall back to literal search instead of rebuilding it.

Stop when you can name the responsible files, the constraints that apply and a
command that checks the requested behavior. Return those paths with one-line
reasons plus any unresolved ownership question.
