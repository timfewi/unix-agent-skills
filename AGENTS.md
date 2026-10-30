# Repository policy

Rule one: few, isolated, short skills. Read README.md before changing a skill,
the layout or the validator.

- Skills live in `skills/<domain>/<skill>/`. A skill never names another skill
  or repository and never links outside its directory; `scripts/validate.py`
  enforces this. Personal or machine-specific skills belong in the private
  catalog `../private-skills-catalog`, never in a project or host
  repository: keep this catalog publishable.
- Edit the smallest thing that fixes an observed problem. Before adding a
  skill, check whether an existing one should absorb the job. Update
  `tests/routing_cases.json` with each new or changed trigger.
- Python uses the standard library only. Scripts in skills are read-only
  helpers, linked from `SKILL.md`, declared in `compatibility`, and tested for
  success and failure in `tests/`.
- Text is English. Run `project-check fast` before handoff. `project-check full`
  evaluates all systems and builds the catalog check; it is a separate workload.
- Commits, pushes, visibility changes and releases need explicit authorization.
