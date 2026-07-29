#!/usr/bin/env python3
"""
Phase 1: Restructure the Skills repo for maximum agent compatibility.

Flat layout under skills/:
    skills/<skill-name>/
        SKILL.md
        references/...
        templates/...
        scripts/...

Works with:
  - Hermes tap (default path: skills/, 1-level scan)
  - Hermes external_dirs
  - agentskills.io format (Codex, Claude Code, Cline, etc.)
"""

import json
import os
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path("D:/Projects/Skills")
SKILLS_DIR = REPO_ROOT / "skills"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from SKILL.md content. Returns (metadata, body)."""
    text = text.lstrip("\ufeff")  # strip BOM
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    fm = text[3:end].strip()
    body = text[end + 3 :].strip()
    meta = {}
    for line in fm.split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            # Strip quotes
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
                val = val[1:-1]
            meta[key] = val
    return meta, body


def get_skill_name(frontmatter: dict, dir_path: Path) -> str:
    """Determine the canonical skill name from frontmatter or directory name."""
    name = frontmatter.get("name", "").strip()
    if name and re.match(r"^[a-z][a-z0-9_-]*$", name):
        return name
    # Fall back to the leaf directory name
    name = dir_path.name
    if re.match(r"^[a-z][a-z0-9_-]*$", name):
        return name
    # Sanitize
    name = re.sub(r"[^a-z0-9_-]", "-", name.lower()).strip("-")
    return name or "unnamed"


SUBDIRS = {"references", "templates", "scripts", "assets", "examples"}


def flatten_skills():
    """Scan all SKILL.md files and copy them to skills/<name>/."""
    print("=" * 60)
    print("PHASE 1: Flattening skills into skills/<name>/ layout")
    print("=" * 60)

    # Find all SKILL.md files (up to 4 levels deep)
    all_skill_paths = list(REPO_ROOT.glob("**/SKILL.md"))
    # Exclude things inside .git or inside skills/ itself
    all_skill_paths = [
        p
        for p in all_skill_paths
        if ".git" not in p.parts and not p.parts[:1] == ("skills",)
    ]
    print(f"Found {len(all_skill_paths)} SKILL.md files to process")

    SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    moved = 0
    name_collisions = []
    no_name_dirs = []
    supporting_dirs = []

    for skill_path in all_skill_paths:
        content = skill_path.read_text(encoding="utf-8", errors="replace")
        meta, body = parse_frontmatter(content)
        skill_name = get_skill_name(meta, skill_path.parent)
        
        if not skill_name:
            no_name_dirs.append(str(skill_path))
            continue

        target_dir = SKILLS_DIR / skill_name
        target_skill = target_dir / "SKILL.md"

        if target_skill.exists():
            # Collision — read existing to compare
            existing_content = target_skill.read_text(encoding="utf-8", errors="replace")
            existing_meta, _ = parse_frontmatter(existing_content)
            name_collisions.append(
                f"  {skill_name}: {skill_path} vs {existing_meta.get('source', 'unknown')}"
            )
            continue

        # Create target dir and write SKILL.md
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Add a source annotation so we know where it came from
        if "name" not in meta:
            # Use first 40 chars of the path as a comment
            pass
        
        target_skill.write_text(content, encoding="utf-8")
        moved += 1

        # Copy supporting subdirectories
        for sub in SUBDIRS:
            src_sub = skill_path.parent / sub
            if src_sub.is_dir():
                tgt_sub = target_dir / sub
                if tgt_sub.exists():
                    shutil.rmtree(tgt_sub)
                shutil.copytree(src_sub, tgt_sub)
                supporting_dirs.append(f"  {skill_name}/{sub}")

    print(f"\nMoved {moved} skills to skills/")
    if name_collisions:
        print(f"\n⚠  {len(name_collisions)} name collisions (skipped duplicates):")
        for c in name_collisions[:10]:
            print(c)
    if no_name_dirs:
        print(f"\n⚠  {len(no_name_dirs)} had no valid name (skipped):")
        for n in no_name_dirs[:5]:
            print(f"  {n}")
    if supporting_dirs:
        print(f"\nCopied {len(supporting_dirs)} supporting directories")

    return moved


def remove_old_structure():
    """Remove old category dirs and flat skill dirs, leaving only skills/, .git, scripts/."""
    print("\n" + "=" * 60)
    print("PHASE 2: Removing old directory structure")
    print("=" * 60)

    keep = {".git", "skills", "scripts"}
    removed = 0
    for entry in REPO_ROOT.iterdir():
        if entry.is_dir() and entry.name not in keep:
            shutil.rmtree(entry)
            removed += 1
            print(f"  Removed: {entry.name}/")
    
    # Remove Hermes internal files at root
    internal_files = [
        ".bundled_manifest",
        ".curator_state",
        ".usage.json",
        ".usage.json.lock",
        ".gitignore",  # we'll rewrite it
    ]
    for f in internal_files:
        fp = REPO_ROOT / f
        if fp.exists():
            fp.unlink()
            print(f"  Removed: {f}")

    print(f"\nCleaned up {removed} old directories")


def build_gitignore():
    """Create a comprehensive .gitignore."""
    content = """# Hermes internal state (never commit these)
