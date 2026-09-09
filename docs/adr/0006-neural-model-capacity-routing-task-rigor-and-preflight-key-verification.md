# ADR 0006: Neural Model Capacity Routing Task Rigor and Preflight Key Verification

## Status

Accepted — 2026-09-09

## Deciders

Sunil Sharma (@mrxsierra)

## Context & Problem Statement

In ADR 0004 and ADR 0005, `omni-agent-skills` established a multi-provider asset evaluation bench and a two-track branching protocol with tiered verification (Tier 1 Mock, Tier 2 Open-Weights, Tier 3 Cloud Heavy Lifting).

However, live empirical testing across Google Gemini, Mistral AI, OpenRouter, and Ollama exposed four critical operational challenges:
1. **Free-Tier Rate Limits & Quotas**: Free and experimentation tiers have strict quotas (OpenRouter: 50 requests/day; Mistral: 125 requests/minute; Google AI Studio: 15 requests/minute for Flash, 2 requests/minute for Pro). A full catalog sweep across 16 assets consumes ~64 API calls, which immediately exhausts daily limits on free-tier keys.
2. **The Frontier Model Saturation Problem ($\Delta = 0\%$)**: Frontier models (Claude 3.5 Sonnet, Gemini 2.5 Pro, GPT-4o) frequently achieve a 100% baseline pass rate on generic programming prompts, producing a Delta Utility of $0.0\%$. This risks misclassifying valuable engineering skills as redundant prompt bloat unless evaluation tasks test negative constraints and disciplined adherence.
3. **Rigid Hardcoding Risk**: Assigning models directly to individual asset filenames (e.g. `clean-code-auditor`) does not scale as new skills, rules, and workflows are continuously contributed.
4. **Credential Blindness**: Contributors and AI agents frequently launch heavy evaluation runs with missing, expired, or deprecated API keys (e.g. calling retired model slugs), resulting in long timeouts, noisy tracebacks, and wasted compute.

This ADR defines the architectural standards for model capacity tiering, dynamic taxonomy routing, evaluation task rigor, and preflight key verification.

## Decision Drivers

- **Driver 1: Resource Efficiency & Quota Protection**: Prevent daily pull requests from exhausting free-tier quotas or burning excessive cloud tokens.
- **Driver 2: Future-Proof Taxonomy Routing**: Automatically assign appropriate model tiers to newly added assets without hardcoding file paths.
- **Driver 3: Meaningful Delta-Utility Signal**: Prevent false positives (from trivial prompts) and false negatives (from frontier ceiling saturation).
- **Driver 4: Contributor & Agent Ergonomics**: Provide fast, zero-leak credential diagnostics before launching long-running evaluations.
- **Driver 5: Zero Third-Party Dependencies**: Enforce all evaluation harness tooling using Python standard library modules only (urllib, json, subprocess).

## Considered Options

- **Option 1: Uniform Model Evaluation**: Evaluate all assets against a single default model (e.g. always `gemini-2.5-flash` or always `qwen2.5-coder:7b`).
- **Option 2: Static Path-to-Model Configuration**: Maintain a static mapping table in a JSON/YAML configuration file binding every asset file path to a specific model.
- **Option 3: Dynamic 3-Tier Capacity Hierarchy (S/M/L) with Taxonomy Routing, Task Rigor Standards, and Preflight Diagnostics**:
  - Classify models into three standard parameter/capacity tiers (Small, Medium, Large).
  - Dynamically infer tier from asset taxonomy (domain and type) with an optional task-suite override.
  - Codify task rigor rules (adversarial trap prompts, negative invariants, conjunctive criteria).
  - Formalize the Frontier Saturation Policy.
  - Mandate preflight key checking.

## Decision

Chosen option: **"Option 3: Dynamic 3-Tier Capacity Hierarchy (S/M/L) with Taxonomy Routing, Task Rigor Standards, and Preflight Diagnostics"**, because it balances resource constraints, evaluation honesty, and extensibility.

### 1. The 3-Tier Model Capacity Hierarchy

Models are categorized into three operational capacity tiers:

| Tier | Parameter Scale | Reference Engines & Models | Primary Evaluation Target |
| :--- | :--- | :--- | :--- |
| **Tier S** (Small / Compact) | 1B – 7B | Ollama `qwen2.5-coder:1.5b/7b`<br>Gemini `gemini-2.5-flash`<br>OpenRouter `nvidia/nemotron-3.5-lightning:free` | Syntactic invariants, formatting, regex/secret shields, linting, anti-overengineering guardrails. |
| **Tier M** (Medium) | 8B – 32B | Mistral `codestral-latest`<br>Ollama `qwen2.5-coder:14b/32b`<br>OpenAI `gpt-4o-mini` | Structured code generation, isolated unit test fixtures, JSON-LD / GEO schemas, RAG QA chunking. |
| **Tier L** (Large / Frontier) | 70B+ / Frontier Cloud | Antigravity `gemini-3.8-flash-high`<br>Gemini `gemini-2.5-pro`<br>Anthropic `claude-3-5-sonnet` | Multi-phase architectural design, competitive analysis, property-based testing, MCP protocol specs. |

