# 🛡️ Security Policy & Privacy Shield (AgentShield)

## 1. Zero Secret & Zero-PII Leak Commitment
**`omni-agent-skills`** strictly prohibits committing or publishing hardcoded API keys, private SSH keys, `.env` file entries, or personal metadata (PII).

All contribution files, skills, rules, and scaffolds MUST use generic parameter placeholders:
- `your-organization` / `your-username`
- `your-project` / `your-repository`
- `YOUR_API_KEY` / `YOUR_SECRET_TOKEN`

## 2. Automated CI Security Gate
Every commit and pull request is scanned by automated security workflows:
- **Gitleaks:** Scans git commits for hardcoded secrets.
- **Sanitizer Script (`scripts/sanitize.py`):** Rejects any file containing non-anonymized metadata.

## 3. Reporting Vulnerabilities
If you discover a potential security flaw or credential exposure in this repository, please notify the security maintainers immediately via GitHub Security Advisories.
