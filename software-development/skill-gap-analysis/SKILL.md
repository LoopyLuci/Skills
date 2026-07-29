---
name: skill-gap-analysis
description: "Use when identifying missing skills and opportunities."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meta, skill-gap, analysis, discovery, opportunity, landscape]
    related_skills: [skill-discovery, skill-inventory-management, skill-cross-reference-mapper, skill-blueprint-generator]
---

# Skill Gap Analysis

Systematically identifying missing skills and opportunities — analyzing domains, technology landscapes, user needs, and coverage gaps.

## When to Use

- Finding new skill opportunities
- Assessing skill coverage in a domain
- Planning skill creation sprints
- Identifying underserved topics
- Building comprehensive skill portfolios

## Gap Analysis Framework

```python
from typing import Dict, List, Set
import re

class SkillGapAnalyzer:
    """Identify missing skills across domains."""
    
    DOMAINS = {
        'programming': ['python', 'javascript', 'typescript', 'rust', 'go', 'java', 'csharp', 'kotlin', 'swift'],
        'web': ['react', 'vue', 'angular', 'svelte', 'next', 'nuxt', 'remix', 'astro'],
        'data': ['sql', 'nosql', 'spark', 'kafka', 'pandas', 'polars', 'duckdb'],
        'ml': ['pytorch', 'tensorflow', 'sklearn', 'xgboost', 'transformers', 'diffusers'],
        'cloud': ['aws', 'azure', 'gcp', 'kubernetes', 'docker', 'terraform'],
        'security': ['pentest', 'crypto', 'network-sec', 'app-sec', 'cloud-sec', 'identity'],
        'business': ['marketing', 'sales', 'product', 'finance', 'hr', 'operations'],
    }
    
    @staticmethod
    def find_gaps(skills: Set[str], depth: int = 2) -> List[Dict]:
        """Find coverage gaps in domains."""
        gaps = []
        for domain, keywords in SkillGapAnalyzer.DOMAINS.items():
            for keyword in keywords:
                # Check breadth and depth coverage
                breadth_count = sum(1 for s in skills if keyword in s)
                if breadth_count < depth:
                    gaps.append({
                        'domain': domain,
                        'keyword': keyword,
                        'current_count': breadth_count,
                        'target': depth,
                        'gap': depth - breadth_count,
                        'suggestion': f"Create {depth - breadth_count} more {keyword} skills",
                    })
        return sorted(gaps, key=lambda g: g['gap'], reverse=True)
    
    @staticmethod
    def suggest_skill(domain: str, technology: str, 
                       existing_skills: Set[str]) -> List[str]:
        """Suggest specific skills based on pattern analysis."""
        patterns = [
            f"{technology}-advanced-patterns",
            f"{technology}-best-practices",
            f"{technology}-optimization",
            f"{technology}-security",
            f"{technology}-testing",
            f"{technology}-deployment",
            f"{technology}-api-integration",
        ]
        return [p for p in patterns if p not in existing_skills]
```

## Discovery Methods

```python
DISCOVERY_METHODS = [
    "Scan technology trends (GitHub trending, ProductHunt, tech conferences)",
    "Analyze search queries and user requests",
    "Map technology ecosystems and find missing pieces",
    "Track language/framework version upgrades for new patterns",
    "Cross-reference certification syllabi (AWS, GCP, Azure, CKx)",
    "Audit existing skills for outdated content that needs replacement",
    "Follow thought leaders and OSS maintainers for emerging practices",
    "Parse changelogs of major frameworks for new features",
]
```

## Common Pitfalls

1. **Creating too early** — building skills for unstable technologies that will change
2. **Too narrow** — a skill about one specific function is rarely useful
3. **Too broad** — "Python" is too large for one skill; break into sub-patterns
4. **Redundancy** — multiple skills covering the same ground; merge or distinguish
5. **Ignoring prerequisites** — advanced skills without foundational context

## Verification Checklist

- [ ] Domain coverage assessed against existing skills
- [ ] Technology gaps identified by ecosystem analysis
- [ ] Suggested skills are specific (not "learn programming")
- [ ] Skills fill real user needs (not just "everything needs a skill")
- [ ] No redundancy with existing skills
- [ ] Priority ordered by impact + frequency of use
- [ ] Each gem has at least 3-5 related existing skills to reference
