"""
Import upstream community skill repos into LoopyLuci/Skills.

Clones live under _sources/<owner>_<repo>/ (git-ignored). Each upstream
SKILL.md is adapted to this repo's canonical schema:

    name / description / version / author / license / platforms
    metadata.hermes.tags (+ metadata.hermes.source attribution)

Rules:
  - Container skills (a SKILL.md whose directory holds child SKILL.md files,
    e.g. oracle's apex/oci/db umbrellas) are skipped.
  - Versioned duplicates (oracle apex/apexlang/26.1 vs 26.2) collapse to the
    highest version.
  - Placeholder skills (e.g. oracle `fusion`) are skipped.
  - Skills already present in skills/ are skipped (never overwritten).
  - Supporting files/dirs next to SKILL.md are copied verbatim.

Usage:
    python scripts/import-upstream-skills.py            # apply
    python scripts/import-upstream-skills.py --dry-run  # report only
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / "_sources"
TARGET_DIR = ROOT / "skills"
MANIFEST = ROOT / "scripts" / "imported-upstream-skills.json"

# upstream repo -> base tags applied to every skill from it
SOURCES = {
    "addyosmani_agent-skills": {
        "repo": "addyosmani/agent-skills",
        "base_tags": ["software-development", "engineering", "agent-skills"],
    },
    "oracle_skills": {
        "repo": "oracle/skills",
        "base_tags": ["oracle"],
    },
    "mattpocock_skills": {
        "repo": "mattpocock/skills",
        "base_tags": ["software-development", "engineering"],
    },
    "obsidianmd_obsidian-skills": {
        "repo": "obsidianmd/obsidian-skills",
        "base_tags": ["note-taking", "obsidian", "productivity"],
    },
    "cloudflare_security-audit-skill": {
        "repo": "cloudflare/security-audit-skill",
        "base_tags": ["security", "auditing", "appsec", "vulnerability-research"],
    },
    "Forward-Future_loopy": {
        "repo": "Forward-Future/loopy",
        "base_tags": ["agent-workflow", "automation", "loops"],
    },
}

# per-skill tag overrides (merged after base+path tags)
TAG_OVERRIDES = {
    "frontend-ui-engineering": ["frontend", "ui", "ux", "accessibility"],
    "security-and-hardening": ["security", "hardening"],
    "test-driven-development": ["testing", "tdd"],
    "performance-optimization": ["performance"],
    "browser-testing-with-devtools": ["testing", "browser", "devtools"],
    "ci-cd-and-automation": ["devops", "ci-cd", "automation"],
    "observability-and-instrumentation": ["observability", "monitoring"],
    "debugging-and-error-recovery": ["debugging", "reliability"],
    "git-workflow-and-versioning": ["git", "version-control"],
    "code-review-and-quality": ["code-review", "quality"],
    "documentation-and-adrs": ["documentation", "adr"],
    "context-engineering": ["ai-agents", "context"],
    "using-agent-skills": ["skills", "meta"],
    "security-audit": ["security", "audit", "pentest"],
}

# names to never import (placeholders / non-skill indexes)
SKIP_NAMES = {"fusion"}

NOISE_SEGMENTS = {"skills", "plugins", "obsidian", ".git"}

CANONICAL_TEMPLATE = """---
name: {name}
description: {description}
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
{extra_frontmatter}metadata:
  hermes:
    tags: [{tags}]
    source: {source}
---

