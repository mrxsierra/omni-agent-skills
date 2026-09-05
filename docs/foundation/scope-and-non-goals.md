# Scope and non-goals

## In scope

- A versioned, machine-readable catalog of reusable agent-facing assets.
- Clear asset conventions, validation, discovery, and installation guidance.
- Engineering workflow and governance patterns that are useful across projects.
- Documentation and decision records for maintaining this open-source project.

## Out of scope for this repository

- A desktop application or hosted control plane.
- Git worktree provisioning, agent-session management, or autonomous delivery.
- General business, sales, finance, HR, or organization-management automation.
- A promise that an asset alone makes generated code production-ready.
- Unverified performance, security, or model-quality claims.

## Boundary test

An addition belongs here when it is a reusable, documented registry asset or
the infrastructure needed to publish it safely. It belongs in the future
control-plane project when it executes a task in a real workspace, manages an
agent, collects task evidence, or presents a delivery UI.
