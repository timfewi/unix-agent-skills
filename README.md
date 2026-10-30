# unix-agent-skills

A small, curated set of [Agent Skills](https://agentskills.io/specification)
for coding agents (Claude Code, Codex, OpenCode and others) working on
Unix-like systems: Linux and macOS, bash and zsh, GNU and BSD userlands.

Each skill does one job, stands alone and is short enough to load whole.

## Domains

| Domain | Skill | Use when |
| --- | --- | --- |
| `agent/` | `context-management` | a session resumes, compacts or fills with output |
| | `goal-workflow` | defining an agent goal or explicitly executing a previously defined goal |
| | `tool-use` | choosing a tool for an evidence question and running calls efficiently |
| | `host-cli-usage` | invoking an unfamiliar CLI or after an argument error |
| | `capability-incident-diagnoser` | a tool, MCP server or sandboxed operation is missing or denied |
| `code/` | `filesystem-wizard` | the owning files or callers are not yet known |
| | `lean-code` | simplifying or consolidating code without changing behavior |
| | `fast-checks` | choosing proportionate verification, or a check fails |
| | `test-freshness` | tests may no longer detect the failure they guard |
| `vcs/` | `brokered-git-operator` | an authorized commit, push or review request on any forge |
| | `finalize-loop` | wrapping up a change: review, verify, judge, land, read back |
| `security/` | `security-boundary-review` | credentials, permissions, sandboxes, egress or publication |
| `system/` | `process-debugging` | a process hangs, burns CPU or memory, holds a port, or a unit fails |
| | `portable-shell` | a script must run on Linux and macOS, or bash/zsh behave differently |

## Rules

- **Isolated.** A skill never names another skill or repository and never
  links outside its own directory. Skills may overlap a little rather than
  depend on each other. Names are unique across domains.
- **Short.** The whole `SKILL.md` stays within 400 words (target 150–300).
  Detail that is needed only sometimes goes into a linked reference.
- **Triggerable.** The `description` says what the skill does and contains
  "Use when" or "Use for".
- **Resources.** `references/*.md`, `scripts/*.{py,sh}` and
  `assets/*.{md,txt,json}`, each linked from `SKILL.md`. Scripts are read-only
  helpers, declare their interpreters in `compatibility`, and are tested for
  success and failure.
- **Invocation policy.** Optional, linked `agents/openai.yaml` supports only
  `policy:` followed by `  allow_implicit_invocation: false` (or `true`). It
  controls native Codex discovery; other harnesses may ignore it. Explicit-only
  skills must also state their activation condition in the entrypoint. Extra
  metadata fields require a deliberate validator extension.
- **Evidence.** Every skill is selected by at least one positive case in
  [tests/routing_cases.json](tests/routing_cases.json); each group also has a
  negative and an ambiguous case. These are rubrics; the validator does not run
  a model. Claim a behavioral improvement only after comparing identical tasks
  with and without the change.

## Install

With Nix, `lib.skills` maps each skill name to its directory, and
`packages.<system>.skills` is a flat directory of all skills. Prefer the map
in modules: listing the package during evaluation imports from a derivation.

```nix
skills = inputs.unix-agent-skills.lib.skills;
# or pick some:
selected = { inherit (inputs.unix-agent-skills.lib.skills) tool-use lean-code; };
# a built directory, for tools that read it at build or run time:
skillsDirectory = inputs.unix-agent-skills.packages.${system}.skills;
```

Without Nix, link each skill directory into the harness's skill directory, for
example for Claude Code:

```sh
for skill in skills/*/*/; do ln -s "$PWD/$skill" ~/.claude/skills/; done
```

## Private overlay

Machine- or person-specific guidance does not belong here, and neither do
skills belong in project or host repositories. Keep personal skills in a
separate private skill repository with the same layout, install it next to
this catalog, and validate it with this catalog as a peer so it names no core
skill:

```sh
python3 scripts/validate.py --root ../my-private-skills --peer .
```

Give a personal variant the catalog skill's name to replace it, so agents see
one definition. Before publishing this catalog, run the validator with a
private term list kept outside this repository:

```sh
python3 scripts/validate.py --deny-file ~/path/to/private-terms.txt
```

## Development

```sh
devenv shell                 # python3, ruff, shellcheck, nixfmt, statix, deadnix
project-check fast          # or run the commands below directly
python3 scripts/validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
nix flake check --no-build  # evaluates all three systems
```

## Support

Created and maintained by Tim Witter. If these skills save you time, please
consider starring the repository, sharing it with attribution, or supporting
its maintenance. Companies benefiting from this project are especially welcome
to sponsor continued development. Financial support is appreciated, never
required.

For sponsorship or support inquiries, contact
[hello@timwitter.com](mailto:hello@timwitter.com).

## Status

2026-10-16: 14 skills in five domains, 40 routing cases. The validator, its
unit tests, the snapshot-script tests (Linux), ruff, shellcheck and Nix lint
pass. The macOS paths of `proc-snapshot.sh` and the macOS forms in
`portable-shell` have not been run on macOS. No model comparison has been run
for the rewritten skills yet. A tracked privacy scan reports only the synthetic
`/home/alice` fixture in `tests/test_validate.py`; the skills pass the
validator's private-term check. The repository is public following a review of
the tracked files, Git history and repository publication surfaces.
