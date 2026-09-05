# Contributing to omni-agent-skills

Thank you for considering contributions to this project. This guide explains how to maintain version consistency, run tests, and prepare changes.

## Version Management

The repo uses a single `VERSION` file as the source of truth for all version numbers across configuration files.

### Current Version
Check the current version:
```bash
cat VERSION
```

### Bumping the Version
When you need to update the version (e.g., from `0.0.1` to `0.1.0`):

1. Run the update script with the new version:
```bash
python3 scripts/bump.py 0.1.0
```

2. Verify changes:
```bash
git diff
```

3. Stage and commit:
```bash
git add VERSION package.json pyproject.toml registry/registry.json
git commit -m "chore: bump version to 0.1.0"
```

The script updates:
- `VERSION` — source of truth
- `package.json` — npm metadata
- `pyproject.toml` — Python package metadata
- `registry/registry.json` — registry metadata

## Running Tests

Before committing, run the repo's validation suite:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

Or use the npm script:
```bash
npm run test
```

## Code Quality

Run the sanitizer and registry rebuild:

```bash
python3 scripts/sanitize.py
python3 scripts/build_registry.py
```

Or in batch:
```bash
npm run sanitize
npm run build
npm run test
```

## Pre-commit Checks

The repo has a `.githooks/pre-commit` hook configured to run automatically before each commit. This runs:
- Sanitizer (secret pattern checks)
- Registry rebuild
- Smoke tests

To ensure these run, configure your Git hooks:
```bash
git config core.hooksPath .githooks
```

## Submitting Changes

1. Keep changes small and focused (one feature or fix per commit).
2. Follow the existing code style and directory structure.
3. Do not claim performance or benchmark wins without reproducible CI-backed evidence.
4. Update documentation if you add or modify skills.
5. Run tests and verify no regressions.
6. Write clear commit messages following the repo's existing convention.

## Skills and Rules

When adding a new skill:
1. Create a folder under `registry/skills/<category>/<skill-name>/`
2. Add a `SKILL.md` file with frontmatter (name, description)
3. Run `python3 scripts/build_registry.py` to auto-generate `registry/registry.json` and `llms.txt`
4. Test with `npm run test` to verify registry consistency
5. Commit with a clear message

Example:
```bash
mkdir -p registry/skills/engineering/my-new-skill
cat > registry/skills/engineering/my-new-skill/SKILL.md << 'EOF'
name: my-new-skill
description: A brief description of what this skill does.

# My New Skill
...
EOF

python3 scripts/build_registry.py
npm run test
```

## Security and Secrets

Do not commit:
- API keys or tokens
- Private credentials
- Passwords or `.env` files with secrets
- Personally identifiable information (PII)

The sanitizer will warn about common patterns, but it is not a guarantee. Always review diffs before pushing.

## Questions?

If you have questions or need clarification, open an issue or contact the maintainers.

Thank you for contributing!
