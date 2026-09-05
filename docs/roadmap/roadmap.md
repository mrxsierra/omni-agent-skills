# Roadmap

## Milestone 1: Repository operating foundation

Create the charter, scope boundary, governance, ADR practice, contribution SOP,
and project roadmap. Align repository documentation with this foundation.

## Milestone 2: Registry contract and usability

Define the published asset model: required metadata, compatibility declarations,
discovery behavior, validation rules, and installation expectations. Repair
current naming, versioning, and command/documentation drift.

## Milestone 3: Reliable registry tooling

Harden registry generation and validation; add tests for schemas, generated
output, and documented commands. Keep the workflow runner a safe reference
harness unless the project explicitly adopts additional execution scope.

## Milestone 4: Curated catalog quality

Review existing assets for accurate scope, consistent terminology, composable
instructions, and truthful claims. Add assets only when they fill a demonstrated
gap.

## Later, separate project

A future engineering control plane may implement task contracts, worktrees,
agent adapters, evidence collection, approval gates, and a developer-facing UI.
It will consume registry releases rather than expanding this repository beyond
its charter.