### 2. Dynamic Taxonomy-Based Capacity Routing

The evaluation runner resolves the required model tier dynamically using a 2-layer resolution procedure:

1. **Explicit Task Suite Metadata (Layer 1)**: If `evals/tasks/<suite_id>.json` contains `"eval_tier": "S" | "M" | "L"`, this value takes precedence.
2. **Taxonomy & Domain Fallback (Layer 2)**: If omitted, the runner infers the tier based on the asset's ADR 0003 directory taxonomy:
   - `registry/rules/**` and `security-and-governance/` $\longrightarrow$ **Tier S**
   - `engineering/` and `web-and-geo/` $\longrightarrow$ **Tier M**
   - `architecture/` and `protocols/` $\longrightarrow$ **Tier L**

New assets added to the repository automatically inherit the correct tier without requiring central configuration updates.

### 3. Task Rigor Standards

To ensure evaluation integrity across both smaller and frontier models, task suites must adhere to three design standards:

1. **Adversarial Trap Prompts**: Prompts must actively tempt the model to take a bad shortcut (e.g. suggesting commenting out an assertion, adding nested conditionals, or hardcoding a test secret). The skill's value is proven when the augmented model rejects the bad practice.
2. **Strict Negative Invariants (`fail_keywords`)**: Tasks must specify forbidden anti-patterns that result in immediate failure if present in the response.
3. **Conjunctive Matching (`match_mode`)**: Scoring supports `match_mode: "all"` and `min_matches: N` so that responses must satisfy multiple distinct domain criteria rather than passing on a single generic word.

### 4. The Frontier Model Saturation Policy ($\Delta = 0\%$)

When evaluating assets against Tier L (Frontier) models:
- **Proof of Actionable Utility**: Must be demonstrated on **Tier S or Tier M models**. A skill that does not boost a Small or Medium model from failure to success ($\Delta > 0\%$) fails acceptance.
- **Frontier Gate Invariant**: If a Tier L model scores 100% baseline, the asset is accepted **if and only if**:
  1. Augmented pass rate maintains 100% parity.
  2. Zero `fail_keywords` are triggered (negative constraint compliance).
  3. Context Token Tax is minimal ($< 750$ tokens/turn).

### 5. Preflight Credential Verification (`check_api_keys.py`)

Before launching neural evaluation runs, contributors and agents execute:
```bash
python3 scripts/check_api_keys.py
# Or helper shortcut:
./scripts/run_local_eval.sh check-keys
```
This utility:
- Safely inspects `.env` with masked output (zero credential exposure).
- Sends a minimal 1-token probe (`"ping" -> "pong"`) to configured providers.
- Checks remaining quotas (e.g. OpenRouter free-tier 50 req/day check via `/api/v1/key`).
- Provides actionable diagnostic hints if a model slug is deprecated or rate-limited.

## Consequences

### Positive Consequences

- **Extensibility**: Future assets automatically inherit their capacity tier from their taxonomy path.
- **Quota Safety**: Daily PRs remain within free-tier quotas (e.g. 4 requests for delta eval vs. 64 requests for full sweep).
- **Rigor & Honesty**: Evaluation tasks target the delta and negative constraints, avoiding misleading baseline passes.
- **Zero Drift**: Eliminates recurring debates on which model to use for which skill.
- **Fast Feedback**: Preflight key check diagnoses invalid keys in < 2 seconds without launching long evaluations.

### Negative Consequences / Trade-offs

- **Task Suite Authoring Discipline**: Requires task authors to craft adversarial trap prompts and negative keywords rather than simple happy-path questions.
- **Mitigation**: Standard templates and documentation in `evals/README.md` guide task creation.

## Pros and Cons of Options

### Option 1: Uniform Model Evaluation
- Good, because single command setup is simple.
- Bad, because testing all rules against a 70B model wastes quota, while testing complex architecture on a 1.5B model produces misleading failures.

### Option 2: Static Path-to-Model Configuration
- Good, because mapping is explicit in one file.
- Bad, because it creates high maintenance overhead; contributors forget to update the config when adding new assets.

### Option 3: Dynamic 3-Tier Capacity Hierarchy with Taxonomy Routing
- Good, because it scales automatically to future assets, preserves free-tier quotas, and enforces task rigor.
- Bad, requires maintaining the taxonomy routing logic in the runner script.

## Validation & Invariants

- **Automated Tests**: `tests/test_check_api_keys.py` and `tests/test_eval_providers.py` validate dynamic tier resolution, key masking, and conjunctive scoring.
- **CI Hygiene**: `python3 scripts/manage_adr.py validate` verifies ADR 0006 formatting and catalog parity.
- **SOP Gate**: `docs/sops/contribution-and-feature-delivery.md` mandates the preflight key check in Step 4.

## Revisit Conditions

- If free-tier provider limits change significantly (e.g. OpenRouter eliminates free models or Google changes Flash quotas).
- If lightweight models (< 3B parameters) achieve reasoning parity with frontier models on complex multi-phase architecture planning.
