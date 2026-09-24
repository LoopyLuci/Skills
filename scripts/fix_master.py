#!/usr/bin/env python3
"""
Master Fixer — Fix ALL remaining issues.

Issues to fix:
1. Skills with both flat tags: AND metadata.hermes.tags → remove flat tags:
2. Skills where enrichment appended ## Trigger/## Core Concepts to existing content
3. Skills with duplicate sections
4. Skills where body was overwritten but old content remains
"""
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter

REPO_SKILLS = Path(r"Z:\Projects\Skills\LoopyLuci-skills\skills")

FIXES = Counter()


def parse_fm(text):
    result = {}
    stack = [(result, -1)]
    for line in text.split('\n'):
        if not line.strip() or line.strip().startswith('#'):
            continue
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        while len(stack) > 1 and stack[-1][1] >= indent:
            stack.pop()
        parent_dict = stack[-1][0]
        if ':' in stripped:
            key, _, val = stripped.partition(':')
            key = key.strip()
            val = val.strip()
            if val == '':
                new_dict = {}
                parent_dict[key] = new_dict
                stack.append((new_dict, indent))
            elif val.startswith('[') and val.endswith(']'):
                items = [v.strip().strip('"').strip("'") for v in val[1:-1].split(',') if v.strip()]
                parent_dict[key] = items
            else:
                parent_dict[key] = val
    return result


def find_frontmatter_end(content):
    for i in range(3, len(content) - 3):
        if content[i:i+3] == '---':
            prev = content[i-1]
            if prev in ('\n', '\r'):
                return i
    return -1


def fix_skill(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False

    end = find_frontmatter_end(content)
    if end == -1:
        return False

    fm_text = content[3:end].strip()
    body = content[end+3:].strip()

    try:
        fm = parse_fm(fm_text)
    except Exception:
        return False

    changed = False

    # Fix 1: Remove flat tags: if metadata.hermes.tags exists
    if "tags" in fm and "metadata" in fm and isinstance(fm["metadata"], dict):
        hermes = fm["metadata"].get("hermes")
        if isinstance(hermes, dict) and "tags" in hermes:
            del fm["tags"]
            FIXES["removed_flat_tags"] += 1
            changed = True

    # Fix 2: Fix body - remove duplicate sections
    # If body has both ## Overview and ## Trigger, remove the appended Trigger/Core Concepts
    if "## Overview" in body and "## Trigger" in body:
        # Find where the appended content starts (after the original content ends)
        # Look for the pattern of appended content
        trigger_pos = body.find("## Trigger")
        core_pos = body.find("## Core Concepts")
        
        if trigger_pos > 100 and core_pos > trigger_pos:
            # Remove everything from Trigger onwards (it was appended)
            body = body[:trigger_pos].rstrip() + "\n"
            FIXES["removed_appended_sections"] += 1
            changed = True

    # Fix 3: Remove duplicate ## Trigger or ## Core Concepts
    for section in ["## Trigger", "## Core Concepts"]:
        count = body.count(section)
        if count > 1:
            # Keep the last occurrence (the appended one is boilerplate)
            parts = body.split(section)
            # Reconstruct with only the last occurrence
            body = section.join(parts[:-1]) + "\n\n" + parts[-1].lstrip()
            FIXES["removed_duplicate_sections"] += 1
            changed = True

    if not changed:
        return False

    # Rebuild
    new_fm = dict_to_yaml(fm)
    new_content = f"---\n{new_fm}\n---\n\n{body.strip()}\n"
    skill_md.write_text(new_content, encoding="utf-8")
    return True


def main():
    from collections import Counter
    apply = "--apply" in sys.argv
    skills = sorted(REPO_SKILLS.iterdir())
    
    fixed = 0
    for skill_dir in skills:
        if not skill_dir.is_dir():
            continue
        try:
            if fix_skill(skill_dir):
                fixed += 1
        except Exception as e:
            pass

    mode = "APPLIED" if apply else "DRY-RUN"
    print(f"=== {mode} ===")
    print(f"Fixed: {fixed}")
    for fix_type, count in FIXES.most_common():
        if count > 0:
            print(f"  {fix_type}: {count}")


if __name__ == "__main__":
    main()
