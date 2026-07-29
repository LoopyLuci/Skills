---
name: skill-ecosystem-cataloging
description: "Use when cataloging and organizing skill ecosystems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meta, skill-ecosystem, cataloging, organization, taxonomy, mapping]
    related_skills: [skill-architecture-patterns, skill-gap-analysis, skill-inventory-management, skill-discovery-techniques]
---

# Skill Ecosystem Cataloging

Cataloging and organizing skill ecosystems — from taxonomy development and category naming through skill relationships, navigation paths, and portfolio management.

## When to Use

- Organizing a large skill inventory
- Designing skill categories and subcategories
- Building skill navigation and discovery
- Analyzing skill portfolio balance
- Planning skill taxonomy evolution

## Ecosystem Mapping

```python
from typing import Dict, List, Set
from collections import defaultdict

class SkillEcosystem:
    """Map and analyze a skill ecosystem."""
    
    ECOSYSTEM_LAYERS = {
        'foundation': 'Core concepts (programming basics, CS fundamentals)',
        'language': 'Programming languages and runtimes',
        'framework': 'Application frameworks and libraries',
        'platform': 'Platforms and infrastructure',
        'integration': 'Cross-cutting patterns and integrations',
        'domain': 'Domain-specific knowledge and practices',
    }
    
    def __init__(self):
        self.categories = defaultdict(set)
        self.skill_metadata = {}
    
    def catalog_skill(self, name: str, category: str, 
                       layer: str, tags: List[str]):
        self.skill_metadata[name] = {
            'category': category,
            'layer': layer,
            'tags': tags,
            'related': [],
        }
        self.categories[category].add(name)
    
    def portfolio_balance(self) -> Dict:
        """Analyze distribution across ecosystem layers."""
        layer_counts = defaultdict(int)
        for meta in self.skill_metadata.values():
            layer_counts[meta['layer']] += 1
        
        total = sum(layer_counts.values()) or 1
        return {
            layer: {
                'count': count,
                'pct': round(count / total * 100, 1),
            }
            for layer, count in sorted(layer_counts.items())
        }
    
    def coverage_gaps(self) -> List[str]:
        """Find underrepresented ecosystem layers."""
        balance = self.portfolio_balance()
        gaps = []
        for layer, expected in {'foundation': 15, 'language': 20, 
                                 'framework': 30, 'domain': 15}.items():
            actual = balance.get(layer, {}).get('pct', 0)
            if actual < expected:
                gaps.append(f"{layer}: {actual}% (target {expected}%)")
        return gaps
```

## Taxonomy Principles

```python
TAXONOMY_PRINCIPLES = {
    'mutual_exclusivity': 'A skill belongs to exactly one primary category',
    'hierarchical_depth': 'Max 3 levels deep (Cat → Subcat → Skill)',
    'consistent_naming': 'Nouns for categories, verb-phrases for skill descriptions',
    'future_room': 'Categories should allow growth without restructuring',
    'user_mental_model': 'Categories match how users think about the domain',
}
```

## Common Pitfalls

1. **Over-categorization** — too many small categories make navigation harder
2. **Inconsistent naming** — some categories are technology names, others are concepts
3. **Skills in multiple categories** — confusion about where a skill lives
4. **No cross-links** — categories are silos; cross-reference between categories
5. **Rigid taxonomy** — categories don't evolve with new technologies

## Verification Checklist

- [ ] Category names are consistent and self-explanatory
- [ ] Each skill maps to exactly one primary category
- [ ] Cross-category navigation links exist
- [ ] Category balance is healthy (no single category > 50%)
- [ ] Taxonomy allows room for 2x growth
- [ ] User can find a skill in ≤3 clicks
- [ ] Categories reviewed and updated annually
