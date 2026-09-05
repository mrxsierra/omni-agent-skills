# Governance

## Maintainer responsibility

Maintainers protect the project charter, review public-facing changes, and
ensure releases remain truthful and reproducible. Contributors may propose any
change through the normal contribution process.

## Decision categories

| Change type | Required record and review |
| --- | --- |
| Documentation correction or small asset fix | Focused pull request and one maintainer review |
| New registry asset or workflow | Scope statement, validation, and one maintainer review |
| Schema, compatibility, installation, security, or release change | ADR plus maintainer approval before merge |
| Emergency security remediation | Maintainer may act immediately; document the decision and follow-up afterward |

## Decision rule

Use the smallest process that preserves clarity. A pull request explains *what*
changed. An ADR explains *why* a consequential decision was chosen and what
trade-offs it creates.

## Source of truth

`docs/` contains durable project decisions and procedures. `.agents/` contains
internal execution instructions. `registry/` contains published assets. A
generated file must not become the only place where a material decision lives.
