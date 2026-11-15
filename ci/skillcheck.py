"""Skill validation rules.

Pure stdlib, import-safe in worker processes. Each skill directory is checked
independently so the scan parallelises cleanly across CPU cores.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

FRONTMATTER_RE = re.compile(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n?", re.S)
KEY_RE = re.compile(r"^([A-Za-z0-9_.-]+):\s*(.*)$")
TAGS_RE = re.compile(r"tags:\s*\[([^\]]*)\]")
REL_LINK_RE = re.compile(r"\]\((\.\./([A-Za-z0-9._-]+)/SKILL\.md)\)")
SUPPORT_RE = re.compile(
    r"\b((?:references|scripts|templates|assets|agents|examples|output-templates|tools|runtime)/[A-Za-z0-9._/-]+)"
)
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return (top-level frontmatter fields, body). Raises ValueError if absent."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if line.startswith((" ", "\t")):
            continue
        km = KEY_RE.match(line)
        if km:
            fields[km.group(1)] = km.group(2).strip().strip('"').strip("'")
    return fields, text[match.end():]


def _strip_code(text: str) -> list[str]:
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.strip():
            out.append(line.strip())
    return out


def _longest_common_run(a: list[str], b: list[str]) -> int:
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    best = 0
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        ai = a[i - 1]
        for j in range(1, len(b) + 1):
            if ai == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best = cur[j]
        prev = cur
    return best


def _similarity(a: list[str], b: list[str]) -> float:
    if not a or not b:
        return 0.0
    import difflib

    return difflib.SequenceMatcher(None, "\n".join(a), "\n".join(b)).ratio()


def check_skill(skill_dir: Path, ctx: dict[str, Any]) -> tuple[list[dict[str, str]], dict[str, str]]:
    """Validate one skill directory.

    Returns (findings, meta) where meta carries the body hash, title and
    description so the parent process can run cross-skill duplicate detection
    after all workers have reported in.
    """
    cfg = ctx["config"]
    findings: list[dict[str, str]] = []
    name = skill_dir.name

    def add(code: str, severity: str, message: str, path: str = "") -> None:
        findings.append({"code": code, "severity": severity,
                         "message": message, "path": path})

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add("E_NO_SKILL_MD", "error", "skill directory has no SKILL.md")
        return findings, {"name": name, "hash": "", "title": "", "description": ""}

    try:
        raw = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        add("E_READ", "error", f"cannot read SKILL.md: {exc}")
        return findings, {"name": name, "hash": "", "title": "", "description": ""}

    if len(raw.encode("utf-8", errors="replace")) > int(cfg["max_file_mb"]) * 1024 * 1024:
        add("E_SIZE", "error", "SKILL.md exceeds the per-file size cap")

    try:
        fields, body = parse_frontmatter(raw)
    except ValueError as exc:
        add("E_FRONTMATTER", "error", str(exc))
        fields, body = {}, raw

    for key in cfg["required_frontmatter"]:
        if key not in fields:
            add("E_KEY_MISSING", "error", f"frontmatter is missing '{key}'")

    declared = fields.get("name", "")
    if declared and declared != name:
        add("E_NAME_MISMATCH", "error", f"frontmatter name '{declared}' != directory '{name}'")

    license_name = fields.get("license", "")
    if cfg.get("allowed_licenses") and license_name and license_name not in cfg["allowed_licenses"]:
        add("E_LICENSE", "error", f"license '{license_name}' is not in the allowlist")

    tags: list[str] = []
    tag_match = TAGS_RE.search(raw)
    if tag_match:
        tags = [t.strip() for t in tag_match.group(1).split(",") if t.strip()]
    if cfg.get("require_tags") and not tags:
        add("E_TAGS", "error", "no non-empty metadata.hermes.tags list found")
    if cfg.get("forbid_self_tag") and name in tags:
        add("E_SELFTAG", "info", "tag list contains the skill's own name")

    if name in ctx.get("adapted", {}) and cfg.get("require_source_for_adapted"):
        has_source = (re.search(r"^source:\s*\S", raw, re.M)
                      or re.search(r"^\s+source:\s*\S", raw, re.M))
        if not has_source:
            add("E_SOURCE", "error", "adapted skill is missing source attribution")

    # relative links to sibling skills must resolve
    for _full, target in REL_LINK_RE.findall(body):
        if target not in ctx["known_names"]:
            add("E_LINK", "error", f"broken cross-link to '../{target}/SKILL.md'")

    # referenced support files must exist locally or elsewhere in the repo
    repo_files = ctx.get("repo_files") or set()
    for rel in SUPPORT_RE.findall(body):
        if "$" in rel or "<" in rel or ">" in rel or "*" in rel:
            continue
        if (skill_dir / rel).exists() or rel in repo_files:
            continue
        add("E_SUPPORT", "warning", f"referenced support file missing: {rel}")

    # hygiene
    for bad in (".git", "__pycache__"):
        if any(p.name == bad for p in skill_dir.rglob("*") if p.is_dir()):
            add("E_NESTED", "error", f"contains a nested {bad}/ directory")

    total = sum(f.stat().st_size for f in skill_dir.rglob("*") if f.is_file())
    if total > int(cfg["max_skill_dir_mb"]) * 1024 * 1024:
        add("E_DIR_SIZE", "warning", "skill directory exceeds the size cap")

    # signatures for cross-skill duplicate detection (done by the parent)
    body_hash = hashlib.sha256("\n".join(_strip_code(body)).encode("utf-8")).hexdigest()
    title = next((ln[2:].strip() for ln in body.splitlines() if ln.startswith("# ")), "")
    meta = {"name": name, "hash": body_hash, "title": title,
            "description": fields.get("description", "")}

    # verbatim overlap against upstream for adapted skills
    upstream_rel = ctx.get("adapted", {}).get(name)
    if upstream_rel and ctx.get("sources_dir"):
        up = ctx["sources_dir"] / upstream_rel
        if up.exists():
            up_raw = up.read_text(encoding="utf-8", errors="replace")
            try:
                _, up_body = parse_frontmatter(up_raw)
            except ValueError:
                up_body = up_raw
            a, b = _strip_code(body), _strip_code(up_body)
            run = _longest_common_run(a, b)
            sim = _similarity(a, b)
            if run > int(cfg["overlap_max_lines"]) or sim > float(cfg["overlap_max_similarity"]):
                add("W_OVERLAP", "warning",
                    f"close to upstream: {run}-line verbatim run, similarity {sim:.2f}")

    return findings, meta


def scan_worker(payload: tuple[str, dict[str, Any]]) -> tuple[str, list[dict[str, str]], dict[str, str]]:
    path_str, ctx = payload
    findings, meta = check_skill(Path(path_str), ctx)
    return Path(path_str).name, findings, meta

