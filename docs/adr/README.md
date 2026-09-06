# Architecture Decision Records (ADRs)

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
| `0001` | [Keep the registry separate from the engineering control plane](0001-registry-not-control-plane.md) | `Accepted` | 2026-09-05 | `omni-agent-skills` will remain a portable open-source registry. It publishes |
| `0002` | [Unified Documentation Layering and Autonomous Agent SDLC](0002-unified-documentation-layering-and-autonomous-agent-sdlc.md) | `Accepted` | 2026-09-06 | Chosen option: **"Option 3: Unified 3-Tier Layering with Dynamic Document Routing"**, b... |
<!-- ADR_CATALOG_END -->
