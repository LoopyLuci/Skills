---
name: skill-content-optimization
description: "Use when optimizing skill content quality and density."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meta, skill-content, optimization, quality, density, readability]
    related_skills: [skill-quality-standards, skill-blueprint-generator, skill-testing-automation, technical-writing-patterns]
---

# Skill Content Optimization

Optimizing skill content for maximum usefulness — balancing depth and conciseness, choosing effective code examples, and structuring for readability.

## When to Use

- Reviewing skill content for quality
- Optimizing existing skills for clarity
- Balancing depth vs. conciseness
- Choosing effective code examples
- Writing for both beginners and experts

## Content Optimization Framework

```python
class SkillContentOptimizer:
    """Analyze and improve skill content."""
    
    DENSITY_WEIGHTS = {
        'code_examples': 0.30,    # 30% should be executable patterns
        'explanations': 0.25,     # 25% clear prose
        'pitfalls': 0.20,         # 20% real-world failure modes
        'checklists': 0.15,       # 15% actionable verification items
        'references': 0.10,       # 10% related skills
    }
    
    @staticmethod
    def analyze_skill(skill_md: str) -> Dict:
        """Analyze a skill's content composition."""
        import re
        lines = skill_md.split('\n')
        
        code_lines = 0
        in_code = False
        for line in lines:
            if line.startswith('```'): in_code = not in_code
            elif in_code: code_lines += 1
        
        total = len(lines)
        code_pct = code_lines / max(total, 1)
        
        has_code = bool(re.search(r'```', skill_md))
        has_pitfalls = '## Common Pitfalls' in skill_md
        has_checklist = '## Verification Checklist' in skill_md
        has_see_also = '## See Also' in skill_md
        
        score = 0
        if has_code: score += 25
        if has_pitfalls: score += 25
        if has_checklist: score += 25
        if has_see_also: score += 15
        if 0.2 <= code_pct <= 0.4: score += 10
        
        return {
            'code_ratio': round(code_pct, 2),
            'has_code': has_code,
            'has_pitfalls': has_pitfalls,
            'has_checklist': has_checklist,
            'has_see_also': has_see_also,
            'quality_score': score,
            'verdict': 'excellent' if score >= 90 else 'good' if score >= 70 else 'needs_work',
        }
```

## Content Density Guidelines

```python
GUIDELINES = {
    'description': 'Exactly 1 sentence starting with "Use when", ≤60 chars, ends with period',
    'frontmatter': 'Name (kebab-case), version, author, 3-8 tags, related_skills',
    'when_to_use': '3-6 bullet points with specific scenarios, not generic',
    'code_examples': '2-5 executable patterns, not pseudo-code, with imports and comments',
    'pitfalls': '4-7 items with specific explanations, not generic warnings',
    'checklist': '5-10 actionable items starting with [ ] that can be verified',
    'see_also': '3-5 related skills with brief "why" explanation',
}
```

## Common Pitfalls

1. **Too much code, no explanations** — code without context is useless; explain the "why"
2. **Too verbose** — skills should be referenceable, not novels; use bullet points
3. **No real-world patterns** — abstract examples don't help; use concrete, practical scenarios
4. **Checklist items not testable** — "Think about X" is not verifiable; "X is configured" is
5. **Missing imports and context** — code snippets that don't compile aren't useful

## Verification Checklist

- [ ] Description fits 60 chars with "Use when" prefix
- [ ] Code examples are executable (include imports, full functions)
- [ ] Pitfalls are specific and actionable (not generic warnings)
- [ ] Checklist items are testable binary states
- [ ] Content ratio: 20-40% code, 25-35% explanation, 15-25% pitfalls/checklist
- [ ] See Also references 3-5 skills that exist in the system
- [ ] Tags include both domain-specific and integration keywords
