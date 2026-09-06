#!/usr/bin/env python3
"""Validate the generated registry against its source skill files."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.build_registry import parse_skill_metadata, read_version

REGISTRY_PATH = REPO_ROOT / "registry" / "registry.json"
REQUIRED_FIELDS = {"id", "category", "summary", "path"}


def validate_registry(registry_path: Path = REGISTRY_PATH) -> list[str]:
    """Return all registry contract violations without modifying project files."""
    errors: list[str] = []
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"cannot read registry: {error}"]

    if registry.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")
    if registry.get("name") != "omni-agent-skills":
        errors.append("name must be 'omni-agent-skills'")
    if registry.get("version") != read_version():
        errors.append("version does not match VERSION")

    skills = registry.get("skills")
    if not isinstance(skills, list) or not skills:
        return errors + ["skills must be a non-empty array"]

    ids: set[str] = set()
    for index, skill in enumerate(skills, start=1):
        if not isinstance(skill, dict):
            errors.append(f"skill {index} must be an object")
            continue
        missing = REQUIRED_FIELDS - skill.keys()
        if missing:
            errors.append(f"skill {index} missing fields: {', '.join(sorted(missing))}")
            continue
        skill_id = skill["id"]
        if skill_id in ids:
            errors.append(f"duplicate skill id: {skill_id}")
        ids.add(skill_id)
        path = REPO_ROOT / skill["path"]
        if not path.is_file() or path.name != "SKILL.md":
            errors.append(f"skill {skill_id} points to a missing SKILL.md")
            continue
        metadata = parse_skill_metadata(path)
        if metadata["name"] != skill_id:
            errors.append(f"skill {skill_id} does not match frontmatter name")
        if metadata["description"] != skill["summary"]:
            errors.append(f"skill {skill_id} summary does not match frontmatter")
        if path.parent.name != skill_id or path.parent.parent.name != skill["category"]:
            errors.append(f"skill {skill_id} path does not match id/category")
    return errors


def main() -> None:
    errors = validate_registry()
    if errors:
        print("Registry validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)
    print("Registry validation passed.")


if __name__ == "__main__":
    main()
