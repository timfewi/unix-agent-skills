"""Validate the catalog: domain layout, frontmatter, resources and skill isolation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
ALLOWED_KEYS = {"name", "description", "license", "compatibility"}
TRIGGER_RE = re.compile(r"\buse (?:when|for)\b", re.IGNORECASE)
MAX_WORDS = 400
MAX_DESCRIPTION = 1024
RESOURCE_SUFFIXES = {
    "references": {".md"},
    "scripts": {".py", ".sh"},
    "assets": {".md", ".txt", ".json"},
    "agents": {".yaml"},
}
RESOURCE_MENTION_RE = re.compile(r"(?:references|scripts|assets|agents)/[\w.-]+\.\w+")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
HOME_RE = re.compile(r"/(?:home|Users)/(?!user\b)[A-Za-z0-9_][\w.-]*")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|FIXME|CHANGEME)\b|\{\{[^}\n]+\}\}")
SECRET_RE = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----|https?://[^\s/@:]+:[^\s/@]+@|"
    r"(?:password|api[_-]?key|access[_-]?token|client[_-]?secret)"
    r"\s*[:=]\s*['\"][^'\"]+",
    re.IGNORECASE,
)
CASE_KINDS = {"positive", "negative", "ambiguous"}
CASE_LISTS = (
    "expected_selected",
    "expected_excluded",
    "expected_initial_tools",
    "unavailable_or_forbidden_tools",
    "expected_completion_evidence",
)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        return None
    end = lines.index("---", 1)
    values = {}
    for line in lines[1:end]:
        key, separator, value = line.partition(":")
        if not separator:
            return None
        values[key.strip()] = value.strip()
    return values


def discover(skills_root: Path, errors: list[str]) -> dict[str, Path]:
    """Map skill name to directory for skills/<domain>/<skill>/SKILL.md."""
    skills: dict[str, Path] = {}
    for domain in sorted(skills_root.iterdir()):
        if not domain.is_dir() or domain.is_symlink():
            errors.append(f"{domain}: layout: only domain directories belong here")
            continue
        if not NAME_RE.fullmatch(domain.name):
            errors.append(f"{domain}: domain-name: use lowercase-hyphen names")
        for skill in sorted(domain.iterdir()):
            if not skill.is_dir() or skill.is_symlink():
                errors.append(f"{skill}: layout: only skill directories belong here")
            elif not (skill / "SKILL.md").is_file():
                errors.append(f"{skill}: layout: missing SKILL.md")
            elif skill.name in skills:
                errors.append(
                    f"{skill}: duplicate-name: also {skills[skill.name]}; "
                    "names must be unique across domains"
                )
            else:
                skills[skill.name] = skill
    return skills


def resource_files(skill: Path, errors: list[str]) -> list[Path]:
    files = []
    for path in sorted(skill.rglob("*")):
        relative = path.relative_to(skill)
        if path.is_symlink() or not (path.is_file() or path.is_dir()):
            errors.append(f"{path}: file-type: regular files and directories only")
        elif path.is_dir():
            if len(relative.parts) > 1 or relative.name not in RESOURCE_SUFFIXES:
                errors.append(f"{path}: layout: unexpected directory")
        elif relative.as_posix() != "SKILL.md":
            allowed = RESOURCE_SUFFIXES.get(relative.parts[0], set())
            if (
                len(relative.parts) != 2
                or path.suffix not in allowed
                or (relative.parts[0] == "agents" and relative.name != "openai.yaml")
            ):
                errors.append(f"{path}: layout: unexpected resource")
            else:
                files.append(path)
    return files


def check_text(path: Path, text: str, others: list[str], deny: list[str]) -> list[str]:
    errors = []
    if SECRET_RE.search(text):
        errors.append(f"{path}: possible-credential: inspect without printing it")
    if match := PLACEHOLDER_RE.search(text):
        errors.append(f"{path}: placeholder: {match.group(0)}")
    if match := HOME_RE.search(text):
        errors.append(f"{path}: personal-path: {match.group(0)}")
    lowered = text.lower()
    errors += [f"{path}: denied-term: {term}" for term in deny if term in lowered]
    errors += [
        f"{path}: isolation: mentions skill {name!r}"
        for name in others
        if re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", text)
    ]
    return errors


def check_skill(
    name: str, skill: Path, catalog: list[str], deny: list[str]
) -> list[str]:
    errors: list[str] = []
    entry = skill / "SKILL.md"
    files = resource_files(skill, errors)
    others = [other for other in catalog if other != name]
    texts = {}
    for path in [entry, *files]:
        try:
            texts[path] = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(f"{path}: encoding: must be readable UTF-8")
            continue
        errors += check_text(path, texts[path], others, deny)
        if path.relative_to(
            skill
        ).as_posix() == "agents/openai.yaml" and not re.fullmatch(
            r"policy:\n  allow_implicit_invocation: (?:true|false)\n?", texts[path]
        ):
            errors.append(
                f"{path}: invocation-policy: expected one literal boolean policy"
            )
        for target in LINK_RE.findall(texts[path]):
            if re.match(r"[a-z]+:|#", target):
                continue
            resolved = (path.parent / target.split("#")[0]).resolve()
            if not resolved.is_relative_to(skill.resolve()):
                errors.append(f"{path}: isolation: link leaves the skill: {target}")
            elif not resolved.exists():
                errors.append(f"{path}: broken-link: {target}")

    text = texts.get(entry, "")
    meta = parse_frontmatter(text)
    if meta is None:
        return [*errors, f"{entry}: frontmatter: expected one ---/--- block"]
    if unknown := sorted(set(meta) - ALLOWED_KEYS):
        errors.append(f"{entry}: frontmatter: unknown keys {unknown}")
    if meta.get("name") != name or not NAME_RE.fullmatch(name) or len(name) > 64:
        errors.append(f"{entry}: name: must equal the directory name {name!r}")
    description = meta.get("description", "")
    if not TRIGGER_RE.search(description) or len(description) > MAX_DESCRIPTION:
        errors.append(
            f"{entry}: description: needs 'Use when/for' and at most "
            f"{MAX_DESCRIPTION} characters"
        )
    if (words := len(text.split())) > MAX_WORDS:
        errors.append(f"{entry}: length: {words} words exceeds {MAX_WORDS}")
    if any(path.parent.name == "scripts" for path in files) and not meta.get(
        "compatibility"
    ):
        errors.append(f"{entry}: compatibility: declare interpreters for scripts")
    mentioned = {skill / item for item in RESOURCE_MENTION_RE.findall(text)}
    errors += [
        f"{path}: orphan: link it from SKILL.md"
        for path in files
        if path not in mentioned
    ]
    errors += [
        f"{entry}: broken-link: {path.relative_to(skill)}"
        for path in mentioned
        if not path.is_file()
    ]
    return errors


def check_routing(path: Path, catalog: list[str]) -> tuple[int, list[str]]:
    try:
        groups = json.loads(path.read_text(encoding="utf-8"))["groups"]
    except (OSError, ValueError, KeyError, TypeError) as error:
        return 0, [f"{path}: routing: {error}"]
    errors: list[str] = []
    seen_ids: set[str] = set()
    selected: set[str] = set()
    count = 0
    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("cases"), list):
            errors.append(f"{path}: routing-group: expected an object with cases")
            continue
        group_id = group.get("id")
        if not group_id or group_id in seen_ids:
            errors.append(f"{path}: routing-id: missing or duplicate {group_id!r}")
        seen_ids.add(group_id)
        kinds = set()
        for case in group["cases"]:
            count += 1
            if not (
                isinstance(case, dict)
                and isinstance(case.get("prompt"), str)
                and all(isinstance(case.get(field), list) for field in CASE_LISTS)
            ):
                errors.append(
                    f"{path}: routing-case: {group_id} needs prompt and lists"
                )
                continue
            kinds.add(case.get("kind"))
            names = case["expected_selected"] + case["expected_excluded"]
            errors += [
                f"{path}: routing-name: {group_id} names unknown skill {name!r}"
                for name in names
                if name not in catalog
            ]
            if case.get("kind") == "positive":
                selected.update(case["expected_selected"])
        if kinds != CASE_KINDS:
            errors.append(f"{path}: routing-kinds: {group_id} has {sorted(kinds)}")
    errors += [
        f"{path}: routing-coverage: no positive case selects {name!r}"
        for name in catalog
        if name not in selected
    ]
    return count, errors


def validate(
    root: Path, deny: list[str], peers: tuple[Path, ...] = ()
) -> tuple[dict[str, Path], int, list[str]]:
    errors: list[str] = []
    skills = discover(root / "skills", errors)
    catalog = sorted(skills)
    # Naming a skill of a catalog installed alongside is a dependency too.
    peer_names = {name for peer in peers for name in discover(peer / "skills", [])}
    names = sorted(peer_names.union(catalog))
    for name, skill in skills.items():
        errors += check_skill(name, skill, names, deny)
    cases, routing_errors = check_routing(
        root / "tests" / "routing_cases.json", catalog
    )
    return skills, cases, errors + routing_errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--deny-file",
        type=Path,
        help="file with one private term per line that no skill may contain",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="catalog with skills/ and tests/routing_cases.json (default: this one)",
    )
    parser.add_argument(
        "--peer",
        type=Path,
        action="append",
        default=[],
        help="catalog installed alongside; its skill names count for isolation",
    )
    args = parser.parse_args()
    deny = []
    if args.deny_file:
        lines = args.deny_file.read_text(encoding="utf-8").splitlines()
        deny = [line.strip().lower() for line in lines if line.strip()]
    root = args.root.resolve()
    skills, cases, errors = validate(root, deny, tuple(args.peer))
    print(f"skills={len(skills)} routing_cases={cases} errors={len(errors)}")
    for error in errors:
        print("ERROR", error.replace(f"{root}/", ""))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
