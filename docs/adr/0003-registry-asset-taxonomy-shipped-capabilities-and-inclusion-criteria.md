# ADR 0003: Registry Asset Taxonomy Shipped Capabilities and Inclusion Criteria

## Status

Accepted — 2026-09-06

## Deciders

Sunil Sharma (@mrxsierra)

## Context & Problem Statement

The guiding philosophy of `omni-agent-skills` is that **we do not trust AI vibes; we trust engineering principles, deterministic verification gates, and structured Standard Operating Procedures (SOPs) to build deployable, shippable software**.

Prior to this decision, the repository maintained an initial catalog of 15 atomic skills and 1 security rule, but lacked a formal architectural taxonomy governing:
1. **What asset classes the registry ships** (e.g., atomic skills vs. composite workflows vs. behavioral rules vs. executable helper scripts).
2. **Why each asset class exists** and how they compose together to support the full **7-Phase Software Development Lifecycle (SDLC)**—enabling a developer or autonomous agent to take a project from a raw idea to architectural planning, greenfield scaffolding, atomic code changes, multi-tier testing, containerization, and production release.
3. **What concrete inclusion criteria and quality gates** determine whether a proposed capability or skill is admitted into the published registry versus rejected as out-of-scope, bloated, or vendor-locked.

Without an explicit taxonomy and admission rubric, the registry risks devolving into an unstructured "prompt junkyard" filled with overlapping, unvalidated, or platform-specific prompt snippets that fail to enforce engineering rigor.

## Decision Drivers

- **End-to-End SDLC Lifecycle Support:** The registry must provide capabilities spanning the complete journey of software creation (Inception $\rightarrow$ Architecture $\rightarrow$ Scaffolding $\rightarrow$ Implementation $\rightarrow$ Verification $\rightarrow$ Containerization $\rightarrow$ Shipping), rather than just isolated point fixes.
- **Deterministic Verification over AI Speculation:** Every published asset must define objective, verifiable success criteria, evidence artifacts, and reproducible validation commands.
- **Tool & Agent Neutrality:** Assets must remain vendor-independent and portable across diverse AI coding environments (Claude Code, Cursor, Copilot, Antigravity, Gemini CLI, Aider, Codex) as well as traditional human engineering toolchains.
- **Single-Purpose Orthogonality & Zero Bloat:** Each asset must serve a distinct, narrow purpose without kitchen-sink bloat or feature overlap.
- **Strict Machine-Readable Governance:** Every published asset must be cataloged in `registry.json`, indexed in `llms.txt`, validated against `registry.schema.json`, and pass automated PII/secret scanners in CI.

## Considered Options

- **Option 1: Unstructured Skill Collection (Ad-hoc Catalog)**
  Publish loose Markdown runbooks without formal asset classification, workflow orchestrations, or standardized quality gates. Rely on end users to manually compose prompt chains.
- **Option 2: Monolithic Agent Runtime & Control Plane**
  Expand the repository to include an execution daemon, state engine, dynamic worktree orchestrator, and web UI to execute agent tasks. (*Evaluated and rejected in ADR 0001*).
- **Option 3: Four-Class Asset Taxonomy with 7-Phase SDLC Lifecycle Mapping and 5-Gate Inclusion Filter**
  Formally define four distinct published asset classes (`skills`, `workflows`, `rules`, `helpers`), map them systematically across the 7 phases of software delivery, and enforce a strict 5-Gate Inclusion Filter for all additions.

## Decision

Chosen option: **"Option 3: Four-Class Asset Taxonomy with 7-Phase SDLC Lifecycle Mapping and 5-Gate Inclusion Filter"**, because:
- It maintains the strict separation of concerns established in ADR 0001 (keeping this repository a portable asset registry, not an execution control plane).
- It provides users and AI agents with clear compositional primitives that assemble into predictable, end-to-end engineering lifecycles.
- It provides maintainers and contributors with an objective, auditable standard for accepting or rejecting new registry assets.

---

### 1. Published Asset Taxonomy

The registry formally recognizes and publishes four asset classes:

