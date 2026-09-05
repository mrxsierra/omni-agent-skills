# Request for Comments (RFC) Process

The Request for Comments (RFC) process provides a structured, collaborative mechanism for proposing and discussing major cross-cutting changes to `omni-agent-skills` before code implementation begins.

---

## 1. When is an RFC Required?

Use an **RFC** when proposing:
1. **Public Protocol Changes**: Cross-agent communication standards, tool capability negotiation, or cross-platform execution formats.
2. **Major Breaking Schema Changes**: Fundamental modifications to published contracts (`spec_version: 2.0`) consumed by third-party agents (e.g. Cursor, Claude Code, Antigravity, OpenCode).
3. **Major Multi-File Subsystems**: Large-scale extensions (e.g. new asset classes, multi-agent orchestration specifications) that require consensus across multiple external maintainers and stakeholders.

> [!NOTE]
> For internal architectural choices, single-component refactors, and repository hygiene, use an **[ADR (Architecture Decision Record)](../adr/README.md)** instead.

---

## 2. RFC Lifecycle States

```text
  [Draft] ──► [Under Review] ──► [Approved] ──► [Implemented]
                   │
                   ├──► [Deferred]
                   ├──► [Withdrawn]
                   └──► [Rejected]
```

- **`Draft`**: Work in progress by the author; not yet open for broad consensus.
- **`Under Review`**: Open for community discussion, feedback, and maintainer evaluation (standard minimum 14-day review window).
- **`Approved`**: Reached consensus; ready for implementation in an upcoming release.
- **`Implemented`**: The specification has been coded, verified in CI, and released.
- **`Deferred`**: Valued proposal postponed for a future milestone roadmap.
- **`Withdrawn`**: Withdrawn by the author.
- **`Rejected`**: Declined due to scope boundaries, security constraints, or unmitigated complexity.

---

## 3. How to Submit an RFC

1. **Scaffold a new RFC**:
   ```bash
   python3 scripts/manage_adr.py new "Proposal Title" --rfc
   ```
2. **Fill out the template**: Complete all required sections in [`template.md`](template.md) (Motivation, Goals & Non-Goals, Detailed Specification, Backward Compatibility, and Open Questions).
3. **Open a Pull Request**: Submit a PR titled `RFC: <Proposal Title>` with status `Draft` or `Under Review`.
4. **Gather Feedback**: Address stakeholder comments, revise design alternatives, and update unresolved questions.
5. **Approval**: Once consensus is reached, maintainers mark the RFC as `Approved` and track implementation in the [Project Roadmap](../roadmap/roadmap.md).
