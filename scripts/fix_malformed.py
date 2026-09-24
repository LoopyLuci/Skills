#!/usr/bin/env python3
"""
Quick fix for the 2 malformed skills + cleanup.
"""
import json
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


def fix_malformed(skill_dir):
    """Fix skills that have description before --- or other malformation."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, "no_file"

    content = skill_md.read_text(encoding="utf-8")
    
    # Case 1: starts with "description:" instead of "---"
    if content.startswith("description:"):
        # Extract description value
        match = re.match(r'^description:\s*(.+)', content)
        desc = match.group(1).strip().strip('"').strip("'") if match else ""
        
        # Get body (everything after the first ---)
        end = content.find("\n---")
        if end == -1:
            end = content.find("\r\n---")
        if end == -1:
            body = ""
        else:
            body = content[end+3:].strip()
        
        # Build proper frontmatter
        fm = {
            "name": skill_dir.name,
            "description": desc,
            "version": "1.0.0",
            "author": "LoopyLuci Community",
            "license": "MIT",
            "platforms": ["any"],
            "metadata": {
                "hermes": {
                    "tags": [skill_dir.name.split("-")[0], "general"]
                }
            }
        }
        
        new_fm = dict_to_yaml(fm)
        new_content = f"---\n{new_fm}\n---\n\n{body.strip()}\n"
        skill_md.write_text(new_content, encoding="utf-8")
        return True, "fixed_description_first"

    return False, "ok"


def main():
    skills = sorted(REPO_SKILLS.iterdir())
    fixed = 0
    
    for skill_dir in skills:
        if not skill_dir.is_dir():
            continue
        
        # Check for empty "skills" directory (the word itself)
        if skill_dir.name == "skills":
            # This is a stray directory, not a skill
            print(f"  Removing stray 'skills' directory")
            import shutil
            shutil.rmtree(skill_dir)
            fixed += 1
            continue
        
        was_fixed, reason = fix_malformed(skill_dir)
        if was_fixed:
            print(f"  Fixed {skill_dir.name}: {reason}")
            fixed += 1
    
    print(f"\nTotal fixed: {fixed}")


if __name__ == "__main__":
    import re
    main()
