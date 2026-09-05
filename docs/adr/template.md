# ADR {NUMBER}: {TITLE}

## Status

Proposed — {YYYY-MM-DD}

## Deciders

{LIST_OF_DECIDERS}

## Context & Problem Statement

{Describe the context, requirements, and problem that necessitates an architectural decision. What is the scope, and why does it matter to the project?}

## Decision Drivers

- Driver 1: {e.g., Zero external runtime dependencies}
- Driver 2: {e.g., Strict schema validation in CI}
- Driver 3: {e.g., Tool neutrality across diverse AI agent platforms}

## Considered Options

- **Option 1**: {Title of Option 1}
- **Option 2**: {Title of Option 2}
- **Option 3**: {Title of Option 3}

## Decision

Chosen option: **"{Option X}"**, because:
- {Rationale 1}
- {Rationale 2}

## Consequences

### Positive Consequences
- {Positive consequence 1: e.g., Preserves reproducible, deterministic catalog builds}
- {Positive consequence 2: e.g., Low memory footprint and instant startup}

### Negative Consequences / Trade-offs
- {Trade-off 1: e.g., Requires manual skill indexing}
- {Mitigation for trade-off 1: e.g., Automated by scripts/build_registry.py}

## Pros and Cons of Options

### Option 1: {Option 1 Title}
- Good, because {reason a}
- Bad, because {reason b}

### Option 2: {Option 2 Title}
- Good, because {reason a}
- Bad, because {reason b}

## Validation & Invariants

- {How will we verify this decision remains valid over time?}
- {What automated tests or lint checks enforce this invariant in CI?}

## Revisit Conditions

- {Under what concrete conditions should this decision be reconsidered or superseded?}
