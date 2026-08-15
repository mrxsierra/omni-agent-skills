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
python3 scripts/build-registry.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

## 4. Reporting concerns

If you discover a likely secret or a real risk in a checked-in file, report it privately to the maintainer or through an appropriate repository security contact before making it public.

## 5. Important caveat

The project is best treated as a small, helpful registry and guardrail repo, not as a fully verified zero-leak security system.
