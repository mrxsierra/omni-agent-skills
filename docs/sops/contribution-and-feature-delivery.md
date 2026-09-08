# Contribution and feature delivery SOP

## Purpose

Use this procedure for every material change to the repository. It keeps work
scoped, reviewable, and traceable whether it is performed by a human developer or
an AI assistant. See [ADR 0002](../adr/0002-unified-documentation-layering-and-autonomous-agent-sdlc.md)
for the underlying documentation layering and autonomous delivery architecture.

## Procedure

1. **State intent.** Record the problem, expected outcome, scope, and
   non-goals in an issue, task description, or pull-request draft.
2. **Check the baseline.** Inspect the relevant documentation and code; confirm
   the working tree is clean and identify affected generated files.
3. **Create a branch from `dev`.** Ensure `dev` is up to date (`git checkout dev && git pull origin dev`).
   Use one of `feat/`, `fix/`, `docs/`, or `chore/` followed by a concise name. Do not make material
   changes directly on `dev` or `main`.
4. **Plan proportionately.** For significant changes, identify affected assets,
   compatibility risks, verification, and whether an ADR is required. If required,
   scaffold an ADR using `python3 scripts/manage_adr.py new "<Title>"`.
5. **Implement the smallest coherent change.** Keep unrelated cleanup out of
   the branch.
6. **Regenerate and verify.** Run the sanitizer, registry build, ADR checks, test
   suite, and any change-specific checks. If modifying or adding registry assets, run
   `python3 scripts/eval_asset.py --asset <path> --provider mock --strict` to verify
   positive delta-utility. Review the final diff.
7. **Document the result.** Update public documentation, an ADR (via
   `python3 scripts/manage_adr.py build-index`), or a roadmap item when the change
   alters behavior, direction, or process.
8. **Commit and prepare review targeting `dev`.** Use a focused conventional-style commit.
   The pull request targets `dev` (`gh pr create --base dev`) stating intent, scope,
   verification performed, risks, and follow-up work.

## Required local checks

```bash
python3 scripts/sanitize.py
python3 scripts/build_registry.py
python3 scripts/validate_registry.py
python3 scripts/manage_adr.py validate
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

*For new or modified registry assets, verify positive delta-utility (delta auto-detected by default):*
```bash
python3 scripts/eval_asset.py --provider mock --strict
# Or evaluate a specific asset: python3 scripts/eval_asset.py --asset <path> --provider mock --strict
```

## Pull-request checklist

- Scope and non-goals are clear.
- Generated registry files are current when registry assets changed.
- Relevant docs and ADRs are updated and `manage_adr.py validate` passes.
- Empirical evaluation passes with positive delta-utility for added assets.
- Existing asset updates prove zero regressions and update snapshots in `evals/baselines/`.
- Verification results are recorded.
- No secrets, credentials, or unrelated changes are included.

---

## Release Promotion Gate (`dev` to `main`)

When promoting an accumulation of verified features from `dev` into a stable release on `main`:

1. **Tag Release Candidate on `dev`:**
   Tag the stabilized `dev` commit with `vX.Y.Z-rc.N` (e.g. `git tag v0.0.3-rc.1 && git push origin v0.0.3-rc.1`).
2. **Execute Full Matrix Verification:**
   Run the full catalog matrix evaluation across all assets:
   ```bash
   python3 scripts/eval_catalog_matrix.py --provider agy --model gemini-3.8-flash-high
   python3 scripts/build_eval_report.py --check
   ```
3. **Open Promotion PR Targeting `main`:**
   ```bash
   gh pr create --base main --head dev --title "release: promote dev to vX.Y.Z"
   ```
4. **Merge and Tag GA Release on `main`:**
   Once PR checks pass, merge into `main` and tag the official release:
   ```bash
   git checkout main && git pull origin main
   git tag vX.Y.Z && git push origin vX.Y.Z
   ```
   This triggers the automated release workflow (`.github/workflows/release.yml`) to publish release tarballs and release notes.
