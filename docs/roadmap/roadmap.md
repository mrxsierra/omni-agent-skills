# Roadmap: Path to v0.1.0 Production Release

This roadmap defines the evolution of `omni-agent-skills` from an initial alpha skill registry into a comprehensive, production-grade library of engineering workflows, skills, and governance assets.

## The End-to-End Lifecycle Framework

To enable developers and AI coding agents to take a project from concept to production with engineering discipline, the registry assets align across 7 operational phases:

1. **Phase 1: Inception & PRD:** Product requirements definition, scope boundaries, and competitive moat analysis.
2. **Phase 2: Architecture & Decision Records:** System specifications, ADR drafting, and interface contracts (MCP/OpenAPI).
3. **Phase 3: Greenfield Scaffolding:** Repository layout, toolchain configuration, linters, pre-commit hooks, and community files.
4. **Phase 4: Atomic Implementation:** Incremental code modification, test-driven development (TDD), and callsite propagation.
5. **Phase 5: Multi-Tier Verification:** Unit tests, integration assertions, diff audits, and zero-secret scanning.
6. **Phase 6: Containerization & CI/CD:** Reproducible Docker packaging, CI matrix automation, and deployment pipelines.
7. **Phase 7: Shipping & Operations:** Semantic versioning, changelog compilation, automated release drafting, and healthchecks.

---

## Completed Milestones

### Milestone 1: Repository Operating Foundation (v0.0.1)
Create the charter, scope boundaries, governance, ADR practice (`scripts/manage_adr.py`), contribution SOP (`docs/sops/contribution-and-feature-delivery.md`), and project roadmap.

### Milestone 2: Registry Contract & Three-Tier Discovery (v0.0.1)
Define the published asset model: required metadata, validation rules, and schema enforcement (`registry.schema.json`). Establish the Three-Tier Agent Discovery architecture:
- Tier 1: Executable registry catalog in `registry/registry.json`.
- Tier 2: LLM text sitemap in `llms.txt`.
- Tier 3: Pre-chunked, tagged Q&A semantic retrieval in `llms-qa.json`.
Eliminate stale planning artifacts and unify documentation layering under ADR 0002.

### Milestone 3: Reliable Tooling, Community Health & Release Automation (v0.0.1)
Harden registry generation (`scripts/build_registry.py`) and schema validation (`scripts/validate_registry.py`). Achieve 100% GitHub Community Health score (`CODE_OF_CONDUCT.md`, `SUPPORT.md`, `.github/CODEOWNERS`, issue forms, and PR template). Implement release engineering automation with tag-vs-`VERSION` parity validation and automated release notes.

### Milestone 4: Curated Catalog Quality (v0.0.2)
Standardize all 15 skills in `registry/skills/` into the canonical 4-section runbook contract (Inputs, Procedure, Expected Outputs, Constraints). Eliminate unverified benchmark marketing claims and ensure tool neutrality across all assets.

---

## Upcoming Milestones

### Milestone 5: Shipped Workflows & Lifecycle Orchestration
Promote multi-step workflows from internal dogfooding to first-class published registry assets:
- **`registry/workflows/` Directory:** Formalize workflow definitions alongside skills.
- **Registry Schema & Compiler Update:** Update `registry.schema.json` and `scripts/build_registry.py` to index workflows in `registry.json` and `llms.txt`.
- **Core Lifecycle Workflows:**
  - `workflow-project-initiation`: Guides problem definition, PRD formulation, and initial task breakdown.
  - `workflow-repo-scaffolding`: Establishes repo structure, linters, pre-commit hooks, and CI gates.
  - `workflow-feature-delivery`: Enforces branch isolation, atomic code changes, verification suites, and PR submission.
  - `workflow-container-deploy`: Orchestrates Docker containerization, CI pipelines, and healthcheck verification.

### Milestone 6: Greenfield Scaffolding & Deployment Skills
Close the functional gaps in the catalog to support full idea-to-deployment lifecycles:
- **Greenfield Scaffolding:** Add `project-scaffold-architect` to bootstrap project layouts, build manifests, and dev environments.
- **Packaging & Deployment:** Add `docker-container-builder` (minimal, multi-stage, rootless containers) and `cicd-pipeline-generator` (GitHub Actions CI/CD templates).
- **Executable Helper Scripts:** Bundle deterministic Python and shell verification utilities inside top skills to eliminate agent speculation.

### Milestone 7: Distribution, Installation UX & Consumer Verification
- **Enhanced Installation Experience:** Expand `install.sh` and `install.ps1` with selective asset installation (`--skill <name>`, `--workflow <name>`).
- **Consumer Dogfood Verification:** Validate that an agent can consume the released registry to build, test, and containerize a new standalone application from scratch.

### Milestone 8: Production Release v0.1.0
- Execute complete regression and integrity verification across all published skills, workflows, and rules.
- Publish official `v0.1.0` release tag and distribution archives.

---

## Boundary with the Future Control Plane

A future engineering control plane may implement task contracts, worktrees, agent adapters, evidence collection, approval gates, and a developer-facing UI. It will consume registry releases rather than expanding this repository beyond its charter as a portable knowledge and capability catalog.
