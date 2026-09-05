# Contribution and feature delivery SOP

## Purpose

Use this procedure for every material change to the repository. It keeps work
scoped, reviewable, and traceable whether it is performed by a human or an AI
assistant.

## Procedure

1. **State intent.** Record the problem, expected outcome, scope, and
   non-goals in an issue, task description, or pull-request draft.
2. **Check the baseline.** Inspect the relevant documentation and code; confirm
   the working tree is clean and identify affected generated files.
3. **Create a branch from `main`.** Use one of `feat/`, `fix/`, `docs/`, or
   `chore/` followed by a concise name. Do not make material changes directly
   on `main`.
4. **Plan proportionately.** For significant changes, identify affected assets,
   compatibility risks, verification, and whether an ADR is required.
5. **Implement the smallest coherent change.** Keep unrelated cleanup out of
   the branch.
6. **Regenerate and verify.** Run the sanitizer, registry build, test suite,
   and any change-specific checks. Review the final diff.
7. **Document the result.** Update public documentation, an ADR, or a roadmap
   item when the change alters behavior, direction, or process.
8. **Commit and prepare review.** Use a focused conventional-style commit.
   The pull request states intent, scope, verification performed, risks, and
   follow-up work.

## Required local checks

```bash
python3 scripts/sanitize.py
python3 scripts/build-registry.py
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

## Pull-request checklist

- Scope and non-goals are clear.
- Generated registry files are current when registry assets changed.
- Relevant docs and ADRs are updated.
- Verification results are recorded.
- No secrets, credentials, or unrelated changes are included.
