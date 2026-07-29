#!/usr/bin/env python3
"""
skill_landscape.py — Analyze skill ecosystem coverage and detect gaps.

Usage:
    python scripts/skill_landscape.py --analyze coverage
    python scripts/skill_landscape.py --analyze gaps
    python scripts/skill_landscape.py --analyze gaps --domain mlops
    python scripts/skill_landscape.py --analyze stale
    python scripts/skill_landscape.py --report full
"""

import json, os, sys, argparse
from collections import defaultdict, Counter
from datetime import datetime, timedelta

HERMES_SKILLS = os.path.expandvars(r'$LOCALAPPDATA/hermes/skills')

# Technology ecosystem definitions for gap analysis
ECOSYSTEMS = {
    "python": {"keywords": ["python", "asyncio", "pytest", "flask", "django", "pandas", "numpy"],
               "expected_count": 25, "domains": ["language", "web", "data", "testing"]},
    "javascript": {"keywords": ["javascript", "node", "npm", "express", "deno"],
                   "expected_count": 20, "domains": ["language", "runtime", "web"]},
    "typescript": {"keywords": ["typescript", "tsconfig", "type"],
                   "expected_count": 15},
    "react": {"keywords": ["react", "jsx", "hooks", "next"],
              "expected_count": 15},
    "kubernetes": {"keywords": ["kubernetes", "k8s", "pod", "helm"],
                   "expected_count": 20},
    "docker": {"keywords": ["docker", "container", "dockerfile", "compose"],
               "expected_count": 10},
    "rust": {"keywords": ["rust", "cargo", "wasm"],
             "expected_count": 15},
    "go": {"keywords": ["golang", "goroutine", "go-"],
           "expected_count": 12},
    "aws": {"keywords": ["aws", "lambda", "s3", "ec2", "iam"],
            "expected_count": 15},
    "security": {"keywords": ["pentest", "exploit", "vuln", "crack", "recon", "malware"],
                 "expected_count": 20},
    "ml": {"keywords": ["pytorch", "tensorflow", "sklearn", "neural", "embedding", "transformer"],
           "expected_count": 25},
}


def scan_skills():
    """Scan all skills and return metadata."""
    skills = []
    for root, dirs, files in os.walk(HERMES_SKILLS):
        if 'SKILL.md' in files and '.hub' not in root:
            rel = os.path.relpath(root, HERMES_SKILLS).replace('\\', '/')
            parts = rel.split('/')
            if parts[0].startswith('.'): continue
            
            # Basic stat
            mtime = os.path.getmtime(os.path.join(root, 'SKILL.md'))
            skills.append({
                "name": parts[-1],
                "category": parts[0],
                "path": rel,
                "last_modified": datetime.fromtimestamp(mtime).isoformat(),
                "age_days": (datetime.now() - datetime.fromtimestamp(mtime)).days,
            })
    
    return skills


def analyze_coverage(skills):
    """Analyze ecosystem coverage."""
    coverage = {}
    for eco_name, eco_def in ECOSYSTEMS.items():
        matching = [s for s in skills 
                    if any(kw in s['name'] or kw in s['category'] for kw in eco_def['keywords'])]
        expected = eco_def['expected_count']
        actual = len(matching)
        coverage[eco_name] = {
            "actual": actual,
            "expected": expected,
            "coverage_pct": round(actual / expected * 100, 1) if expected else 0,
            "status": "good" if actual >= expected else "low" if actual >= expected * 0.5 else "critical",
        }
    return coverage


def find_gaps(skills):
    """Find skill gaps by ecosystem."""
    all_names = {s['name'] for s in skills}
    gaps = []
    
    for eco_name, eco_def in ECOSYSTEMS.items():
        kw = eco_def['keywords'][0]  # primary keyword
        pattern_skills = [f"{kw}-advanced-patterns", f"{kw}-best-practices",
                          f"{kw}-security", f"{kw}-testing", f"{kw}-optimization",
                          f"{kw}-deployment", f"{kw}-api-integration"]
        
        for suggestion in pattern_skills:
            if suggestion not in all_names:
                gaps.append({
                    "ecosystem": eco_name,
                    "suggested_skill": suggestion,
                    "reason": f"standard {eco_name} skill missing",
                    "priority": "high" if eco_name in ["python", "javascript", "security", "ml"] else "medium"
                })
    
    return sorted(gaps, key=lambda g: g["priority"], reverse=True)


def find_stale(skills):
    """Find skills that haven't been updated recently."""
    threshold = 90  # days
    stale = [s for s in skills if s['age_days'] > threshold]
    return sorted(stale, key=lambda s: s['age_days'], reverse=True)


def main():
    parser = argparse.ArgumentParser(description="Skill landscape analysis")
    parser.add_argument("--analyze", choices=["coverage", "gaps", "stale"])
    parser.add_argument("--domain", help="Filter by domain")
    parser.add_argument("--report", choices=["full", "summary"])
    args = parser.parse_args()
    
    skills = scan_skills()
    
    if args.analyze == "coverage":
        coverage = analyze_coverage(skills)
        print(f"{'Ecosystem':<20} {'Actual':>8} {'Expected':>8} {'Status':>10}")
        print("-" * 50)
        for eco, data in sorted(coverage.items()):
            print(f"{eco:<20} {data['actual']:>8} {data['expected']:>8} {data['status']:>10}")
    
    elif args.analyze == "gaps":
        gaps = find_gaps(skills)
        if args.domain:
            gaps = [g for g in gaps if g['ecosystem'] == args.domain]
        print(f"Found {len(gaps)} skill gaps:\n")
        for g in gaps[:30]:
            print(f"  [{g['priority']:>6}] {g['suggested_skill']} ({g['reason']})")
        if len(gaps) > 30:
            print(f"  ... and {len(gaps) - 30} more")
    
    elif args.analyze == "stale":
        stale = find_stale(skills)
        print(f"Found {len(stale)} stale skills (>90 days without update):\n")
        for s in stale[:20]:
            print(f"  {s['path']:<50} {s['age_days']:>4} days ago")
        if len(stale) > 20:
            print(f"  ... and {len(stale) - 20} more")
    
    else:
        # Default: full report
        coverage = analyze_coverage(skills)
        gaps = find_gaps(skills)
        stale = find_stale(skills)
        print(f"📊 SKILL LANDSCAPE REPORT")
        print(f"{'='*60}")
        print(f"Total skills: {len(skills)}")
        print(f"\nCoverage:")
        for eco, data in sorted(coverage.items()):
            print(f"  {eco:<15} {data['actual']:>3}/{data['expected']:<3} ({data['coverage_pct']:.0f}%) {data['status']}")
        print(f"\nGaps: {len(gaps)} (top priority: {len([g for g in gaps if g['priority']=='high'])} high)")
        print(f"Stale: {len(stale)} skills")

if __name__ == "__main__":
    main()
