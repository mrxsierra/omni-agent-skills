# ADR 0005: Two-Track Branching and Dual-Engine Evaluation

## Status

Accepted — 2026-09-08

## Deciders

Sunil Sharma (@mrxsierra)

## Context & Problem Statement

As `omni-agent-skills` matures into an open-source registry with an empirical evaluation pipeline, two operational friction points have emerged:

1. **Single-Branch Trunk Fragility:**
   Under ADR 0002, all feature branches branched directly from and targeted `main`. This created release instability: in-flight feature iterations, pre-release testing, and catalog experiments landed directly on the production release branch, complicating version tagging and clean release boundaries.

2. **The Model Capacity & Infrastructure Dilemma:**
   - **The Capacity Floor (< 3B models):** Testing skills with tiny models like `qwen2.5-coder:1.5b` on CPU runners revealed an empirical limitation: smaller models lack the reasoning capacity to follow complex multi-step refactoring or architectural planning prompts. They fail with or without skill injection, leading to false-negative $\Delta\text{Utility} = 0.0\%$ rejections.
   - **The CI CPU Bottleneck (7B+ models):** Free GitHub Actions runners have 2–4 vCPUs and 7 GB RAM with no GPU. Running a 7B model across the catalog takes 45+ minutes, consuming disproportionate runner minutes and risking CI timeouts.
   - **Developer Machine Friction:** Forcing developers to install native daemons or run heavy local models creates friction for contributors on resource-constrained machines.
   - **Evaluation Transparency Gap:** Real neural evaluation runs in CI uploaded temporary artifact zip files that expired after 7 days, leaving no permanent, public visual scorecard for the open-source community.

We require a structured git branching model, a tiered evaluation strategy that separates fast CI gates from cloud-powered heavy lifting, and public transparency for evaluation results.

---

## Decision Drivers

- **Driver 1 (Release Stability):** Isolate active development from release-tagged production code.
- **Driver 2 (Zero CI Bottlenecks):** Keep pull request verification fast (< 2 minutes) while enabling deep reasoning benchmarks on complex skills.
- **Driver 3 (Frictionless Developer On-Ramp):** Enable contributors to test changes locally via fast mock, rootless containerized open weights (Podman/Docker), or zero-download cloud CLI (`agy`).
- **Driver 4 (Public Transparency):** Provide immediate, visual evaluation feedback in pull requests and permanent scorecards in the repository.

---

## Considered Options

- **Option 1 (Status Quo):** Continue single-branch `main` delivery with CPU-only Ollama runs in CI.
- **Option 2 (Heavy CI Runners):** Provision paid GPU self-hosted runners to run 7B–14B models on every PR.
- **Option 3 (Two-Track Branching + Dual-Engine Tiered Evaluation):** Establish `dev` as the integration trunk, reserve `main` for releases, run fast mock + lightweight smoke on PRs, and utilize cloud-based engines for complex heavy-lifting evaluation on schedule/release gates.

---

## Decision

Chosen option: **Option 3: Two-Track Branching + Dual-Engine Tiered Evaluation**.

### 1. Two-Track Git Flow (`dev` vs. `main`)
- **`dev` Branch (Active Integration Trunk):**
  - All new feature, bugfix, documentation, and chore branches (`feat/*`, `fix/*`, `chore/*`, `docs/*`) branch from `dev` and submit pull requests targeting `dev`.
  - Enforces the Tier 0 Static Hygiene suite, Tier 1 Deterministic Mock Gate (< 2s), and lightweight neural smoke tests.
- **`main` Branch (Production Release Trunk):**
  - Protected release branch containing only verified, release-ready code.
  - Promoted from `dev` periodically (weekly or at milestone boundaries) after passing the full cloud-based catalog evaluation matrix.
  - Release tags (`v0.0.3`, `v0.1.0`) are cut exclusively from `main`.

### 2. Dual-Engine Evaluation Strategy
We decouple fast pull request validation from deep cognitive evaluation across three explicit tiers:

| Tier | Engine & Provider | Target Environment | Scope | Frequency |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Harness Gate** | `MockProvider` | Local & CI | All 16 assets in < 2 seconds | Every commit and PR to `dev` |
| **Tier 2: Neural Smoke** | `ollama` (`qwen2.5-coder:1.5b`) | CI & Local Podman | Changed asset format & simple reasoning | PRs to `dev` touching `registry/` |
| **Tier 3: Cloud Heavy Lifting** | Cloud (`agy` / Gemini Flash / Claude) | Local & Scheduled CI | Deep architectural & complex skills matrix | Weekly cron, release promotion, or manual dispatch |

### 3. Frictionless Local Development Options
Contributors may choose the evaluation method that best matches their hardware:
- **Fast Mock:** `python3 scripts/eval_asset.py --asset <path> --provider mock` (offline, instant).
- **Containerized Open-Weights:** Rootless Podman/Docker Ollama container (`scripts/run_local_eval.sh podman`) using lightweight models by default.
- **Native Cloud CLI (`agy`):** Native integration with `/home/sunil/.local/bin/agy` (`--provider agy --model gemini-3.8-flash-high`) enabling instant cloud evaluation without downloading model weights.

### 4. Public Transparency & Scorecards
- **GitHub PR Step Summary:** When evaluation runs in CI, automatically generate a GitHub Step Summary Markdown table (`$GITHUB_STEP_SUMMARY`) on the pull request run page.
- **Public Evaluation Scorecard:** Maintain committed benchmark baselines in `evals/baselines/` and compile them into a public scorecard at `evals/README.md`.

---

## Consequences

### Positive Consequences
- **Stable Releases:** `main` remains permanently green, verified, and ready for packaging.
- **Eliminated CI Bottlenecks:** Pull requests validate in seconds, not 45+ minutes.
- **Meaningful Evaluation:** Complex skills are evaluated on models capable of multi-step reasoning (avoiding false-negative capacity floor failures).
- **Zero Host Pollution:** Local testing leverages rootless Podman containers or lightweight CLI invocations.
- **Transparent Evidence:** Empirical scores are visible on PR check pages and documented in version-controlled scorecards.

### Negative Consequences / Trade-offs
- **Two Branches to Manage:** Requires maintaining `dev` and executing promotion PRs to `main`.
- **Mitigation:** Automate promotion gating via release workflows and document clear branching rules in `.agents/AGENTS.md` and `docs/sops/`.

---

## Validation & Invariants

1. **Branch Target Invariant:** All pull requests from contributors or AI agents must target `dev` (enforced via PR templates and CI checks).
2. **Deterministic CI Invariant:** Tier 1 mock gate runs in < 5 seconds with zero external network or API key requirements on every PR.
3. **Step Summary Invariant:** When running in GitHub Actions, `scripts/eval_asset.py` appends a clean markdown scorecard table to `$GITHUB_STEP_SUMMARY`.
4. **Tool Neutrality Invariant:** Evaluation scripts require zero third-party pip dependencies beyond standard Python 3.11+.

---

## Revisit Conditions

This decision should be reconsidered if:
- GitHub Actions introduces free native GPU runners that eliminate the CPU inference bottleneck.
- Local quantized models (< 3B) achieve frontier-level instruction following on complex code refactoring.
