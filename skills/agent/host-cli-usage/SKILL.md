---
name: host-cli-usage
description: Use for unfamiliar CLI syntax, rejected arguments, missing command environments, or translating an API operation into a shell invocation.
---

# Resolve the installed contract

Use installed help for the command and relevant subcommand; an API schema or
remembered example may describe a different interface. Inspect `command -v`
or `type -a` when aliases, wrappers, or multiple versions could explain the
result. Use the prescribed launcher, not an unwrapped substitute.

After an argument rejection, correct the invocation from help or the manual
instead of guessing flag spellings. API fields may become positional
arguments. Confirm an unfamiliar mapping with a small, authorized invocation
before multiplying it in a loop. Do not repeat probes for a known contract.

GNU, BSD, BusyBox, and wrapper commands can share a name. A missing GNU
banner or rejected `--version` does not identify BSD. Check available flags
and the actual executable; the operating system alone does not determine
the userland.

## Missing environments

Non-interactive shells may lack interactive environment hooks. Check the
documented wrapper or project environment before declaring a tool absent.
Where authorized, use the declared per-command environment entrypoint.

An unapproved automatic hook is not necessarily a denial of manual
execution, but neither grants permission. Never use manual entry to bypass
an explicit denial. Installing replacements, changing the system, or trusting
recurring hooks requires the applicable authorization.

Distinguish an empty result from invocation failure. Return the working
invocation and decisive result, or the specific environment or approval gap.
