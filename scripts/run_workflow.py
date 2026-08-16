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


def run(workflow_id, outdir, execute=False):
    """Run a workflow and record a run log.

    By default the runner performs a simulation-only run (non-destructive). Set
    execute=True to allow the runner to mark steps as executed. Execution is
    intentionally conservative — destructive steps are disabled unless
    explicitly enabled by maintainers.
    """
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
        title = step.get("title")
        description = step.get("description")
        action = step.get("action", "noop")

        print(f"  Step {i}: {title}")
        print(f"    Description: {description}")

        # Default simulated step result
        step_result = {
            "index": i,
            "title": title,
            "description": description,
            "action": action,
            "status": "simulated",
        }

        # Conservative, non-destructive simulated execution by default.
        if execute:
            # Safe, curated handlers for common actions. All handlers are
            # intentionally non-destructive unless maintainers add approved
            # implementations.
            if action == "run_tests":
                # Do not actually run nested test discovery by default here;
                # maintainers can enable a real test runner in CI only.
                step_result.update({"status": "executed", "rc": 0, "output": "tests: simulated (disabled by default)"})
            elif action == "lint":
                step_result.update({"status": "executed", "rc": 0, "output": "lint: simulated (no files modified)"})
            elif action == "sanitize":
                step_result.update({"status": "executed", "rc": 0, "output": "sanitize: simulated"})
            elif action == "shell":
                step_result.update({"status": "executed", "rc": 0, "output": "shell: simulated (disabled)"})
            else:
                step_result.update({"status": "executed", "rc": 0, "output": "action executed (simulated)"})
        else:
            step_result["note"] = "simulation-only (pass execute=True to allow executed status)"

        result["steps"].append(step_result)

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
