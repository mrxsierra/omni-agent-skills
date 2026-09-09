# 📊 Empirical Evaluation & Quality Scorecard

This directory contains the empirical evaluation baselines, benchmark task suites,
and reproducible results for the assets published in the `omni-agent-skills` registry.

> [!IMPORTANT]
> **Zero-Hype Empirical Gate (ADR 0004 & ADR 0005):**
> Every skill, rule, or workflow admitted to this registry must prove positive $\Delta$-utility
> or high baseline parity with minimal token tax. Prompt bloat, unverified claims, and
> performance-degrading instructions are rejected automatically.

## Summary Metrics

- **Total Catalog Assets Benchmarked:** 16 (15 of 15 skills + 1 security rule)
- **Benchmark Pass Rate:** 100.0% (32/32 baseline evaluations passed)
- **Average Context Token Tax:** +548 tokens / turn
- **Evaluated Provider Engines:** `mock`, `agy` (`gemini-3.8-flash-high`), `gemini` (`gemini-2.5-flash`), `mistral` (`codestral-latest`), `openrouter` (`cohere/north-mini-code:free`), `ollama` (`qwen2.5-coder:1.5b`)
- **Evaluation Coverage Status:** 100% of skills covered; 3 non-security rules in `registry/rules/` tracked in roadmap backlog.

---

## Multi-Tier Evaluation Architecture (ADR 0005 & ADR 0006)

Evaluation is decoupled into three operational tiers with dynamic capacity routing and preflight credential checks:

### 1. Preflight Credential & Quota Diagnostics

Run an instant zero-leak check before launching neural evaluations to verify configured keys and remaining quotas:
```bash
# Run preflight diagnostics across all configured providers
./scripts/run_local_eval.sh check-keys
# Or direct CLI:
python3 scripts/check_api_keys.py
```

### 2. Model Capacity Hierarchy & Dynamic Taxonomy Routing (ADR 0006)

Assets dynamically resolve their evaluation capacity tier to ensure resource protection and rigorous testing without hardcoded paths:

| Capacity Tier | Parameter Scale | Reference Engines | Target Asset Types / Domains | Evaluation Focus |
| :--- | :--- | :--- | :--- | :--- |
| **Tier S** | 1B – 7B | Ollama `qwen:1.5b`<br>Gemini `gemini-2.5-flash`<br>OpenRouter `:free` | `registry/rules/**`<br>`security-and-governance/` | Syntactic guardrails, secret detection regex, anti-overengineering. Must show positive $\Delta$-utility. |
| **Tier M** | 8B – 32B | Mistral `codestral-latest`<br>Ollama `qwen:14b`<br>OpenAI `gpt-4o-mini` | `engineering/`<br>`web-and-geo/` | Structured code generation, isolated unit test fixtures, JSON-LD / GEO schemas. |
| **Tier L** | 70B+ / Cloud | Antigravity `gemini-3.8-flash-high`<br>Gemini `gemini-2.5-pro`<br>Claude `claude-3-5-sonnet` | `architecture/`<br>`protocols/` | Multi-phase architecture specs, MCP protocol design, competitive analysis. |

> [!TIP]
> **Dynamic Routing:** An asset automatically inherits its tier from its domain directory. Any task suite can explicitly override this by setting `"eval_tier": "S" | "M" | "L"` in `evals/tasks/<suite>.json`.

### 3. Task Rigor & Frontier Saturation Policy

- **Adversarial Trap Prompts:** Evaluation tasks actively tempt the model with anti-patterns (e.g. commenting out failing tests or adding nested conditionals) to test refusal and rule enforcement.
- **Strict Negative Invariants (`fail_keywords`):** Tasks enforce zero-tolerance forbidden keywords, penalizing models that take unprincipled shortcuts.
- **Conjunctive Criteria:** Scoring supports `match_mode: all` and `min_matches: N` requiring multiple distinct domain concepts.
- **Frontier Saturation Rule ($\Delta = 0%$):** On Tier L models, high baseline parity (100%) is accepted only if augmented maintains 100% parity, triggers zero `fail_keywords`, and incurs Context Token Tax $< 750$ tokens/turn. Inherent utility must be proven on Tier S or Tier M.

