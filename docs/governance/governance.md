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
| Schema, compatibility, installation, security, or release change | ADR in `Proposed` status plus maintainer approval before merge |
| Major cross-agent protocol, multi-tool specification, or breaking wire format | RFC proposal (`docs/rfc/`), community review period, and consensus approval |
| Emergency security remediation | Maintainer may act immediately; document the decision and follow-up afterward |

## Decision rule

Use the smallest process that preserves clarity:
- A **pull request** explains *what* changed and validates that it works.
- An **ADR** explains *why* an internal architectural choice was chosen, what trade-offs were accepted, and what invariants must be enforced.
- An **RFC** invites collaborative feedback on *how* public interfaces, wire protocols, or cross-agent ecosystems should be specified before writing code.

## Source of truth

`docs/` contains durable project decisions and procedures. `.agents/` contains
internal execution instructions. `registry/` contains published assets. A
generated file must not become the only place where a material decision lives.
