"""build — generate the machine-readable skills index and a release archive."""

from __future__ import annotations

import json
import re
import time
import zipfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from ..util import Finding, StageResult, ensure_dirs, human_bytes, load_config, repo_root
from ..skillcheck import parse_frontmatter

SKIP_DIRS = {".git", "__pycache__", "node_modules"}
SKIP_PREFIXES = ("ci" + "/", "dist" + "/")


def _index_one(payload: tuple[str, str]) -> tuple[str, dict]:
    skills_root, name = payload
    d = Path(skills_root) / name
    entry = {"name": name, "title": "", "description": "", "tags": [],
             "license": "", "source": "", "adapted": False, "files": 0, "bytes": 0}
    skill_md = d / "SKILL.md"
    try:
        raw = skill_md.read_text(encoding="utf-8", errors="replace")
        fields, body = parse_frontmatter(raw)
        entry["title"] = next((ln[2:].strip() for ln in body.splitlines()
                               if ln.startswith("# ")), "")
        entry["description"] = fields.get("description", "")
        entry["license"] = fields.get("license", "")
        entry["source"] = fields.get("source", "") or fields.get("metadata.source", "")
        entry["adapted"] = bool(re.search(r"^\s+adapted:\s*true", raw, re.M))
        m = re.search(r"tags:\s*\[([^\]]*)\]", raw)
        if m:
            entry["tags"] = [t.strip() for t in m.group(1).split(",") if t.strip()]
    except Exception:
        pass
    files = [f for f in d.rglob("*") if f.is_file() and "__pycache__" not in f.parts]
    entry["files"] = len(files)
    entry["bytes"] = sum(f.stat().st_size for f in files)
    return name, entry


def build_index(skills_dir: Path, jobs: int) -> list[dict]:
    names = sorted(p.name for p in skills_dir.iterdir() if p.is_dir())
    entries: list[dict] = []
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        payloads = [(str(skills_dir), n) for n in names]
        for _name, entry in pool.map(_index_one, payloads, chunksize=64):
            entries.append(entry)
    return entries


def make_archive(root: Path, cfg: dict, dest: Path) -> int:
    excludes = set(cfg.get("archive_exclude", []))
    count = 0
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            top = rel.split("/", 1)[0]
            if top in SKIP_DIRS or any(rel.startswith(f"{e.rstrip('/')}/") or rel == e.rstrip("/")
                                       for e in excludes):
                continue
            if path.suffix == ".pyc":
                continue
            zf.write(path, rel)
            count += 1
    return count


def run(ctx: dict) -> StageResult:
    start = time.time()
    cfg = ctx["config"]
    root = repo_root()
    ensure_dirs()
    findings: list[Finding] = []
    skills_dir = root / cfg["skills_dir"]
    jobs = int(cfg.get("jobs", 8))

    entries = build_index(skills_dir, jobs)
    entries.sort(key=lambda e: e["name"])

    index_path = root / "dist" / "skills-index.json"
    payload = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
        "repo": "LoopyLuci/Skills",
        "count": len(entries),
        "skills": entries,
    }
    index_path.write_text(json.dumps(payload, indent=1), encoding="utf-8")

    stats = {
        "skills_indexed": len(entries),
        "index_bytes": index_path.stat().st_size,
        "adapted": sum(1 for e in entries if e["adapted"]),
        "total_bytes": sum(e["bytes"] for e in entries),
    }

    archive_path = None
    if cfg.get("make_archive"):
        archive_path = root / "dist" / f"skills-{time.strftime('%Y%m%d-%H%M%S')}.zip"
        n = make_archive(root, cfg, archive_path)
        stats["archive"] = archive_path.name
        stats["archive_files"] = n
        stats["archive_bytes"] = archive_path.stat().st_size

    ctx["index_path"] = str(index_path)
    ctx["archive_path"] = str(archive_path) if archive_path else None

    summary = (f"indexed {len(entries)} skills ({human_bytes(stats['index_bytes'])}), "
               f"{stats['adapted']} adapted")
    if archive_path:
        summary += f", archive {archive_path.name} ({human_bytes(stats['archive_bytes'])})"
    return StageResult("build", True, time.time() - start, summary, findings, stats)