{body}"""


def slug(text):
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def parse_frontmatter(text):
    """Return (dict_of_top_level_keys, body)."""
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n?", text, re.S)
    if not m:
        return {}, text
    raw = m.group(1)
    body = text[m.end():]
    fields = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip().strip('"').strip("'")
    return fields, body


def version_key(rel_path):
    """Higher version numbers win when deduping (26.2 > 26.1)."""
    best = 0
    for seg in rel_path.parts:
        m = re.fullmatch(r"(\d+)(?:\.(\d+))?", seg)
        if m:
            best = max(best, int(m.group(1)) * 100 + int(m.group(2) or 0))
    return best


def collect_candidates(src_dir, src_name):
    """All SKILL.md under a source, minus containers and skipped names."""
    repo = SOURCES[src_name]["repo"]
    base_tags = SOURCES[src_name]["base_tags"]
    candidates = []
    for sk in sorted(src_dir.rglob("SKILL.md")):
        if ".git" in sk.parts:
            continue
        rel = sk.relative_to(src_dir)
        fields, _ = parse_frontmatter(sk.read_text(encoding="utf-8", errors="replace"))
        name = fields.get("name") or sk.parent.name
        if name in SKIP_NAMES:
            continue
        # container = child directory that itself has a SKILL.md
        children = [c for c in sk.parent.iterdir()
                    if c.is_dir() and (c / "SKILL.md").exists()]
        if children:
            continue
        parent_parts = rel.parts[:-2]  # drop filename and the skill's own dir
        path_tags = [
            slug(p) for p in parent_parts
            if p.lower() not in NOISE_SEGMENTS and not re.fullmatch(r"\d+(?:\.\d+)?", p)
        ]
        tags = list(dict.fromkeys(base_tags + path_tags + TAG_OVERRIDES.get(name, [])))
        candidates.append({
            "name": name,
            "path": sk,
            "rel": rel,
            "repo": repo,
            "tags": tags,
            "version": version_key(rel),
        })
    return candidates


def dedupe(candidates):
    """Collapse same-name candidates to the highest-version one."""
    by_name = {}
    dropped = []
    for c in candidates:
        prev = by_name.get(c["name"])
        if prev is None or c["version"] > prev["version"]:
            if prev is not None:
                dropped.append((c["name"], prev["rel"], c["rel"]))
            by_name[c["name"]] = c
        else:
            dropped.append((c["name"], c["rel"], prev["rel"]))
    return list(by_name.values()), dropped


def build_skill_md(cand):
    fields, body = parse_frontmatter(cand["path"].read_text(encoding="utf-8", errors="replace"))
    name = cand["name"]
    description = fields.get("description", "").replace("\n", " ").strip()
    if not description:
        description = f"Imported from {cand['repo']}."
    # preserve any non-canonical upstream keys (argument-hint, etc.)
    extra_keys = [k for k in fields if k not in ("name", "description")]
    extra = "".join(f"{k}: {fields[k]}\n" for k in extra_keys)
    if extra:
        extra = extra + "\n"
    body = body.strip("\n")
    return CANONICAL_TEMPLATE.format(
        name=name,
        description=description,
        extra_frontmatter=extra,
        tags=", ".join(cand["tags"]),
        source=cand["repo"],
        body=body,
    )


def copy_support_files(src_skill_dir, target_skill_dir):
    """Copy everything next to SKILL.md except SKILL.md itself."""
    copied = []
    for entry in src_skill_dir.iterdir():
        if entry.name == "SKILL.md" or entry.name == ".git":
            continue
        dest = target_skill_dir / entry.name
        if entry.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(entry, dest, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            copied.append(entry.name + "/")
        else:
            shutil.copy2(entry, dest)
            copied.append(entry.name)
    return copied


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    existing = {d.name for d in TARGET_DIR.iterdir() if (d / "SKILL.md").exists()}
    print(f"existing skills in repo: {len(existing)}")
    print(f"upstream sources: {len(SOURCES)}\n")

    total_imported = total_existing = total_container = total_dedupe = 0
    manifest = {}

    for src_name, cfg in SOURCES.items():
        src_dir = SOURCES_DIR / src_name
        if not src_dir.is_dir():
            print(f"--- {src_name}: MISSING (clone it first)")
            continue
        cands = collect_candidates(src_dir, src_name)
        total_container += sum(
            1 for sk in src_dir.rglob("SKILL.md")
            if ".git" not in sk.parts
            and any(c.is_dir() and (c / "SKILL.md").exists() for c in sk.parent.iterdir())
        )
        cands, dropped = dedupe(cands)
        total_dedupe += len(dropped)

        imported, already = [], []
        for c in sorted(cands, key=lambda x: x["name"]):
            if c["name"] in existing:
                already.append(c["name"])
                continue
            target = TARGET_DIR / c["name"]
            content = build_skill_md(c)
            support = []
            if not args.dry_run:
                target.mkdir(parents=True, exist_ok=True)
                (target / "SKILL.md").write_text(content, encoding="utf-8")
                support = copy_support_files(c["path"].parent, target)
            imported.append({"name": c["name"], "source": c["repo"],
                              "tags": c["tags"], "support": support})
            existing.add(c["name"])

        manifest[src_name] = imported
        total_imported += len(imported)
        total_existing += len(already)
        print(f"--- {src_name} ({cfg['repo']})")
        print(f"    candidates: {len(cands)}  imported: {len(imported)}  "
              f"already present: {len(already)}")
        if dropped:
            for name, loser, keeper in dropped:
                print(f"    deduped: {name} -> kept {keeper} (dropped {loser})")
        if already:
            print(f"    skipped (exists): {', '.join(sorted(already))}")

    if not args.dry_run:
        MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("\n" + "=" * 60)
    print(f"imported:        {total_imported}")
    print(f"already present: {total_existing}")
    print(f"containers skip: {total_container}")
    print(f"version deduped: {total_dedupe}")
    print(f"manifest:        {MANIFEST}")
    print("=" * 60)


if __name__ == "__main__":
    main()
