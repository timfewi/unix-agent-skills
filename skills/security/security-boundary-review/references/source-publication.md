# Source-publication privacy review

Publication exposes the tracked tree **and** the full history. Review both.

## Coverage

1. Inventory what will be published: `git ls-files` for the current tree,
   `git rev-list --all --count` for history size, `git submodule status` for
   nested repositories. Untracked files are not published but often hold the
   evidence that leaks later; list them with `git status --short --ignored`.
2. Prefer an installed secret/privacy scanner (for example `gitleaks`,
   `trufflehog`, or a host-provided privacy scanner). Read its `--help` and
   select the mode that scans tracked files and, separately, history:
   `gitleaks dir <path>` versus `gitleaks git <repo>` in current gitleaks.
3. Record coverage explicitly: which paths, which revisions, which rules, what
   was skipped (binaries, large files, submodules, untracked files).
4. If no scanner is available, report that limit and continue with manual
   review; absence of a scanner is not a clean result.

## Manual checks

- Personal identifiers: home paths (`/home/<name>`, `/Users/<name>`), host
  names, e-mail addresses, internal URLs, private repository names.
  `git log --format='%an <%ae>' | sort -u` shows author identities in history.
- Credentials: keys, tokens, `.env` files, cloud config, private CA material,
  even if later deleted (deleted files remain in history).
- Data: databases, logs, transcripts, model outputs, customer content.
- Config that reveals private infrastructure: IPs, tailnet names, ports.

## Findings

Keep reports outside the repository. Reference rule IDs, paths and line
numbers, not the matched secret. Distinguish synthetic fixtures and required
upstream coordinates from real personal data. A clean scan grants no authority
to change visibility, push, or rewrite history; each needs its own explicit
authorization. A leaked credential must be rotated even after removal.
