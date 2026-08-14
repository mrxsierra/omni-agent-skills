#!/usr/bin/env python3
"""Auto-generates registry.json and llms.txt from skills/ directory."""
import os
import json
import glob

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")
REGISTRY_PATH = os.path.join(REPO_ROOT, "registry.json")
LLMS_PATH = os.path.join(REPO_ROOT, "llms.txt")

skills_list = []
llms_content = [
    "# omni-agent-skills",
    "",
    "> Universal AI Agent Skill Registry & Workflow Engine for Google Antigravity, Claude Code, Cursor, and OpenCode.",
    "",
    "## Overview",
    "omni-agent-skills is a modular, zero-bloat repository of AI agent skills, security rules, and scaffolds.",
    "",
    "## Machine Indexes",
    "- Registry: https://raw.githubusercontent.com/mrxsierra/omni-agent-skills/main/registry.json",
    "- Tagged Vector Dataset: https://raw.githubusercontent.com/mrxsierra/omni-agent-skills/main/qa_pairs_generic_tagged.json",
    "",
    "## Core Skills",
]

for domain in sorted(os.listdir(SKILLS_DIR)):
    domain_path = os.path.join(SKILLS_DIR, domain)
    if not os.path.isdir(domain_path):
        continue
    
    llms_content.append(f"\n### {domain.replace('-', ' ').title()}")
    
    for skill_name in sorted(os.listdir(domain_path)):
        skill_file = os.path.join(domain_path, skill_name, "SKILL.md")
        if os.path.exists(skill_file):
            rel_path = os.path.relpath(skill_file, REPO_ROOT)
            
            # Extract description from frontmatter
            desc = skill_name
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "description:" in content:
                    for line in content.splitlines():
                        if line.startswith("description:"):
                            desc = line.split("description:", 1)[1].strip()
                            break
            
            skills_list.append({
                "id": skill_name,
                "category": domain,
                "summary": desc,
                "path": rel_path
            })
            
            llms_content.append(f"- {skill_name}: {desc} ({rel_path})")

registry_data = {
    "$schema": "https://json.schemastore.org/json",
    "name": "omni-agent-skills",
    "version": "1.0.0",
    "description": "Universal AI Agent Skill Registry & Security Harness",
    "repository": "https://github.com/mrxsierra/omni-agent-skills",
    "license": "MIT",
    "skills": skills_list
}

with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
    json.dump(registry_data, f, indent=2)

with open(LLMS_PATH, 'w', encoding='utf-8') as f:
    f.write("\n".join(llms_content) + "\n")

print(f"✅ Rebuilt registry.json ({len(skills_list)} skills) and llms.txt successfully!")
