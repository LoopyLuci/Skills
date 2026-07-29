#!/usr/bin/env python3
"""
skill_quality_score.py — Score skill quality (0-100) with detailed report.

Usage:
    python scripts/skill_quality_score.py --name python-async-patterns
    python scripts/skill_quality_score.py --all
    python scripts/skill_quality_score.py --all --min-score 70
    python scripts/skill_quality_score.py --category mlops
"""

import os, sys, re, argparse
from collections import defaultdict

HERMES_SKILLS = os.path.expandvars(r'$LOCALAPPDATA/hermes/skills')

def score_skill(skill_path: str) -> dict:
    """Score a single skill's quality."""
    with open(os.path.join(skill_path, 'SKILL.md')) as f:
        content = f.read()
    
    score = 0
    issues = []
    
    # Frontmatter (20 points)
    if content.startswith('---'):
        fm = content.split('---')[1] if '---' in content else ''
        if 'name:' in fm: score += 4
        else: issues.append("Missing 'name' in frontmatter")
        if 'description:' in fm: score += 4
        else: issues.append("Missing 'description' in frontmatter")
        if 'version:' in fm: score += 2; score += 2
        if 'tags:' in fm: score += 4
        else: issues.append("Missing 'tags' in frontmatter")
        if 'related_skills:' in fm: score += 4
        else: issues.append("Missing 'related_skills' in frontmatter")
    else:
        issues.append("Missing YAML frontmatter")
    
    # Description check (5 points)
    desc_match = re.search(r'description:\s*"([^"]+)"', content)
    if desc_match:
        desc = desc_match.group(1)
        if desc.startswith('Use when'): score += 3
        else: issues.append("Description should start with 'Use when'")
        if len(desc) <= 60: score += 2
        else: issues.append(f"Description too long ({len(desc)} chars, max 60)")
    else:
        issues.append("Could not read description")
    
    # Structure (30 points)
    if '## When to Use' in content or '## Core' in content: score += 5
    else: issues.append("Missing main content section")
    if '## Common Pitfalls' in content: score += 10
    else: issues.append("Missing 'Common Pitfalls' section (-10)")
    if '## Verification Checklist' in content: score += 10
    else: issues.append("Missing 'Verification Checklist' section (-10)")
    if '## See Also' in content: score += 5
    else: issues.append("Missing 'See Also' section (-5)")
    
    # Code examples (25 points)
    code_blocks = re.findall(r'```', content)
    if len(code_blocks) >= 2:  # at least one pair
        score += 15
        # Check for import statements (suggest real code)
        if re.search(r'import |from |require\(|using ', content): score += 10
        else: issues.append("Code examples may be placeholders (no imports detected)")
    else:
        issues.append("No code examples")
    
    # Checklist quality (10 points)
    checklist_items = re.findall(r'- \[ \]', content)
    if len(checklist_items) >= 3: score += 5
    if len(checklist_items) >= 5: score += 5
    if len(checklist_items) == 0: issues.append("No checklist items")
    
    # Cross-references (10 points)
    if 'related_skills:' in content: score += 5
    see_also_items = re.findall(r'^- \[.+\]|^- [a-z]', content.split('## See Also')[-1] if '## See Also' in content else '')
    if len(see_also_items) >= 3: score += 5
    
    return {
        "score": min(score, 100),
        "issues": issues,
        "grade": "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D" if score >= 40 else "F",
    }


def main():
    parser = argparse.ArgumentParser(description="Score skill quality")
    parser.add_argument("--name", help="Score specific skill by name")
    parser.add_argument("--all", action="store_true", help="Score all skills")
    parser.add_argument("--category", help="Score skills in a category")
    parser.add_argument("--min-score", type=int, default=0, help="Minimum score to show")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    results = {}
    
    for root, dirs, files in os.walk(HERMES_SKILLS):
        if 'SKILL.md' in files and '.hub' not in root:
            rel = os.path.relpath(root, HERMES_SKILLS).replace('\\', '/')
            parts = rel.split('/')
            if parts[0].startswith('.'): continue
            
            skill_name = parts[-1]
            
            if args.name and skill_name != args.name: continue
            if args.category and parts[0] != args.category: continue
            
            result = score_skill(root)
            if result['score'] >= args.min_score:
                results[rel] = result
    
    if args.json:
        print(json.dumps(results, indent=2))
        return
    
    # Table output
    print(f"{'Skill':<50} {'Score':>6} {'Grade':>3}")
    print("-" * 62)
    for path, result in sorted(results.items(), key=lambda x: -x[1]['score']):
        print(f"{path:<50} {result['score']:>6}  {result['grade']:>3}")
    
    if not args.name and not args.category:
        avg = sum(r['score'] for r in results.values()) / max(len(results), 1)
        print(f"\n{'Average':<50} {avg:>5.1f}  ")
        grades = defaultdict(int)
        for r in results.values(): grades[r['grade']] += 1
        print(f"Grade distribution: {dict(grades)}")

if __name__ == "__main__":
    main()
