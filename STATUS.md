Status: v0.0.1 (alpha)

What is present (this tag):

- registry/registry.json (generated from registry/skills/ by scripts/build-registry.py)
- llms.txt (generated summary)
- registry/skills/ documentation (SKILL.md files per skill)
- scripts/sanitize.py (regex-based secret/PII scanner)
- scripts/build-registry.py (machine index generator)
- tests/test_repo_integrity.py (smoke checks for registry and files)
- install.sh and install.ps1 (local install helpers that prefer local installs and pinned tags)

What is not included in this tag:

- A CI-executed benchmark harness that runs models, stores raw outputs, and scores them against golden answers. Any benchmark claim must be accompanied by a CI run id, raw artifacts, and signed checksums.
- Any signed release artifacts in this tag (maintainers must publish signed releases and checksums).
- A production-grade secret-scanning system; the sanitizer is a helpful but limited guardrail.

How to reproduce the registry:

1. Clone the repo at this tag

   git clone --depth 1 --branch v0.0.1 https://github.com/mrxsierra/omni-agent-skills.git

2. Run:

   python3 scripts/build-registry.py

3. Inspect registry/registry.json and llms.txt for the generated index and summary.

How to add verified benchmark evidence (future work):

- Implement a CI job that:
  - runs the model(s) in a reproducible container,
  - captures raw outputs to benchmarks/logs/<run-id>/,
  - compares outputs to golden answers using a documented metric,
  - stores a run manifest with commit SHA, container hash, and model/version metadata,
  - publishes results along with signed artifacts and raw logs.

FAQ

Q: Can I trust published benchmark claims?
A: Only if a claim references a reproducible CI run ID, signed artifacts (checksums/signatures), and raw output logs. Without these, treat benchmark claims as unverified.

Q: Is this repo safe to use?
A: The repository provides useful starter tooling and registry scaffolding. It includes basic sanitization and smoke checks, but users should not assume a zero-leak guarantee or that benchmark claims have been validated.
