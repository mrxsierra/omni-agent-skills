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

## Other assets and compatibility

Rules, workflows, subagent roles, prompts, hooks, snippets, and MCP templates
remain under their matching `registry/` directories. Until each has a versioned
machine schema, additions must include local metadata or documentation and
state any platform-specific syntax, tool dependency, permission, or execution
assumption. The registry is conceptually tool-neutral; consumers must not infer
support that an asset has not explicitly declared.

`registry/registry.json` and `llms.txt` are generated. Run
`python3 scripts/build_registry.py` after changing a skill.

Validate the checked-in index without changing it with:

```bash
python3 scripts/validate_registry.py
```
