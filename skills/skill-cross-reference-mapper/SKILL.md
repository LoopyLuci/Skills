---
name: skill-cross-reference-mapper
description: "Use when mapping skill dependencies and cross-references."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skill-cross-reference, dependency-map, graph, relationships, meta]
    related_skills: [skill-inventory-management, skill-quality-standards, meta-skill-patterns]
---

# Skill Cross-Reference Mapper

Mapping dependencies and relationships between skills — from related_skills extraction through dependency graph building, gap analysis, and circular dependency detection.

## When to Use

- Understanding how skills relate to each other
- Finding skill clusters and knowledge domains
- Detecting orphaned skills with no cross-references
- Building skill navigation and discovery tools
- Identifying prerequisites in learning paths

## Reference Mapper

```python
import re, json
from collections import defaultdict

class ReferenceMapper:
    """Map cross-references between skills."""
    
    def __init__(self):
        self.graph = defaultdict(set)  # skill -> [related_skills]
    
    def extract_references(self, skill_md: str, skill_name: str):
        """Extract related_skills from frontmatter."""
        match = re.search(r'related_skills:\s*\[(.*?)\]', skill_md)
        if match:
            refs = [r.strip() for r in match.group(1).split(',')]
            self.graph[skill_name].update(refs)
            for ref in refs:
                self.graph[ref]  # ensure it exists
    
    def find_orphans(self, all_skills: set) -> List[str]:
        """Skills with no incoming references."""
        referenced = set()
        for refs in self.graph.values():
            referenced.update(refs)
        return list(all_skills - referenced)
    
    def detect_cycles(self) -> List[tuple]:
        """Detect circular references (A→B→A)."""
        cycles = []
        for skill, refs in self.graph.items():
            for ref in refs:
                if skill in self.graph.get(ref, set()):
                    cycles.append((skill, ref))
        return cycles
```

## Verification Checklist

- [ ] related_skills extracted from all skills
- [ ] Orphaned skills identified and flagged
- [ ] Circular references detected
- [ ] Cross-reference graph exportable (JSON/DOT)
- [ ] Prerequisite chains visible for learning paths