---

## Asset Benchmark Scorecard

| Asset / Skill | Domain | Suite ID | Provider (Model) | Base % | Aug % | $\Delta$-Utility | Token Tax | Gate Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ai-eval-benchmarker` | data-and-ai | `ai_eval_benchmarker` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +539 tok | ✅ PASS |
| `ai-eval-benchmarker` | data-and-ai | `ai_eval_benchmarker` | `agy` (`gemini-3.8-flash-high`) | 100.0% | 100.0% | **+0.0%** | +539 tok | ✅ PASS |
| `rag-qa-chunking-engine` | data-and-ai | `rag_qa_chunking_engine` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +624 tok | ✅ PASS |
| `rag-qa-chunking-engine` | data-and-ai | `rag_qa_chunking_engine` | `agy` (`gemini-3.8-flash-high`) | 50.0% | 100.0% | **+50.0%** | +624 tok | ✅ PASS |
| `atomic-feature-implementer` | engineering | `atomic_feature_implementer` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +528 tok | ✅ PASS |
| `atomic-feature-implementer` | engineering | `atomic_feature_implementer` | `agy` (`gemini-3.8-flash-high`) | 50.0% | 100.0% | **+50.0%** | +527 tok | ✅ PASS |
| `clean-code-auditor` | engineering | `clean_code_audit` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +522 tok | ✅ PASS |
| `clean-code-auditor` | engineering | `clean_code_audit` | `agy` (`gemini-3.8-flash-high`) | 100.0% | 100.0% | **+0.0%** | +523 tok | ✅ PASS |
| `code-anti-overengineer` | engineering | `code_anti_overengineer` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +537 tok | ✅ PASS |
| `code-anti-overengineer` | engineering | `code_anti_overengineer` | `agy` (`gemini-3.8-flash-high`) | 100.0% | 100.0% | **+0.0%** | +537 tok | ✅ PASS |
| `pytest-verification-runner` | engineering | `pytest_verification_runner` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +542 tok | ✅ PASS |
| `pytest-verification-runner` | engineering | `pytest_verification_runner` | `agy` (`gemini-3.8-flash-high`) | 100.0% | 100.0% | **+0.0%** | +541 tok | ✅ PASS |
| `semver-release-manager` | engineering | `semver_release_manager` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +553 tok | ✅ PASS |
| `semver-release-manager` | engineering | `semver_release_manager` | `agy` (`gemini-3.8-flash-high`) | 50.0% | 100.0% | **+50.0%** | +553 tok | ✅ PASS |
| `system-architecture-planner` | engineering | `system_architecture_planner` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +565 tok | ✅ PASS |
| `system-architecture-planner` | engineering | `system_architecture_planner` | `agy` (`gemini-3.8-flash-high`) | 100.0% | 100.0% | **+0.0%** | +566 tok | ✅ PASS |
| `advanced-verification-testing` | security-and-governance | `advanced_verification_testing` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +575 tok | ✅ PASS |
| `advanced-verification-testing` | security-and-governance | `advanced_verification_testing` | `agy` (`gemini-3.8-flash-high`) | 100.0% | 100.0% | **+0.0%** | +575 tok | ✅ PASS |
| `ai-native-product-design` | security-and-governance | `ai_native_product_design` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +541 tok | ✅ PASS |
| `ai-native-product-design` | security-and-governance | `ai_native_product_design` | `agy` (`gemini-3.8-flash-high`) | 100.0% | 100.0% | **+0.0%** | +540 tok | ✅ PASS |
| `oss-launch-governance` | security-and-governance | `oss_launch_governance` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +538 tok | ✅ PASS |
| `oss-launch-governance` | security-and-governance | `oss_launch_governance` | `agy` (`gemini-3.8-flash-high`) | 100.0% | 100.0% | **+0.0%** | +539 tok | ✅ PASS |
| `secret-leak-shield` | security-and-governance | `secret_leak_shield` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +567 tok | ✅ PASS |
| `secret-leak-shield` | security-and-governance | `secret_leak_shield` | `agy` (`gemini-3.8-flash-high`) | 100.0% | 100.0% | **+0.0%** | +567 tok | ✅ PASS |
| `security_shield.md` | security-and-governance | `security_shield` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +406 tok | ✅ PASS |
| `security_shield.md` | security-and-governance | `security_shield` | `agy` (`gemini-3.8-flash-high`) | 50.0% | 100.0% | **+50.0%** | +407 tok | ✅ PASS |
| `tech-competitive-intelligence` | security-and-governance | `tech_competitive_intelligence` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +566 tok | ✅ PASS |
| `tech-competitive-intelligence` | security-and-governance | `tech_competitive_intelligence` | `agy` (`gemini-3.8-flash-high`) | 100.0% | 100.0% | **+0.0%** | +567 tok | ✅ PASS |
| `a11y-web-auditor` | web-and-geo | `a11y_audit` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +574 tok | ✅ PASS |
| `a11y-web-auditor` | web-and-geo | `a11y_audit` | `agy` (`gemini-3.8-flash-high`) | 100.0% | 100.0% | **+0.0%** | +574 tok | ✅ PASS |
| `ai-first-web-geo` | web-and-geo | `ai_first_web_geo` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +590 tok | ✅ PASS |
| `ai-first-web-geo` | web-and-geo | `ai_first_web_geo` | `agy` (`gemini-3.8-flash-high`) | 100.0% | 100.0% | **+0.0%** | +591 tok | ✅ PASS |

---

## Reproducing & Running Evaluations

The evaluation harness operates in three execution modes across local development and CI/CD:

1. **Delta Mode (Default):** Evaluates only modified or newly added assets compared to `dev`. If no registry assets were changed, evaluation is skipped automatically.
2. **Single Asset:** Evaluates a specific target asset.
3. **Full Catalog Sweep (`--all`):** Evaluates all 16 assets across the registry (used by weekly CI crons and release gates).

### Local Execution (Helper Script)

```bash
# 0. Preflight credential and connectivity diagnostics
scripts/run_local_eval.sh check-keys

