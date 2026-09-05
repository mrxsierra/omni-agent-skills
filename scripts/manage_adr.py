#!/usr/bin/env python3
"""Architecture Decision Record (ADR) and RFC management tool for omni-agent-skills.

Usage:
  python3 scripts/manage_adr.py new <title>
  python3 scripts/manage_adr.py new <title> --rfc
  python3 scripts/manage_adr.py build-index
  python3 scripts/manage_adr.py validate
"""

import argparse
import datetime
import os
import re
import sys
from typing import Dict, List, Optional, Tuple

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADR_DIR = os.path.join(REPO_ROOT, "docs", "adr")
RFC_DIR = os.path.join(REPO_ROOT, "docs", "rfc")

VALID_ADR_STATUSES = {"proposed", "accepted", "superseded", "deprecated", "rejected"}
VALID_RFC_STATUSES = {"draft", "under review", "approved", "implemented", "deferred", "withdrawn", "rejected"}

ADR_FILENAME_RE = re.compile(r"^(\d{4})-([a-z0-9-]+)\.md$")


def slugify(text: str) -> str:
    """Convert arbitrary title text to a clean URL/filename-safe kebab-case slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


def get_next_id(directory: str) -> Tuple[int, str]:
    """Find the next 4-digit sequential ID in the given directory."""
    os.makedirs(directory, exist_ok=True)
    existing_ids = []
    for filename in os.listdir(directory):
        match = ADR_FILENAME_RE.match(filename)
        if match:
            existing_ids.append(int(match.group(1)))
    next_num = max(existing_ids, default=0) + 1
    return next_num, f"{next_num:04d}"


def scaffold_doc(title: str, is_rfc: bool = False, deciders: str = "Sunil Sharma (@mrxsierra)") -> str:
    """Scaffold a new ADR or RFC markdown document with pre-populated metadata."""
    target_dir = RFC_DIR if is_rfc else ADR_DIR
    doc_type = "RFC" if is_rfc else "ADR"
    num, num_str = get_next_id(target_dir)
    slug = slugify(title)
    filename = f"{num_str}-{slug}.md"
    file_path = os.path.join(target_dir, filename)

    date_str = datetime.date.today().isoformat()
    template_path = os.path.join(target_dir, "template.md")

    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("{NUMBER}", num_str)
        content = content.replace("{TITLE}", title)
        content = content.replace("{RFC_TITLE}", title)
        content = content.replace("{YYYY-MM-DD}", date_str)
        content = content.replace("{LIST_OF_DECIDERS}", deciders)
        content = content.replace("{NAME / GITHUB_HANDLE}", deciders)
    else:
        if is_rfc:
            content = f"""# RFC {num_str}: {title}

* **Status**: Draft
* **Author(s)**: {deciders}
* **Created**: {date_str}
* **Target Version**: v0.1.0
* **Discussion Issue/PR**: 

---

## 1. Summary & Motivation

Provide a concise explanation of the proposal. What problem does it solve, and why should this change be incorporated?

---

## 2. Goals & Non-Goals

### Goals
- Goal 1

### Non-Goals
- Non-goal 1

---

## 3. Detailed Specification & Design

### A. Technical Specification
Describe schemas, data structures, and protocol specifications.

### B. Downstream Impact
Impact on existing clients, performance, and tooling.

---

## 4. Backward Compatibility & Migration Plan

Is this a breaking change? Provide migration guidance.

---

## 5. Alternatives Considered

- Alternative 1: Why it was rejected.

---

## 6. Unresolved Questions & Open Discussions

1. Open question 1
"""
        else:
            content = f"""# ADR {num_str}: {title}

## Status

Proposed — {date_str}

## Deciders

{deciders}

## Context

Describe the context and problem that requires an architectural decision. What is the scope, and why does it matter?

## Decision Drivers

- Driver 1 (e.g. Zero external runtime dependencies)
- Driver 2 (e.g. Tool neutrality across agent platforms)

## Considered Options

- Option 1: Title of Option 1
- Option 2: Title of Option 2

## Decision

Describe the selected architectural option and the specific rationale for choosing it.

## Consequences

### Positive Consequences
- Positive consequence 1

