# Project documentation

This directory is the human-readable source of truth for how
`omni-agent-skills` is defined, governed, and evolved. It is deliberately
separate from `.agents/` (internal contributor instructions) and `registry/`
(the published catalog).

## Start here

- [Project charter](foundation/project-charter.md): purpose and intended users.
- [Scope and non-goals](foundation/scope-and-non-goals.md): current product
  boundary.
- [Principles](foundation/principles.md): durable engineering commitments.
- [Governance](governance/governance.md): authority and decision rules.
- [Decision records](adr/README.md): why significant choices were made.
- [Contribution and feature delivery SOP](sops/contribution-and-feature-delivery.md):
  how a change moves from intent to merge.
- [Roadmap](roadmap/roadmap.md): active milestones and future direction.

## Documentation lifecycle

Use a note or issue for exploration. Promote a conclusion to a document only
when it is useful project knowledge:

```text
exploration -> proposal -> decision/specification -> implementation -> evidence
```

Do not record unfiltered conversation transcripts as project truth. Capture the
decision, context, alternatives, and consequences instead.

## Repository layers

```text
docs/      durable human/project knowledge
.agents/   internal instructions for agents contributing to this repository
registry/  versioned assets published for users and compatible agent systems
```
