---
name: tool-use
description: Choose the tool that answers a concrete evidence question and run multi-step tool calls efficiently, with batching, bounded output, preserved exit status and deliberate retries. Use when planning tool calls, shaping large output or deciding whether to retry.
---

# Efficient tool use

Name the missing evidence first; supplied context may already answer it.
Read a known file directly instead of rediscovering it. A listed tool may be
unavailable: check the live schema or `--help`.
Use the environment's prescribed runtime launcher even when another interpreter
is on PATH; probe the command through that launcher.

| Question | First route |
| --- | --- |
| What changed? | `git status --short`, `git diff --stat`, then a scoped diff |
| Which structured values? | `jq`/`yq` projection or a selected runtime's parser; Python's standard library can query JSON/CSV without dependencies |
| Does this change work? | The repository's declared fast check, then a focused behavior check |
| What does this CLI accept? | Installed `--help` before composing the call |
| What does this library do now? | Version-matched documentation, not memory |
| Which package or config option? | An exposed package/option index, then the project's pinned source or evaluation |

## Run calls well

- Batch independent reads in one step; keep edits, dependent commands and
  retries sequential so each result informs the next action.
- Shape output to the question: counts or paths first (`rg -c`, `rg -l`,
  `--stat`), then specific lines. Bound at the source (`head`, `sed -n`,
  `--max-count`) or write long output to a file and read the relevant range.
  Budget the combined batch output: per-call limits multiply. On truncation,
  narrow the projection or range instead of repeating the same dump.
- Run non-interactively: disable pagers and color (`GIT_PAGER=cat`,
  `NO_COLOR=1`, `--no-pager`), pass `-y`/`--yes` only for actions already
  authorized, and avoid commands that wait for a TTY.
- Preserve the real exit status when filtering. In bash or zsh use
  `set -o pipefail`; a successful `| tail` proves nothing about the command.
- Keep the handle of a running process and observe it instead of starting a
  second copy.
- Retry only after an input, environment or hypothesis changed. Read the
  error, fix the cause, then rerun the same narrow command.

Report the command, its exit status and the decisive output, not a paraphrase.
