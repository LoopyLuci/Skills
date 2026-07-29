---
name: skill-authoring-workflows
description: "Use when designing efficient skill authoring workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meta, skill-authoring, workflow, efficiency, templates, batch]
    related_skills: [skill-blueprint-generator, skill-template-catalog, skill-content-optimization, skill-quality-standards]
---

# Skill Authoring Workflows

Designing efficient workflows for creating skills at scale — from batch creation strategies through template pipelines, review cycles, and publishing.

## When to Use

- Creating skills efficiently at scale
- Designing repeatable authoring processes
- Batch-creating related skills
- Building skill creation pipelines
- Training new skill authors

## Workflow Patterns

```python
WORKFLOW_PATTERNS = {
    'ecosystem_sweep': 'Map all technologies in an ecosystem → create skills for each gap',
    'progressive_deepening': 'Create foundation → intermediate → advanced in sequence building on each other',
    'cross_cutting_integration': 'Create skills connecting pairs of technologies (A+B, A+C, B+C)',
    'version_follow': 'When major framework version releases, create migration skills',
    'pattern_extraction': 'Identify repeated patterns across projects → generalize into skills',
}

class BatchAuthoringPipeline:
    """Efficiently create batches of related skills."""
    
    def __init__(self):
        self.templates = {}
        self.batch_plan = []
    
    def define_template(self, name: str, content_template: str):
        """Define a reusable content template."""
        self.templates[name] = content_template
    
    def plan_batch(self, skills: List[Dict], template_name: str):
        """Plan a batch of skills using a template."""
        for skill in skills:
            self.batch_plan.append({
                **skill,
                'template': template_name,
            })
    
    def estimate_time(self) -> Dict:
        """Estimate total creation time for a batch."""
        return {
            'total_skills': len(self.batch_plan),
            'research_per_skill': 15,  # minutes
            'writing_per_skill': 25,   # minutes
            'review_per_skill': 10,    # minutes
            'total_hours': round(len(self.batch_plan) * 50 / 60, 1),
        }
```

## Efficiency Principles

```python
EFFICIENCY_PRINCIPLES = {
    'template_first': 'Create reusable templates before batch creation',
    'single_source': 'One canonical source for patterns shared across skills',
    'progressive_detail': 'Write skeleton first (frontmatter + headings), fill details later',
    'review_in_batches': 'Review all skills in a batch together for consistency',
    'cross_reference_early': 'Link related_skills before writing bodies (breaks circular deps)',
}

def batch_creation_workflow():
    return [
        "1. RESEARCH: Identify ecosystem gaps (30 min)",
        "2. PLAN: Decide skill names, categories, relationships (20 min)",
        "3. TEMPLATE: Define shared content template (15 min)",
        "4. SKELETON: Create all skills with frontmatter only (2 min/skill)",
        "5. FILL: Add When to Use + Common Pitfalls for all (10 min/skill)",
        "6. CODE: Add code examples for all (15 min/skill)",
        "7. CHECKLIST: Add verification checklists (5 min/skill)",
        "8. CROSS-REF: Update related_skills across batch (10 min)",
        "9. REVIEW: Batch review for consistency (30 min)",
        "10. PUBLISH: Deploy skills (automated)",
    ]
```

## Common Pitfalls

1. **Over-planning** — spending more time planning than creating
2. **No templates** — starting from scratch every time wastes effort
3. **Inconsistent quality** — first skill is detailed, last is sparse
4. **Batch too large** — momentum loss on 20+ skill batches; break into 5-10
5. **No review step** — batch-created skills need batch review for consistency

## Verification Checklist

- [ ] Template defined for the skill category
- [ ] Batch size manageable (5-10 skills optimal)
- [ ] Skeleton first approach used (frontmatter → fill later)
- [ ] All skills in batch use consistent terminology
- [ ] Cross-references within batch linked
- [ ] Review completed before publishing
- [ ] Time per skill tracked for future estimates
