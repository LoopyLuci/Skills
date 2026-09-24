#!/usr/bin/env python3
"""
Skill Validator — Check that all skills in the repo meet format standards.

Usage:
  python validate_skill.py                    # Validate all skills
  python validate_skill.py skills/my-skill    # Validate one skill
  python validate_skill.py --fix              # Attempt to fix common issues
"""
import json
import re
import sys
from pathlib import Path

REPO_SKILLS = Path(r"Z:\Projects\Skills\LoopyLuci-skills\skills")

REQUIRED_FRONTMATTER = ["name", "description", "version", "author", "license", "metadata"]
REQUIRED_SECTIONS = ["## Trigger", "## Core Concepts"]


def parse_frontmatter(content):
    """Extract and parse YAML frontmatter. Returns (frontmatter_text, body, parsed_dict)."""
    if not content.startswith("---"):
        return None, content, None

    end = content.find("---", 3)
    if end == -1:
        return None, content, None

    fm_text = content[3:end].strip()
    body = content[end+3:].strip()

    # Simple parser
    fm = {}
    current_key = None
    for line in fm_text.split('\n'):
        if not line.strip():
            continue
        if line.startswith('  ') or line.startswith('\t'):
            # continuation or nested
            continue
        if ':' in line:
            key, _, val = line.partition(':')
            key = key.strip()
            val = val.strip()
            if val.startswith('[') and val.endswith(']'):
                val = [v.strip() for v in val[1:-1].split(',')]
            fm[key] = val
            current_key = key

    return fm_text, body, fm


def validate_skill(skill_dir):
    """Validate a single skill directory. Returns list of issues."""
    issues = []
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return [f"Missing SKILL.md in {skill_dir.name}"]

    content = skill_md.read_text(encoding="utf-8")
    fm_text, body, fm = parse_frontmatter(content)

    if fm is None:
        issues.append("Invalid or missing YAML frontmatter")
        return issues

    # Check required fields
    for field in REQUIRED_FRONTMATTER:
        if field not in fm:
            issues.append(f"Missing required field: {field}")

    # Check name matches directory
    if "name" in fm:
        expected = skill_dir.name
        actual = str(fm["name"]).strip()
        if actual != expected:
            issues.append(f"Name mismatch: frontmatter='{actual}', dir='{expected}'")

    # Check tags
    metadata = fm.get("metadata", {})
    if isinstance(metadata, dict):
        hermes = metadata.get("hermes", {})
        if isinstance(hermes, dict):
            tags = hermes.get("tags", [])
            if not tags:
                issues.append("No tags")
            else:
                for tag in tags:
                    if tag != tag.lower():
                        issues.append(f"Tag not lowercase: {tag}")

    # Check body
    if len(body) < 100:
        issues.append(f"Body too short ({len(body)} chars)")
    else:
        for section in REQUIRED_SECTIONS:
            if section not in body:
                issues.append(f"Missing section: {section}")

    return issues


def validate_all(fix=False):
    """Validate all skills. Returns (valid_count, issue_count, issues_by_skill)."""
    skills = sorted(REPO_SKILLS.iterdir())
    valid = 0
    with_issues = 0
    all_issues = {}

    for skill_dir in skills:
        if not skill_dir.is_dir():
            continue
        issues = validate_skill(skill_dir)
        if issues:
            with_issues += 1
            all_issues[skill_dir.name] = issues
            if fix:
                # Attempt common fixes
                pass
        else:
            valid += 1

    return valid, with_issues, all_issues


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', help='Specific skill to validate')
    parser.add_argument('--fix', action='store_true', help='Fix common issues')
    args = parser.parse_args()

    if args.path:
        issues = validate_skill(Path(args.path))
        if issues:
            print(f"Issues ({len(issues)}):")
            for i in issues:
                print(f"  - {i}")
        else:
            print(f"Valid: {args.path}")
        return

    valid, with_issues, all_issues = validate_all(args.fix)
    total = valid + with_issues

    print(f"=== Validation Summary ===")
    print(f"  Total: {total}")
    print(f"  Valid: {valid}")
    print(f"  With issues: {with_issues}")
    print()

    if all_issues:
        # Group by issue type
        from collections import Counter
        issue_types = Counter()
        for issues in all_issues.values():
            for issue in issues:
                # Normalize
                if "Missing required field" in issue:
                    issue_types["Missing required field"] += 1
                elif "Missing section" in issue:
                    issue_types["Missing section"] += 1
                elif "too short" in issue:
                    issue_types["Body too short"] += 1
                elif "Name mismatch" in issue:
                    issue_types["Name mismatch"] += 1
                elif "No tags" in issue:
                    issue_types["No tags"] += 1
                elif "not lowercase" in issue:
                    issue_types["Tag not lowercase"] += 1
                else:
                    issue_types[issue] += 1

        print("Issue breakdown:")
        for issue_type, count in issue_types.most_common(20):
            print(f"  {issue_type}: {count}")


if __name__ == "__main__":
    main()