### Negative Consequences / Trade-offs
- Trade-off 1 and mitigation strategy

## Validation & Invariants

- How this decision is verified and tested in the repository.

## Revisit Conditions

- Conditions under which this decision should be reconsidered.
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created {doc_type} {num_str}: {os.path.relpath(file_path, REPO_ROOT)}")
    return file_path


def parse_doc(file_path: str) -> Dict[str, str]:
    """Parse metadata and key sections from an ADR or RFC file."""
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    lines = raw_text.splitlines()
    filename = os.path.basename(file_path)
    match = ADR_FILENAME_RE.match(filename)
    doc_id = match.group(1) if match else "0000"

    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            # Strip "ADR XXXX: " or "RFC XXXX: " prefix if present
            title = re.sub(r"^(ADR|RFC)\s+\d{4}:\s*", "", title, flags=re.IGNORECASE)
            break

    status = "Proposed"
    date_str = ""

    # Check for markdown bullet format: * **Status**: Accepted
    status_bullet_match = re.search(r"\*\s*\*\*Status\*\*:\s*([^\n\r]+)", raw_text, re.IGNORECASE)
    if status_bullet_match:
        status_raw = status_bullet_match.group(1).strip()
        status_tokens = status_raw.split("|")[0].split("—")[0].split("-")[0].strip()
        status = status_tokens.strip()

    # Check for markdown header format: ## Status \n\n Accepted — YYYY-MM-DD
    status_section_match = re.search(r"##\s+Status\s*\n+([^\n\r#]+)", raw_text, re.IGNORECASE)
    if status_section_match:
        status_line = status_section_match.group(1).strip()
        if "—" in status_line:
            parts = status_line.split("—", 1)
            status = parts[0].strip()
            date_str = parts[1].strip()
        elif "-" in status_line and len(status_line.split("-")) == 4:
            # e.g., "Accepted - 2026-09-05"
            parts = status_line.split("-", 1)
            status = parts[0].strip()
            date_str = parts[1].strip()
        else:
            status = status_line.split()[0].strip()

    # Extract date if present in bullet
    date_bullet_match = re.search(r"\*\s*\*\*Date\*\*:\s*([0-9-]+)", raw_text, re.IGNORECASE)
    if date_bullet_match:
        date_str = date_bullet_match.group(1).strip()

    # Extract short summary / decision snippet
    decision_summary = ""
    decision_match = re.search(r"##\s+Decision\s*\n+([^\n\r#]+)", raw_text, re.IGNORECASE)
    if decision_match:
        decision_summary = decision_match.group(1).strip()
    elif is_rfc_summary := re.search(r"##\s+1\.\s+Summary[^\n\r]*\n+([^\n\r#]+)", raw_text, re.IGNORECASE):
        decision_summary = is_rfc_summary.group(1).strip()

    if len(decision_summary) > 90:
        decision_summary = decision_summary[:87] + "..."

    return {
        "id": doc_id,
        "filename": filename,
        "title": title or filename,
        "status": status,
        "date": date_str,
        "summary": decision_summary,
        "path": file_path,
    }


def get_all_docs(directory: str) -> List[Dict[str, str]]:
    """Retrieve and parse all ADR/RFC files sorted by sequential ID."""
    if not os.path.exists(directory):
        return []
    docs = []
    for filename in sorted(os.listdir(directory)):
        if filename in ("README.md", "template.md"):
            continue
        if ADR_FILENAME_RE.match(filename):
            doc = parse_doc(os.path.join(directory, filename))
            docs.append(doc)
    return sorted(docs, key=lambda d: int(d["id"]))


