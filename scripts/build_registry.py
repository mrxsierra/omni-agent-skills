#!/usr/bin/env python3
"""Build registry.json and llms.txt from skill metadata."""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "registry" / "skills"
REGISTRY_PATH = REPO_ROOT / "registry" / "registry.json"
LLMS_PATH = REPO_ROOT / "llms.txt"
VERSION_PATH = REPO_ROOT / "VERSION"


def read_version() -> str:
    return VERSION_PATH.read_text(encoding="utf-8").strip()


def parse_skill_metadata(skill_file: Path) -> dict[str, str]:
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{skill_file}: missing opening frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError(f"{skill_file}: missing closing frontmatter delimiter") from error
    metadata = {}
    for line in lines[1:end]:
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"')
    missing = [key for key in ("name", "description") if not metadata.get(key)]
    if missing:
        raise ValueError(f"{skill_file}: missing metadata: {', '.join(missing)}")
    return metadata


def build_registry() -> dict[str, object]:
    skills = []
    llms = ["# omni-agent-skills", "", "> A tool-neutral registry of focused skills, rules, and workflow assets for AI-assisted engineering.", "", "## Skills"]
    for domain_path in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        category = domain_path.name
        llms.append(f"\n### {category.replace('-', ' ').title()}")
        for skill_path in sorted(path for path in domain_path.iterdir() if path.is_dir()):
            skill_file = skill_path / "SKILL.md"
            if not skill_file.exists():
                continue
            metadata = parse_skill_metadata(skill_file)
            if metadata["name"] != skill_path.name:
                raise ValueError(f"{skill_file}: name must match directory name")
            relative_path = skill_file.relative_to(REPO_ROOT).as_posix()
            skills.append({"id": metadata["name"], "category": category, "summary": metadata["description"], "path": relative_path})
            llms.append(f"- {metadata['name']}: {metadata['description']} ({relative_path})")
    registry = {"schema_version": "1.0", "name": "omni-agent-skills", "version": read_version(), "description": "Tool-neutral registry of AI-assisted engineering skills and governance assets", "repository": "https://github.com/mrxsierra/omni-agent-skills", "license": "MIT", "skills": skills}
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    LLMS_PATH.write_text("\n".join(llms) + "\n", encoding="utf-8")
    return registry


def main() -> None:
    registry = build_registry()
    print(f"Rebuilt registry.json ({len(registry['skills'])} skills) and llms.txt.")


if __name__ == "__main__":
    main()
