#!/usr/bin/env python3
"""
skill_bulk_manage.py — Bulk operations on skills (move, tag, validate, report).

Usage:
    python scripts/skill_bulk_manage.py --action move --from productivity --to software-development --name python-*
    python scripts/skill_bulk_manage.py --action tag --add "async,coroutines" --filter "python-async*"
    python scripts/skill_bulk_manage.py --action validate --all
    python scripts/skill_bulk_manage.py --action report --format csv
    python scripts/skill_bulk_manage.py --action deduplicate
"""

import os, sys, re, json, argparse, shutil, fnmatch
from collections import defaultdict

HERMES_SKILLS = os.path.expandvars(r'$LOCALAPPDATA/hermes/skills')


def find_skills(pattern: str = "*", category: str = None):
    """Find skills matching a pattern."""
    results = []
    for root, dirs, files in os.walk(HERMES_SKILLS):
        if 'SKILL.md' in files and '.hub' not in root:
            rel = os.path.relpath(root, HERMES_SKILLS).replace('\\', '/')
            parts = rel.split('/')
            if parts[0].startswith('.'): continue
            
            name = parts[-1]
            if not fnmatch.fnmatch(name, pattern): continue
            if category and parts[0] != category: continue
            
            results.append({"name": name, "category": parts[0], "path": rel, "full_path": root})
    return results


def action_move(skills, target_cat: str, dry_run: bool = False):
    """Move skills to a different category."""
    moved = 0
    for skill in skills:
        src = skill["full_path"]
        dst = os.path.join(HERMES_SKILLS, target_cat, skill["name"])
        if os.path.exists(dst):
            print(f"  ⚠️  {skill['name']}: target exists, skipping")
            continue
        
        if dry_run:
            print(f"  📦 {skill['name']}: {skill['category']} → {target_cat}")
            moved += 1
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            moved += 1
    
    return moved


def action_tag(skills, add_tags: list = None, remove_tags: list = None, dry_run: bool = False):
    """Add or remove tags from skills."""
    tagged = 0
    for skill in skills:
        md_path = os.path.join(skill["full_path"], 'SKILL.md')
        with open(md_path) as f:
            content = f.read()
        
        # Find existing tags
        tag_match = re.search(r'tags:\s*\[(.*?)\]', content, re.DOTALL)
        if not tag_match: continue
        
        current_tags = [t.strip().strip('"').strip("'") for t in tag_match.group(1).split(',')]
        original = current_tags.copy()
        
        if add_tags:
            for t in add_tags:
                if t not in current_tags: current_tags.append(t)
        
        if remove_tags:
            current_tags = [t for t in current_tags if t not in remove_tags]
        
        if set(current_tags) == set(original): continue
        
        new_tag_str = ", ".join(f'"{t}"' for t in current_tags)
        new_content = content.replace(
            f'tags: [{tag_match.group(1)}]',
            f'tags: [{new_tag_str}]'
        )
        
        if dry_run:
            print(f"  🏷️  {skill['name']}: {set(current_tags) - set(original)}")
        else:
            with open(md_path, 'w') as f: f.write(new_content)
        
        tagged += 1
    
    return tagged


def action_validate(skills):
    """Run quality checks on skills."""
    issues = []
    for skill in skills:
        md_path = os.path.join(skill["full_path"], 'SKILL.md')
        with open(md_path) as f:
            content = f.read()
        
        skill_issues = []
        if '## Common Pitfalls' not in content: skill_issues.append("no_pitfalls")
        if '## Verification Checklist' not in content: skill_issues.append("no_checklist")
        if '```' not in content: skill_issues.append("no_code")
        if 'description:' not in content: skill_issues.append("no_description")
        if 'related_skills:' not in content: skill_issues.append("no_related")
        
        if skill_issues:
            issues.append({"skill": skill["name"], "issues": skill_issues})
    
    return issues


def action_report(skills, fmt: str = "text"):
    """Generate a comprehensive skill inventory report."""
    cats = defaultdict(list)
    for s in skills:
        cats[s["category"]].append(s["name"])
    
    lines = []
    lines.append(f"SKILL INVENTORY REPORT")
    lines.append(f"{'='*60}")
    lines.append(f"Total skills: {len(skills)}")
    lines.append(f"Categories: {len(cats)}")
    lines.append("")
    
    for cat in sorted(cats):
        names = cats[cat]
        lines.append(f"  {cat}: {len(names)}")
    
    if fmt == "csv":
        print("category,skill_name")
        for cat in sorted(cats):
            for name in cats[cat]:
                print(f"{cat},{name}")
        return
    
    return "\n".join(lines)


def action_deduplicate(skills):
    """Find and report duplicate skill names across categories."""
    by_name = defaultdict(list)
    for s in skills:
        by_name[s["name"]].append(s["category"])
    
    dups = {n: cats for n, cats in by_name.items() if len(cats) > 1}
    removed = 0
    
    for name, cats in dups.items():
        # Keep the one in the most appropriate category
        priority = ["software-development", "networking", "mlops", "productivity"]
        keep_cat = None
        for p in priority:
            if p in cats:
                keep_cat = p
                break
        if not keep_cat:
            keep_cat = cats[0]
        
        for cat in cats:
            if cat != keep_cat:
                path = os.path.join(HERMES_SKILLS, cat, name)
                if os.path.exists(path):
                    shutil.rmtree(path)
                    removed += 1
    
    return removed


def main():
    parser = argparse.ArgumentParser(description="Bulk skill management")
    parser.add_argument("--action", required=True,
                        choices=["move", "tag", "validate", "report", "deduplicate"])
    parser.add_argument("--name", default="*", help="Skill name pattern")
    parser.add_argument("--category", help="Source category filter")
    parser.add_argument("--from", dest="from_cat", help="Source category (move)")
    parser.add_argument("--to", help="Target category (move)")
    parser.add_argument("--add", help="Comma-separated tags to add")
    parser.add_argument("--remove", help="Comma-separated tags to remove")
    parser.add_argument("--format", choices=["text", "csv"], default="text")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    
    if args.all:
        skills = find_skills("*")
    else:
        skills = find_skills(args.name, args.category)
    
    print(f"Found {len(skills)} matching skills\n")
    
    if args.action == "move":
        if not args.to:
            print("Error: --to required for move action")
            return
        count = action_move(skills, args.to, args.dry_run)
        print(f"\n{'Would move' if args.dry_run else 'Moved'} {count} skills to '{args.to}'")
    
    elif args.action == "tag":
        add_tags = [t.strip() for t in args.add.split(",")] if args.add else None
        remove_tags = [t.strip() for t in args.remove.split(",")] if args.remove else None
        count = action_tag(skills, add_tags, remove_tags, args.dry_run)
        print(f"\n{'Would update' if args.dry_run else 'Updated'} tags on {count} skills")
    
    elif args.action == "validate":
        issues = action_validate(skills)
        print(f"Skills with issues: {len(issues)}")
        for s in issues[:20]:
            print(f"  ⚠️  {s['skill']}: {', '.join(s['issues'])}")
    
    elif args.action == "report":
        result = action_report(skills, args.format)
        if result: print(result)
    
    elif args.action == "deduplicate":
        count = action_deduplicate(skills)
        print(f"Removed {count} duplicate skill copies")

if __name__ == "__main__":
    main()
