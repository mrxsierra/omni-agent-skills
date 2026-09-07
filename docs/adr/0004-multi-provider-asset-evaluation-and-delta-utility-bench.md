# ADR 0004: Multi-Provider Asset Evaluation and Delta-Utility Bench

## Status

Accepted — 2026-09-07

## Deciders

Sunil Sharma (@mrxsierra)

## Context & Problem Statement

Anyone can write markdown prompts and submit them to a repository, but adding unverified prompts, rules, or instructions often causes **negative utility**:
1. **Prompt Dilution & Distraction:** Injected prompt tokens can distract foundation models from following immediate user constraints.
2. **The Token Tax:** Every injected skill, rule, or subagent burns context tokens across every subsequent interaction turn.
3. **Over-Engineering & Loops:** Poorly specified runbooks encourage models to generate unnecessary layers of abstraction or enter infinite retry loops.

Prior to this decision, `omni-agent-skills` enforced static schema validity ([`registry.schema.json`](../../registry/registry.schema.json)) and regex-based claim checks ([`scripts/sanitize.py`](../../scripts/sanitize.py)), but lacked an **empirical evaluation harness** to prove whether a proposed registry asset genuinely improves an agent's task performance over a baseline foundation model.

Furthermore, in accordance with the repository's core principle of **Tool Neutrality** ([ADR 0001](../0001-registry-not-control-plane.md) and [ADR 0003](../0003-registry-asset-taxonomy-shipped-capabilities-and-inclusion-criteria.md)), contributors and developers operate across diverse AI ecosystems: some prefer **Google Antigravity**, others use **local Ollama** for privacy and zero cost, while others utilize **OpenAI/ChatGPT**, **Anthropic/Claude**, or **OpenRouter**. An evaluation system that mandates a single proprietary vendor or paid API key would violate tool neutrality and exclude open-source contributors.

## Decision Drivers

- **Tool Neutrality & Pluggable Providers:** The evaluation harness must support Google Antigravity, local Ollama (open weights), OpenAI, Anthropic, OpenRouter, and offline mock runners.
- **Empirical $\Delta$-Utility Verification:** We do not admit assets on faith or vibes; proposed assets must prove a measurable positive delta over the baseline foundation model.
- **Anti-Junk / Token Tax Guard:** Assets that introduce excessive prompt tokens without measurable performance improvements must be flagged as bloat and rejected.
- **Zero Mandatory External Dependencies:** The provider interface and runner must use Python standard library modules (`urllib.request`, `json`, `os`, `abc`) to avoid brittle dependency churn or heavy framework lock-in.
- **Deterministic CI Execution:** Pull request validation in GitHub Actions must run offline via golden mock fixtures without requiring live API keys or network access.

## Considered Options

- **Option 1: Vendor-Locked Benchmark Harness (OpenAI Evals / LangSmith)**
  Require contributors to run benchmarks against a single paid vendor API. (*Rejected: Violates tool neutrality, forces contributors to pay API fees, and creates heavy external dependencies*).
- **Option 2: Pure Static Verification without Empirical Agent Evaluation**
  Rely solely on schema validation and manual pull-request reviews without evaluating actual agent execution. (*Rejected: Fails to detect prompt bloat, hallucination traps, or negative utility*).
- **Option 3: Pluggable Multi-Provider $\Delta$-Utility Evaluation Bench with Standard Task Suites**
  Build a lightweight, zero-dependency evaluation harness that tests assets across pluggable provider adapters (Antigravity, Ollama, OpenAI, Anthropic, OpenRouter, Mock) and enforces positive $\Delta$-utility admission gates.

## Decision

Chosen option: **"Option 3: Pluggable Multi-Provider Delta-Utility Evaluation Bench with Standard Task Suites"**, because:
- It respects contributor choice by allowing anyone to evaluate assets locally using their preferred provider (Google Antigravity, free local Ollama, or commercial cloud APIs).
- It introduces an objective, empirical standard to separate genuine engineering capabilities from placebo prompt bloat.
- It enables 100% offline, zero-secret CI execution using mock replay fixtures.

---

### 1. Pluggable Provider Architecture

The evaluation harness abstracts model interaction behind a unified, zero-dependency interface (`scripts/eval_providers.py`):

```text
                     scripts/eval_asset.py (CLI Runner)
                                     │
            ┌────────────────────────┴────────────────────────┐
            ▼                                                 ▼
   Task Runner & Scorer                             Pluggable Provider
                                                              │
            ┌──────────────────┬──────────────────┬───────────┴──────┬──────────────────┐
            ▼                  ▼                  ▼                  ▼                  ▼
     Antigravity /        Local Ollama       OpenAI /          Anthropic /        Deterministic
     Google Gemini      (Open Weights)       ChatGPT             Claude               Mock
   (GEMINI_API_KEY/   (http://localhost: (OPENAI_API_KEY)  (ANTHROPIC_API_KEY)    (Offline CI
     Native Env)            11434)                                                  Fixtures)
```

