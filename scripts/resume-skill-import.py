"""
Resume the interrupted community skill import — reading from the local
clones in D:\Projects\skills-import (no network fetches) and writing
enhanced SKILL.md files into D:\Projects\Skills/skills/.

Mirrors the SOURCES / NAME_ALIASES / ENHANCEMENTS logic from
import-community-skills.py but skips the fragile GitHub raw fetches
(the data is already cloned locally) and re-applies Hermes frontmatter
enhancement. Supporting reference/template/script files are copied too.
"""

import os
import shutil
import sys
from pathlib import Path

SRC_ROOT = Path(r"D:\Projects\skills-import")
DST_ROOT = Path(r"D:\Projects\Skills\skills")  # LoopyLuci/Skills tap repo

# repo dir name (in skills-import) -> source repo key
REPO_MAP = {
    "anthropics-skills": "anthropics/skills",
    "emilkowalski-skills": "emilkowalski/skills",
    "google-skills": "google/skills",
    "mattpocock-skills": "mattpocock/skills",
    "minimax-skills": "MiniMax-AI/skills",
    "slavingia-skills": "slavingia/skills",
    "superpowers": "hermes/superpowers",
}

# Collisions where the later import must be disambiguated.
# emilkowalski's `prototype` wins; mattpocock's → prototype-solution
NAME_ALIASES = {
    "prototype": {
        "mattpocock/skills": "prototype-solution",
    },
}

# Tag enhancements (subset; mirrors import-community-skills.py ENHANCEMENTS)
ENHANCEMENTS = {
    "codebase-design": {"hermes_tags": ["engineering", "architecture", "design-patterns"], "category": "software-development"},
    "code-review": {"hermes_tags": ["engineering", "code-review", "qa"], "category": "software-development"},
    "handoff": {"hermes_tags": ["productivity", "agent-workflow", "handoff"], "category": "productivity"},
    "teach": {"hermes_tags": ["productivity", "education", "teaching"], "category": "productivity"},
    "writing-great-skills": {"hermes_tags": ["skills", "authoring", "meta-skills"], "category": "software-development"},
    "emil-design-eng": {"hermes_tags": ["design", "animation", "ui-ux", "frontend"], "category": "creative"},
    "apple-design": {"hermes_tags": ["design", "apple", "hci", "animation"], "category": "creative"},
    "prototype": {"hermes_tags": ["design", "prototype", "frontend"], "category": "creative"},
    "claude-api": {"hermes_tags": ["api", "claude", "llm", "documentation"], "category": "mlops"},
    "mcp-builder": {"hermes_tags": ["mcp", "server", "tools", "integration"], "category": "software-development"},
}

# Source frontmatter key -> (repo_name -> sub_path) overrides for mattpocock
MATTPOCOCK_SUBCATS = {
    "ask-matt": "engineering/ask-matt",
    "code-review": "engineering/code-review",
    "codebase-design": "engineering/codebase-design",
    "diagnosing-bugs": "engineering/diagnosing-bugs",
    "domain-modeling": "engineering/domain-modeling",
    "grill-with-docs": "engineering/grill-with-docs",
    "implement": "engineering/implement",
    "improve-codebase-architecture": "engineering/improve-codebase-architecture",
    "prototype": "engineering/prototype",
    "research": "engineering/research",
    "resolving-merge-conflicts": "engineering/resolving-merge-conflicts",
    "tdd": "engineering/tdd",
    "to-spec": "engineering/to-spec",
    "to-tickets": "engineering/to-tickets",
    "triage": "engineering/triage",
    "wayfinder": "engineering/wayfinder",
    "grill-me": "productivity/grill-me",
    "grilling": "productivity/grilling",
    "handoff": "productivity/handoff",
    "teach": "productivity/teach",
    "writing-great-skills": "productivity/writing-great-skills",
    "git-guardrails-claude-code": "misc/git-guardrails-claude-code",
    "setup-pre-commit": "misc/setup-pre-commit",
}


def resolve_name(repo, skill_name):
    if skill_name in NAME_ALIASES and repo in NAME_ALIASES[skill_name]:
        return NAME_ALIASES[skill_name][repo]
    return skill_name


