# Project charter

## Mission

`omni-agent-skills` is an open-source, tool-neutral registry of reusable
engineering capabilities and governance assets for AI-assisted software work.
It helps compatible agent systems retrieve focused guidance when it is needed
instead of carrying every instruction in their default context.

## The problem

AI coding tools can produce changes quickly, but a project still needs clear
scope, safe constraints, repeatable procedures, and independently checkable
results. Repositories often encode this knowledge inconsistently or only in
chat history, which makes it difficult for people and agents to work reliably.

## What we publish

The registry may publish skills, rules, workflow templates, SOP templates,
subagent-role definitions, prompts, hooks, snippets, and integration templates.
Each asset should be narrow, composable, truthful about its guarantees, and
useful outside this repository.

## Intended users

- Developers and maintainers using AI coding agents.
- Agent platforms that can discover and selectively load registry assets.
- Open-source projects that want reusable engineering and governance patterns.

## Relationship to the future engineering control plane

This project is a portable knowledge and capability library. A future,
separate engineering control-plane application may consume a versioned release
of this registry to select skills, policies, and workflow templates for a
specific task. That application is not implemented or owned by this repository.
