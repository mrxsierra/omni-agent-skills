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
- **Option 3: Unified Eight-Asset-Type Taxonomy across Two Tiers with 3D SDLC Discovery Coordinates and 5-Gate Inclusion Filter**
  Formally define eight concrete published asset types structured across two functional tiers (`Core Orchestration` vs `Deterministic Integration`), map them systematically across a 3-Dimensional Coordinate System (SDLC Phase, Domain/Stack Archetype, and Relational Composition), and enforce a strict 5-Gate Inclusion Filter for all additions.

## Decision

Chosen option: **"Option 3: Unified Eight-Asset-Type Taxonomy across Two Tiers with 3D SDLC Discovery Coordinates and 5-Gate Inclusion Filter"**, because:
- It eliminates taxonomy naming confusion by maintaining strict 1-to-1 parity between published asset types and their physical directories in `registry/`, removing abstract "phantom" terms like generic "helpers".
- It maintains the strict separation of concerns established in ADR 0001 (keeping this repository a portable asset registry, not an execution control plane).
- It provides users and AI agents with a multi-dimensional coordinate system (Phase, Domain, Stack, and Complements) so agents make contextual, high-precision asset choices without cognitive friction.
- It provides maintainers and contributors with an objective, auditable standard for accepting or rejecting new registry assets.

---

### 1. Published Asset Taxonomy (1-to-1 Directory Alignment)

To eliminate naming divergence between abstract concepts and physical storage, the registry formally recognizes **8 Concrete Asset Types** organized across **Two Functional Tiers**:

```text
omni-agent-skills Published Asset Hierarchy
├── Tier 1: Core Orchestration & Reasoning Primitives (Agent Planning & Logic)
│   ├── skills/          (registry/skills/<domain>/<id>/SKILL.md)  ──► Atomic Runbooks
│   ├── workflows/       (registry/workflows/<id>/WORKFLOW.md)     ──► Multi-Step SDLC Pipelines
│   ├── rules/           (registry/rules/<category>/<id>.md)       ──► Invariant Behavioral Constraints
│   └── subagents/       (registry/subagents/<id>.json)            ──► Persona & Tool Isolation Manifests
│
└── Tier 2: Deterministic Integration & Context Primitives (Execution Substrate)
    ├── hooks/           (registry/hooks/<pre|post>-tool/<id>.sh)   ──► Lifecycle Guard Shell Scripts
    ├── mcp-configs/     (registry/mcp-configs/<id>.json)          ──► Tool Server Wire Configurations
    ├── snippets/        (registry/snippets/<lang>/<id>)           ──► Battle-Tested Reference Code & Tokens
    └── prompts/         (registry/prompts/<category>/<id>.md)     ──► System Prompt & Persona Templates
```

*(Note: Repository-level verification, schema compilers, and lifecycle tooling reside separately in root `scripts/`).*

#### Tier 1: Core Orchestration & Reasoning Primitives

##### A. Skills (`registry/skills/<domain>/<skill-id>/SKILL.md`)
- **Nature:** Atomic, domain-specific engineering runbooks executing a single focused task.
- **Contract:** Must strictly implement the canonical 4-section runbook contract:
  1. `Inputs & Context Required`: Declares preconditions, configuration, and environment dependencies.
  2. `Step-by-Step Procedure`: Provides deterministic, reproducible instructions.
  3. `Expected Outputs & Verifiable Artifacts`: Lists concrete files, test results, and verifiable diffs.
  4. `Constraints & Tool Neutrality`: States boundaries, prohibited actions, and portability requirements.
- **Schema:** Indexed in `registry/registry.json` and validated by `registry/registry.schema.json`.

##### B. Workflows (`registry/workflows/<workflow-id>/WORKFLOW.md`)
- **Nature:** Composite, multi-step operational orchestrations that chain together skills, subagents, and quality gates to achieve an end-to-end SDLC outcome (e.g., `workflow-project-initiation`, `workflow-repo-scaffolding`, `workflow-feature-delivery`, `workflow-container-deploy`).
- **Contract:** Defined by a structured workflow manifest specifying discrete stages, entry preconditions, invoked skills/subagents, mandatory transition gates, and terminal deliverables.

##### C. Rules (`registry/rules/<category>/<rule-id>.md`)
- **Nature:** Persistent behavioral invariants, security shields, and engineering constraints loaded into agent system contexts.
- **Scope:** Universal and framework principles (e.g., `security_shield.md` enforcing branch isolation, zero secrets, non-destructive file operations, and staging-first execution).

