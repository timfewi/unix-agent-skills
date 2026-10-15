---
name: process-debugging
description: Inspect and debug running processes and services on Linux or macOS (hangs, high CPU or memory, port already in use, zombies, crash loops, failing systemd or launchd units) with bounded, read-only evidence first. Use when a program misbehaves at runtime and the cause is in its process state, resources or service manager.
compatibility: scripts/proc-snapshot.sh needs a POSIX sh, ps and pgrep; ss (Linux) or lsof add socket details.
---

# Process debugging

Observe before acting. Every probe is read-only and time-bounded.

1. **Find the process.**
   - By name: `pgrep -af <name>` on Linux, `pgrep -lf <name>` on macOS.
   - Top consumers: `ps -eo pid,ppid,stat,etime,%cpu,%mem,args --sort=-%cpu | head`
     on Linux, `ps -Ao pid,ppid,stat,etime,%cpu,%mem,command -r | head` on macOS.
   - By port: `ss -ltnp 'sport = :8080'` or `lsof -nP -iTCP:8080 -sTCP:LISTEN`.
2. **Snapshot it.** Run `sh scripts/proc-snapshot.sh <pid>` from this skill
   directory ([script](scripts/proc-snapshot.sh)). It prints the state, children,
   memory, wait channel, cwd, fd count, limits, cgroup and sockets.
3. **Read the state letter.**
   - `R`: busy on CPU, so profile it.
   - `S`: waiting; check the wait channel and sockets.
   - `D`: uninterruptible I/O; signals will not help, so check disk and NFS.
   - `Z`: zombie; the parent is not reaping it.
   - `T`: stopped by a signal or debugger.
4. **Go one level deeper only where the evidence points:**
   - Hang: `timeout 10 strace -f -p <pid> -o <file>` (Linux; ptrace may be
     restricted), `sample <pid> 5` (macOS), or py-spy/gdb if installed.
   - CPU: `top -b -n 1 -H -p <pid>` (Linux) or `top -l 1 -pid <pid>` (macOS).
   - Memory: compare two snapshots over time; for OOM kills check
     `journalctl -k --since -1h --no-pager | grep -i oom`.
   - Services: `systemctl status <unit> --no-pager`,
     `journalctl -u <unit> -n 100 --no-pager` (add `--user` for user units);
     on macOS `launchctl print gui/$(id -u)/<label>` and
     `log show --last 10m --predicate 'process == "<name>"'`.
5. **Bound everything.** Use `timeout` on Linux; macOS lacks it by default, so
   use tool-native durations. Write traces to a file and read a summary.

Signals and restarts change system state. Send them only to processes you
started or were authorized to stop: `SIGTERM` first, wait, then `SIGKILL`.
Never signal PID 1, the agent's own harness or another user's process.
Restarting units is an availability change that needs authorization.

Report the PID, state, evidence and cause, marked confirmed or hypothesis.
