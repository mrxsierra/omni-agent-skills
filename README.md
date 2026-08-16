# agent-validation-kit

A lightweight repository for AI-native developer workflows: a skill registry, schema/index files for AI discovery, guardrail scripts, and a minimal validation harness.

This project is best understood as a practical starter kit for repository-aware AI workflows, not as a benchmarked production AI platform with independently verified performance claims.

## What this repository contains

- A curated set of skill documents under [`skills/`](skills)
- Machine-readable indexes: [`registry.json`](registry.json) and [`llms.txt`](llms.txt)
- A small sanitization script for obvious secret-pattern scans: [`scripts/sanitize.py`](scripts/sanitize.py)
- A registry rebuild script: [`scripts/build-registry.py`](scripts/build-registry.py)
- A simple integrity test suite: [`tests/test_repo_integrity.py`](tests/test_repo_integrity.py)
- Local installation helpers: [`install.sh`](install.sh) and [`install.ps1`](install.ps1)

## Truthful status

This repository does not publish benchmark performance claims unless those claims are backed by a reproducible CI run with explicit golden data, raw outputs, and reviewable artifacts.

At the moment, the repo has:

- real registry generation logic,
- real helper scripts,
- a real test smoke check,
- and a real security guardrail pattern,

but it does not claim to have independently verified benchmark performance or a fully mature production benchmark suite in the checked-in codebase.

## Quick start

### Local usage

Clone the repo and inspect the skills directly:

```bash
git clone https://github.com/mrxsierra/agent-validation-kit.git
cd agent-validation-kit
ls skills
```

Then rebuild the machine-readable index if needed:

```bash
python3 scripts/build-registry.py
```

### Local install

If you want to copy the repo assets into a local directory for use with your own agent setup, review the script before running it.

Preferred: install from a pinned release tag (do not pipe remote scripts to a shell).

```bash
# clone a specific, pinned tag
git clone --depth 1 --branch vX.Y.Z https://github.com/mrxsierra/agent-validation-kit.git
cd agent-validation-kit
# verify a released tarball before extracting
curl -fsSL -o ./agent-validation-kit-vX.Y.Z.tar.gz \
  https://github.com/mrxsierra/agent-validation-kit/archive/refs/tags/vX.Y.Z.tar.gz
# compute and check the sha256 against the published checksum
sha256sum ./agent-validation-kit-vX.Y.Z.tar.gz
# or verify against a published checksum file
# echo "<expected-sha256>  agent-validation-kit-vX.Y.Z.tar.gz" | sha256sum -c -
```

If you must run the local helper, inspect `install.sh` first and prefer running it from a checked-out revision (or with `--local`). Avoid `curl | bash` one-liners; always pin a tag or verify checksums and signatures (see INSTALL.md for guidance).

## Validation commands

These are the repo’s current smoke checks:

```bash
python3 scripts/sanitize.py
python3 scripts/build-registry.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

These checks are useful hygiene and integrity checks, but they are not a substitute for a full benchmark evaluation harness with gold answers and independent verification.

## Skill areas included

- Engineering
  - [`system-architecture-planner`](skills/engineering/system-architecture-planner/SKILL.md)
  - [`atomic-feature-implementer`](skills/engineering/atomic-feature-implementer/SKILL.md)
  - [`pytest-verification-runner`](skills/engineering/pytest-verification-runner/SKILL.md)
  - [`clean-code-auditor`](skills/engineering/clean-code-auditor/SKILL.md)
  - [`code-anti-overengineer`](skills/engineering/code-anti-overengineer/SKILL.md)
  - [`semver-release-manager`](skills/engineering/semver-release-manager/SKILL.md)

- Web and GEO
  - [`ai-first-web-geo`](skills/web-and-geo/ai-first-web-geo/SKILL.md)
  - [`a11y-web-auditor`](skills/web-and-geo/a11y-web-auditor/SKILL.md)

- Data and AI
  - [`rag-qa-chunking-engine`](skills/data-and-ai/rag-qa-chunking-engine/SKILL.md)
  - [`ai-eval-benchmarker`](skills/data-and-ai/ai-eval-benchmarker/SKILL.md)

- Security and governance
  - [`secret-leak-shield`](skills/security-and-governance/secret-leak-shield/SKILL.md)
  - [`oss-launch-governance`](skills/security-and-governance/oss-launch-governance/SKILL.md)
  - [`tech-competitive-intelligence`](skills/security-and-governance/tech-competitive-intelligence/SKILL.md)
  - [`advanced-verification-testing`](skills/security-and-governance/advanced-verification-testing/SKILL.md)
  - [`ai-native-product-design`](skills/security-and-governance/ai-native-product-design/SKILL.md)

## Privacy and security

This repo has basic guardrails:

- generic secret regex patterns,
- a local sanitizer script,
- CI validation,
- and a recommended practice of avoiding personal data in repo content.

This is useful for local hygiene, but it is not a guarantee of zero leaks in all environments or all future changes. The sanitization logic is intentionally conservative and narrow.

See [`SECURITY.md`](SECURITY.md) for the current policy.

## License

Distributed under the [MIT License](LICENSE).
