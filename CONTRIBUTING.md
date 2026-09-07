# Contributing to omni-agent-skills

Thank you for considering contributions to this project. All contributors—whether human developers or AI agents—follow our formal [Contribution and Feature Delivery SOP](docs/sops/contribution-and-feature-delivery.md) and [ADR 0002](docs/adr/0002-unified-documentation-layering-and-autonomous-agent-sdlc.md). This guide provides a quick reference for local development commands, version management, and skill creation.

## Version Management

The repo uses a single `VERSION` file as the source of truth for all version numbers across configuration files.

### Current Version
Check the current version:
```bash
cat VERSION
```

### Bumping the Version
When you need to update the version (e.g., from `0.0.1` to `0.1.0`):

1. Run the update script with the new version:
```bash
python3 scripts/bump.py 0.1.0
```

2. Verify changes:
```bash
git diff
```

3. Stage and commit:
```bash
git add VERSION package.json pyproject.toml registry/registry.json
git commit -m "chore: bump version to 0.1.0"
```

The script updates:
- `VERSION` — source of truth
- `package.json` — npm metadata
- `pyproject.toml` — Python package metadata
- `registry/registry.json` — registry metadata

## Running Tests and Validation Suite

Before committing, run the repo's full verification suite:

```bash
python3 scripts/sanitize.py
python3 scripts/build_registry.py
python3 scripts/validate_registry.py
python3 scripts/manage_adr.py validate
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

Or in batch:
```bash
npm run sanitize
npm run build
npm run validate
npm run test
```

## Pre-commit Checks

The repo has a `.githooks/pre-commit` hook configured to run automatically before each commit. This runs:
- Sanitizer (secret pattern checks)
- Registry rebuild
- Smoke tests

To ensure these run, configure your Git hooks:
```bash
git config core.hooksPath .githooks
```

## Submitting Changes

1. Keep changes small and focused (one feature or fix per commit).
2. Follow the existing code style and directory structure.
3. Do not claim performance or benchmark wins without reproducible CI-backed evidence.
4. Update documentation if you add or modify skills.
5. Run tests and verify no regressions.
6. Write clear commit messages following the repo's existing convention.

## Published Asset Types & Architecture

Per [ADR 0003](docs/adr/0003-registry-asset-taxonomy-shipped-capabilities-and-inclusion-criteria.md) and [ARCHITECTURE.md](ARCHITECTURE.md), the repository publishes **eight concrete asset types** organized across two functional tiers:

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

---

## The 5-Gate Inclusion Filter

To prevent the registry from becoming an uncurated "prompt junkyard", every proposed asset must pass the mandatory **5-Gate Filter**:
1. **Gate 1 (Orthogonality & Single Purpose):** The asset addresses a distinct, recurring software engineering need without duplicating existing catalog capabilities.
2. **Gate 2 (Tool & Agent Neutrality):** Expressible in standard Markdown, JSON, POSIX shell, or standard Python. Does not require closed, vendor-locked agent SDKs.
3. **Gate 3 (Deterministic Verification Invariant):** Concrete, testable success criteria (e.g. reproducible test command, artifact format, schema check).
4. **Gate 4 (Canonical Contract Conformance):** Skills must implement all 4 required sections without omission:
   - `1. Inputs & Context Required`
   - `2. Step-by-Step Procedure`
   - `3. Expected Outputs & Verifiable Artifacts`
   - `4. Constraints & Tool Neutrality`
5. **Gate 5 (Zero-Secret, Zero-PII, Zero-Hype):** Passes `python3 scripts/sanitize.py` and contains zero unverified benchmark superlatives.

---

## Testing & Evaluating Assets Before Contribution

Per [ADR 0004](docs/adr/0004-multi-provider-asset-evaluation-and-delta-utility-bench.md), we do not accept assets on faith or subjective vibes. Every new skill, rule, or workflow must prove **positive empirical utility ($\Delta$-utility)** over a baseline model.

### 1. The 3-Tier Testing Pipeline

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

### 2. Running Local Asset Evaluations

You can test assets locally using whatever AI provider you prefer—including **Google Antigravity**, **free local Ollama**, **OpenAI/ChatGPT**, **Anthropic/Claude**, **OpenRouter**, or **offline Mock**:

```bash
# A. Google Antigravity / Gemini (via GEMINI_API_KEY):
python3 scripts/eval_asset.py --asset registry/skills/web-and-geo/a11y-web-auditor/SKILL.md \
                             --provider antigravity --model gemini-2.5-pro

# B. Local Ollama (100% free, private, offline):
python3 scripts/eval_asset.py --asset registry/skills/engineering/clean-code-auditor/SKILL.md \
                             --provider ollama --model qwen2.5-coder:7b

