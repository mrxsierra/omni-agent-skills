# ADR 0002: Unified Documentation Layering and Autonomous Agent SDLC

## Status

Accepted — 2026-09-06

## Deciders

Sunil Sharma (@mrxsierra)

## Context & Problem Statement

In an AI-native repository, separating documentation into distinct silos for "human developers" versus "AI agents" creates documentation fragmentation, drift, and operational confusion. Furthermore, without an explicit autonomous execution protocol, AI agents may perform partial in-place edits directly on `main` and stop at each micro-step rather than autonomously delivering changes through the full branch, test, PR, and CI lifecycle.

We need a unified documentation architecture that provides a single source of truth for both human and AI contributors, while empowering AI agents to autonomously execute the repository's Standard Operating Procedures (SOPs).

## Decision Drivers

- **Single Source of Truth:** Avoid duplicating contribution standards across `CONTRIBUTING.md`, `docs/sops/`, and `.agents/`.
- **Quality Gate Parity:** Ensure that engineering rigor (branching, linting, secret hygiene, tests, conventional commits, PRs) applies identically whether work is performed by a human engineer or an AI agent.
- **Autonomous Agent Execution:** Instruct AI agents to dynamically consult canonical documentation in `docs/` and repository root files, while enforcing an autonomous delivery loop (branch guard -> implement -> test -> PR -> CI).

## Considered Options

- **Option 1: Fragmented Silos** — Maintain separate, duplicated contribution and workflow rules in `.agents/`, `docs/sops/`, and root `CONTRIBUTING.md`.
- **Option 2: Eliminate SOPs** — Delete `docs/sops/` and store all guidelines solely in root `CONTRIBUTING.md`.
- **Option 3: Unified 3-Tier Layering with Dynamic Document Routing** — Establish complementary roles:
  1. *Gateway:* Root `CONTRIBUTING.md` as the developer entrypoint.
  2. *Formal SOP:* `docs/sops/` as durable governance and auditable quality gates.
  3. *Operational Execution:* `.agents/` as the AI agent system prompt and machine-executable runbooks that dynamically route to canonical `docs/` and execute the SDLC autonomously.

## Decision

Chosen option: **"Option 3: Unified 3-Tier Layering with Dynamic Document Routing"**, because:
- It preserves `docs/sops/` as formal, auditable governance documentation for human engineers and maintainers.
- It keeps root `CONTRIBUTING.md` clean, standard, and linked to the formal SOPs.
- It configures `.agents/AGENTS.md` as an operational trigger that commands AI agents to actively read canonical `docs/` and root `.md` files without duplicating documentation.
- It establishes the **Autonomous Agent SDLC Protocol**, requiring agents to automatically checkout scoped branches before editing files, run all local verification gates, open PRs, and monitor CI to completion.

## Consequences

### Positive Consequences
- Zero documentation duplication or maintenance drift.
- Identical engineering rigor and quality standards across human and AI contributions.
- Eliminates manual micromanagement of AI agents by enforcing autonomous end-to-end delivery.
- Machine-executable workflows in `.agents/workflows/` complement formal human SOPs.

### Negative Consequences / Trade-offs
- AI agents must inspect canonical files on demand using tools.
- *Mitigation:* Explicit routing directives in `.agents/AGENTS.md` and repository map guide agents directly to relevant paths.

## Pros and Cons of Options

### Option 1: Fragmented Silos
- Good: Specific documents tailored narrowly to immediate audiences.
- Bad: High maintenance burden, rapid documentation drift, and conflicting instructions between human and AI workflows.

### Option 2: Eliminate SOPs
- Good: Minimizes file count.
- Bad: Destroys formal engineering governance, reduces clarity for external contributors, and mixes high-level policy with quick developer setup.

### Option 3: Unified 3-Tier Layering with Dynamic Document Routing
- Good: Clean separation of concerns, single source of truth, auditable governance, and fully automated AI agent workflows.
- Bad: Requires clear cross-referencing and adherence to the ADR.

## Validation & Invariants

- Verified by `python3 scripts/manage_adr.py validate` to ensure ADR index parity.
- Tested by `python3 -m unittest discover -s tests -p 'test_*.py'` to verify repository integrity and claims.
- Validated by `.agents/workflows/feature-delivery` execution via `python3 scripts/run_workflow.py`.

## Revisit Conditions

- Revisit if new agent execution environments require alternative file layout schemas that cannot be satisfied by the `.agents/` operational layer.