```text
omni-agent-skills Registry Assets
 ├── 1. Skills       (registry/skills/<domain>/<id>/SKILL.md)  ──► Atomic Runbooks
 ├── 2. Workflows    (registry/workflows/<id>/)               ──► Multi-Step SDLC Orchestrations
 ├── 3. Rules        (registry/rules/<category>/<id>.md)      ──► Invariant Behavioral Constraints
 └── 4. Helpers      (scripts/ or skill-bundled utilities)    ──► Deterministic Executable Scripts
```

#### A. Skills (`registry/skills/<domain>/<skill-id>/`)
- **Nature:** Atomic, domain-specific engineering runbooks executing a single focused task.
- **Contract:** Must strictly implement the canonical 4-section runbook contract:
  1. `Inputs & Context Required`: Declares preconditions, configuration, and environment dependencies.
  2. `Step-by-Step Procedure`: Provides deterministic, reproducible instructions.
  3. `Expected Outputs & Verifiable Artifacts`: Lists concrete files, test results, and verifiable diffs.
  4. `Constraints & Tool Neutrality`: States boundaries, prohibited actions, and portability requirements.
- **Schema:** Indexed in `registry/registry.json` and validated by `registry/registry.schema.json`.

#### B. Workflows (`registry/workflows/<workflow-id>/`)
- **Nature:** Composite, multi-step operational orchestrations that chain together skills, tools, and quality gates to achieve an end-to-end SDLC outcome (e.g., `workflow-project-initiation`, `workflow-repo-scaffolding`, `workflow-feature-delivery`, `workflow-container-deploy`).
- **Contract:** Defined by a structured workflow manifest (`WORKFLOW.md` and machine-readable metadata) specifying:
  - Sequence of discrete stages.
  - Entry preconditions and required context.
  - Skills and tools invoked at each stage.
  - Mandatory verification gates between stages (e.g., tests must pass before PR creation).
  - Terminal deliverables and release artifacts.

#### C. Rules (`registry/rules/<category>/<rule-id>.md`)
- **Nature:** Persistent behavioral invariants, security shields, and engineering constraints loaded into agent system contexts.
- **Scope:** Universal principles that apply across multiple tasks (e.g., `security_shield.md` enforcing branch isolation, zero secrets, non-destructive file operations, and staging-first execution).

#### D. Deterministic Helpers & Scaffolding Scripts (`scripts/` or skill-bundled)
- **Nature:** Executable Python or POSIX shell scripts bundled with skills or repo tooling.
- **Purpose:** Eliminate LLM guesswork, hallucinations, and syntax divergence by providing pre-tested, deterministic executables for verification, sanitization, schema checking, and project scaffolding.

---

### 2. End-to-End 7-Phase SDLC Lifecycle Matrix

All published assets must map explicitly to one or more phases in the 7-Phase SDLC:

| Phase | Lifecycle Stage | Primary Objective | Example Registry Assets | Key Verification Gate |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | **Inception & PRD** | Requirements definition, scope boundaries, non-goals, and competitive moats | `workflow-project-initiation`, `prd-architecture-generator`, `tech-competitive-intelligence` | Documented charter, user stories, and acceptance criteria |
| **Phase 2** | **Architecture & ADR** | System specs, interface contracts (OpenAPI/MCP), and durable architectural decisions | `rfc-adr-architecture`, `scripts/manage_adr.py`, `docs/adr/` | Validated ADRs (`manage_adr.py validate`), explicit SemVer contracts |
| **Phase 3** | **Greenfield Scaffolding** | Repository initialization, toolchain config, linters, pre-commit hooks, and community health | `workflow-repo-scaffolding`, `project-scaffold-architect`, `oss-launch-governance` | Clean build, linters configured, 100% community health |
| **Phase 4** | **Atomic Implementation** | Focused, single-purpose code modifications, TDD, and callsite updates | `workflow-feature-delivery`, `git-atomic-commit-orchestration`, `refactoring-clean-code` | Scoped git branch, atomic diff, no unintended edits |
| **Phase 5** | **Multi-Tier Verification** | Unit tests, integration assertions, diff audits, and zero-secret hygiene | `advanced-verification-testing`, `security_shield.md`, `scripts/sanitize.py` | Automated test suite passes, zero secrets, clean `git diff --check` |
| **Phase 6** | **Containerization & CI/CD** | Reproducible multi-stage Docker packaging, CI matrix, and automated deployment | `workflow-container-deploy`, `docker-container-builder`, `cicd-pipeline-generator` | Passing CI matrix build, container image scan passes |
| **Phase 7** | **Shipping & Operations** | Semantic versioning, changelog generation, release drafting, and health checks | `release-engineering-semver`, `scripts/bump.py`, `CHANGELOG.md` | Tag-vs-version parity check, release notes generated |

