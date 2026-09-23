#!/usr/bin/env python3
"""Validate the portable structure of a single Agent Skill.

This intentionally uses only the Python standard library so it can run in a
fresh checkout and in GitHub Actions without installing dependencies.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
YAML_VALUE_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*[\"']?(.*?)[\"']?\s*$")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, list[str]]:
    errors: list[str] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text, ["SKILL.md must start with YAML frontmatter delimited by ---"]

    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, text, ["SKILL.md frontmatter is missing its closing ---"]

    data: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = YAML_VALUE_RE.match(line)
        if not match:
            errors.append(f"Unsupported frontmatter syntax on line {number}: {line!r}")
            continue
        key, value = match.groups()
        if key in data:
            errors.append(f"Duplicate frontmatter key: {key}")
        data[key] = value.strip()

    return data, "\n".join(lines[end + 1 :]).strip(), errors


def _clean_link_target(target: str) -> str:
    target = target.strip().split("#", 1)[0]
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return target


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_dir = skill_dir.resolve()
    manifest = skill_dir / "SKILL.md"

    if not manifest.is_file():
        return [f"Missing required file: {manifest}"]

    text = manifest.read_text(encoding="utf-8")
    frontmatter, body, parse_errors = parse_frontmatter(text)
    errors.extend(parse_errors)

    expected_keys = {"name", "description"}
    actual_keys = set(frontmatter)
    missing = expected_keys - actual_keys
    extra = actual_keys - expected_keys
    if missing:
        errors.append(f"Missing frontmatter keys: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"Unsupported frontmatter keys: {', '.join(sorted(extra))}")

    name = frontmatter.get("name", "")
    if name and not NAME_RE.fullmatch(name):
        errors.append("Skill name must use lowercase letters, digits, and hyphens only")
    if len(name) > 64:
        errors.append("Skill name must be at most 64 characters")
    if not frontmatter.get("description", "").strip():
        errors.append("Skill description must not be empty")
    if not body:
        errors.append("SKILL.md body must not be empty")
    if len(text.splitlines()) > 500:
        errors.append("SKILL.md should stay below 500 lines; move details into references/")

    for path in skill_dir.rglob("*"):
        if path.is_file():
            content = path.read_text(encoding="utf-8", errors="replace")
            if "[TODO" in content or "TODO:" in content:
                errors.append(f"Placeholder TODO remains in {path.relative_to(skill_dir)}")

    for raw_target in MARKDOWN_LINK_RE.findall(text):
        target = _clean_link_target(raw_target)
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        candidate = (skill_dir / target).resolve()
        try:
            candidate.relative_to(skill_dir)
        except ValueError:
            errors.append(f"Link escapes the skill directory: {raw_target}")
            continue
        if not candidate.exists():
            errors.append(f"Broken local link in SKILL.md: {raw_target}")

    ui_metadata = skill_dir / "agents" / "openai.yaml"
    if not ui_metadata.is_file():
        errors.append("Missing recommended UI metadata: agents/openai.yaml")
    else:
        ui_text = ui_metadata.read_text(encoding="utf-8")
        for field in ("display_name:", "short_description:", "default_prompt:"):
            if field not in ui_text:
                errors.append(f"agents/openai.yaml is missing {field[:-1]}")
        if name and f"${name}" not in ui_text:
            errors.append(f"default_prompt should explicitly mention ${name}")
        for icon_path in re.findall(r"icon_(?:small|large):\s*[\"']?([^\"'\n]+)", ui_text):
            icon_path = icon_path.strip()
            if not (skill_dir / icon_path).is_file():
                errors.append(f"Referenced icon does not exist: {icon_path}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path, help="Path to the skill directory")
    args = parser.parse_args()

    errors = validate_skill(args.skill_dir)
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Skill validation passed: {args.skill_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
