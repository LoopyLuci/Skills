"""skills — parallel validation of every skill directory.

Rules live in ci/skillcheck.py so the unit tests can exercise them directly.
"""

from __future__ import annotations

import json
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from ..util import (Finding, StageResult, git_out, load_config, repo_root)
from ..skillcheck import scan_worker


def _repo_files(root: Path) -> set[str]:
    out = git_out(["ls-files", "--cached", "--others", "--exclude-standard"])
    return {line.replace("\\", "/") for line in out.splitlines() if line.strip()}


def _adapted_map(root: Path, cfg: dict) -> dict[str, str]:
    """skill name -> upstream relative path (for overlap checks)."""
    adapted: dict[str, str] = {}
    worklist = root / "scripts" / "customization-worklist.json"
    if worklist.exists():
        try:
            data = json.loads(worklist.read_text(encoding="utf-8"))
            for entry in data.get("skills", []):
                adapted[entry["name"]] = entry["upstream_path"]
        except Exception:
            pass
    return adapted


def run(ctx: dict) -> StageResult:
    start = time.time()
    cfg = ctx["config"]
    root = repo_root()
    skills_dir = root / cfg["skills_dir"]
    only = ctx.get("only_changed_skills")

    dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir())
    if only:
        wanted = set(only)
        dirs = [d for d in dirs if d.name in wanted]

    known_names = {d.name for d in skills_dir.iterdir() if d.is_dir()}
    sources_dir = root / cfg["source_dir"]
    worker_ctx = {
        "config": cfg,
        "known_names": known_names,
        "adapted": _adapted_map(root, cfg),
        "sources_dir": sources_dir if sources_dir.is_dir() else None,
        "repo_files": _repo_files(root),
    }

    jobs = max(1, min(int(cfg.get("jobs", 8)), len(dirs) or 1))
    results: list[tuple[str, list[dict], dict]] = []
    if dirs:
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            payloads = [(str(d), worker_ctx) for d in dirs]
            for out in pool.map(scan_worker, payloads, chunksize=64):
                results.append(out)

    findings: list[Finding] = []
    metas: dict[str, dict] = {}
    for name, raw_findings, meta in results:
        metas[name] = meta
        for f in raw_findings:
            findings.append(Finding(f["code"], f["severity"], f["message"],
                                    f.get("path") or name))

    # cross-skill duplicate detection
    by_hash: dict[str, str] = {}
    by_sig: dict[tuple[str, str], str] = {}
    dup_body = dup_sig = 0
    for name, meta in metas.items():
        h = meta.get("hash", "")
        if h:
            if h in by_hash:
                findings.append(Finding("E_DUP_BODY", "warning",
                                        f"body identical to {by_hash[h]}", name))
                dup_body += 1
            else:
                by_hash[h] = name
        sig = (meta.get("title", ""), meta.get("description", ""))
        if sig[0] or sig[1]:
            if sig in by_sig:
                findings.append(Finding("E_DUP_DESC", "warning",
                                        f"title+description identical to {by_sig[sig]}", name))
                dup_sig += 1
            else:
                by_sig[sig] = name

    sev = Counter(f.severity for f in findings)
    codes = Counter(f.code for f in findings)
    stats = {
        "skills_checked": len(dirs),
        "jobs": jobs,
        "errors": sev.get("error", 0),
        "warnings": sev.get("warning", 0),
        "info": sev.get("info", 0),
        "duplicate_bodies": dup_body,
        "duplicate_descriptions": dup_sig,
        "by_code": dict(codes.most_common(20)),
    }

    limit = int(cfg.get("max_findings_per_stage", 200))
    truncated = max(0, len(findings) - limit)
    if truncated:
        findings = findings[:limit]

    ok = sev.get("error", 0) == 0
    summary = (f"{len(dirs)} skills checked on {jobs} workers: "
               f"{sev.get('error', 0)} errors, {sev.get('warning', 0)} warnings"
               + (f" ({truncated} more suppressed)" if truncated else ""))
    return StageResult("skills", ok, time.time() - start, summary, findings, stats)