##### D. Subagents (`registry/subagents/<subagent-id>.json`)
- **Nature:** Declarative persona manifests defining isolated execution boundaries, system instructions, and tool whitelists.
- **Role:** Workflow execution actors. Workflows delegate discrete stages to scoped subagents (e.g., `system-architecture-planner.json`, `secret-leak-shield.json`, `code-anti-overengineer.json`) to prevent context pollution.

#### Tier 2: Deterministic Integration & Context Primitives

##### E. Hooks (`registry/hooks/<pre|post>-tool/<hook-id>.sh`)
- **Nature:** Deterministic shell scripts executed before or after tool calls (`pre-tool`, `post-tool`).
- **Role:** Operational guardrails. Mechanically enforce rules (e.g. `secret-leak-guard.sh` intercepting destructive edits or secret exposures; `auto-formatter.sh` reformatting modified code).

##### F. MCP Configs (`registry/mcp-configs/<mcp-id>.json`)
- **Nature:** Model Context Protocol configuration templates connecting agents to external tool servers.
- **Role:** Open tool wire specifications (e.g., `chrome-devtools.json` for DOM inspection, a11y testing, and CWV audits) portable across Claude Desktop, Cursor, and Antigravity.

##### G. Snippets (`registry/snippets/<language>/<snippet-id>`)
- **Nature:** Reusable, battle-tested code implementations, boilerplate, and design tokens (e.g., `async_http_client.py`, `hsl_theme_tokens.ts`).
- **Role:** Anti-hallucination code primitives. Agents reference or drop in pre-tested code rather than generating boilerplate from scratch.

##### H. Prompts (`registry/prompts/<category>/<prompt-id>.md`)
- **Nature:** Reusable system prompt templates and specialized role on-ramps (e.g., `architect-persona.md`).
- **Role:** Cognitive priming. Initializes agent mindset and constraints prior to workflow or skill invocation.

---

### 2. End-to-End 7-Phase SDLC Lifecycle Matrix

All published assets map explicitly across the 7-Phase SDLC:

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

### 3. The 3-Dimensional Coordinate System for Agent Discovery & Composition

To prevent decision paralysis and enable autonomous agents to make optimal, context-aware choices when executing tasks, all assets navigate along three orthogonal dimensions:

```text
               DIMENSION 1: SDLC Phase (WHEN?)
      Inception ──► Scaffolding ──► Implementation ──► Shipping
           │
           │           DIMENSION 2: Domain & Stack (WHERE?)
           ├──► Universal Foundation (Any repository regardless of stack)
           ├──► Web & Frontend (Next.js, TypeScript, CSS, DOM)
           ├──► Backend & Systems (Python, Go, Node, REST APIs, SQL)
           └──► Data & AI (RAG, Evals, Benchmarks, Pipelines)
           │
           │           DIMENSION 3: Relational Composition (WITH WHAT?)
           └──► Cohesive Stack: Workflow + Subagent + Skill + Rule + Hook + Snippet + MCP
```

#### Dimension 1: Temporal Phase (When does it apply?)
Defines the lifecycle moment in the 7-Phase SDLC (`Phase 1` through `Phase 7`). Assets specify which phases they activate in, preventing early-phase tasks (like PRD writing) from triggering late-phase tooling (like deployment).

#### Dimension 2: Domain & Stack Archetype (Where does it apply?)
Distinguishes universal engineering baselines from domain-specific toolchains:
1. **Universal Foundation (Cross-Cutting):**
   Applies to *any* software project regardless of language or architecture.
   - Examples: `security_shield.md` (zero-leak rule), `secret-leak-guard.sh` (pre-tool hook), `semver-release-manager` (skill), `clean-code-auditor` (skill), `oss-launch-governance` (skill).
2. **Domain-Specific Stacks:**
   Activated *only* when the workspace matches the domain or technology stack:
   - **Web & Frontend:** `ai-first-web-geo`, `a11y-web-auditor`, `nextjs_rules.md`, `hsl_theme_tokens.ts`, `chrome-devtools.json`.
   - **Backend & Systems:** `pytest-verification-runner`, `python_rules.md`, `async_http_client.py`.
   - **Data & AI Systems:** `rag-qa-chunking-engine`, `ai-eval-benchmarker`, `system-architecture-planner.json`.

#### Dimension 3: Relational Composition & Archetype Presets (With what does it work?)
Assets work in complementing bundles rather than isolated silos. The registry curates standard **Archetype Stacks**:

