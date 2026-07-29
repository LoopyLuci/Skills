---
name: skill-architecture-patterns
description: "Use when designing multi-skill architectures."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meta, skill-architecture, patterns, design, multi-skill, systems]
    related_skills: [skill-architecture-planning, skill-content-optimization, skill-gap-analysis, meta-skill-patterns]
---

# Skill Architecture Patterns

Designing multi-skill architectures — from skill families and dependency graphs through progressive complexity, cross-cutting skills, and skill ecosystems.

## When to Use

- Designing a suite of related skills
- Building skill hierarchies (foundation → intermediate → advanced)
- Creating cross-cutting skill categories
- Managing skill dependencies and prerequisites
- Designing learning paths through skills

## Architecture Patterns

```python
ARCHITECTURE_PATTERNS = {
    'progressive_depth': 'Foundation → Intermediate → Advanced → Expert — each level builds on previous',
    'radial_coverage': 'Core technology in center, integration skills radiating outward',
    'cross_cutting': 'Skills that span multiple domains (security, observability, testing)',
    'ecosystem_map': 'Full technology landscape mapped as interconnected skill graph',
}

class SkillArchitect:
    """Design skill architectures and learning paths."""
    
    def __init__(self):
        self.skills = {}
        self.relationships = {}  # skill -> [prerequisite_skills]
    
    def add_skill(self, name: str, level: str = 'intermediate'):
        self.skills[name] = {'level': level, 'prerequisites': []}
    
    def add_prerequisite(self, skill: str, prerequisite: str):
        if skill in self.skills and prerequisite in self.skills:
            self.skills[skill]['prerequisites'].append(prerequisite)
    
    def generate_learning_path(self, target_skill: str) -> List[str]:
        """Generate ordered learning path to a target skill."""
        path = []
        visited = set()
        
        def dfs(skill):
            if skill in visited: return
            visited.add(skill)
            for prereq in self.skills.get(skill, {}).get('prerequisites', []):
                dfs(prereq)
            path.append(skill)
        
        dfs(target_skill)
        return path
    
    def detect_cycles(self) -> List[tuple]:
        """Detect circular prerequisite chains."""
        cycles = []
        for skill in self.skills:
            visited = set()
            def dfs(s, path):
                if s in path:
                    idx = path.index(s)
                    cycles.append((' -> '.join(path[idx:] + [s]),))
                    return
                if s in visited: return
                visited.add(s)
                for p in self.skills.get(s, {}).get('prerequisites', []):
                    dfs(p, path + [s])
            dfs(skill, [skill])
        return cycles
```

## Architecture Patterns

```python
PATTERNS = {
    'foundation_layer': {
        'description': 'Core concepts that don't change much',
        'example': 'python-basics, git-fundamentals, sql-basics',
        'update_frequency': 'Low (yearly)',
    },
    'technology_deep_dive': {
        'description': 'Specific technology patterns and best practices',
        'example': 'react-hooks-advanced, dockerfile-best-practices',
        'update_frequency': 'Medium (quarterly)',
    },
    'integration_patterns': {
        'description': 'How technologies work together',
        'example': 'react-graphql-integration, docker-aws-deployment',
        'update_frequency': 'High (monthly)',
    },
    'cross_cutting': {
        'description': 'Spans all technology levels (security, testing)',
        'example': 'web-security-patterns, api-testing-contracts',
        'update_frequency': 'Medium',
    },
}
```

## Common Pitfalls

1. **No progression** — jump from beginner to advanced without intermediate steps
2. **Circular dependencies** — skill A requires B, B requires A; redesign hierarchy
3. **Orphan skills** — skills that reference non-existent prerequisites
4. **Flat landscape** — all skills at same depth without progression structure
5. **Overlapping scope** — two skills covering the same 80% of content

## Verification Checklist

- [ ] Skill hierarchy defined (foundation → intermediate → advanced)
- [ ] Prerequisites mapped and non-circular
- [ ] Each skill has 3-5 related_skills for navigation
- [ ] Cross-cutting skills identified and linked to all affected domains
- [ ] Learning paths generate correctly from any start point
- [ ] No orphan skills (zero incoming or outgoing references)
- [ ] Update frequency assigned to match technology velocity
