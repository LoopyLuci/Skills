"""static — compile, lint, secret scan, size and JSON validity.

Scopes scans to the working tree (tracked + untracked, respecting .gitignore),
never the historical diff range, so removed build artifacts cannot fail a run.

Severity policy:
  ci/ and tests/      -> strict (errors)
  scripts/            -> warnings (legacy utilities; real bugs still surfaced)
  skills/             -> warnings/info (content, not first-party code)
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

from ..util import (Finding, StageResult, git_out, human_bytes, load_config,
                    repo_root, run_cmd)

TEXT_SCAN_LIMIT = 8 * 1024 * 1024
STRICT_PREFIXES = ("ci/", "tests/")
SCRIPTS_PREFIX = "scripts/"


def _working_tree_files() -> list[Path]:
    out = git_out(["ls-files", "--cached", "--others", "--exclude-standard"])
    root = repo_root()
    return [root / line for line in out.splitlines() if line.strip()]


def _severity_for(rel: str, base: str) -> str:
    """Promote to error only for first-party pipeline code."""
    if rel.startswith(STRICT_PREFIXES):
        return "error"
    return base


def _ignored(match_text: str, markers: list[str]) -> bool:
    low = match_text.lower()
    return any(marker in low for marker in markers)


_ENV_CONST = re.compile(r"^[A-Z_][A-Z0-9_]{7,}$")
_CODE_CHARS = set(" \t\r\n()=${}<>")


def _code_like(match_text: str) -> bool:
    """Filter out env-var names and code that merely looks like an assignment."""
    values = re.findall(r"['\"]([^'\"]+)['\"]", match_text)
    if not values:
        return True
    for value in values:
        if _ENV_CONST.match(value):
            return True
        if any(ch in _CODE_CHARS for ch in value):
            return True
    return False


def run(ctx: dict) -> StageResult:
    start = time.time()
    cfg = ctx["config"]
    root = repo_root()
    findings: list[Finding] = []
    stats: dict = {"files_scanned": 0, "python_files": 0}

    files = _working_tree_files()
    stats["working_tree_files"] = len(files)

    # --- compileall ---
    targets = [str(p) for p in ("ci", "scripts", "tests", "generate_skills.py") if (root / p).exists()]
    if targets:
        rc, out, err = run_cmd(["python", "-m", "compileall", "-q", *targets], timeout=300)
        if rc != 0:
            findings.append(Finding("S_COMPILE", "error",
                                    f"compileall failed: {(err or out).strip()[:500]}"))
        else:
            stats["compileall"] = "ok"

    # --- ruff ---
    if ctx.get("ruff_available"):
        for target, base in (("ci tests", "error"), ("scripts", "warning")):
            rc, out, err = run_cmd(
                ["ruff", "check", "--select", cfg["ruff_select"], "--output-format", "concise",
                 *target.split()],
                timeout=300)
            lines = [ln for ln in (out or "").splitlines()
                     if ln.strip() and "All checks passed" not in ln]
            stats[f"ruff_{target.replace(' ', '_')}"] = len(lines)
            for ln in lines[:60]:
                findings.append(Finding("S_RUFF", _severity_for(target, base), ln))
            if rc != 0 and not lines:
                findings.append(Finding("S_RUFF", "error",
                                        f"ruff failed on {target}: {(err or '').strip()[:400]}"))
    else:
        stats["ruff"] = "not installed (skipped)"

    # --- per-file checks ---
    high_patterns = [(re.compile(p), p) for p in cfg.get("secret_patterns", [])]
    assign_patterns = [(re.compile(p), p) for p in cfg.get("secret_assignment_patterns", [])]
    code_exts = set(cfg.get("secret_code_extensions", []))
    ignore_markers = [m.lower() for m in cfg.get("secret_ignore_markers", [])]
    bare_except = re.compile(r"^\s*except\s*:")
    max_bytes = int(cfg["max_file_mb"]) * 1024 * 1024
    big: list[str] = []
    secrets: list[tuple[str, str]] = []
    bare: list[tuple[str, int, str]] = []
    bad_json: list[str] = []
    scanned = 0

    for path in files:
        if not path.is_file():
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        rel = str(path.relative_to(root)).replace("\\", "/")
        if size > max_bytes:
            big.append(f"{rel} ({human_bytes(size)})")
            continue
        if path.suffix == ".py":
            stats["python_files"] += 1
        if size > TEXT_SCAN_LIMIT:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        scanned += 1

        if path.suffix == ".py":
            for i, line in enumerate(text.splitlines(), 1):
                if bare_except.match(line):
                    sev = "error" if rel.startswith(STRICT_PREFIXES + (SCRIPTS_PREFIX,)) else "warning"
                    bare.append((rel, i, sev))
        if path.suffix == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                bad_json.append(f"{rel}: {exc.msg} (line {exc.lineno})")

        base_sev = "error" if rel.startswith(STRICT_PREFIXES) else "warning"
        for pattern, label in high_patterns:
            m = pattern.search(text)
            if m and not _ignored(m.group(0), ignore_markers):
                secrets.append((f"{rel}: matched {label[:40]}", base_sev))
        if path.suffix.lower() in code_exts:
            for pattern, _label in assign_patterns:
                m = pattern.search(text)
                if m and not _ignored(m.group(0), ignore_markers) and not _code_like(m.group(0)):
                    secrets.append((f"{rel}: possible credential assignment", base_sev))

    stats["files_scanned"] = scanned
    stats["big_files"] = len(big)
    stats["secrets"] = len(secrets)
    stats["bare_except"] = len(bare)
    stats["bad_json"] = len(bad_json)

    for item in big[:20]:
        findings.append(Finding("S_BIG_FILE", "warning", f"file exceeds size cap: {item}"))
    for message, severity in secrets[:30]:
        findings.append(Finding("S_SECRET", severity, f"possible secret: {message}"))
    for rel, line, severity in bare[:30]:
        findings.append(Finding("S_BARE_EXCEPT", severity, f"bare except at {rel}:{line}"))
    for item in bad_json[:20]:
        findings.append(Finding("S_BAD_JSON", "error", f"invalid JSON: {item}"))

    ok = not any(f.severity == "error" for f in findings)
    summary = (f"{stats['working_tree_files']} working-tree files, "
               f"{stats['python_files']} python, "
               f"{stats.get('ruff_ci_tests', 0)} ruff errors (ci/tests), "
               f"{stats.get('ruff_scripts', 0)} ruff warnings (scripts), "
               f"{len(secrets)} secret hits, {len(bare)} bare excepts, "
               f"{len(bad_json)} bad JSON")
    return StageResult("static", ok, time.time() - start, summary, findings, stats)
