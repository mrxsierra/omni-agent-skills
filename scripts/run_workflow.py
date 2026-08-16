#!/usr/bin/env python3
"""Simple workflow runner for omni-agent-skills example workflows.

Usage:
  python3 scripts/run-workflow.py --workflow workflow-id --outdir ./workflow-run-output

This is a minimal, local-first runner that prints the steps for a workflow and writes a simple log.
"""
import argparse
import json
import os
import sys
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOWS_DIR = os.path.join(REPO_ROOT, "workflows")


def load_workflow(workflow_id):
    path = os.path.join(WORKFLOWS_DIR, workflow_id, "workflow.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Workflow not found: {workflow_id}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run(workflow_id, outdir):
    wf = load_workflow(workflow_id)
    os.makedirs(outdir, exist_ok=True)
    log_path = os.path.join(outdir, f"{workflow_id}-{int(datetime.utcnow().timestamp())}.json")

    result = {
        "workflow_id": workflow_id,
        "name": wf.get("name"),
        "started_at": datetime.utcnow().isoformat() + "Z",
        "steps": [],
    }

    print(f"Running workflow: {workflow_id} - {wf.get('name')}")
    for i, step in enumerate(wf.get("steps", []), start=1):
        print(f"  Step {i}: {step.get('title')}")
        print(f"    Description: {step.get('description')}")
        # No execution semantics in MVP - just record the intended action
        result["steps"].append({
            "index": i,
            "title": step.get("title"),
            "description": step.get("description"),
            "action": step.get("action", "n/a"),
        })

    result["finished_at"] = datetime.utcnow().isoformat() + "Z"

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Workflow run recorded to: {log_path}")
    return log_path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--workflow", required=True)
    p.add_argument("--outdir", default="./workflow-run-output")
    args = p.parse_args()

    try:
        run(args.workflow, args.outdir)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