| Archetype Stack | Target Task / Workspace | Workflow & Subagent | Skills Invoked | Rules & Prompts | Hooks & Snippets | MCP Tooling |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Universal OSS Baseline** | Any repo scaffolding, PR, or release | `workflow-repo-scaffolding`, `secret-leak-shield.json` | `oss-launch-governance`, `semver-release-manager` | `security_shield.md` | `secret-leak-guard.sh`, `auto-formatter.sh` | — |
| **Modern Web & Frontend** | Next.js / React UI feature delivery | `workflow-feature-delivery`, `system-architecture-planner.json` | `atomic-feature-implementer`, `ai-first-web-geo`, `a11y-web-auditor` | `nextjs_rules.md`, `architect-persona.md` | `auto-formatter.sh`, `hsl_theme_tokens.ts` | `chrome-devtools.json` |
| **Python Backend / CLI** | Python service, testing, and clean code | `workflow-feature-delivery`, `code-anti-overengineer.json` | `atomic-feature-implementer`, `clean-code-auditor`, `pytest-verification-runner` | `python_rules.md` | `auto-formatter.sh`, `async_http_client.py` | — |
| **Data & AI Systems** | RAG pipelines, model eval, dataset chunks | `workflow-feature-delivery`, `system-architecture-planner.json` | `rag-qa-chunking-engine`, `ai-eval-benchmarker` | `security_shield.md` | `async_http_client.py` | — |

---

### 4. The 5-Gate Inclusion Filter

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
   - Subagents, rules, hooks, snippets, and MCP configs must conform to their directory standards and pass local validation.
5. **Gate 5: Zero-Secret, Zero-PII, Zero-Hype**
   - Must pass `python3 scripts/sanitize.py` with zero hardcoded credentials, keys, or private identifiers.
   - Must NOT contain unverified benchmark marketing claims (e.g., "state-of-the-art", "guaranteed 100% accuracy", "beats all rivals") as enforced by `test_repo_integrity.py`.

---

## Consequences

### Positive Consequences

- **Zero Naming Confusion:** Perfect 1-to-1 parity between published asset types and `registry/` directories eliminates phantom folder confusion.
- **Context-Aware Agent Execution:** Agents query assets by SDLC Phase, Domain, and Stack, activating pre-composed archetype bundles instead of guessing combinations.
- **Universal vs. Domain Clarity:** Clear separation ensures universal hygiene rules (security, clean git diffs, semver) are never mixed up with stack-specific tooling (Next.js, Python).
- **Deterministic Quality:** Preserves the 5-Gate filter and zero-hype integrity invariant across all 8 asset types.

### Negative Consequences / Trade-offs

- **Catalog Governance Overhead:** Maintaining 8 asset directories requires consistent validation scripts and clear documentation.
- *Mitigation:* Automated validation scripts (`scripts/validate_registry.py`, `scripts/sanitize.py`, `scripts/manage_adr.py`) provide rapid, mechanical enforcement in CI.

## Pros and Cons of Options

### Option 1: Unstructured Skill Collection
- Good: Lowest barrier to entry for rapid skill dumps.
- Bad: Rapid quality degradation, severe prompt drift, duplicate capabilities, and no compositional guidance for multi-step tasks.

### Option 2: Monolithic Agent Runtime & Control Plane
- Good: Full end-to-end execution within a single codebase.
- Bad: Violates project charter, introduces heavy runtime dependencies, duplicates existing agent platforms, and creates massive maintenance overhead.

### Option 3: Unified Eight-Asset-Type Taxonomy across Two Tiers with 3D SDLC Discovery Coordinates and 5-Gate Inclusion Filter
- Good: Combines portable, tool-neutral assets with 1-to-1 directory clarity, 3D agent discovery coordinates, and multi-tier quality gates.
- Bad: Requires active catalog curation and maintenance of JSON schemas.

## Validation & Invariants

- Validated by `python3 scripts/manage_adr.py validate` and `scripts/manage_adr.py build-index` to ensure catalog integrity.
- Verified by `python3 scripts/validate_registry.py` to ensure schema compliance of all published assets.
- Protected by `python3 -m unittest discover -s tests -p 'test_*.py'` to ensure zero false benchmark claims and complete catalog integrity.

## Revisit Conditions

Revisit this decision only if:
1. An open industry standard for AI agent capability packages (e.g., an accepted IETF or W3C standard) emerges that defines an alternative canonical packaging format.
2. Major workflow automation engines converge on a universal declarative workflow spec that replaces the need for custom Markdown/JSON workflow manifests.
