"""smoke — prove the build artifacts actually work, not just exist."""

from __future__ import annotations

import json
import random
import time
import zipfile
from pathlib import Path

from ..skillcheck import parse_frontmatter
from ..util import Finding, StageResult, load_config, repo_root


def run(ctx: dict) -> StageResult:
    start = time.time()
    cfg = ctx["config"]
    root = repo_root()
    findings: list[Finding] = []
    stats: dict = {}

    index_path = root / "dist" / "skills-index.json"
    if not index_path.exists():
        return StageResult("smoke", False, time.time() - start,
                           "no index to smoke-test (run build first)")

    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        findings.append(Finding("M_INDEX", "error", f"index is not valid JSON: {exc}"))
        return StageResult("smoke", False, time.time() - start, "index unreadable", findings)

    entries = payload.get("skills", [])
    names = [e.get("name") for e in entries]
    skills_dir = root / cfg["skills_dir"]
    actual = {p.name for p in skills_dir.iterdir() if p.is_dir()}

    stats["index_count"] = len(entries)
    stats["dir_count"] = len(actual)
    if len(entries) != len(actual):
        findings.append(Finding("M_COUNT", "error",
                                f"index has {len(entries)} skills but {len(actual)} directories exist"))
    if len(set(names)) != len(names):
        findings.append(Finding("M_DUP", "error", "index contains duplicate names"))
    missing_meta = [n for n in names if not n]
    if missing_meta:
        findings.append(Finding("M_META", "error", f"{len(missing_meta)} index entries lack a name"))

    # sample: real files parse
    sample = random.sample(names, min(50, len(names)))
    unparsable = []
    for name in sample:
        f = skills_dir / name / "SKILL.md"
        try:
            parse_frontmatter(f.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            unparsable.append(name)
    stats["sampled"] = len(sample)
    if unparsable:
        findings.append(Finding("M_PARSE", "error",
                                f"{len(unparsable)} sampled SKILL.md files do not parse: "
                                f"{', '.join(unparsable[:10])}"))

    # archive integrity
    archive_path = ctx.get("archive_path")
    if archive_path and Path(archive_path).exists():
        try:
            with zipfile.ZipFile(archive_path) as zf:
                bad = zf.testzip()
                names_in = set(zf.namelist())
                stats["archive_entries"] = len(names_in)
                if bad:
                    findings.append(Finding("M_ARCHIVE", "error", f"archive corrupt at {bad}"))
                if not any(n.startswith("skills/") for n in names_in):
                    findings.append(Finding("M_ARCHIVE", "error", "archive has no skills/ entries"))
        except zipfile.BadZipFile:
            findings.append(Finding("M_ARCHIVE", "error", "archive is not a valid zip"))
    else:
        stats["archive"] = "not built"

    ok = not any(f.severity == "error" for f in findings)
    summary = (f"index {stats['index_count']} skills, sampled {stats['sampled']} parse clean"
               + (f", archive {stats.get('archive_entries', 0)} entries ok"
                  if stats.get("archive_entries") else ""))
    return StageResult("smoke", ok, time.time() - start, summary, findings, stats)
