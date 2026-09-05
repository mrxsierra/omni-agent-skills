# ADR 0001: Keep the registry separate from the engineering control plane

## Status

Accepted — 2026-09-05

## Context

The project shares principles with a future Conductor-inspired engineering
control plane: explicit scope, disciplined workflows, verification, evidence,
and human approval. The two efforts were initially discussed together, which
created a risk of making this repository responsible for both a portable asset
catalog and an execution application.

## Decision

`omni-agent-skills` will remain a portable open-source registry. It publishes
reusable assets and the tooling needed to discover, validate, and install them.
The engineering control plane will be a separate project that may consume this
registry as a versioned dependency.

## Alternatives considered

- Build the control-plane runtime in this repository.
- Treat this repository as a collection of unstructured prompts.

## Consequences

The registry stays useful across multiple agent platforms and keeps a focused
release cycle. Runtime-specific worktree management, agent adapters, evidence
collection, and user interfaces remain outside its scope.

## Revisit conditions

Revisit only if maintaining two projects creates a concrete integration problem
that cannot be solved through versioned schemas, packages, or adapters.