def build_adr_index() -> None:
    """Regenerate docs/adr/README.md with an automated catalog table."""
    docs = get_all_docs(ADR_DIR)
    readme_path = os.path.join(ADR_DIR, "README.md")

    table_rows = []
    for doc in docs:
        link = f"[{doc['title']}]({doc['filename']})"
        table_rows.append(f"| `{doc['id']}` | {link} | `{doc['status']}` | {doc['date']} | {doc['summary']} |")

    table_content = "\n".join(table_rows) if table_rows else "| *None* | *No records recorded yet* | - | - | - |"

    content = f"""# Architecture Decision Records (ADRs)

Architecture Decision Records (ADRs) capture significant, durable architectural choices, their context, rationale, and consequences. They prevent architectural drift and eliminate the need to reconstruct historical trade-offs from chat transcripts or git logs.

---

## 1. When, Where, How, and Why

### Why Create an ADR?
- **Preserve Durable Context**: Prevent recurring debates about previously evaluated trade-offs.
- **Enforce Invariants**: Explicitly state system constraints that tests and code reviews must uphold.
- **Traceability for Agents & Developers**: Provide a single, authoritative reference for past architectural decisions.

### When to Create an ADR?
Create an ADR for decisions involving:
1. Changes to registry schemas (`registry.schema.json`) or metadata requirements.
2. Introduction or modification of agent discovery tiers (e.g. `llms-qa.json`, `llms.txt`).
3. Changes to installation behavior, POSIX/Windows scripts, or security boundaries.
4. Scope boundaries (e.g. keeping execution runtime separate from the registry).
5. Tooling additions or breaking CI/release policy changes.

*Do NOT create an ADR for*: routine bug fixes, typos, doc updates, or adding standard skills that follow existing schemas.

### Where are ADRs Stored?
- Directory: [`docs/adr/`](.)
- Naming format: `XXXX-kebab-case-title.md` (e.g., `0001-registry-not-control-plane.md`).
- Template: [`docs/adr/template.md`](template.md).

### How to Create & Manage ADRs?
- **Scaffold a new ADR**: `python3 scripts/manage_adr.py new "Short Decision Title"`
- **Regenerate this index table**: `python3 scripts/manage_adr.py build-index`
- **Validate integrity and status**: `python3 scripts/manage_adr.py validate`

---

## 2. ADR Lifecycle States

```text
  [Proposed] ──► [Accepted] ──► [Superseded by ADR-XXXX]
      │               │
      ▼               ▼
  [Rejected]     [Deprecated]
```

- **`Proposed`**: Under review by maintainers and contributors.
- **`Accepted`**: Approved and actively enforced in the repository.
- **`Superseded`**: Replaced by a newer ADR (must link to the superseding record).
- **`Deprecated`**: Phased out or no longer applicable.
- **`Rejected`**: Evaluated but declined due to unfavorable trade-offs.

---

## 3. Published Decision Catalog

<!-- ADR_CATALOG_START -->
| ID | Title | Status | Date | Summary / Core Decision |
| :--- | :--- | :--- | :--- | :--- |
{table_content}
<!-- ADR_CATALOG_END -->
"""

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated ADR index: {os.path.relpath(readme_path, REPO_ROOT)} ({len(docs)} ADRs cataloged)")