---

### 3. The 5-Gate Inclusion Filter

To be accepted into `omni-agent-skills`, every proposed asset must pass all five mandatory gates:

1. **Gate 1: Orthogonality & Need**
   - The proposed asset must address a real, recurring software engineering problem.
   - It must not duplicate an existing asset in `registry/`. If overlap exists, the existing asset must be enhanced or refactored.
2. **Gate 2: Tool & Agent Neutrality**
   - The asset must NOT require proprietary, closed agent SDKs or vendor-specific platforms.
   - It must be expressible in standard Markdown, JSON Schema, POSIX shell, or standard Python (standard library preferred).
3. **Gate 3: Deterministic Verification Invariant**
   - The asset must specify concrete, objective success criteria (e.g., test command, artifact format, schema check).
   - Subjective outcomes (e.g., "ensure the code looks nice") are rejected.
4. **Gate 4: Canonical Contract Conformance**
   - Skills must implement all 4 required sections without omission.
   - Workflows must define discrete stages, input requirements, and transition gates.
   - Asset metadata must pass `scripts/validate_registry.py` and conform to `registry.schema.json`.
5. **Gate 5: Zero-Secret, Zero-PII, Zero-Hype**
   - Must pass `python3 scripts/sanitize.py` with zero hardcoded credentials, keys, or private identifiers.
   - Must NOT contain unverified benchmark marketing claims (e.g., "state-of-the-art", "guaranteed 100% accuracy", "beats all rivals") as enforced by `test_repo_integrity.py`.

---

## Consequences

### Positive Consequences

- **Unambiguous Catalog Boundaries:** Maintainers and contributors have an explicit rubric for reviewing pull requests and evaluating new asset proposals.
- **End-to-End Usability:** Users and AI agents can execute the entire software lifecycle using published registry assets rather than cobbling together isolated prompt snippets.
- **Deterministic Quality:** Eliminates unverified benchmark hype and replaces speculative AI suggestions with verifiable engineering procedures.
- **Preserved ADR 0001 Scope:** Maintains the registry as a lightweight, portable asset catalog without turning it into a heavy execution runtime.

### Negative Consequences / Trade-offs

- **Higher Contribution Friction:** Contributors must satisfy all 5 quality gates and format their assets to strict schema contracts.
- *Mitigation:* Clear templates, scaffold tooling (`scripts/manage_adr.py`), and automated validation scripts (`scripts/validate_registry.py`) provide rapid, localized feedback.

## Pros and Cons of Options

### Option 1: Unstructured Skill Collection
- Good: Lowest barrier to entry for rapid skill dumps.
- Bad: Rapid quality degradation, severe prompt drift, duplicate capabilities, and no compositional guidance for multi-step tasks.

### Option 2: Monolithic Agent Runtime & Control Plane
- Good: Full end-to-end execution within a single codebase.
- Bad: Violates project charter, introduces heavy runtime dependencies, duplicates existing agent platforms, and creates massive maintenance overhead.

### Option 3: Four-Class Asset Taxonomy with 7-Phase SDLC Mapping and 5-Gate Inclusion Filter
- Good: Combines portable, tool-neutral assets with end-to-end lifecycle coverage, strict quality gates, and high architectural clarity.
- Bad: Requires active catalog curation and maintenance of JSON schemas.

## Validation & Invariants

- Validated by `python3 scripts/manage_adr.py validate` and `scripts/manage_adr.py build-index` to ensure catalog integrity.
- Verified by `python3 scripts/validate_registry.py` to ensure schema compliance of all published assets.
- Protected by `python3 -m unittest discover -s tests -p 'test_*.py'` to ensure zero false benchmark claims and complete catalog integrity.

## Revisit Conditions

Revisit this decision only if:
1. An open industry standard for AI agent capability packages (e.g., an accepted IETF or W3C standard) emerges that defines an alternative canonical packaging format.
2. Major workflow automation engines converge on a universal declarative workflow spec that replaces the need for custom Markdown/JSON workflow manifests.
