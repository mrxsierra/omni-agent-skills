#!/usr/bin/env python3
"""Sanitizer script: Verifies zero secrets, zero API keys, and zero private credentials exist in public files."""
import os
import re
import sys
import json

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Abstract, generic security patterns (Zero personal PII/project names hardcoded)
GENERIC_SECURITY_PATTERNS = [
    re.compile(r'sk-[a-zA-Z0-9]{20,}'),           # Generic API key format
    re.compile(r'ghp_[a-zA-Z0-9]{30,}'),          # Generic GitHub token format
    re.compile(r'AIzaSy[a-zA-Z0-9_-]{33}'),        # Generic Google API key format
    re.compile(r'-----BEGIN PRIVATE KEY-----'),  # Private SSH key header
    re.compile(r'-----BEGIN RSA PRIVATE KEY-----'),
]

# Load optional uncommitted local private patterns from .gitignore-d file
LOCAL_PATTERNS_FILE = os.path.join(REPO_ROOT, ".sanitize-local.json")
local_patterns = []

if os.path.exists(LOCAL_PATTERNS_FILE):
    try:
        with open(LOCAL_PATTERNS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for pat_str in data.get("forbidden_patterns", []):
                local_patterns.append(re.compile(pat_str))
    except Exception as e:
        print(f"⚠️ Warning: Could not parse local sanitizer config: {e}")

ALL_PATTERNS = GENERIC_SECURITY_PATTERNS + local_patterns
violations = []

for root, _, files in os.walk(REPO_ROOT):
    if ".git" in root or "node_modules" in root or ".venv" in root:
        continue
    for file in files:
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, REPO_ROOT)
        
        # Skip binary files, lockfiles, or the sanitizer script itself
        if rel_path.endswith(('.png', '.jpg', '.ico', '.lock', '.zip')) or rel_path == "scripts/sanitize.py":
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                for pattern in ALL_PATTERNS:
                    if pattern.search(content):
                        violations.append((rel_path, pattern.pattern))
        except Exception:
            pass

if violations:
    print("❌ SECURITY SANITIZER VIOLATIONS FOUND:")
    for filepath, pat in violations:
        print(f"  - {filepath}: Matched forbidden pattern '{pat}'")
    sys.exit(1)
else:
    print("✅ Zero-PII & Zero-Secret Sanitizer Check Passed!")
    sys.exit(0)
