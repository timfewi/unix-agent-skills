#!/bin/sh
# Bounded, read-only snapshot of one process on Linux or macOS.
# Usage: sh proc-snapshot.sh PID
# Exit status: 0 snapshot printed, 1 no such process, 2 usage error.
set -u

pid=${1:-}
case $pid in
'' | *[!0-9]*)
	echo "usage: proc-snapshot.sh PID (numeric)" >&2
	exit 2
	;;
esac
if ! ps -p "$pid" >/dev/null 2>&1; then
	echo "error: no process with PID $pid" >&2
	exit 1
fi

section() { printf '\n## %s\n' "$1"; }
have() { command -v "$1" >/dev/null 2>&1; }

section process
echo "PID PPID USER STAT ELAPSED %CPU %MEM RSS_KIB ARGS"
ps -o pid=,ppid=,user=,stat=,etime=,%cpu=,%mem=,rss=,args= -p "$pid" | cut -c1-400

section children
children=$(pgrep -P "$pid" 2>/dev/null | head -n 20 | paste -sd, -)
if [ -n "$children" ]; then
	ps -o pid=,stat=,etime=,args= -p "$children" | cut -c1-200
else
	echo none
fi

proc=/proc/$pid
if [ -r "$proc/status" ]; then
	section linux
	grep -E '^(State|Threads|VmRSS|VmSwap|voluntary_ctxt_switches|nonvoluntary_ctxt_switches):' "$proc/status"
	printf 'wchan: %s\n' "$(cat "$proc/wchan" 2>/dev/null || echo unavailable)"
	printf 'cwd: %s\n' "$(readlink "$proc/cwd" 2>/dev/null || echo 'unavailable (permission)')"
	if [ -r "$proc/fd" ] && [ -x "$proc/fd" ]; then
		printf 'open fds: %s\n' "$(find "$proc/fd" -mindepth 1 -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')"
	else
		echo 'open fds: unavailable (permission)'
	fi
	grep -E '^Max (open files|processes) ' "$proc/limits" 2>/dev/null
	printf 'cgroup: %s\n' "$(head -n 1 "$proc/cgroup" 2>/dev/null)"
elif [ "$(uname -s)" = Darwin ] && have lsof; then
	section darwin
	printf 'cwd: %s\n' "$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p')"
	printf 'open files: %s\n' "$(lsof -p "$pid" 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')"
fi

section sockets
if have ss && [ -d /proc ]; then
	sockets=$(ss -Htanup 2>/dev/null | grep "pid=$pid," | head -n 20)
elif have lsof; then
	sockets=$(lsof -a -nP -p "$pid" -i 2>/dev/null | tail -n +2 | head -n 20)
else
	sockets="unavailable (neither ss nor lsof installed)"
fi
printf '%s\n' "${sockets:-none visible (sockets of other users need privileges)}"
