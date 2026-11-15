"""Shared helpers for the local CI pipeline.

Stdlib only. Everything here is import-safe on Windows and in a bare
interpreter (no third-party packages required).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "ci" / "config.json"
LOCK_PATH = REPO_ROOT / "ci" / ".pipeline.lock"
REPORTS_DIR = REPO_ROOT / "ci" / "reports"
LOGS_DIR = REPO_ROOT / "ci" / "logs"
DIST_DIR = REPO_ROOT / "dist"


def load_config() -> dict[str, Any]:
    with CONFIG_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def repo_root() -> Path:
    return REPO_ROOT


def ensure_dirs() -> None:
    for d in (REPORTS_DIR, LOGS_DIR, DIST_DIR):
        d.mkdir(parents=True, exist_ok=True)


@dataclass
class Finding:
    code: str
    severity: str  # "error" | "warning" | "info"
    message: str
    path: str = ""

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "severity": self.severity,
                "message": self.message, "path": self.path}


@dataclass
class StageResult:
    name: str
    ok: bool
    duration: float
    summary: str = ""
    findings: list[Finding] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)
    skipped: bool = False
    flaky: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "ok": self.ok,
            "skipped": self.skipped,
            "duration_s": round(self.duration, 3),
            "summary": self.summary,
            "stats": self.stats,
            "flaky": self.flaky,
            "findings": [f.as_dict() for f in self.findings],
        }


def run_cmd(cmd: list[str], timeout: int | None = None, cwd: Path | None = None,
            env: dict[str, str] | None = None) -> tuple[int, str, str]:
    """Run a command with a hard timeout, killing the whole tree on expiry."""
    timeout = timeout or load_config().get("command_timeout", 600)
    merged = os.environ.copy()
    if env:
        merged.update(env)
    try:
        proc = subprocess.Popen(
            [str(c) for c in cmd],
            cwd=str(cwd or REPO_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=merged,
            creationflags=_creationflags(),
        )
    except FileNotFoundError:
        return 127, "", f"command not found: {cmd[0]}"
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        _kill_tree(proc)
        out, err = proc.communicate()
        return 124, out, err + f"\n[TIMEOUT after {timeout}s]"
    return proc.returncode, out, err


def _creationflags() -> int:
    if os.name != "nt":
        return 0
    # CREATE_NEW_PROCESS_GROUP so we can kill the whole tree cleanly.
    return getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)


def _kill_tree(proc: subprocess.Popen) -> None:
    if os.name == "nt":
        try:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=30)
            return
        except Exception:
            pass
    try:
        proc.kill()
    except Exception:
        pass


def git(args: list[str], timeout: int = 120) -> tuple[int, str, str]:
    return run_cmd(["git", *args], timeout=timeout)


def git_out(args: list[str], timeout: int = 120) -> str:
    rc, out, _ = git(args, timeout=timeout)
    return out.strip() if rc == 0 else ""


def changed_files(base_ref: str | None = None) -> list[str]:
    """Files changed in the working tree plus the diff range, best effort."""
    files: set[str] = set()
    # working tree (staged + unstaged + untracked)
    rc, out, _ = git(["status", "--porcelain"])
    if rc == 0:
        for line in out.splitlines():
            if len(line) > 3:
                files.add(line[3:].strip().strip('"'))
    # diff range against base
    ref = base_ref or _default_base()
    if ref:
        rc, out, _ = git(["diff", "--name-only", f"{ref}...HEAD"])
        if rc == 0:
            files.update(x for x in out.splitlines() if x.strip())
        rc, out, _ = git(["diff", "--name-only", ref])
        if rc == 0:
            files.update(x for x in out.splitlines() if x.strip())
    return sorted(files)


def _default_base() -> str | None:
    for cand in ("origin/main", "origin/master", "main", "master"):
        rc, _, _ = git(["rev-parse", "--verify", cand])
        if rc == 0:
            return cand
    return None


def human_bytes(n: int) -> str:
    step = 1024.0
    units = ["B", "KB", "MB", "GB", "TB"]
    val = float(n)
    for unit in units:
        if val < step or unit == units[-1]:
            return f"{val:.1f} {unit}"
        val /= step
    return f"{n} B"


def truncate(text: str, limit: int = 4000) -> str:
    text = text.rstrip()
    return text if len(text) <= limit else text[: limit - 3] + "..."


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


def safe_name(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