# C. OpenAI / ChatGPT (via OPENAI_API_KEY):
python3 scripts/eval_asset.py --asset registry/rules/global/security_shield.md \
                             --provider openai --model gpt-4o

# D. OpenRouter (multi-vendor comparison):
python3 scripts/eval_asset.py --asset registry/skills/data-and-ai/rag-qa-chunking-engine/SKILL.md \
                             --provider openrouter --model anthropic/claude-3.5-sonnet

# E. Offline CI Mock Gate (zero API keys):
python3 scripts/eval_asset.py --asset registry/skills/engineering/clean-code-auditor/SKILL.md \
                             --provider mock --strict
```

### 3. Adding an Evaluation Task Suite

When proposing a new skill or rule, include a matching task suite in [`evals/tasks/<domain>_<name>.json`](evals/tasks/):
```json
{
  "suite_id": "my_skill_eval",
  "domain": "engineering",
  "phase": "phase-4-implementation",
  "description": "Evaluates edge-case task completion with and without the skill",
  "target_asset": "registry/skills/engineering/my-skill/SKILL.md",
  "tasks": [
    {
      "id": "task-01",
      "name": "Targeted refactoring challenge",
      "user_prompt": "Audit the following code for...",
      "expected_keywords": ["must_contain_keyword"],
      "fail_keywords": ["prohibited_response"]
    }
  ]
}
```

An asset is **accepted** when $\Delta \text{Utility} > 0$ and the context token tax is proportional to value added.

### 4. Updating Existing Assets (A/B Regression Measurement)

When modifying or refactoring an existing published asset ($A_{\text{old}} \to A_{\text{new}}$), contributors must demonstrate **positive revision delta or token efficiency gains** without regression:

1. **Zero Regression Invariant:** $A_{\text{new}}$ must solve any new edge cases without breaking previously passing tasks ($\text{Regressions} = 0$).
2. **Improvement Metrics:**
   - **$\Delta\Delta$ Utility Gain:** $\Delta \text{Improvement} = \text{Score}(A_{\text{new}}) - \text{Score}(A_{\text{old}})$
   - **Token Economy Gain:** If the pass rate is unchanged, did $A_{\text{new}}$ reduce prompt verbosity and context token tax?
3. **Record Snapshot:** Update the baseline record in [`evals/baselines/<suite_id>.json`](evals/baselines/) with your latest benchmark numbers and paste the JSON summary into your PR description.

---

## Step-by-Step Asset Contribution Flow

1. Create a scoped branch: `git checkout -b feat/<asset-name>`.
2. Author the asset file adhering to its contract (e.g. 4-section runbook in `registry/skills/<domain>/<id>/SKILL.md`).
3. Add a matching evaluation task suite in `evals/tasks/`.
4. Rebuild the catalog and compile index files:
   ```bash
   python3 scripts/build_registry.py
   python3 scripts/validate_registry.py
   ```
5. Run the evaluation benchmark:
   ```bash
   # Test using your preferred provider (or mock for offline verification):
   python3 scripts/eval_asset.py --asset registry/skills/<domain>/<id>/SKILL.md --provider mock --strict
   ```
6. Run the complete local test suite:
   ```bash
   python3 scripts/sanitize.py
   python3 scripts/manage_adr.py validate
   python3 -m unittest discover -s tests -p 'test_*.py'
   git diff --check
   ```
7. Commit, push, and submit a Pull Request with the benchmark output recorded in your PR description.

---

## Architecture Decisions (ADRs & RFCs)

When proposing material architectural changes (such as modifying registry schemas, adding discovery tiers, adjusting installation scripts, or altering repository scope):

1. **Check existing records**: Review [`docs/adr/README.md`](docs/adr/README.md) to understand current invariants and prior trade-offs.
2. **Scaffold a new ADR**:
   ```bash
   npm run adr:new -- "Short Decision Title"
   # or: python3 scripts/manage_adr.py new "Short Decision Title"
   ```
3. **Fill in the record**: Complete the generated file under `docs/adr/XXXX-title.md` (Context, Decision Drivers, Considered Options, Decision Outcome, Consequences, and Invariants).
4. **Rebuild index & validate**:
   ```bash
   npm run adr:build
   npm run adr:validate
   ```
5. **RFCs for major public protocols**: For proposals involving multi-agent wire formats or cross-tool standards, scaffold an RFC via `python3 scripts/manage_adr.py new "Proposal Title" --rfc` and follow [`docs/rfc/README.md`](docs/rfc/README.md).

## Security and Secrets

Do not commit:
- API keys or tokens
- Private credentials
- Passwords or `.env` files with secrets
- Personally identifiable information (PII)

The sanitizer will warn about common patterns, but it is not a guarantee. Always review diffs before pushing.

## Questions?

If you have questions or need clarification, open an issue or contact the maintainers.

Thank you for contributing!
