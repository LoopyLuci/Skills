#!/usr/bin/env python3
"""
skill_auto_related.py — Auto-generate related_skills from tag overlap and co-occurrence.

Usage:
    python scripts/skill_auto_related.py --name react-hooks-advanced
    python scripts/skill_auto_related.py --all
    python scripts/skill_auto_related.py --all --dry-run
    python scripts/skill_auto_related.py --rebuild
"""

import os, sys, re, json, argparse
from collections import defaultdict, Counter

HERMES_SKILLS = os.path.expandvars(r'$LOCALAPPDATA/hermes/skills')


def load_skill_tags():
    """Load all skills with their tags and categories."""
    skills = {}
    for root, dirs, files in os.walk(HERMES_SKILLS):
        if 'SKILL.md' in files and '.hub' not in root:
            rel = os.path.relpath(root, HERMES_SKILLS).replace('\\', '/')
            parts = rel.split('/')
            if parts[0].startswith('.'): continue
            
            name = parts[-1]
            path = root
            
            with open(os.path.join(root, 'SKILL.md')) as f:
                content = f.read()
            
            # Extract tags
            tag_match = re.search(r'tags:\s*\[(.*?)\]', content, re.DOTALL)
            tags = []
            if tag_match:
                tag_str = tag_match.group(1)
                tags = [t.strip().strip('"').strip("'") for t in tag_str.split(',')]
            
            # Extract existing related
            rel_match = re.search(r'related_skills:\s*\[(.*?)\]', content, re.DOTALL)
            existing_related = []
            if rel_match:
                rel_str = rel_match.group(1)
                existing_related = [r.strip().strip('"').strip("'") for r in rel_str.split(',') if r.strip()]
            
            skills[name] = {
                "name": name,
                "category": parts[0],
                "path": rel,
                "tags": tags,
                "existing_related": existing_related,
                "content": content,
            }
    
    return skills


def compute_related(skills, target: str, max_suggestions: int = 5) -> list:
    """Compute related skills based on tag overlap + category co-occurrence."""
    target_data = skills.get(target)
    if not target_data: return []
    
    target_tags = set(target_data["tags"])
    target_cat = target_data["category"]
    
    scored = []
    for name, data in skills.items():
        if name == target: continue
        
        score = 0
        
        # Tag overlap
        common_tags = target_tags & set(data["tags"])
        score += len(common_tags) * 3
        
        # Same category bonus
        if data["category"] == target_cat:
            score += 2
        
        # Name similarity (shared root words)
        target_words = set(target.replace("-", "_").split("_"))
        skill_words = set(name.replace("-", "_").split("_"))
        common_words = target_words & skill_words
        score += len(common_words) * 1
        
        if score > 0:
            scored.append((name, score))
    
    scored.sort(key=lambda x: -x[1])
    return [s[0] for s in scored[:max_suggestions]]


def update_related(skills, name: str, new_related: list, dry_run: bool = False) -> bool:
    """Update related_skills in a skill's frontmatter."""
    if name not in skills: return False
    data = skills[name]
    content = data["content"]
    
    related_str = ", ".join(f'"{r}"' for r in new_related)
    
    # Replace existing related_skills or add it
    if 'related_skills:' in content:
        new_content = re.sub(
            r'related_skills:\s*\[.*?\]',
            f'related_skills: [{related_str}]',
            content,
            count=1,
            flags=re.DOTALL
        )
    else:
        new_content = content
    
    if dry_run:
        return True
    
    with open(os.path.join(HERMES_SKILLS, data["path"], 'SKILL.md'), 'w') as f:
        f.write(new_content if 'related_skills:' in content else content)
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Auto-generate related_skills")
    parser.add_argument("--name", help="Update specific skill")
    parser.add_argument("--all", action="store_true", help="Update all skills")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild all from scratch")
    args = parser.parse_args()
    
    skills = load_skill_tags()
    print(f"Loaded {len(skills)} skills with tags")
    
    if args.name:
        related = compute_related(skills, args.name)
        existing = skills[args.name]["existing_related"]
        print(f"\n'{args.name}':")
        print(f"  Existing: {existing}")
        print(f"  Suggested: {related}")
        if not args.dry_run and related:
            update_related(skills, args.name, related)
            print(f"  ✅ Updated")
    
    elif args.all or args.rebuild:
        updated = 0
        skipped = 0
        for name in skills:
            related = compute_related(skills, name)
            if len(related) < 3:  # Need at least 3 suggestions
                skipped += 1
                continue
            
            if args.rebuild or set(related) != set(skills[name]["existing_related"]):
                if update_related(skills, name, related, args.dry_run):
                    updated += 1
                action = "would update" if args.dry_run else "updated"
        
        mode = "Dry run" if args.dry_run else "Updated"
        print(f"{mode}: {updated} skills, {skipped} skipped (insufficient related)")
    
    else:
        # Show stats
        related_counts = defaultdict(int)
        for name, data in skills.items():
            related_counts[len(data.get("existing_related", []))] += 1
        
        print("\nRelated skills distribution:")
        for count, freq in sorted(related_counts.items()):
            bar = "#" * (freq // max(1, max(related_counts.values()) // 20))
            print(f"  {count:>2} related: {freq:>4} skills {bar}")

if __name__ == "__main__":
    main()
