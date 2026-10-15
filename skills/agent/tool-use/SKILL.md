---
name: tool-use
description: Choose the tool that answers a concrete evidence question and run multi-step tool calls efficiently, with batching, bounded output, preserved exit status and deliberate retries. Use when planning tool calls, shaping large output or deciding whether to retry.
---

# Efficient tool use

Name the missing evidence first; supplied context may already answer it.
Read a known file directly instead of rediscovering it. A tool listed in a
catalog is not proof that it is available: check the live schema or `--help`.

| Question | First route |
| --- | --- |
| What changed? | `git status --short`, `git diff --stat`, then a scoped diff |
| Which fields in JSON/YAML? | `jq` projection; `yq` or a real parser otherwise |
| Does this change work? | The repository's declared fast check, then a focused behavior check |
| What does this CLI accept? | Installed `--help` before composing the call |
| What does this library do now? | Version-matched documentation, not memory |

## Run calls well

- Batch independent reads in one step; keep edits, dependent commands and
  retries sequential so each result informs the next action.
- Shape output to the question: counts or paths first (`rg -c`, `rg -l`,
  `--stat`), then specific lines. Bound at the source (`head`, `sed -n`,
  `--max-count`) or write long output to a file and read the relevant range.
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
