# Security policy

This repository includes basic safety checks for obvious secret patterns, but it does not claim to be a full secret-scanning or security-auditing platform.

## 1. Expected practices

Contributors should avoid committing:

- API keys
- private SSH keys
- access tokens
- `.env` secrets
- personal or customer data

Use generic placeholders instead, such as:

- `your-org`
- `your-project`
- `YOUR_API_KEY`
- `YOUR_SECRET_TOKEN`

## 2. Current automated checks

The repo currently includes:

- `scripts/sanitize.py` for basic regex-based detection of common secret formats
- CI validation in `.github/workflows/ci.yml` that runs the sanitizer and smoke tests

This is useful local hygiene, but it is intentionally limited. It does not guarantee there are no secrets in all cases, and it does not replace a full secret scan, review process, or secure deployment pipeline.

## 3. Local reproducible checks

Run the repo’s current checks before publication or release:

```bash
python3 scripts/sanitize.py
python3 scripts/build_registry.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

## 4. Reporting concerns

If you discover a likely secret, vulnerability, or security risk in a checked-in file:

1. **GitHub Private Advisory (Preferred):** Submit a private report via [GitHub Security Advisories](https://github.com/mrxsierra/omni-agent-skills/security/advisories/new).
2. **Direct Maintainer Contact:** Email `9.sunilsharma@gmail.com` with details and reproduction steps.

Please do not open a public issue for sensitive security or credential exposure concerns until maintainers have reviewed and mitigated the issue. Reports will be acknowledged within 48 hours.

## 5. Important caveat

The project is best treated as a small, helpful registry and guardrail repo, not as a fully verified zero-leak security system.

## 6. Secure installation guidance

See INSTALL.md for the repository's secure installation and release verification guidance. In short:

- Prefer pinned-tag installs (don't install from `main` or via unpinned scripts).
- Verify SHA256 checksums and, where available, signatures (GPG or sigstore/cosign) before extracting or executing code.
- Do not run `curl | bash` on this project; instead download artifacts, verify them, then install locally.

Maintainers: publish checksum files and signatures with releases so users can validate artifacts before installation.
