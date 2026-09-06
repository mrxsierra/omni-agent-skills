#!/usr/bin/env python3
"""Update/Bump version across all repo files from a single VERSION file."""
import os
import sys
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.build_registry import build_registry

VERSION_FILE = os.path.join(REPO_ROOT, "VERSION")

def read_version():
    """Read version from VERSION file."""
    with open(VERSION_FILE, "r") as f:
        return f.read().strip()

def update_file(filepath, old_pattern, new_pattern):
    """Update a file with a regex pattern replacement."""
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return False
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if old_pattern not in content:
        print(f"⚠️  Pattern not found in {filepath}: {old_pattern[:50]}")
        return False
    
    updated = content.replace(old_pattern, new_pattern)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(updated)
    
    print(f"✅ Updated {filepath}")
    return True

def main():
    old_version = read_version()
    if len(sys.argv) > 1:
        new_version = sys.argv[1]
        # Write new version to VERSION file
        with open(VERSION_FILE, "w") as f:
            f.write(new_version)
        print(f"📝 Updated VERSION file to {new_version}")
    else:
        new_version = read_version()
    
    print(f"🔄 Updating repo version to {new_version}...\n")
    
    # List of files and their version patterns
    updates = [
        (
            os.path.join(REPO_ROOT, "package.json"),
            f'"version": "{old_version}"',
            f'"version": "{new_version}"'
        ),
        (
            os.path.join(REPO_ROOT, "pyproject.toml"),
            f'version = "{old_version}"',
            f'version = "{new_version}"'
        ),
        (
            os.path.join(REPO_ROOT, "registry", "registry.json"),
            f'"version": "{old_version}"',
            f'"version": "{new_version}"'
        ),
        (
            os.path.join(REPO_ROOT, "install.ps1"),
            f'Write-Host "🚀 Installing omni-agent-skills (v{old_version})',
            f'Write-Host "🚀 Installing omni-agent-skills (v{new_version})'
        ),
    ]
    
    success_count = 0
    for filepath, old_pattern, new_pattern in updates:
        if update_file(filepath, old_pattern, new_pattern):
            success_count += 1
    
    build_registry()
    print(f"\n✨ Version update complete! ({success_count} files updated; registry regenerated)")
    print(f"📌 Current version: {new_version}")

    changelog_path = os.path.join(REPO_ROOT, "CHANGELOG.md")
    if os.path.exists(changelog_path):
        with open(changelog_path, "r", encoding="utf-8") as f:
            if f"## [{new_version}]" not in f.read():
                print(f"⚠️  Remember to document changes under '## [{new_version}]' in CHANGELOG.md!")

    print("\nNext steps:")
    print(f"  git add VERSION package.json pyproject.toml registry/registry.json install.ps1 CHANGELOG.md")
    print(f"  git commit -m 'chore: release v{new_version}'")
    print(f"  git tag v{new_version}")

if __name__ == "__main__":
    main()
