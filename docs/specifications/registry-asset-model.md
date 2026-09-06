# Registry asset model

`registry/registry.json` is generated from skills and its version must match
the root `VERSION` file. Each index entry contains a stable `id`, `category`,
truthful `summary`, and repository-relative `path`.

## Skill contract

Skills live at `registry/skills/<category>/<skill-id>/SKILL.md` and begin with:

```yaml
---
name: <skill-id>
description: <concise, truthful description>
---
```

The frontmatter name must match the directory name. Content defines a reusable
capability, its constraints, and expected outputs; it must not promise results
that cannot be verified.

## Published Asset Types and 3D Coordinate System

Per [ADR 0003](../adr/0003-registry-asset-taxonomy-shipped-capabilities-and-inclusion-criteria.md) and [ARCHITECTURE.md](../../ARCHITECTURE.md), the registry formally publishes **eight concrete asset types** organized across two functional tiers:
1. **Tier 1 (Core Orchestration & Reasoning Primitives):** `skills/`, `workflows/`, `rules/`, and `subagents/`.
2. **Tier 2 (Deterministic Integration & Context Primitives):** `hooks/`, `mcp-configs/`, `snippets/`, and `prompts/`.

All assets navigate along a **3-Dimensional Coordinate System**:
- **Dimension 1 (SDLC Phase):** Temporal placement across the 7-Phase SDLC (`Phase 1: Inception` to `Phase 7: Shipping & Operations`).
- **Dimension 2 (Domain & Stack Archetype):** Universal Foundation (cross-cutting) vs Domain-Specific (Web, Backend, Data/AI).
- **Dimension 3 (Relational Composition):** Complementary asset combinations forming curated Archetype Stacks.

Until each non-skill asset has a versioned machine schema, additions must include local metadata or documentation and state any platform-specific syntax, tool dependency, permission, or execution assumption. The registry is conceptually tool-neutral; consumers must not infer support that an asset has not explicitly declared.

`registry/registry.json` and `llms.txt` are generated. Run
`python3 scripts/build_registry.py` after changing a skill.

Validate the checked-in index without changing it with:

```bash
python3 scripts/validate_registry.py
```
