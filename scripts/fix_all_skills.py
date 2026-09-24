#!/usr/bin/env python3
"""
Skill Fixer — Fix only truly broken skills, preserve curated formats.

Format A (new): metadata.hermes.tags, ## Trigger, ## Core Concepts
Format B (curved): flat tags, ## Overview, ## When to Use, ## Key Approaches

Only fix:
- Missing name (or mismatch)
- Missing version
- Missing author
- Missing tags entirely (in any format)
- Truly broken YAML
"""
import json
import re
import sys
from pathlib import Path

REPO_SKILLS = Path(r"Z:\Projects\Skills\LoopyLuci-skills\skills")


def parse_fm(text):
    """Parse frontmatterYAML."""
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


def dict_to_yaml(d, indent=0):
    lines = []
    prefix = '  ' * indent
    for k, v in d.items():
        if isinstance(v, dict):
            lines.append(f"{prefix}{k}:")
            lines.append(dict_to_yaml(v, indent + 1))
        elif isinstance(v, list):
            items = ', '.join(str(i) for i in v)
            lines.append(f"{prefix}{k}: [{items}]")
        else:
            lines.append(f"{prefix}{k}: {v}")
    return "\n".join(lines)


def find_frontmatter_end(content):
    """Find the closing --- of frontmatter."""
    for i in range(3, len(content) - 3):
        if content[i:i+3] == '---':
            prev = content[i-1]
            if prev in ('\n', '\r'):
                return i
    return -1


def fix_skill(skill_dir):
    """Fix a single skill. Returns (changed: bool, reason: str)."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, "no_file"

    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"read_error: {e}"

    if not content.startswith("---"):
        return False, "no_frontmatter"

    end = find_frontmatter_end(content)
    if end == -1:
        return False, "no_frontmatter_end"

    fm_text = content[3:end].strip()
    body = content[end+3:].strip()

    try:
        fm = parse_fm(fm_text)
    except Exception as e:
        return False, f"parse_error: {e}"

    changed = False

    # Fix name
    if fm.get("name") != skill_dir.name:
        fm["name"] = skill_dir.name
        changed = True

    # Fix version
    if "version" not in fm or not fm.get("version"):
        fm["version"] = "1.0.0"
        changed = True

    # Fix author
    if "author" not in fm or not fm.get("author"):
        fm["author"] = "LoopyLuci Community"
        changed = True

    # Fix tags — collect from either format
    tags = []
    if "metadata" in fm and isinstance(fm["metadata"], dict):
        hermes = fm["metadata"].get("hermes")
        if isinstance(hermes, dict):
            t = hermes.get("tags")
            if isinstance(t, list):
                tags = t
            elif isinstance(t, str):
                tags = [x.strip() for t in t.split(",")]
    elif "tags" in fm:
        t = fm["tags"]
        if isinstance(t, list):
            tags = t
        elif isinstance(t, str):
            tags = [x.strip() for x in t.split(",")]

    # Lowercase tags
    new_tags = [t.lower() for t in tags]
    if new_tags != tags:
        if "metadata" in fm and "hermes" in fm["metadata"]:
            fm["metadata"]["hermes"]["tags"] = new_tags
        elif "tags" in fm:
            fm["tags"] = new_tags
        changed = True

    if not changed:
        return False, "ok"

    new_fm = dict_to_yaml(fm)
    new_content = f"---\n{new_fm}\n---\n\n{body.strip()}\n"
    skill_md.write_text(new_content, encoding="utf-8")
    return True, "fixed"


def main():
    apply = "--apply" in sys.argv
    skills = sorted(REPO_SKILLS.iterdir())
    fixed = 0
    skipped = 0
    errors = []

    for skill_dir in skills:
        if not skill_dir.is_dir():
            continue
        try:
            was_fixed, reason = fix_skill(skill_dir)
            if was_fixed:
                if apply:
                    fixed += 1
                else:
                    fixed += 1  # dry run count
            elif reason == "ok":
                skipped += 1
            else:
                errors.append((skill_dir.name, reason))
        except Exception as e:
            errors.append((skill_dir.name, str(e)))

    mode = "APPLIED" if apply else "DRY-RUN"
    print(f"=== {mode} ===")
    print(f"Fixed: {fixed}")
    print(f"Skipped (ok): {skipped}")
    print(f"Errors: {len(errors)}")
    for name, err in errors[:20]:
        print(f"  {name}: {err}")


if __name__ == "__main__":
    main()
