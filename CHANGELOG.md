# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Three-Tier Agent Discovery model (`registry/registry.json`, `llms.txt`, and `llms-qa.json`).
- `llms-qa.json`: Pre-chunked, tagged Q&A semantic retrieval dataset for RAG vector search over this repository.
- Architecture Decision Record (ADR) and RFC management CLI tool (`scripts/manage_adr.py`) with automatic catalog table building and invariant validation.
- Standard ADR and RFC templates under `docs/adr/template.md` and `docs/rfc/template.md`.
- Contributor Covenant Code of Conduct v2.1 (`CODE_OF_CONDUCT.md`).
- Repository support guidelines (`SUPPORT.md`) and code ownership rules (`.github/CODEOWNERS`).
- Structured GitHub YAML issue forms for bugs, feature requests, and skill proposals.
- Contribution SOP-aligned pull request template (`.github/pull_request_template.md`).
- ADR and RFC integrity checks integrated into CI and pre-commit hooks.

### Changed
- Streamlined `README.md` and completely rewrote `ARCHITECTURE.md` to align with ADR 0001.
- Updated `CONTRIBUTING.md` with ADR/RFC procedures and `scripts/validate_registry.py` checks.
- Refactored `tests/test_workflow_runner.py` into a standard `unittest.TestCase` suite.
- Replaced deprecated Python 3.11+ `utcnow()` calls in `scripts/run_workflow.py` with timezone-aware UTC timestamps.

### Removed
- Stale tracking files: `docs/phase_tracking.md`, `plan.md`, `PROGRESS.md`, and `STATUS.md`.
- Legacy sample file `qa_pairs_generic_tagged.json` (superseded by `llms-qa.json`).

## [0.0.1] - 2026-08-16

### Added
- Initial release of `omni-agent-skills` alpha registry.
- 15 specialized skills across Engineering, Web & GEO, Data & AI, and Security & Governance.
- Machine registry compiler `scripts/build_registry.py` producing `registry/registry.json` and `llms.txt`.
- Schema validator `scripts/validate_registry.py` and JSON Schema `registry/registry.schema.json`.
- Secret pattern sanitizer `scripts/sanitize.py`.
- Safe-by-default cross-platform installer helpers (`install.sh` and `install.ps1`).
- Repository smoke test suite (`tests/test_repo_integrity.py`).
- Single source of truth version management (`VERSION` and `scripts/bump.py`).
