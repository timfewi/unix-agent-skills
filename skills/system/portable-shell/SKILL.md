---
name: portable-shell
description: Use for shell portability across bash, zsh, Linux, and macOS, especially globbing, word splitting, shebangs, or GNU/BSD option differences.
---

# Preserve shell and userland semantics

Establish the target shell and installed utilities where they affect the
command. The login shell, script interpreter, and userland can differ.
macOS can run GNU utilities; Linux can use BusyBox. Do not infer the executable
from the OS or a rejected `--version`.

## Failure-prone differences

- zsh does not split unquoted `$var` like bash, and an unmatched glob normally
  errors. Use explicit arguments or arrays; quote patterns intended for tools.
- zsh can expand a word starting with `=` as a command path. Quote literal
  separators such as `'==='`.
- `/bin/bash` is not universal; macOS's system bash is 3.2. An environment
  shebang still needs a suitable interpreter in `PATH`. Avoid associative
  arrays, `mapfile`, and `${var,,}` on that older target.
- `set -e` is context-sensitive, not universal failure handling. Handle
  expected nonzero statuses explicitly and preserve pipeline failures where
  supported. Do not add strict-mode flags without checking the script's
  control flow and target shell.
- Preserve arbitrary filenames with NUL-delimited processing or
  `find ... -exec ... {} +`; never parse `ls`. Quote expansions and protect
  leading-dash operands using the command's supported syntax.
- Create temporary paths securely, quote cleanup, and remove only paths the
  invocation owns. Replacing a file can change permissions, links, or metadata.

For `sed -i`, dates, `stat`, canonical paths, `xargs`, checksums, and timeouts,
consult [references/gnu-bsd.md](references/gnu-bsd.md) for the relevant
difference rather than loading every platform recipe.

Use available shell checks and exercise the affected behavior on reachable
targets. Name the tested shell/userland and any untested target; one Linux run
does not prove macOS compatibility.
