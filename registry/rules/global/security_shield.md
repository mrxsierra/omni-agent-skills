---
trigger: always_on
---

# 🛡️ Global Security Shield & Agent Quality Rules (AgentShield)

These rules are enforced automatically across all sessions, workspaces, and subagents on this system.

## 1. Secret Protection & Leak Prevention
- **NEVER** output, log, or commit hardcoded secret keys, API tokens, passwords, private SSH keys, or credentials.
- **NEVER** expose `.env`, `.env.local`, `credentials.json`, `id_rsa`, or private tokens in file edits or git commits.
- All public examples and code snippets MUST use generic placeholders (`your-org`, `YOUR_API_KEY`).
- Run `scripts/sanitize.py` or local pre-tool hooks to verify no secret patterns exist before staging.

## 2. Staging-First & Non-Destructive Safety Protocol
- **Non-Destructive Operations:** NEVER execute destructive shell commands (`rm -rf`, `git reset --hard`, `git push --force`) without explicit human approval.
- **Staging-First Isolation:** When generating large or experimental new modules, draft them in isolated branches or scratch directories before integrating into production paths.
- **Atomic Commits:** Separate architectural changes, code refactors, and dependency updates into distinct, focused commits.

## 3. Empirically Verified Edits
- Editing a file does NOT equal task completion. Always run build, lint, or test commands (`python3 -m unittest discover`, `pytest`, `npm test`, `cargo test`) after changes to verify behavior.
- If a build or test fails, trace the root cause instead of silencing errors, commenting out assertions, or swallowing exceptions.
