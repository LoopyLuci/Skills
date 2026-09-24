#!/usr/bin/env python3
"""
Comprehensive Skill Fixer — Debug version to find problematic skills.
"""
import json
import re
import sys
from pathlib import Path

REPO_SKILLS = Path(r"Z:\Projects\Skills\LoopyLuci-skills\skills")

errors = []


def parse_yaml_fm(text):
    """Parse nested YAML frontmatter into a dict. Handles 2 levels of nesting."""
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


def fix_skill(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, "no_skill_md"

    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"read_error: {e}"

    if not content.startswith("---"):
        return False, "no_frontmatter_start"

    # Find the closing --- (handle both \n and \r\n)
    end = -1
    for i in range(3, len(content)):
        if content[i:i+3] == '---' and (content[max(0,i-1)] in ('\n', '\r')):
            end = i
            break
    
    if end == -1:
        return False, "no_frontmatter_end"

    frontmatter_text = content[3:end].strip()
    body = content[end+3:].strip()

    try:
        fm = parse_yaml_fm(frontmatter_text)
    except Exception as e:
        return False, f"parse_error: {e}"

    changed = False

    # Fix 1: Name
    if fm.get("name") != skill_dir.name:
        fm["name"] = skill_dir.name
        changed = True

    # Fix 2: Version
    if "version" not in fm or not fm.get("version"):
        fm["version"] = "1.0.0"
        changed = True

    # Fix 3: Author
    if "author" not in fm or not fm.get("author"):
        fm["author"] = "LoopyLuci Community"
        changed = True

    # Fix 4: Tags
    tags = []
    metadata = fm.get("metadata")
    if isinstance(metadata, dict):
        hermes = metadata.get("hermes")
        if isinstance(hermes, dict):
            tags_val = hermes.get("tags")
            if isinstance(tags_val, list):
                tags = tags_val
            elif isinstance(tags_val, str):
                tags = [t.strip() for t in tags_val.split(",")]

    if not tags and "tags" in fm:
        tags_val = fm["tags"]
        if isinstance(tags_val, list):
            tags = tags_val
        elif isinstance(tags_val, str):
            tags = [t.strip() for t in tags_val.split(",")]
        del fm["tags"]
        fm["metadata"] = {"hermes": {"tags": tags}}
        changed = True

    if not tags:
        name_parts = skill_dir.name.split("-")
        tags = name_parts[:3] if len(name_parts) >= 3 else name_parts
        if "metadata" not in fm:
            fm["metadata"] = {"hermes": {"tags": tags}}
        else:
            fm["metadata"]["hermes"] = {"tags": tags}
        changed = True

    new_tags = [t.lower() for t in tags]
    if new_tags != tags:
        if "metadata" not in fm:
            fm["metadata"] = {"hermes": {"tags": new_tags}}
        elif "hermes" not in fm["metadata"]:
            fm["metadata"]["hermes"] = {"tags": new_tags}
        else:
            fm["metadata"]["hermes"]["tags"] = new_tags
        changed = True

    if not changed:
        return False, "no_changes"

    # Write
    new_fm = dict_to_yaml(fm)
    new_content = f"---\n{new_fm}\n---\n\n{body.strip()}\n"
    skill_md.write_text(new_content, encoding="utf-8")
    return True, "ok"


def main():
    skills = sorted(REPO_SKILLS.iterdir())
    fixed = 0
    error_list = []

    for skill_dir in skills:
        if not skill_dir.is_dir():
            continue
        try:
            was_fixed, status = fix_skill(skill_dir)
            if was_fixed:
                fixed += 1
            elif status not in ("no_changes", "no_skill_md"):
                error_list.append((skill_dir.name, status))
        except Exception as e:
            error_list.append((skill_dir.name, str(e)))

    print(f"Fixed: {fixed}")
    print(f"Errors: {len(error_list)}")
    for name, err in error_list[:30]:
        print(f"  {name}: {err}")


if __name__ == "__main__":
    main()
