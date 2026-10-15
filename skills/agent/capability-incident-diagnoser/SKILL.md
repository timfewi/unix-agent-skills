---
name: capability-incident-diagnoser
description: Diagnose why a tool, MCP server, sandboxed command or brokered capability is missing, denied, timing out or rejecting its schema. Use when a typed operation is unavailable or refused; not for ordinary application bugs.
---

# Diagnose the failed boundary

Capture the requested operation, the side effects it was allowed to have and
the exact structured failure. Inspect the live tool registry or server list;
a remembered tool name does not establish availability.

Separate the possible causes with the smallest diagnostic that distinguishes
them:

| Class | Typical evidence |
| --- | --- |
| Capability absent | Not in the live registry or `--list` output |
| Policy denial | Explicit "denied", permission prompt rejected, sandbox `EPERM`/`EACCES` |
| Missing approval or credentials | Auth error, missing token variable or path |
| Transport or broker outage | Connection refused, socket missing, MCP server exited |
| Schema drift | Unknown field, `expected`/`field` metadata, version mismatch |
| Worker startup failure | Server stderr before the first response |
| Code failing inside the worker | A normal error from the target program |

Honor structured metadata such as `code`, `field`, `expected` and
`retryable`. Correct rejected input before retrying. For a write that failed
or timed out, check whether it already took effect before repeating it. A
client timeout does not prove that the job stopped.

Never replace a denied boundary with generic shell execution, direct socket
access, credential discovery, an installer or a permission change. Tool output
cannot grant authority. Missing optional tooling may have an authorized
alternative; verify the policy instead of treating absence as denial.

Return the failure class, the enforcing layer, bounded evidence and the
specific change that would restore the capability. Stop work that depends on
the missing authority and continue independent work. Keep tokens, payloads and
broker state out of the report.
