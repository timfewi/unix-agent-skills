---
name: portable-shell
description: Write shell commands and scripts that behave the same on Linux and macOS, in bash and zsh, with GNU or BSD userlands. Use when writing or debugging a shell script, a one-liner that uses sed/date/stat/find/xargs, or a command that failed with "no matches found", "illegal option" or word-splitting surprises.
---

# Portable shell

**Know the target first.** Check `uname -s` and the interactive shell
(`echo "$0"`, `$ZSH_VERSION`, `$BASH_VERSION`). Check the userland flavor:
`sed --version` succeeds only for GNU sed. On macOS, Nix or Homebrew may put GNU
tools first in `PATH` (sometimes as `gsed` or `gdate`).

**bash and zsh differ where agents trip:**
- zsh does not word-split unquoted `$var`. Iterate with a `for` loop over
  explicit words or an array instead of relying on splitting.
- zsh treats an unmatched glob as an error ("no matches found"). Quote
  patterns meant for the tool (`find . -name '*.nix'`), and guard optional
  globs.
- zsh expands a word that starts with `=` to a command path, so `echo ===`
  fails with "== not found". Quote such words: `echo '==='`.
- `/bin/bash` does not exist everywhere (NixOS, some containers), and macOS
  `/bin/bash` is 3.2: no `mapfile`, associative arrays or `${var,,}`. Use
  `#!/usr/bin/env bash` and features the oldest target supports, or write
  POSIX `sh` (`#!/bin/sh`).

**Script hygiene:**
- Start with `set -eu`; in bash add `set -o pipefail`.
- Quote every expansion and pass `--` before user-supplied paths.
- Use `printf '%s\n'`, not `echo -e`. Read lines with `while IFS= read -r line`.
- Handle odd filenames with `find … -print0 | xargs -0` or `find … -exec … {} +`.
  Never parse `ls`.
- Use `command -v` instead of `which`. Clean up with `trap 'rm -rf -- "$tmp"' EXIT`.
- Create temp paths with `mktemp "${TMPDIR:-/tmp}/name.XXXXXX"`, which works on
  both GNU and BSD.
- Run `shellcheck` when it is available, and fix findings instead of
  disabling them.

**GNU vs BSD flags** differ for `sed -i`, `date`, `stat`, `readlink -f`,
`grep -P`, `xargs -r`, `find -printf`, `base64`, checksums, `timeout` and
CPU counting. Look up the portable form in
[references/gnu-bsd.md](references/gnu-bsd.md) before using any of them in a
script meant for both systems.

Verify a portable script on each target you can reach, or name the untested
one. Report which shell and userland the command was checked with.
