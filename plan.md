Plan and phased work for omni-agent-skills (updated)

Date: 2026-08-16T18:46:33Z

Overview:
This plan captures phases, objectives, and immediate next steps to make the repo truthful, safe to install, and recommendable. Progress is tracked in PROGRESS.md and the session SQL todos table.

Phases:
- Phase 0 (Truth & Safety) [COMPLETED]
  - Truth-first docs rewrite, installer hardening, STATUS/INSTALL added.

- Phase 1 (Product definition) [COMPLETED]
  - Defined MVP flows and product north-star.

- Phase 2 (Workflow engine) [IN PROGRESS]
  - Deliverables:
    - MVP local workflow runner (scripts/run_workflow.py) — implemented (simulation-first)
    - Example runbooks (.agents/workflows/*) — present
    - Unit tests verifying runner writes reproducible logs — added
  - Next tasks:
    1. Wire safe, non-destructive step handlers for:
       - lint, sanitize, dependency-check, manifest-check
    2. Add step-level logging and retry semantics
    3. Add a "dry-run" vs "execute" runtime flag and document security implications in INSTALL.md
    4. Integrate selective execution in CI using OIDC secrets and allow-list of safe steps

- Phase 3 (Release & CI hardening) [PENDING]
  - Deliverables:
    - Release signing (cosign/GPG) in CI
    - Release artifact checksums, reproducible tarballs
    - CI jobs for evidence-backed benchmarks (if adopted)

- Phase 4 (Benchmark evidence pipeline) [OPTIONAL]
  - Containerized reproducible runs, golden-answer storage, scoring, signed artifacts

Immediate next steps taken (now):
- Implemented simulated action handlers in scripts/run_workflow.py (non-destructive by default)
- Updated PROGRESS.md to mark Phase 2 IN PROGRESS
- Created plan.md capturing tasks and next actions
- Added tests that assert workflow logs are produced (existing)

Planned actionable todos (for maintainers / automated agent):
- implement-step-handlers: Implement safe step handlers and unit tests (priority: high)
- ci-signing: Configure cosign or GPG signing in repository actions and store secrets (priority: high, maintainer required)
- pr-draft: Push branch and open draft PR for these changes (priority: medium)
- benchmark-pipeline-design: If benchmarking is desired, design evidence pipeline (priority: low)

How to run locally:
- Simulation run (safe):
  python3 scripts/run_workflow.py --workflow pr-review --outdir /tmp/runs
  (this writes a JSON log describing the intended steps; no destructive actions performed)

- Execute mode (MAINTAINER-ONLY):
  The runner supports execute=True programmatically. Maintain a CI-approved allowlist before enabling execution.

Notes:
- The runner intentionally avoids executing arbitrary shell commands. Any additional execution capability must be gated behind maintainer review and CI secrets.
