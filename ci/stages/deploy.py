"""deploy — verify the remote and record a deploy receipt; optional push.

Never pushes unless --push is passed and the tree is clean.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from ..util import (Finding, StageResult, ensure_dirs, git_out, load_config,
                    repo_root, run_cmd)


def run(ctx: dict) -> StageResult:
    start = time.time()
    cfg = ctx["config"]
    root = repo_root()
    ensure_dirs()
    findings: list[Finding] = []
    stats: dict = {}

    remote = cfg.get("deploy_remote", "origin")
    branch = cfg.get("deploy_branch", "main")

    rc, out, err = run_cmd(["git", "ls-remote", "--heads", remote, branch], timeout=120)
    reachable = rc == 0 and bool(out.strip())
    stats["remote_reachable"] = reachable
    if not reachable:
        findings.append(Finding("D_REMOTE", "error",
                                f"cannot reach {remote}/{branch}: {(err or '').strip()[:300]}"))

    local_sha = git_out(["rev-parse", "HEAD"])
    remote_sha = git_out(["ls-remote", "--heads", remote, branch]).split()[0] if reachable else ""
    stats["local_sha"] = local_sha[:12]
    stats["remote_sha"] = remote_sha[:12] if remote_sha else "(unknown)"

    dirty = git_out(["status", "--porcelain"])
    stats["dirty_files"] = len([x for x in dirty.splitlines() if x.strip()])

    pushed = False
    if ctx.get("push"):
        if dirty:
            findings.append(Finding("D_DIRTY", "error",
                                    "refusing to push with uncommitted changes"))
        elif not reachable:
            findings.append(Finding("D_REMOTE", "error", "refusing to push: remote unreachable"))
        else:
            rc, out, err = run_cmd(["git", "push", remote, f"HEAD:{branch}"], timeout=600)
            pushed = rc == 0
            if not pushed:
                findings.append(Finding("D_PUSH", "error",
                                        f"push failed: {(err or out).strip()[:400]}"))
    stats["pushed"] = pushed

    receipt = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
        "remote": remote,
        "branch": branch,
        "local_sha": local_sha,
        "remote_sha": remote_sha,
        "dirty_files": stats["dirty_files"],
        "pushed": pushed,
        "index": ctx.get("index_path"),
        "archive": ctx.get("archive_path"),
        "stages": [r.name for r in ctx.get("results", [])],
    }
    (root / "dist" / "deploy-receipt.json").write_text(json.dumps(receipt, indent=2),
                                                       encoding="utf-8")
    stats["receipt"] = "dist/deploy-receipt.json"

    ok = not any(f.severity == "error" for f in findings)
    summary = (f"remote {remote}/{branch} "
               + ("reachable" if reachable else "UNREACHABLE")
               + f", local {stats['local_sha']} vs remote {stats['remote_sha']}"
               + (", pushed" if pushed else ", not pushed"))
    return StageResult("deploy", ok, time.time() - start, summary, findings, stats)
