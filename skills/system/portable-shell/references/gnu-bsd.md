# GNU vs BSD/macOS quick reference

Check the installed variant with `<tool> --version` (GNU prints a banner; BSD
tools usually reject the flag) and `man <tool>`. Older macOS releases lack some
of the newer BSD additions noted below.

| Task | GNU (Linux) | BSD (macOS) | Portable choice |
| --- | --- | --- | --- |
| In-place edit | `sed -i 's/a/b/' f` | `sed -i '' 's/a/b/' f` | `sed 's/a/b/' f > f.tmp && mv f.tmp f`, or `perl -pi -e 's/a/b/' f` |
| Extended regex | `sed -E`, `grep -E` | same | `-E`; avoid GNU-only `\+`, `\?` in basic regex |
| Perl regex | `grep -P` | not available | `grep -E`, `rg`, or `perl -ne` |
| Date arithmetic | `date -d '1 day ago' +%F` | `date -v-1d +%F` | compute in `python3`/`perl`, or branch on `uname -s` |
| Epoch to date | `date -d @1700000000` | `date -r 1700000000` | same as above |
| File size | `stat -c %s f` | `stat -f %z f` | `wc -c < f` |
| Modification time | `stat -c %Y f` | `stat -f %m f` | branch on `uname -s` |
| Canonical path | `readlink -f p`, `realpath p` | newer macOS has both; old ones lack them | `(cd "$dir" && pwd -P)` for a directory; otherwise `python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$p"` |
| Skip empty xargs input | `xargs -r` | default behavior; `-r` accepted on newer macOS | `find … -exec cmd {} +` |
| Custom find output | `find -printf '%s %p\n'` | not available | `find … -exec stat … {} +` per platform, or `python3` |
| Base64 without wrapping | `base64 -w0` | `base64` (no wrap by default) | `base64 | tr -d '\n'` |
| SHA-256 | `sha256sum f` | `shasum -a 256 f` | `shasum -a 256` exists on most Linux too (Perl); else branch |
| Run with timeout | `timeout 10 cmd` | not installed by default (`gtimeout` via coreutils) | tool-native time limits, or `perl -e 'alarm shift; exec @ARGV' 10 cmd` |
| CPU count | `nproc` | `sysctl -n hw.ncpu` | `getconf _NPROCESSORS_ONLN` |
| Negative head/tail counts | `head -n -1` | not available | `sed '$d'` |
| Sort versions | `sort -V` | supported on newer macOS only | branch, or compare in a real language |
| Process listing | `ps -eo pid,args --sort=-%cpu` | `ps -Ao pid,command -r` | `ps -eo pid,args` (no sort flag) |
| Listening ports | `ss -ltnp` | `lsof -nP -iTCP -sTCP:LISTEN` | `lsof` when installed on both |

## Shell-language differences

| Behavior | bash | zsh | POSIX sh (dash) |
| --- | --- | --- | --- |
| Unquoted `$var` word splitting | yes | no (use `${=var}` or arrays) | yes |
| Unmatched glob | left literal | error (`nomatch`) | left literal |
| Arrays | indexed from 0 | indexed from 1 | none; use `set --` |
| `[[ … ]]` | yes | yes | no; use `[ … ]` |
| `pipefail` | `set -o pipefail` | `setopt pipefail` / `set -o pipefail` | not in older dash |
| `local` | yes | yes | widely supported, not POSIX |
