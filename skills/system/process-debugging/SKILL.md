---
name: process-debugging
description: Use for hangs, resource spikes, occupied ports, zombies, crash loops, or failing Linux/macOS services; start with bounded process evidence.
compatibility: scripts/proc-snapshot.sh needs a POSIX sh, ps and pgrep; ss (Linux) or lsof add socket details.
---

# Diagnose the process, not the symptom

Identify the task-related PID or unit, its owner, and the observation interval.
Start read-only and inspect only the relevant process tree. A snapshot is not
a trend, and a busy process is not necessarily the bottleneck.

Useful entrypoints include `pgrep -af <name>` on Linux, `pgrep -lf <name>` on
macOS, and a port-specific `ss` or `lsof` query. For a bounded baseline, run
`sh scripts/proc-snapshot.sh <pid>` from this skill directory
([script](scripts/proc-snapshot.sh)). Inspect and redact sensitive arguments
or paths before sharing output.

| State | Next question |
| --- | --- |
| R | Sustained CPU work or just this sample? |
| S | Which wait channel, socket, or child explains the wait? |
| D | Blocked storage or NFS? Killing cannot resolve the I/O wait. |
| Z | Why is the parent not reaping children? |
| T | Which signal or debugger stopped it? |

Follow the evidence: compare memory snapshots; inspect bounded service logs
or OOM evidence; use thread views for CPU. `systemctl`/`journalctl` and
`launchctl`/`log` have different scopes. A debugger or syscall trace can
perturb or pause the target: attach only within permission and with a time
limit. macOS often needs tool-native durations rather than `timeout`.

Signals and restarts change availability. Signal only processes you started
or are authorized to stop: terminate gracefully, wait, and escalate only if
needed and authorized. Never signal PID 1, the agent's harness, or another
user's process. Unit restarts need authorization.

Report PID/unit, observed state, decisive evidence, and whether the cause is
confirmed or a hypothesis.
