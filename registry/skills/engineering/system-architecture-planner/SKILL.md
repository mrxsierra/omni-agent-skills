---
name: system-architecture-planner
description: Analyzes system requirements, evaluates codebase dependencies, formulates architecture specifications, and scopes atomic implementation tasks.
---

# 📐 System Architecture & Implementation Planner

The **System Architecture Planner** analyzes requirements, maps dependencies, drafts architectural specifications (ADRs, implementation plans), and scopes implementation tasks before code changes begin.

## 1. Inputs & Context Required
- **Requirement Source:** Feature request, user prompt, bug report, or system enhancement specification.
- **Repository Architecture:** Directory structure, dependency graph, existing ADRs, and boundary documentation (`docs/foundation/`).
- **Target Deliverables:** Scope of work (ADR, RFC, `implementation_plan.md`, or task breakdown).

## 2. Step-by-Step Procedure
1. **Scope & Boundary Analysis:** Identify functional goals, non-functional requirements, architectural constraints, and explicit non-goals.
2. **Dependency & System Inspection:** Review relevant modules, configuration files, and dependencies to avoid introducing redundant abstractions.
3. **Architecture Specification Drafting:** Document architectural context, decision rationale, trade-offs, and consequences in an ADR or implementation plan.
4. **Atomic Task Decomposition:** Break down complex milestones into granular, self-contained implementation steps with explicit verification criteria.
5. **Verification Plan Design:** Define automated tests, command checks, and manual validations for each step.

## 3. Expected Outputs & Artifacts
- **Implementation Plan / Spec:** Structured document outlining technical context, proposed changes per file, and verification commands.
- **Task Checklist:** Ordered, actionable task items suitable for autonomous or paired execution.

## 4. Constraints & Tool Neutrality
- **Non-Mutating Phase:** During the planning phase, inspect and analyze without editing production source code.
- **Scope Discipline:** Adhere to established project boundaries and architectural principles.
- **Tool Neutral:** Compatible with any planning framework, markdown workflow, or agent orchestration tool.