def enhance_frontmatter(content, skill_name, source_repo):
    """Insert/replace Hermes metadata in frontmatter. Idempotent.
    Parses existing frontmatter into a dict, drops stale hermes/source/name
    keys, then appends clean Hermes metadata."""
    has_fm = content.startswith("---")
    if has_fm:
        end = content.find("---", 3)
        if end == -1:
            has_fm = False
            body = content
        else:
            fm = content[3:end]
            body = content[end + 3:]
    else:
        fm = ""
        body = content

    # Parse existing frontmatter, dropping the entire old metadata block
    # (all indented sub-lines under `metadata:`) and rewriting name/source.
    kept_lines = []
    existing_name = ""
    i = 0
    fm_rows = fm.split("\n")
    while i < len(fm_rows):
        line = fm_rows[i]
        stripped = line.strip()
        if stripped.startswith("name:"):
            existing_name = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            i += 1
            continue  # rewrite below
        if stripped.startswith("source:"):
            i += 1
            continue  # rewrite below
        if stripped == "metadata:" or stripped.startswith("metadata:"):
            # Drop this line and all following indented lines (the whole block)
            i += 1
            while i < len(fm_rows):
                nl = fm_rows[i]
                if nl.strip() and not nl.startswith(" ") and not nl.startswith("\t"):
                    break  # hit next top-level key
                i += 1
            continue
        kept_lines.append(line)
        i += 1

    target_name = existing_name or skill_name
    enh = ENHANCEMENTS.get(skill_name, {})
    meta_tags = ", ".join(enh.get("hermes_tags", ["agent", "skill"]))
    category = enh.get("category")

    new_fm_lines = ["---"]
    # Preserve other frontmatter (description, license, etc.)
    for line in kept_lines:
        if line.strip():
            new_fm_lines.append(line)
    new_fm_lines.append(f"name: {target_name}")
    new_fm_lines.append(f"source: {source_repo}")
    new_fm_lines.append("metadata:")
    new_fm_lines.append("  hermes:")
    new_fm_lines.append(f"    tags: [{meta_tags}]")
    if category:
        new_fm_lines.append(f"    category: {category}")
    new_fm_lines.append("---")
    new_fm = "\n".join(new_fm_lines)

    return new_fm + "\n\n" + body.strip() + "\n"


def restore_skill(skill_name: str, content: str, source_repo: str) -> str:
    """Re-apply Hermes frontmatter to existing skill content.

    Use when restoring a backed-up or pre-existing skill into the user store:
    re-runs the same enhancement (idempotent) so restored skills match the
    canonical format. Delegates to enhance_frontmatter."""
    return enhance_frontmatter(content, skill_name, source_repo)


def main():
    print("=" * 60)
    print("SKILL IMPORT RESUME — local clone harvest")
    print("=" * 60)

    DST_ROOT.mkdir(parents=True, exist_ok=True)

    total_imported = 0
    total_skipped = 0
    total_errors = 0
    collisions = 0

    for repo_dir, source_repo in REPO_MAP.items():
        src_base = SRC_ROOT / repo_dir
        if not src_base.exists():
            print(f"\n--- {source_repo} (SKIP: clone not present) ---")
            continue

        print(f"\n--- {source_repo} ---")

        # Discover all skill dirs under this repo that contain SKILL.md
        # (excluding template dirs and .git)
        skill_dirs = []
        for item in sorted(src_base.rglob("SKILL.md")):
            if ".git" in item.parts:
                continue
            if "/template" in str(item) or item.parent.name.lower() == "template":
                continue
            skill_dirs.append(item.parent)

        for sk_dir in skill_dirs:
            # Determine skill name from the dir name
            skill_name = sk_dir.name

            # Resolve mattpocock sub-paths (some skills live in subcats)
            if source_repo == "mattpocock/skills":
                rel = sk_dir.relative_to(src_base / "skills")
                # rel like engineering/codebase-design or productivity/teach
                mapped = MATTPOCOCK_SUBCATS.get(skill_name)
                if mapped:
                    expected_rel = Path(mapped)
                else:
                    expected_rel = rel

            mapped_name = resolve_name(source_repo, skill_name)
            target_dir = DST_ROOT / mapped_name
            target_file = target_dir / "SKILL.md"

            # Skip if already exists (idempotent resume)
            if target_file.exists():
                total_skipped += 1
                continue

            # Read the SKILL.md
            src_file = sk_dir / "SKILL.md"
            try:
                content = src_file.read_text(encoding="utf-8")
            except Exception as e:
                print(f"  ✗  {skill_name}: read error: {e}")
                total_errors += 1
                continue

            if len(content) < 100 or "name:" not in content[:300]:
                print(f"  ⚠  {skill_name}: too short or no frontmatter ({len(content)} bytes)")
                total_errors += 1
                continue

            # Enhance frontmatter
            try:
                enhanced = enhance_frontmatter(content, skill_name, source_repo)
            except Exception as e:
                print(f"  ✗  {skill_name}: enhance error: {e}")
                total_errors += 1
                continue

            # Write
            try:
                target_dir.mkdir(parents=True, exist_ok=True)
                target_file.write_text(enhanced, encoding="utf-8")
                total_imported += 1
                if mapped_name != skill_name:
                    collisions += 1
                    print(f"  ✓  {skill_name} → {mapped_name} (collisions)")
                else:
                    print(f"  ✓  {skill_name}")
            except Exception as e:
                print(f"  ✗  {skill_name}: write error: {e}")
                total_errors += 1
                continue

            # Copy supporting dirs: references, templates, scripts, assets, examples
            for subdir in ["references", "templates", "scripts", "assets", "examples"]:
                src_sub = sk_dir / subdir
                if src_sub.exists() and src_sub.is_dir():
                    dst_sub = target_dir / subdir
                    try:
                        shutil.copytree(src_sub, dst_sub, dirs_exist_ok=True)
                    except Exception:
                        pass

    print("\n" + "=" * 60)
    print(f"TOTAL: {total_imported} skills imported to {DST_ROOT}")
    print(f"       {total_skipped} skipped (already exist)")
    print(f"       {total_errors} errors")
    print(f"       {collisions} name collisions resolved")
    print("=" * 60)
    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
