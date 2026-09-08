# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.3] - 2026-09-08

### Added
- **Multi-Tier Model Evaluation Framework (ADR 0004 & ADR 0005):**
  - Evaluation harnesses (`scripts/eval_asset.py`, `scripts/eval_providers.py`, and `scripts/eval_catalog_matrix.py`) for automated delta-utility and context token tax benchmarking.
  - Multi-provider support: `mock` (deterministic harness verification), `ollama` (local open-weights CPU evaluation), `openai`, `openrouter`, and `agy` (zero-API-key local Antigravity CLI access to frontier models like `gemini-3.8-flash-high`).
  - Container manifests for reproducible local neural evaluation: root-level `docker-compose.eval.yml` and `Containerfile.eval` with named volume caching for Ollama models.
  - Automated local evaluation runner (`scripts/run_local_eval.sh`) with auto-detection of Docker / Podman Compose.
  - Full suite of 16 evaluation task definitions under `evals/tasks/*.json` covering all catalog skills and rules.
  - Architecture Decision Record [ADR 0005](docs/adr/0005-multi-tier-model-evaluation-and-open-weights-benchmark.md) defining the three-tier evaluation architecture and zero-hype anti-bloat admission gate.
  - Empirical baseline repository (`evals/baselines/*.json`) recording verified pass rates, delta-utility, and token taxes across all 16 catalog assets.
  - Public quality scorecard generator (`scripts/build_eval_report.py`) compiling `evals/README.md` (100% benchmark pass rate, 32/32 tests passed across `mock` and `agy`).
  - Scheduled and manual GitHub Actions workflow (`.github/workflows/eval-cloud-matrix.yml`) for frontier model evaluation.
  - Open-weights neural model smoke testing workflow (`.github/workflows/ci.yml`) using `qwen2.5-coder:1.5b`.
- **Release Promotion Protocol:**
  - Formal dual-branch promotion lifecycle (`dev` to `main`) in `ARCHITECTURE.md` and `docs/sops/contribution-and-feature-delivery.md`.

### Changed
- Rebuilt `registry/registry.json` and `llms.txt` with version `0.0.3`.
- Hardened `scripts/eval_providers.py` to prevent headless tool-call timeouts during benchmark execution.
- Calibrated brittle keyword checks in `evals/tasks/` to eliminate false negatives against high-capability reasoning models.
- Expanded `tests/test_repo_integrity.py` to assert presence and valid structure of all container and evaluation assets.

## [0.0.2] - 2026-09-06

### Added
- Three-Tier Agent Discovery model (`registry/registry.json`, `llms.txt`, and `llms-qa.json`).
- `llms-qa.json`: Pre-chunked, tagged Q&A semantic retrieval dataset for RAG vector search over this repository.
- Architecture Decision Record (ADR) and RFC management CLI tool (`scripts/manage_adr.py`) with automatic catalog table building and invariant validation.
- Standard ADR and RFC templates under `docs/adr/template.md` and `docs/rfc/template.md`.
- Architecture Decision Record [ADR 0002](docs/adr/0002-unified-documentation-layering-and-autonomous-agent-sdlc.md) defining canonical documentation layering and autonomous agent SDLC protocols.
- Autonomous agent SDLC protocol and workflow runner instructions in `.agents/AGENTS.md` and `.agents/workflows/feature-delivery`.
- Contributor Covenant Code of Conduct v2.1 (`CODE_OF_CONDUCT.md`).
- Repository support guidelines (`SUPPORT.md`) and code ownership rules (`.github/CODEOWNERS`).
- Structured GitHub YAML issue forms for bugs, feature requests, and skill proposals.
- Contribution SOP-aligned pull request template (`.github/pull_request_template.md`).
- Modernized GitHub Actions release workflow (`.github/workflows/release.yml`) with automated tag-vs-`VERSION` parity gating and release drafter config (`.github/release.yml`).
- ADR and RFC integrity checks integrated into CI and pre-commit hooks.

### Changed
- Standardized all 15 skills in the skill catalog (`registry/skills/`) into the canonical 4-section contract (Inputs, Procedure, Outputs, Constraints) with truthful scope, tool neutrality, and zero unverified benchmark claims.
- Hardened global security rule (`registry/rules/global/security_shield.md`) to focus strictly on staging-first, zero-secret, and non-destructive software engineering protocols.
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