def validate_adrs() -> List[str]:
    """Validate naming conventions, sequential ordering, required sections, and index parity."""
    errors = []
    if not os.path.exists(ADR_DIR):
        return ["ADR directory docs/adr/ does not exist."]

    files = sorted(os.listdir(ADR_DIR))
    adr_files = [f for f in files if f not in ("README.md", "template.md")]

    expected_id = 1
    for filename in adr_files:
        match = ADR_FILENAME_RE.match(filename)
        if not match:
            errors.append(f"ADR filename '{filename}' violates convention '^\\d{{4}}-[a-z0-9-]+\\.md$'.")
            continue

        file_id = int(match.group(1))
        if file_id != expected_id:
            errors.append(f"ADR sequence gap: expected ID {expected_id:04d}, but found '{filename}' ({file_id:04d}).")
        expected_id = file_id + 1

        # Check file content and required sections
        file_path = os.path.join(ADR_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        doc = parse_doc(file_path)
        status_clean = doc["status"].lower().strip()
        if status_clean not in VALID_ADR_STATUSES:
            errors.append(f"ADR '{filename}' has invalid status '{doc['status']}'. Must be one of {sorted(VALID_ADR_STATUSES)}.")

        # Required sections: Context, Decision, Consequences
        for req_section in ["context", "decision", "consequences"]:
            if not re.search(rf"##\s+.*{req_section}", content, re.IGNORECASE):
                errors.append(f"ADR '{filename}' is missing required section '## {req_section.capitalize()}'.")

    # Check that template.md exists
    template_path = os.path.join(ADR_DIR, "template.md")
    if not os.path.exists(template_path):
        errors.append("docs/adr/template.md is missing.")

    # Check index table parity
    readme_path = os.path.join(ADR_DIR, "README.md")
    if not os.path.exists(readme_path):
        errors.append("docs/adr/README.md is missing.")
    else:
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_text = f.read()
        for filename in adr_files:
            match = ADR_FILENAME_RE.match(filename)
            if match:
                doc_id = match.group(1)
                if f"`{doc_id}`" not in readme_text:
                    errors.append(f"docs/adr/README.md does not index ADR {doc_id} ('{filename}'). Run 'python3 scripts/manage_adr.py build-index'.")

    return errors


def validate_adr_catalog() -> List[str]:
    """Alias for validate_adrs to validate ADR catalog."""
    return validate_adrs()


def validate_rfc_catalog() -> List[str]:
    """Validate RFC directory, templates, naming conventions, and required sections."""
    errors = []
    if not os.path.exists(RFC_DIR):
        return ["RFC directory docs/rfc/ does not exist."]

    # Check that template.md and README.md exist
    for req_file in ["template.md", "README.md"]:
        if not os.path.exists(os.path.join(RFC_DIR, req_file)):
            errors.append(f"docs/rfc/{req_file} is missing.")

    files = sorted(os.listdir(RFC_DIR))
    rfc_files = [f for f in files if f not in ("README.md", "template.md")]

    expected_id = 1
    for filename in rfc_files:
        match = ADR_FILENAME_RE.match(filename)
        if not match:
            errors.append(f"RFC filename '{filename}' violates convention '^\\d{{4}}-[a-z0-9-]+\\.md$'.")
            continue

        file_id = int(match.group(1))
        if file_id != expected_id:
            errors.append(f"RFC sequence gap: expected ID {expected_id:04d}, but found '{filename}' ({file_id:04d}).")
        expected_id = file_id + 1

        file_path = os.path.join(RFC_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        doc = parse_doc(file_path)
        status_clean = doc["status"].lower().strip()
        if status_clean not in VALID_RFC_STATUSES:
            errors.append(f"RFC '{filename}' has invalid status '{doc['status']}'. Must be one of {sorted(VALID_RFC_STATUSES)}.")

        for req_section in ["summary", "goals", "specification", "compatibility"]:
            if not re.search(rf"##\s+.*{req_section}", content, re.IGNORECASE):
                errors.append(f"RFC '{filename}' is missing required section related to '{req_section}'.")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Manage Architecture Decision Records (ADRs) and RFCs.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: new
    new_parser = subparsers.add_parser("new", help="Scaffold a new ADR or RFC document.")
    new_parser.add_argument("title", help="Title of the architectural decision or RFC proposal.")
    new_parser.add_argument("--rfc", action="store_true", help="Scaffold an RFC instead of an ADR.")
    new_parser.add_argument("--deciders", default="Sunil Sharma (@mrxsierra)", help="Author(s) or deciders.")

    # Subcommand: build-index
    subparsers.add_parser("build-index", help="Regenerate the ADR README catalog table.")

    # Subcommand: validate
    subparsers.add_parser("validate", help="Validate ADR and RFC integrity, naming, sections, and index parity.")

    args = parser.parse_args()

    if args.command == "new":
        scaffold_doc(args.title, is_rfc=args.rfc, deciders=args.deciders)
        if not args.rfc:
            build_adr_index()
    elif args.command == "build-index":
        build_adr_index()
    elif args.command == "validate":
        adr_errors = validate_adr_catalog()
        rfc_errors = validate_rfc_catalog()
        all_errors = adr_errors + rfc_errors
        if all_errors:
            print(f"❌ Validation failed with {len(all_errors)} error(s):", file=sys.stderr)
            for err in all_errors:
                print(f"  - {err}", file=sys.stderr)
            sys.exit(1)
        else:
            print("✅ All Architecture Decision Records (ADRs) and RFC structures passed validation.")


if __name__ == "__main__":
    main()
