#!/usr/bin/env python3
"""
Skill Validator — Properly validates both Format A (new) and Format B (curated).

Format A: metadata.hermes.tags, ## Trigger, ## Core Concepts
Format B: flat tags, ## Overview, ## When to Use, ## Key Approaches, ## Common Pitfalls, ## Verification Checklist
"""
import json
import re
import sys
from pathlib import Path

REPO_SKILLS = Path(r"Z:\Projects\Skills\LoopyLuci-skills\skills")

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


def detect_format(body, fm):
    """Detect which format a skill uses."""
    is_format_a = (
        "## Trigger" in body and "## Core Concepts" in body
    )
    is_format_b = (
        "## Overview" in body or "## When to Use" in body
    )
    
    if is_format_a and is_format_b:
        return "mixed"
    elif is_format_a:
        return "A"
    elif is_format_b:
        return "B"
    else:
        return "unknown"


def validate_skill(skill_dir):
    issues = []
    skill_md = skill_dir / "SKILL.md"
    
    if not skill_md.exists():
        return [("error", "Missing SKILL.md")]
    
    content = skill_md.read_text(encoding="utf-8")
    
    if not content.startswith("---"):
        return [("error", "Missing frontmatter start")]
    
    end = find_frontmatter_end(content)
    if end == -1:
        return [("error", "Missing frontmatter end")]
    
    fm_text = content[3:end].strip()
    body = content[end+3:].strip()
    
    try:
        fm = parse_fm(fm_text)
    except Exception:
        return [("error", "YAML parse error")]
    
    # Check required fields (both formats)
    for field in ["name", "description"]:
        if field not in fm or not fm.get(field):
            issues.append(("error", f"Missing required field: {field}"))
    
    # Check name matches directory
    if fm.get("name") and fm["name"] != skill_dir.name:
        issues.append(("error", f"Name mismatch: {fm['name']} != {skill_dir.name}"))
    
    # Check version/author (warn only for format B)
    if "version" not in fm:
        issues.append(("warn", "Missing version"))
    if "author" not in fm:
        issues.append(("warn", "Missing author"))
    
    # Check tags (either format)
    has_tags = False
    if "metadata" in fm and isinstance(fm["metadata"], dict):
        hermes = fm["metadata"].get("hermes")
        if isinstance(hermes, dict) and hermes.get("tags"):
            has_tags = True
    if "tags" in fm and fm["tags"]:
        has_tags = True
    
    if not has_tags:
        issues.append(("error", "No tags"))
    
    # Check body
    fmt = detect_format(body, fm)
    if len(body) < 50:
        issues.append(("error", f"Body too short ({len(body)} chars)"))
    elif fmt == "unknown" and len(body) < 200:
        issues.append(("warn", f"Body may be too short ({len(body)} chars)"))
    
    return issues


def main():
    fix_mode = "--fix" in sys.argv
    skills = sorted(REPO_SKILLS.iterdir())
    
    valid = 0
    with_errors = 0
    with_warnings = 0
    
    error_skills = {}
    warn_skills = {}
    
    for skill_dir in skills:
        if not skill_dir.is_dir():
            continue
        issues = validate_skill(skill_dir)
        
        errors = [i for i in issues if i[0] == "error"]
        warns = [i for i in issues if i[0] == "warn"]
        
        if errors:
            with_errors += 1
            error_skills[skill_dir.name] = issues
        elif warns:
            with_warnings += 1
            warn_skills[skill_dir.name] = issues
            valid += 1
        else:
            valid += 1
    
    total = valid + with_errors
    
    print(f"=== Validation Summary ===")
    print(f"  Total: {total}")
    print(f"  Valid: {valid}")
    print(f"  With warnings: {with_warnings}")
    print(f"  With errors: {with_errors}")
    
    if error_skills:
        print(f"\n=== Errors ===")
        from collections import Counter
        error_types = Counter()
        for issues in error_skills.values():
            for _, msg in issues:
                error_types[msg] += 1
        for msg, count in error_types.most_common(20):
            print(f"  {msg}: {count}")
    
    if warn_skills:
        print(f"\n=== Warnings ===")
        from collections import Counter
        warn_types = Counter()
        for issues in warn_skills.values():
            for _, msg in issues:
                warn_types[msg] += 1
        for msg, count in warn_types.most_common(10):
            print(f"  {msg}: {count}")


if __name__ == "__main__":
    main()
