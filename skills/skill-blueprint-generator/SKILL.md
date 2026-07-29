---
name: skill-blueprint-generator
description: "Use when generating skill blueprints and structures."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skill-blueprint, generator, template, scaffold, meta, structure]
    related_skills: [skill-quality-standards, skill-template-catalog, meta-skill-patterns, skill-testing-automation]
---

# Skill Blueprint Generator

Generating complete skill blueprints from natural language prompts — from structure templates and frontmatter generation through section outlines and code scaffolding.

## When to Use

- Creating a new skill from scratch
- Generating skill structure from a topic description
- Prototyping skill content before full development
- Ensuring consistent skill structure across authors
- Speeding up skill authoring workflow

## Blueprint Generation

```python
from typing import List, Dict, Optional
import json

class SkillBlueprint:
    """Generate skill blueprint from topic description."""
    
    SECTIONS = [
        ('When to Use', 'List specific scenarios when this skill applies'),
        ('Core Content', 'Executable patterns, code examples, frameworks'),
        ('Common Pitfalls', '5-6 actionable failure modes with explanations'),
        ('Verification Checklist', '5-10 testable verification items'),
        ('See Also', '3-5 related skills with descriptions'),
    ]
    
    DOMAIN_MAPPINGS = {
        'programming': 'software-development',
        'networking': 'networking',
        'machine_learning': 'mlops',
        'ai': 'mlops',
        'business': 'productivity',
        'marketing': 'productivity',
        'security': 'networking',
        'design': 'creative',
    }
    
    @staticmethod
    def generate(topic: str, category: str = None) -> Dict:
        """Generate a complete skill blueprint."""
        if not category:
            category = 'productivity'
        
        name = topic.lower().replace(' ', '-').replace('_', '-')
        if len(name) > 60: name = name[:60]
        
        return {
            'name': name,
            'category': category,
            'description': f"Use when {topic.lower().strip()}.",
            'frontmatter': {
                'version': '1.0.0',
                'author': 'Hermes Agent',
                'license': 'MIT',
                'metadata': {
                    'hermes': {
                        'tags': [topic.split()[0].lower()],
                        'related_skills': [],
                    }
                }
            },
            'sections': [
                {'title': '# Skill Title', 'content': 'Brief overview (2-3 sentences)'},
                {'title': '## When to Use', 'content': '- Bullet list of use cases'},
                {'title': '## Core Content', 'content': '```python\n# Code example\n```'},
                {'title': '## Common Pitfalls', 'content': '1. **Pitfall name** — explanation'},
                {'title': '## Verification Checklist', 'content': '- [ ] Actionable check item'},
                {'title': '## See Also', 'content': '- related-skill — why related'},
            ]
        }
    
    @staticmethod
    def to_markdown(blueprint: Dict) -> str:
        """Convert blueprint to SKILL.md format."""
        lines = ['---']
        lines.append(f"name: {blueprint['name']}")
        lines.append(f"description: \"{blueprint['description']}\"")
        lines.append(f"version: {blueprint['frontmatter']['version']}")
        lines.append(f"author: {blueprint['frontmatter']['author']}")
        lines.append('---')
        lines.append('')
        for section in blueprint['sections']:
            lines.append(section['title'])
            lines.append(section['content'])
            lines.append('')
        return '\n'.join(lines)
```

## Use Cases

```python
# Example: Generate a skill blueprint for "Kubernetes deployment patterns"
blueprint = SkillBlueprint.generate(
    topic="implementing Kubernetes deployment patterns",
    category="software-development"
)
print(blueprint['name'])  # implementing-kubernetes-deployment-patterns
```

## Verification Checklist

- [ ] Blueprint generates valid frontmatter YAML
- [ ] Description starts with "Use when" and fits 60 chars
- [ ] All standard sections included
- [ ] Category maps to existing Hermes category
- [ ] Skill name is kebab-case
- [ ] Tags generated from topic keywords
- [ ] Code scaffolding included (at minimum a pattern comment)
