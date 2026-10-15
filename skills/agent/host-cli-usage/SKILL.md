---
name: host-cli-usage
description: Resolve the installed syntax of a command-line tool before invoking it or retrying an argument error. Use when running an unfamiliar CLI, after "unknown option" or "unexpected argument" errors, or when translating an MCP/API operation into a shell command.
---

# Installed command syntax

The installed binary is authoritative. A README, blog post, MCP schema or your
memory may describe another version.

1. **Identify the binary.** `command -v <tool>` (or `type -a <tool>` to see
   shadowing aliases and functions), then `<tool> --version`.
2. **Read installed help.** `<tool> --help`, then `<tool> <subcommand> --help`.
   Fall back to `<tool> help <subcommand>`, `man <tool>` with `MANPAGER=cat`,
   or `-h`. Shell builtins use `help <name>` (bash) or `man zshbuiltins`.
3. **Map, do not copy.** MCP or API field names (`query`, `file`, `limit`) are
   often positional arguments or differently named flags on the CLI.
4. **Probe once.** Confirm one small real invocation before composing a
   pipeline or loop around it.

After an argument or subcommand rejection, read help before retrying; never
cycle through guessed flag spellings. An empty result or an ambiguity message
is an answer to interpret, not an error to retry.

Same name, different tool: GNU and BSD/macOS userlands differ (`sed -i`,
`date`, `stat`, `grep -P`). If `<tool> --version` fails or prints no GNU
banner, assume the BSD variant and check its man page.

When a command is missing, look for a wrapper or toolbox the host documents
before declaring it unavailable. Do not install replacements or change the
system to obtain a command unless that is part of the task.

Return the exact invocation, its exit status and the relevant output.