#### Provider Contracts:
1. **`antigravity`**: Targets Google Antigravity / Gemini CLI or Google GenAI endpoints.
2. **`ollama`**: Connects directly to local Ollama daemon (`http://localhost:11434/api/chat`), enabling zero-cost, private, offline evaluations using models like `qwen2.5-coder:7b` or `llama3:8b`.
3. **`openai` / `openai-compatible`**: Connects to OpenAI, OpenRouter (`https://openrouter.ai/api/v1`), Groq, DeepSeek, or vLLM via standard `/v1/chat/completions`.
4. **`anthropic`**: Connects to the Anthropic Messages API (`/v1/messages`).
5. **`mock`**: Operates completely offline with zero API keys or network access, replaying checked-in golden responses to validate the test harness itself in CI.

---

### 2. The Empirical $\Delta$-Utility Admission Formula

To be admitted into the registry, a proposed skill, rule, or workflow must demonstrate a positive delta utility on a representative task suite:

$$\Delta \text{Utility}(A) = \text{Task Pass Rate}(+A) - \text{Task Pass Rate}(\text{Baseline})$$
$$\text{Token Tax}(A) = \text{Prompt Tokens Injected} \times \text{Interaction Turns}$$

#### The Anti-Junk Admission Gate:
- **`ACCEPTED (Positive Utility)`**: $\Delta \text{Utility} > 0$ and procedural compliance verified.
- **`REJECTED (Bloat/Placebo)`**: $\Delta \text{Utility} \le 0$ (the baseline model solves the task just as well without the asset, proving the asset is redundant context bloat).
- **`REJECTED (High Token Tax)`**: If $\Delta \text{Utility}$ is marginal ($< +5\%$) but the asset injects $> 1,000$ prompt tokens per turn, it is rejected for poor token economics.

---

### 3. Three-Tier Evaluation Pipeline

```text
[Proposed Asset PR]
         │
         ▼
┌────────────────────────────────────────────────────────┐
│ Tier 0: Static & Contract Hygiene (sanitize + schema) │ ──► Instant syntax & zero-hype gates
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ Tier 1: Deterministic Bench (pytest, tsc, hook tests) │ ──► Validates executable code & scripts
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ Tier 2: Delta-Utility Ablation (Pluggable Providers)  │ ──► Proves Δ-Utility > Token Tax
└────────────────────────────────────────────────────────┘
```

---

## Consequences

### Positive Consequences

- **Contributor Inclusivity:** Anyone can run evaluations locally with zero cost using Ollama, with high-reasoning models using Antigravity/Gemini, or across multi-vendor suites via OpenRouter.
- **Empirical Quality Invariant:** Eliminates placebo prompts and low-quality prompt dumps; every published asset has measured proof of value.
- **Zero Flaky CI:** GitHub Actions CI executes deterministic mock runs without depending on external API rate limits or exposing secret tokens.

### Negative Consequences / Trade-offs

- **Evaluation Runtime Cost:** Running full agent evaluations across multiple tasks and providers takes longer than static schema validation.
- *Mitigation:* Heavy multi-model evals are run on-demand or during feature authoring; CI enforces Tier 0 (static) and Tier 1 (deterministic mock replay) on every commit.

## Pros and Cons of Options

### Option 1: Vendor-Locked Benchmark Harness
- Good: Leverages pre-existing commercial evaluation SaaS dashboards.
- Bad: Excludes contributors without paid accounts, violates tool neutrality, and creates vendor lock-in.

### Option 2: Pure Static Verification without Empirical Agent Evaluation
- Good: Fast and zero cost.
- Bad: Blind to prompt regressions, context bloat, and actual agent effectiveness.

### Option 3: Pluggable Multi-Provider Delta-Utility Evaluation Bench
- Good: Tool-neutral, works locally for free or in the cloud, zero external dependencies, and enforces positive delta value.
- Bad: Requires authoring and maintaining standardized evaluation task suites.

## Validation & Invariants

- Validated by `python3 scripts/manage_adr.py validate` and `scripts/manage_adr.py build-index`.
- Unit tests in `tests/test_eval_providers.py` verify all provider adapters and mock execution in CI.
- Sanity checked via `python3 scripts/eval_asset.py --asset <path> --provider mock`.

## Revisit Conditions

Revisit this decision only if:
1. An open industry standard emerges (e.g. from the Model Context Protocol or Open-Source AI foundations) that provides a universal, cross-vendor agent evaluation harness adopted by all major agent frameworks.
