---
name: skill-discovery-techniques
description: "Use when discovering new skill creation opportunities."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meta, skill-discovery, techniques, research, opportunity, scanning]
    related_skills: [skill-gap-analysis, skill-architecture-patterns, skill-content-optimization, skill-inventory-management]
---

# Skill Discovery Techniques

Systematically discovering new skill creation opportunities — from technology trend scanning and ecosystem mapping through user need analysis and competitive research.

## When to Use

- Finding next skills to create
- Researching emerging technologies
- Mapping skill ecosystems
- Identifying underserved skill areas
- Planning skill creation roadmap

## Discovery Framework

```python
class SkillDiscoveryEngine:
    """Systematic skill discovery from multiple signals."""
    
    SIGNALS = [
        'github_trending_repos',
        'stackoverflow_tags_growth',
        'npm/pypi/crates_downloads',
        'conference_talks_topics',
        'job_postings_skill_demand',
        'hackernews_mentions',
        'reddit_community_discussions',
        'user_search_queries',
        'competitor_skill_inventories',
        'technology_changelogs',
    ]
    
    @staticmethod
    def score_opportunity(name: str, demand: int, existing_supply: int, 
                           growth_rate: float) -> float:
        """Score a skill opportunity by demand-supply gap."""
        if existing_supply == 0:
            return demand * growth_rate * 2  # First mover bonus
        
        saturation = existing_supply / max(demand, 1)
        if saturation > 0.5:
            return 0  # Market saturated
        
        return demand * growth_rate * (1 - saturation)
    
    @staticmethod
    def suggest_from_ecosystem(tech_stack: List[str], 
                                existing: set) -> List[Dict]:
        """Suggest skills from gaps in technology ecosystem coverage."""
        suggestions = []
        combos = [(a, b) for a in tech_stack for b in tech_stack if a < b]
        for t1, t2 in combos:
            integration_name = f"{t1}-{t2}-integration"
            if integration_name not in existing:
                suggestions.append({
                    'name': integration_name,
                    'opportunity': f'{t1} + {t2} integration patterns',
                    'priority': 'high' if t1 in existing and t2 in existing else 'medium',
                })
        return suggestions
```

## Discovery Channels

```python
DISCOVERY_CHANNELS = {
    'technology_watch': [
        'Follow major framework release notes (React, Angular, Vue, K8s)',
        'Monitor new Cloud provider services (re:Invent, Google Cloud Next)',
        'Track new programming language releases and features',
        'Watch AI/ML model releases (HuggingFace, ArXiv)',
    ],
    'demand_signals': [
        'Analyze internal user search queries for skill topics',
        'Monitor community forum questions and gaps',
        'Track StackOverflow tag growth rates',
        'Review job description skill requirements by role',
    ],
    'ecosystem_mapping': [
        'Map technology landscape for missing pieces',
        'Identify integration points between technologies',
        'Find "connector" skills (how A works with B)',
        'Document migrations (legacy → modern patterns)',
    ],
    'user_pain_points': [
        'Common errors and gotchas (great pitfall content)',
        'Installation and configuration challenges',
        'Performance issues that need optimization patterns',
        'Security vulnerabilities requiring mitigation skills',
    ],
}
```

## Common Pitfalls

1. **Chasing hype** — creating skills for trends that won't last; wait for stabilization
2. **No user validation** — creating skills nobody needs; check search demand first
3. **Ignoring existing content** — duplicating what already exists
4. **Too narrow** — a skill about one specific API parameter is useless
5. **Timing mismatch** — too early (unstable API) or too late (already commoditized)

## Verification Checklist

- [ ] Demand signal confirmed (searches, questions, job posts)
- [ ] Technology is stable enough (not breaking weekly)
- [ ] No existing skill covers the same ground
- [ ] Skill fits into the broader architecture (has prerequisite/related skills)
- [ ] Topic has enough depth for a meaningful skill (not one-paragraph content)
- [ ] Target audience identified (beginner, intermediate, advanced)
- [ ] At least 3 related_skills exist for cross-referencing
