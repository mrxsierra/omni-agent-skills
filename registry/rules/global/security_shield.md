---
trigger: always_on
---

# 🛡️ Global Security Shield & Agent Quality Rules (AgentShield)

These rules are enforced automatically across all sessions, workspaces, and subagents on this system.

## 1. Secret Protection & Leak Prevention
- **NEVER** output, log, or commit hardcoded secret keys, API tokens, passwords, private SSH keys, or credentials.
- **NEVER** expose `.env`, `.env.local`, `credentials.json`, `id_rsa`, or private tokens in file edits or git commits.
- All public examples and code snippets MUST use generic placeholders (`your-org`, `YOUR_API_KEY`).

## 2. Staging-First Safety Protocol
- All generated social media posts (LinkedIn, X/Twitter, Reddit, Medium) MUST be written to `drafts/posts/`.
- All outbound pitch drafts and outreach emails MUST be written to `drafts/pitches/`.
- **NEVER** publish, post, or send outbound messages directly without explicit human review and 1-click user approval.

## 3. Empirically Verified Edits
- Editing a file does NOT equal task completion. Always run build, lint, or test commands (`pytest`, `npm test`, `cargo test`) after changes to verify zero regressions.
- If a build or test fails, trace the root cause instead of silencing errors or swallowing exceptions.
