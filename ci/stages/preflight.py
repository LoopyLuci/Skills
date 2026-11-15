"""preflight — environment, repository and tool checks that gate everything else."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from ..util import Finding, StageResult, git_out, human_bytes, load_config, repo_root


def _disk_free(path: Path) -> int:
    try:
        usage = shutil.disk_usage(path)
        return usage.free
    except Exception:
        return -1


def run(ctx: dict) -> StageResult:
    import time

    start = time.time()
    cfg = ctx["config"]
    findings: list[Finding] = []
    stats: dict = {}

    # --- python ---
    ver = sys.version_info
    stats["python"] = f"{ver.major}.{ver.minor}.{ver.micro}"
    major_minor = f"{ver.major}.{ver.minor}"
    req = str(cfg.get("min_python", "3.10"))
    if tuple(int(x) for x in major_minor.split(".")) < tuple(int(x) for x in req.split(".")):
        findings.append(Finding("P_PYTHON", "error", f"Python {major_minor} < required {req}"))

    root = repo_root()
    stats["root"] = str(root)

    # --- git ---
    branch = git_out(["rev-parse", "--abbrev-ref", "HEAD"])
    commit = git_out(["rev-parse", "HEAD"])
    stats["branch"] = branch
    stats["commit"] = commit[:12]
    if not commit:
        findings.append(Finding("P_GIT", "error", "not a git repository or git unavailable"))

    dirty = git_out(["status", "--porcelain"])
    stats["dirty_files"] = len([x for x in dirty.splitlines() if x.strip()])
    if dirty:
        findings.append(Finding("P_DIRTY", "info",
                                f"working tree has {stats['dirty_files']} uncommitted change(s)"))

    remote = git_out(["remote", "get-url", cfg.get("deploy_remote", "origin")])
    stats["remote"] = remote or "(none)"
    if not remote:
        findings.append(Finding("P_REMOTE", "warning", "no origin remote configured"))

    # --- disk ---
    free = _disk_free(root)
    stats["disk_free"] = human_bytes(free) if free > 0 else "unknown"
    if 0 < free < 2 * 1024 ** 3:
        findings.append(Finding("P_DISK", "error", f"less than 2 GB free ({human_bytes(free)})"))

    # --- repo size ---
    skills_dir = root / cfg["skills_dir"]
    stats["skills_dirs"] = sum(1 for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else 0
    if not skills_dir.is_dir():
        findings.append(Finding("P_SKILLS_DIR", "error", f"missing {cfg['skills_dir']}/ directory"))

    # --- tools ---
    tools = {}
    for tool in ("git", "ruff"):
        path = shutil.which(tool)
        tools[tool] = path or "(missing)"
        if tool == "git" and not path:
            findings.append(Finding("P_TOOL", "error", "git is required but not on PATH"))
    stats["tools"] = tools
    ctx["ruff_available"] = bool(shutil.which("ruff"))

    # --- config sanity ---
    try:
        load_config()
    except Exception as exc:  # pragma: no cover - config is committed
        findings.append(Finding("P_CONFIG", "error", f"cannot load ci/config.json: {exc}"))

    ok = not any(f.severity == "error" for f in findings)
    summary = (f"python {stats['python']}, branch {stats['branch']}@{stats['commit']}, "
               f"{stats['skills_dirs']} skills, {stats['disk_free']} free")
    return StageResult("preflight", ok, time.time() - start, summary, findings, stats)
