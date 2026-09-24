#!/usr/bin/env python3
"""
Fix malformed skills — upstream imports with broken YAML.

These skills have:
- tags: at top level (outside metadata)
- Stray hermes: line
- version/author outside frontmatter
- Improper nesting

Fix: Extract data, rebuild proper frontmatter, preserve body.
"""
import json
import re
import sys
from pathlib import Path

REPO_SKILLS = Path(r"Z:\Projects\Skills\LoopyLuci-skills\skills")


def fix_malformed_skill(skill_dir):
    """Fix a single malformed skill. Returns True if changed."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False

    content = skill_md.read_text(encoding="utf-8")
    
    # Check if this skill has the malformed pattern
    # Pattern: tags: at top level + stray hermes: line + version/author after hermes:
    if "tags:" not in content or "hermes:" not in content:
        return False
    
    # Check for the specific malformed pattern
    lines = content.split('\n')
    
    # Find frontmatter boundaries
    if not lines[0].strip() == '---':
        return False
    
    # Find closing ---
    fm_end = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            fm_end = i
            break
    
    if fm_end == -1:
        return False
    
    frontmatter_lines = lines[1:fm_end]
    body_lines = lines[fm_end+1:]
    
    # Check if it has the malformed pattern
    has_flat_tags = any(l.strip().startswith('tags:') for l in frontmatter_lines)
    has_stray_hermes = any(l.strip() == 'hermes:' for l in frontmatter_lines)
    
    if not (has_flat_tags and has_stray_hermes):
        return False
    
    # Extract fields from malformed frontmatter
    name = skill_dir.name
    description = ""
    tags = []
    
    for line in frontmatter_lines:
        stripped = line.strip()
        if stripped.startswith('name:'):
            name = stripped.split(':', 1)[1].strip()
        elif stripped.startswith('description:'):
            desc_val = stripped.split(':', 1)[1].strip()
            # Remove >- and quotes
            desc_val = desc_val.lstrip('>-').strip().strip('"').strip("'")
            description = desc_val
        elif stripped.startswith('tags:'):
            tags_str = stripped.split(':', 1)[1].strip()
            # Parse list
            if tags_str.startswith('[') and tags_str.endswith(']'):
                tags = [t.strip().strip('"').strip("'") for t in tags_str[1:-1].split(',')]
            else:
                tags = [t.strip() for t in tags_str.split(',')]
    
    # Build proper frontmatter
    fm = {
        "name": name,
        "description": description or f"Skill for {name.replace('-', ' ')}",
        "version": "1.0.0",
        "author": "LoopyLuci Community",
        "license": "MIT",
        "platforms": ["any"],
        "metadata": {
            "hermes": {
                "tags": [t.lower() for t in tags] if tags else [name.split("-")[0], "general"]
            }
        }
    }
    
    # Build YAML
    new_fm_lines = ["---"]
    new_fm_lines.append(f"name: {fm['name']}")
    new_fm_lines.append(f"description: {fm['description']}")
    new_fm_lines.append(f"version: {fm['version']}")
    new_fm_lines.append(f"author: {fm['author']}")
    new_fm_lines.append(f"license: {fm['license']}")
    new_fm_lines.append(f"platforms: [{', '.join(fm['platforms'])}]")
    new_fm_lines.append("metadata:")
    new_fm_lines.append("  hermes:")
    tags_str = ', '.join(fm['metadata']['hermes']['tags'])
    new_fm_lines.append(f"    tags: [{tags_str}]")
    new_fm_lines.append("---")
    
    # Rebuild content
    new_content = "\n".join(new_fm_lines) + "\n\n" + "\n".join(body_lines).strip() + "\n"
    skill_md.write_text(new_content, encoding="utf-8")
    return True


def main():
    apply = "--apply" in sys.argv
    skills = sorted(REPO_SKILLS.iterdir())
    
    fixed = 0
    for skill_dir in skills:
        if not skill_dir.is_dir():
            continue
        try:
            if fix_malformed_skill(skill_dir):
                fixed += 1
                if not apply:
                    print(f"  Would fix: {skill_dir.name}")
        except Exception as e:
            print(f"  Error fixing {skill_dir.name}: {e}")
    
    mode = "APPLIED" if apply else "DRY-RUN"
    print(f"\n=== {mode} ===")
    print(f"Fixed: {fixed}")


if __name__ == "__main__":
    main()
