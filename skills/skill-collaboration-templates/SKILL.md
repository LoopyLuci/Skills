---
name: skill-collaboration-templates
description: "Use when creating collaborative skill authoring templates."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meta, skill-collaboration, templates, teamwork, review, co-authoring]
    related_skills: [skill-authoring-workflows, skill-review-feedback-loops, skill-template-catalog, skill-quality-standards]
---

# Skill Collaboration Templates

Enabling collaborative skill authoring — from team-based creation through review assignments, version control, and handoff workflows.

## When to Use

- Multiple authors working on skill inventory
- Required peer review for skill quality
- Handoff between research, writing, and review roles
- Managing skill contributions from community

## Collaboration Workflow

```python
class SkillCollaboration:
    """Manage collaborative skill authoring."""
    
    ROLES = ['researcher', 'writer', 'reviewer', 'editor', 'publisher']
    
    def __init__(self):
        self.tasks = []
        self.workflow = []
    
    def assign_task(self, skill: str, role: str, assignee: str):
        self.tasks.append({
            'skill': skill, 'role': role,
            'assignee': assignee, 'status': 'pending',
        })
    
    def workflow_status(self, skill: str) -> List[Dict]:
        return [t for t in self.tasks if t['skill'] == skill]
    
    def review_assignment(self, skill_count: int, reviewers: int) -> Dict:
        """Distribute review load evenly."""
        per_reviewer = max(1, skill_count // reviewers)
        return {'skills_per_reviewer': per_reviewer, 'total_reviews': skill_count}
```

## Collaboration Templates

```python
TEMPLATES = {
    'skill_research': """
## Research Brief
- Technology name and version
- Key patterns to cover (3-5)
- Common pitfalls from docs/forums
- Existing skills in the ecosystem
- Target audience
""",
    'skill_review': """
## Review Checklist
- [ ] Technical accuracy verified
- [ ] Code examples execute correctly
- [ ] Pitfalls are accurate and relevant
- [ ] Checklist items are testable
- [ ] related_skills all exist
- [ ] Description fits 60 char limit
""",
}
```

## Common Pitfalls

1. **No clear ownership** — skills without assigned authors/owners don't get maintained
2. **Review bottlenecks** — all reviews go to one person; distribute across team
3. **Version conflicts** — concurrent edits on same skill; use clear handoffs
4. **Context switching** — authors switching between 10+ skill drafts is inefficient
5. **Inconsistent voice** — multiple authors without style guide produce uneven content

## Verification Checklist

- [ ] Clear ownership assigned per skill or category
- [ ] Review tools and checklists defined
- [ ] Handoff workflow documented (research → write → review → publish)
- [ ] Style guide for consistent voice and terminology
- [ ] Review load distributed across team
- [ ] Collaboration tooling (shared drafts, comments, version history)
- [ ] SLA for review turnaround time
