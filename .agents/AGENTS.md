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
6. Make material changes on a scoped feature branch, never directly on `main`.
7. Follow the contribution and feature delivery SOP before committing a change.
8. Treat `docs/` and root `.md` files as the single source of truth; do not duplicate documentation in `.agents/`.

## Key files & Document Routing

AI agents must actively read and utilize the canonical files in `docs/` and the repository root rather than assuming rules or duplicating documentation:

- [README.md](../README.md): Project overview, installation, and public index catalog.
- [ARCHITECTURE.md](../ARCHITECTURE.md): System design, asset hierarchy, and verification pipeline.
- [CONTRIBUTING.md](../CONTRIBUTING.md): Unified developer on-ramp and contribution standard.
- [SECURITY.md](../SECURITY.md): Security policy and vulnerability disclosure procedures.
- [docs/sops/contribution-and-feature-delivery.md](../docs/sops/contribution-and-feature-delivery.md): Formal 8-step delivery and quality-gate SOP.
- [docs/adr/README.md](../docs/adr/README.md): Architecture Decision Records catalog.
- [docs/foundation/](../docs/foundation/): Charter, scope boundaries, and non-goals.
- [registry.json](../registry.json) & [llms.txt](../llms.txt): Machine-readable registry and LLM context indexes.
- [scripts/build_registry.py](../scripts/build_registry.py): Canonical registry compiler.
- [scripts/manage_adr.py](../scripts/manage_adr.py): ADR and RFC lifecycle tooling.
- [scripts/sanitize.py](../scripts/sanitize.py): Zero-secret and zero-PII pattern scanner.
- [tests/test_repo_integrity.py](../tests/test_repo_integrity.py): Test suite enforcing repo integrity and claim policies.

## Autonomous Agent SDLC Protocol

When an AI agent is tasked with implementing a feature, fix, documentation update, or cleanup, it must execute the delivery pipeline **autonomously end-to-end** without pausing for micro-approvals unless blocked:

1. **Pre-flight Branch Guard (Mandatory):**
   - Check current git branch (`git status` / `git branch --show-current`).
   - If on `main` or `master`, automatically create and switch to a scoped branch (`feat/<name>`, `fix/<name>`, `docs/<name>`, `chore/<name>`) *before* modifying any files.
2. **Context & Document Routing:**
   - Inspect relevant canonical documentation in `docs/` or root files to gather context without hallucinating requirements.
   - If significant architectural changes or schema modifications are introduced, scaffold an ADR (`python3 scripts/manage_adr.py new "<Title>"`).
3. **Implement Minimal Coherent Change:**
   - Apply focused, single-purpose edits. Keep unrelated cleanup out of the branch.
4. **Run Local Verification Suite:**
   - Execute all required local verification checks:
     ```bash
     python3 scripts/sanitize.py
     python3 scripts/build_registry.py
     python3 scripts/validate_registry.py
     python3 scripts/manage_adr.py validate
     python3 -m unittest discover -s tests -p 'test_*.py'
     git diff --check
     ```
5. **Stage & Commit:**
   - Stage affected files and create a conventional commit (`feat:`, `fix:`, `docs:`, `chore:`).
6. **Push & Open Pull Request:**
   - Push branch to origin (`git push -u origin <branch-name>`).
   - Create a Pull Request via GitHub CLI (`gh pr create`) using the structured template with clear scope, verification results, and checklists.
7. **Monitor CI to Completion:**
   - Monitor remote GitHub Actions CI status (`gh pr checks <PR_NUM> --watch`) until checks pass.
   - Report the PR link, CI status, and summary back to the user.

## Architecture decisions (ADRs & RFCs) for AI agents

Before proposing or implementing significant architectural changes, AI agents must adhere to the ADR process:

1. **When to create an ADR**:
   - Modifying registry schema contracts (`registry.schema.json`).
   - Introducing new discovery tiers (e.g. `llms-qa.json`, `llms.txt`).
   - Changing installation helpers (`install.sh`, `install.ps1`) or execution semantics.
   - Adjusting project boundaries, security scanning, documentation layering, or release policies.
2. **When to use an RFC**:
   - Designing public cross-agent communication protocols or multi-tool wire formats.
3. **Agent workflow commands**:
   ```bash
   python3 scripts/manage_adr.py new "Short Decision Title"
   # Fill out context, decision, consequences, and validation in docs/adr/XXXX-title.md
   python3 scripts/manage_adr.py build-index
   python3 scripts/manage_adr.py validate
   ```

## Repository boundary

This repository publishes portable registry assets. It is not the future
engineering control-plane application that may consume those assets. Read
`docs/foundation/scope-and-non-goals.md` before proposing work that involves
agent execution, worktrees, delivery gates, or user interfaces.
