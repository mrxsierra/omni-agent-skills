import os
import shutil
import tempfile
import json
from pathlib import Path

from scripts.run_workflow import run


def test_run_pr_review_creates_log(tmp_path):
    outdir = tmp_path / "runs"
    outdir.mkdir()
    log = run("pr-review", str(outdir))
    assert os.path.exists(log)
    with open(log, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data['workflow_id'] == 'pr-review'
    assert 'steps' in data


def test_run_feature_plan_creates_log(tmp_path):
    outdir = tmp_path / "runs"
    outdir.mkdir()
    log = run("feature-plan", str(outdir))
    assert os.path.exists(log)
    with open(log, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data['workflow_id'] == 'feature-plan'


def test_run_security_audit_creates_log(tmp_path):
    outdir = tmp_path / "runs"
    outdir.mkdir()
    log = run("security-audit", str(outdir))
    assert os.path.exists(log)
    with open(log, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data['workflow_id'] == 'security-audit'
