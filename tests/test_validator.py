from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


skill_validator = load_module("validate_skill", ROOT / "scripts" / "validate_skill.py")
case_validator = load_module("validate_cases", ROOT / "scripts" / "validate_cases.py")


class SkillValidatorTests(unittest.TestCase):
    def test_repository_skill_is_valid(self):
        errors = skill_validator.validate_skill(ROOT / "skills" / "learn-by-evidence")
        self.assertEqual([], errors)

    def test_missing_description_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            skill = Path(temp)
            (skill / "agents").mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: sample-skill\n---\n\nDo the work.\n",
                encoding="utf-8",
            )
            (skill / "agents" / "openai.yaml").write_text(
                "interface:\n  display_name: Sample\n  short_description: Sample skill\n"
                "  default_prompt: Use $sample-skill.\n",
                encoding="utf-8",
            )
            errors = skill_validator.validate_skill(skill)
            self.assertTrue(any("Missing frontmatter keys: description" in error for error in errors))

    def test_broken_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            skill = Path(temp)
            (skill / "agents").mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: sample-skill\ndescription: Sample.\n---\n\n"
                "Read [missing](references/missing.md).\n",
                encoding="utf-8",
            )
            (skill / "agents" / "openai.yaml").write_text(
                "interface:\n  display_name: Sample\n  short_description: Sample skill\n"
                "  default_prompt: Use $sample-skill.\n",
                encoding="utf-8",
            )
            errors = skill_validator.validate_skill(skill)
            self.assertTrue(any("Broken local link" in error for error in errors))


class CaseValidatorTests(unittest.TestCase):
    def test_repository_cases_are_valid(self):
        errors = case_validator.validate_cases(ROOT / "tests" / "cases.json")
        self.assertEqual([], errors)

    def test_duplicate_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "cases.json"
            item = {
                "id": "DUP-01",
                "type": "behavior",
                "severity": "P1",
                "input": "Test",
                "must": [],
                "must_not": [],
            }
            path.write_text(
                json.dumps({"schema_version": 1, "cases": [item, item]}),
                encoding="utf-8",
            )
            errors = case_validator.validate_cases(path)
            self.assertTrue(any("Duplicate case id" in error for error in errors))


class RepositoryManifestTests(unittest.TestCase):
    def test_plugin_manifest_has_required_portable_fields(self):
        payload = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual("learn-by-evidence", payload["name"])
        self.assertEqual("1.1.0", payload["version"])
        self.assertTrue(payload["description"])
        self.assertEqual(
            "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            payload["$schema"],
        )

    def test_repository_has_standard_mit_license(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(license_text.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2026 Calico Li", license_text)
        self.assertIn("Permission is hereby granted, free of charge", license_text)


if __name__ == "__main__":
    unittest.main()
