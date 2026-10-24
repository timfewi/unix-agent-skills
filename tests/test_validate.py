import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate import validate  # noqa: E402

SKILL = """---
name: {name}
description: Do {name} things. Use when {name} is needed.
---

# {name}

{body}
"""


def case(kind, selected):
    return {
        "kind": kind,
        "prompt": "p",
        "expected_selected": selected,
        "expected_excluded": [],
        "expected_initial_tools": [],
        "unavailable_or_forbidden_tools": [],
        "expected_completion_evidence": [],
    }


class ValidateTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)
        self.write_skill("alpha", "one-skill", "Plain guidance.")
        self.write_skill("beta", "two-skill", "More guidance.")
        self.routing = {
            "groups": [
                {
                    "id": "g",
                    "cases": [
                        case("positive", ["one-skill"]),
                        case("positive", ["two-skill"]),
                        case("negative", []),
                        case("ambiguous", ["one-skill", "two-skill"]),
                    ],
                }
            ]
        }
        self.write_routing()

    def write_skill(self, domain, name, body, frontmatter=None):
        directory = self.root / "skills" / domain / name
        directory.mkdir(parents=True, exist_ok=True)
        text = frontmatter or SKILL.format(name=name, body=body)
        (directory / "SKILL.md").write_text(text, encoding="utf-8")
        return directory

    def write_routing(self):
        path = self.root / "tests" / "routing_cases.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(self.routing), encoding="utf-8")

    def errors(self, deny=()):
        return validate(self.root, list(deny))[2]

    def assertError(self, check, deny=()):
        errors = self.errors(deny)
        self.assertTrue(any(f": {check}:" in e for e in errors), errors)

    def test_valid_catalog(self):
        skills, cases, errors = validate(self.root, [])
        self.assertEqual(errors, [])
        self.assertEqual(sorted(skills), ["one-skill", "two-skill"])
        self.assertEqual(cases, 4)

    def test_native_invocation_policy_is_supported_and_linked(self):
        directory = self.write_skill(
            "alpha", "one-skill", "See [native policy](agents/openai.yaml)."
        )
        (directory / "agents").mkdir()
        policy = directory / "agents/openai.yaml"
        policy.write_text("policy:\n  allow_implicit_invocation: false\n")
        self.assertEqual(self.errors(), [])
        self.write_skill("alpha", "one-skill", "Plain guidance.")
        self.assertError("orphan")

    def test_native_policy_rejects_ambiguous_values_and_other_metadata(self):
        directory = self.write_skill(
            "alpha", "one-skill", "See [native policy](agents/openai.yaml)."
        )
        (directory / "agents").mkdir()
        policy = directory / "agents/openai.yaml"
        for value in (
            "policy:\n  allow_implicit_invocation: 'false'\n",
            "policy:\n  allow_implicit_invocation: false\n  allow_implicit_invocation: true\n",
            "policy:\n  allow_implicit_invocation: false\ndependencies: {}\n",
        ):
            with self.subTest(value=value):
                policy.write_text(value)
                self.assertError("invocation-policy")
        policy.write_text("policy:\n  allow_implicit_invocation: false\n")
        (directory / "agents/other.yaml").write_text("other: true\n")
        self.assertError("layout")

    def test_mentioning_another_skill_breaks_isolation(self):
        self.write_skill("alpha", "one-skill", "Then load two-skill.")
        self.assertError("isolation")

    def test_link_outside_skill_breaks_isolation(self):
        self.write_skill("alpha", "one-skill", "See [x](../../beta/README.md).")
        self.assertError("isolation")

    def test_duplicate_name_across_domains(self):
        self.write_skill("gamma", "one-skill", "Copy.")
        self.assertError("duplicate-name")

    def test_skill_outside_a_domain(self):
        (self.root / "skills" / "loose").mkdir()
        (self.root / "skills" / "loose" / "SKILL.md").write_text("x")
        self.assertError("layout")

    def test_orphan_and_unlinked_resource(self):
        directory = self.root / "skills" / "alpha" / "one-skill"
        (directory / "references").mkdir()
        (directory / "references" / "extra.md").write_text("Extra.")
        self.assertError("orphan")

    def test_script_requires_compatibility(self):
        directory = self.write_skill("alpha", "one-skill", "Run scripts/run.sh.")
        (directory / "scripts").mkdir()
        (directory / "scripts" / "run.sh").write_text("#!/bin/sh\n")
        self.assertError("compatibility")

    def test_missing_trigger_phrase(self):
        text = "---\nname: one-skill\ndescription: Does things.\n---\n\nBody.\n"
        self.write_skill("alpha", "one-skill", "", frontmatter=text)
        self.assertError("description")

    def test_word_budget(self):
        self.write_skill("alpha", "one-skill", "word " * 420)
        self.assertError("length")

    def test_personal_home_path_and_denied_term(self):
        self.write_skill("alpha", "one-skill", "Open /home/alice/notes and acme-corp.")
        self.assertError("personal-path")
        self.assertError("denied-term", deny=["acme-corp"])

    def test_routing_names_and_coverage(self):
        self.routing["groups"][0]["cases"][1] = case("positive", ["ghost"])
        self.write_routing()
        self.assertError("routing-name")
        self.assertError("routing-coverage")

    def test_routing_group_needs_all_kinds(self):
        self.routing["groups"][0]["cases"].pop(2)
        self.write_routing()
        self.assertError("routing-kinds")

    def test_peer_catalog_names_break_isolation(self):
        peer = self.root / "peer"
        (peer / "skills/core/core-skill").mkdir(parents=True)
        (peer / "skills/core/core-skill/SKILL.md").write_text("x", encoding="utf-8")
        self.write_skill("alpha", "one-skill", "Load core-skill first.")
        self.assertEqual(self.errors(), [])
        errors = validate(self.root, [], (peer,))[2]
        self.assertTrue(
            any(": isolation: mentions skill 'core-skill'" in e for e in errors), errors
        )

    def test_cli_validates_another_root(self):
        def run():
            return subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/validate.py"),
                    "--root",
                    self.root,
                ],
                capture_output=True,
                text=True,
                check=False,
            )

        valid = run()
        self.assertEqual(valid.returncode, 0, valid.stdout)
        self.assertIn("skills=2 ", valid.stdout)
        self.write_skill("alpha", "one-skill", "Use two-skill first.")
        invalid = run()
        self.assertEqual(invalid.returncode, 1)
        self.assertIn("isolation", invalid.stdout)


SNAPSHOT = ROOT / "skills/system/process-debugging/scripts/proc-snapshot.sh"


@unittest.skipUnless(shutil.which("ps") and shutil.which("pgrep"), "needs ps")
class ProcSnapshotTest(unittest.TestCase):
    def run_snapshot(self, *args):
        return subprocess.run(
            ["sh", str(SNAPSHOT), *args],
            capture_output=True,
            check=False,
            text=True,
            timeout=30,
        )

    def test_snapshot_of_running_process(self):
        child = subprocess.Popen(["sleep", "30"])
        self.addCleanup(child.wait)
        self.addCleanup(child.kill)
        result = self.run_snapshot(str(child.pid))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("## process", result.stdout)
        self.assertIn("sleep 30", result.stdout)
        self.assertIn("## sockets", result.stdout)

    def test_rejects_non_numeric_pid(self):
        self.assertEqual(self.run_snapshot("1; rm -rf /").returncode, 2)
        self.assertEqual(self.run_snapshot().returncode, 2)

    def test_missing_process(self):
        self.assertEqual(self.run_snapshot("999999999").returncode, 1)


if __name__ == "__main__":
    unittest.main()
