# Roadmap

## Milestone 1: Repository operating foundation

Create the charter, scope boundary, governance, ADR practice, contribution SOP,
and project roadmap. Align repository documentation with this foundation.

## Milestone 2: Registry contract and usability

Define the published asset model: required metadata, compatibility declarations,
validation rules, and installation expectations. Establish the Three-Tier Agent
Discovery architecture (executable registry catalog in `registry/registry.json`,
LLM text sitemap in `llms.txt`, and semantic RAG Q&A retrieval in `llms-qa.json`).
Eliminate stale planning artifacts and resolve naming, versioning, and
documentation drift.

## Milestone 3: Reliable tooling, community health, and release automation

Harden registry generation and validation; ensure the test suite comprehensively
covers schemas, runner harnesses, and documented commands. Establish open-source
community health foundations (Code of Conduct, governance, issue and PR templates).
Implement standard release engineering with automated changelogs, tag-version
parity verification, and reproducible release workflows.

## Milestone 4: Curated catalog quality

Review existing assets for accurate scope, consistent terminology, composable
instructions, and truthful claims. Add assets only when they fill a demonstrated
gap.

## Later, separate project

A future engineering control plane may implement task contracts, worktrees,
agent adapters, evidence collection, approval gates, and a developer-facing UI.
It will consume registry releases rather than expanding this repository beyond
its charter.