# 1. Delta evaluation (evaluates only modified/added assets vs dev)
scripts/run_local_eval.sh mock
scripts/run_local_eval.sh gemini                                              # Tier S / Free Flash
scripts/run_local_eval.sh mistral                                             # Tier M / Codestral
scripts/run_local_eval.sh openrouter                                          # Free-tier model
scripts/run_local_eval.sh agy                                                 # Cloud eval via agy CLI

# 2. Full catalog sweep (all 16 assets)
scripts/run_local_eval.sh mock --all
scripts/run_local_eval.sh agy --all

# 3. Single specific asset
scripts/run_local_eval.sh gemini registry/skills/engineering/clean-code-auditor/SKILL.md
scripts/run_local_eval.sh mistral registry/skills/engineering/clean-code-auditor/SKILL.md

# 4. Rootless containerized open-weights evaluation (Podman/Docker)
scripts/run_local_eval.sh podman start qwen2.5-coder:1.5b
scripts/run_local_eval.sh podman eval                                           # Delta mode
scripts/run_local_eval.sh podman eval --all                                     # Full sweep
scripts/run_local_eval.sh podman stop
```

### Direct Python CLI (`scripts/eval_asset.py`)

```bash
# Preflight credential check
python3 scripts/check_api_keys.py

# Delta mode (auto-detects changes against origin/dev)
python3 scripts/eval_asset.py --provider gemini --model gemini-2.5-flash
python3 scripts/eval_asset.py --provider mistral --model codestral-latest

# Full catalog sweep
python3 scripts/eval_asset.py --all --provider mock --strict
```

To rebuild this scorecard after updating baselines:
```bash
python3 scripts/build_eval_report.py
```