.bundled_manifest
.curator_state
.curator_state.bak
.usage.json
.usage.json.lock
IDEA.md

# OS files
.DS_Store
Thumbs.db
*.swp
*.swo
*~

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
.venv/
venv/

# IDE
.idea/
.vscode/
*.sublime-*
"""
    (REPO_ROOT / ".gitignore").write_text(content, encoding="utf-8")
    print("\n  Written: .gitignore")


def build_readme():
    """Create comprehensive README.md."""
    readme = """# LoopyLuci Skills

A curated collection of **1,028+ AI agent skills** built for [Hermes Agent](https://hermes-agent.nousresearch.com/) and compatible with any agent that supports the [agentskills.io](https://agentskills.io/) open standard.

These skills cover: software development, ML/AI, networking, security, creative tools, productivity, DevOps, system administration, and more — designed to be loaded on-demand by AI agents.

---

## How to Use

### With Hermes Agent

#### Option A: Clone + External Directory (recommended)

```bash
git clone https://github.com/LoopyLuci/Skills.git ~/LoopyLuci-skills
```

Then add to your `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - ~/LoopyLuci-skills/skills
```

All skills are instantly available as `/skill-name` slash commands. No install per skill needed.

#### Option B: Skill Tap (hub-managed updates)

```bash
hermes skills tap add LoopyLuci/Skills
```

Then edit `~/.hermes/.hub/taps.json` to set the path to root:

```json
{
  "taps": [
    {"repo": "LoopyLuci/Skills", "path": "skills/"}
  ]
}
```

Then install individual skills:

```bash
hermes skills search <query>
hermes skills install LoopyLuci/Skills/<skill-name>
```

#### Option C: Direct URL Install

```bash
hermes skills install https://raw.githubusercontent.com/LoopyLuci/Skills/main/skills/<skill-name>/SKILL.md
```

### With Other Agents

Most AI coding agents (Claude Code, Codex, Cline, Aider) support the [agentskills.io](https://agentskills.io/) format. Clone the repo and point your agent at the `skills/` directory:

```bash
git clone https://github.com/LoopyLuci/Skills.git
# Then configure your agent to scan ./Skills/skills/
```

---

## Structure

```
LoopyLuci/Skills/
├── skills/                        # All skills (flat, one directory per skill)
│   ├── blocklist-manager/
│   │   ├── SKILL.md               # Skill definition (required)
│   │   ├── references/            # Additional documentation
│   │   ├── templates/             # Output templates
│   │   └── scripts/               # Helper scripts
│   ├── git-workflow-optimization/
│   │   └── SKILL.md
│   ├── kubernetes-deployment/
│   │   └── SKILL.md
│   ├── ... 1,028+ skills
├── scripts/
│   └── sync-from-hermes.sh        # Sync script (maintainer use)
├── README.md                      # This file
└── .gitignore
```

---

## Automatic Updates

This repository is synced from Hermes Agent's local skill library. Skills added or modified in Hermes are automatically committed and pushed here.

To sync changes back to your local Hermes (pull from repo):

```bash
cd ~/LoopyLuci-skills && git pull
```

---

## Skill Format

Each skill follows the [agentskills.io](https://agentskills.io/specification) standard:

```yaml
---
name: my-skill
description: Brief description, ~60 chars
tags: [python, automation]
---
```

Full format details at the [Hermes Skills Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills).

---

## License

MIT — free to use, share, and contribute.
"""
    (REPO_ROOT / "README.md").write_text(readme, encoding="utf-8")
    print("  Written: README.md")


def main():
    moved = flatten_skills()
    remove_old_structure()
    build_gitignore()
    build_readme()

    print("\n" + "=" * 60)
    print("RESTRUCTURE COMPLETE")
    print("=" * 60)
    print(f"Skills in skills/: {moved}")
    print("Old directories removed: yes")
    print("README.md: written")
    print("Next: review, commit, and push")


if __name__ == "__main__":
    main()
