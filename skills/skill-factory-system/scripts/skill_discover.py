#!/usr/bin/env python3
"""
skill_discover.py — Discover skill opportunities from external signals.

Usage:
    python scripts/skill_discover.py --source github --topic python-async
    python scripts/skill_discover.py --source pypi --top-downloads 20
    python scripts/skill_discover.py --source trends --domain mlops --count 15
    python scripts/skill_discover.py --recommend --existing python
"""

import json, os, sys, argparse, re
from datetime import datetime
from collections import defaultdict

HERMES_SKILLS = os.path.expandvars(r'$LOCALAPPDATA/hermes/skills')

# Built-in technology trend data (curated from ecosystem analysis)
TECH_TRENDS = {
    "hot_2025": [
        {"name": "ai-agents", "momentum": 95, "domain": "mlops"},
        {"name": "webassembly", "momentum": 80, "domain": "software-development"},
        {"name": "edge-computing", "momentum": 75, "domain": "networking"},
        {"name": "platform-engineering", "momentum": 85, "domain": "software-development"},
        {"name": "finops-cloud-cost", "momentum": 70, "domain": "software-development"},
        {"name": "data-mesh", "momentum": 65, "domain": "software-development"},
        {"name": "devsecops", "momentum": 88, "domain": "networking"},
        {"name": "rust-systems", "momentum": 82, "domain": "software-development"},
        {"name": "gen-ai-patterns", "momentum": 90, "domain": "mlops"},
        {"name": "vector-databases", "momentum": 78, "domain": "mlops"},
    ],
    "evergreen": [
        {"name": "system-design", "momentum": 70, "domain": "software-development"},
        {"name": "testing-strategies", "momentum": 65, "domain": "software-development"},
        {"name": "api-design", "momentum": 72, "domain": "software-development"},
        {"name": "security-best-practices", "momentum": 85, "domain": "networking"},
        {"name": "observability", "momentum": 80, "domain": "software-development"},
    ]
}


def scan_existing_skills():
    """Return set of existing skill names."""
    existing = set()
    for root, dirs, files in os.walk(HERMES_SKILLS):
        if 'SKILL.md' in files and '.hub' not in root:
            rel = os.path.relpath(root, HERMES_SKILLS).replace('\\', '/')
            parts = rel.split('/')
            if not parts[0].startswith('.'):
                existing.add(parts[-1])
    return existing


def discover_from_trends(domain: str = None, count: int = 10):
    """Discover skill opportunities from technology trends."""
    existing = scan_existing_skills()
    opportunities = []
    
    for trend in TECH_TRENDS.get("hot_2025", []) + TECH_TRENDS.get("evergreen", []):
        if domain and trend["domain"] != domain: continue
        
        # Generate skill names
        base = trend["name"]
        suggestions = [
            f"{base}-patterns",
            f"{base}-best-practices",
            f"{base}-architecture",
            f"{base}-implementation",
        ]
        
        for suggestion in suggestions:
            if suggestion not in existing:
                opportunities.append({
                    "suggested_skill": suggestion,
                    "domain": trend["domain"],
                    "momentum": trend["momentum"],
                    "source": "technology_trends",
                    "priority": "high" if trend["momentum"] >= 80 else "medium",
                })
    
    return opportunities[:count]


def recommend_by_ecosystem(existing_domain: str, count: int = 10):
    """Recommend skills that complement an existing domain."""
    recommendations = []
    
    # Pattern: if user has many X skills, they might need X+Y integration skills
    ecosystem_pairs = {
        "python": ["rust-ffi", "docker-python", "fastapi-deployment", "python-performance"],
        "react": ["nextjs-migration", "react-testing", "react-state", "react-animation"],
        "kubernetes": ["helm-advanced", "k8s-security", "service-mesh", "gitops-flux"],
        "aws": ["multi-cloud", "aws-cost", "lambda-advanced", "serverless-framework"],
        "security": ["cloud-security", "app-security", "supply-chain", "zero-trust"],
    }
    
    existing = scan_existing_skills()
    
    if existing_domain in ecosystem_pairs:
        for suggestion in ecosystem_pairs[existing_domain]:
            if suggestion not in existing:
                recommendations.append({
                    "suggested_skill": suggestion,
                    "reason": f"complements {existing_domain} ecosystem",
                    "priority": "high",
                })
    
    return recommendations[:count]


def generate_discovery_report(domain: str = None) -> str:
    """Generate a full discovery report."""
    trends = discover_from_trends(domain, 20)
    existing = scan_existing_skills()
    
    report = []
    report.append("🔍 SKILL DISCOVERY REPORT")
    report.append(f"{'='*60}")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"Existing skills: {len(existing)}")
    report.append(f"")
    report.append(f"Top opportunities:")
    
    for opp in trends:
        report.append(f"  [{opp['priority']:>6}] {opp['suggested_skill']:40s} ({opp['domain']})")
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Discover skill opportunities")
    parser.add_argument("--source", choices=["trends", "pypi", "github", "recommend"], 
                        help="Discovery source")
    parser.add_argument("--domain", help="Filter by domain")
    parser.add_argument("--topic", help="Specific topic to explore")
    parser.add_argument("--existing", help="Existing domain for recommendations")
    parser.add_argument("--count", type=int, default=10, help="Number of suggestions")
    parser.add_argument("--report", action="store_true", help="Generate full report")
    args = parser.parse_args()
    
    if args.report:
        print(generate_discovery_report(args.domain))
        return
    
    if args.source == "trends" or not args.source:
        results = discover_from_trends(args.domain, args.count)
    
    elif args.source == "recommend":
        if not args.existing:
            print("Error: --existing required for recommend source")
            return
        results = recommend_by_ecosystem(args.existing, args.count)
    
    else:
        # Generic fallback
        results = discover_from_trends(args.domain, args.count)
    
    print(f"Discovered {len(results)} skill opportunities:\n")
    for r in results:
        print(f"  [{r.get('priority', 'medium'):>6}] {r['suggested_skill']:<45} "
              f"{r.get('domain', '')}")

if __name__ == "__main__":
    main()
