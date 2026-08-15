# omni-agent-skills internal guide

This repository is a small, practical AI-native skill registry and repo hygiene project. It is intended to help organize AI workflows and make repo-aware agent usage more structured.

## Current state

- Version: `v0.0.1` alpha
- Includes: skill documents, registry generation, index files, local validation scripts, and installation helpers
- Does not include: independently verified benchmark performance claims or a full benchmark suite with golden answers

## Operating principles

1. Keep each skill narrow and single-purpose.
2. Prefer structured repo metadata over ad hoc prompts.
3. Do not claim performance without reproducible evidence.
4. Treat local checks as hygiene checks, not as proof of product quality.
5. Keep docs and implementation aligned with the actual repo state.

## Key files

- [ARCHITECTURE.md](../ARCHITECTURE.md)
- [README.md](../README.md)
- [llms.txt](../llms.txt)
- [registry.json](../registry.json)
- [SECURITY.md](../SECURITY.md)
- [scripts/build-registry.py](../scripts/build-registry.py)
- [scripts/sanitize.py](../scripts/sanitize.py)
- [tests/test_repo_integrity.py](../tests/test_repo_integrity.py)

## Practical guidance

Use this repo to:

- discover repo-aware skill patterns,
- maintain a lightweight machine-readable catalog,
- validate obvious syntax and secret hygiene issues,
- and promote clearer AI-assisted workflows.

Do not use this repo as evidence of benchmark wins or production readiness unless explicit CI-backed artifacts exist.
