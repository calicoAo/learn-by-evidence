#!/usr/bin/env python3
"""Validate the schema of the behavior-evaluation case catalog."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ALLOWED_TYPES = {
    "activation_positive",
    "activation_negative",
    "behavior",
    "multiturn",
    "state",
    "robustness",
}
ALLOWED_SEVERITIES = {"P0", "P1", "P2"}


def validate_cases(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot load {path}: {exc}"]

    if not isinstance(payload, dict):
        return ["Root JSON value must be an object"]
    if payload.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        return errors + ["cases must be a non-empty array"]

    seen: set[str] = set()
    required = {"id", "type", "severity", "input", "must", "must_not"}
    for index, case in enumerate(cases):
        prefix = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = required - set(case)
        if missing:
            errors.append(f"{prefix} is missing: {', '.join(sorted(missing))}")
            continue
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"{prefix}.id must be a non-empty string")
        elif case_id in seen:
            errors.append(f"Duplicate case id: {case_id}")
        else:
            seen.add(case_id)
        if case["type"] not in ALLOWED_TYPES:
            errors.append(f"{prefix}.type is invalid: {case['type']}")
        if case["severity"] not in ALLOWED_SEVERITIES:
            errors.append(f"{prefix}.severity is invalid: {case['severity']}")
        if not isinstance(case["input"], (str, list)) or not case["input"]:
            errors.append(f"{prefix}.input must be a non-empty string or conversation array")
        for field in ("must", "must_not"):
            value = case[field]
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                errors.append(f"{prefix}.{field} must be an array of strings")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases_file", type=Path, help="Path to tests/cases.json")
    args = parser.parse_args()
    errors = validate_cases(args.cases_file)
    if errors:
        print("Case validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Case validation passed: {args.cases_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
