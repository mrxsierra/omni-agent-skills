## Summary

<!-- Provide a concise description of what this PR accomplishes. -->

## Intent & Context

<!-- Explain why this change is needed and what problem it solves. -->

## Scope & Non-Goals

- **In Scope:** <!-- What is explicitly included in this PR -->
- **Out of Scope:** <!-- What is intentionally left for future work -->

---

## Required Local Verification

Before submitting, verify that all local checks have run and passed:

```bash
python3 scripts/sanitize.py
python3 scripts/build_registry.py
python3 scripts/validate_registry.py
python3 scripts/manage_adr.py validate
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

- [ ] `scripts/sanitize.py` passed (no secrets or sensitive patterns)
- [ ] `scripts/build_registry.py` rebuilt `registry.json` and `llms.txt` (if skills changed)
- [ ] `scripts/validate_registry.py` passed
- [ ] `scripts/manage_adr.py validate` passed (if ADRs/RFCs touched)
- [ ] All unit and smoke tests passed (`unittest discover`)
- [ ] `git diff --check` passed with no whitespace errors

---

## Pull Request Checklist

- [ ] My change follows the [Contribution and Feature Delivery SOP](docs/sops/contribution-and-feature-delivery.md).
- [ ] Any material architectural changes include an ADR (`docs/adr/`) in `Proposed` status.
- [ ] No personal credentials, tokens, or `.env` files are included.
- [ ] Documentation (`README.md`, `ARCHITECTURE.md`, or relevant skill docs) has been updated.
