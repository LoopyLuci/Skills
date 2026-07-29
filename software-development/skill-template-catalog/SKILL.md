---
name: skill-template-catalog
description: "Use when selecting skill templates by category."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skill-templates, catalog, categories, patterns, meta, scaffolding]
    related_skills: [skill-blueprint-generator, meta-skill-patterns, skill-quality-standards, skill-testing-automation]
---

# Skill Template Catalog

A catalog of reusable skill templates by category — from programming and ML templates through business, networking, and creative patterns.

## When to Use

- Starting a new skill with a proven template structure
- Choosing the right template format for your skill type
- Ensuring consistency across skills in the same domain
- Speed up skill creation with pre-built section layouts

## Template Catalog

```python
TEMPLATE_CATALOG = {
    'programming_language': {
        'description': 'Skills about a programming language or framework',
        'sections': ['Language Overview', 'Installation/Setup', 'Core Syntax', 'Key Patterns', 'Performance Tips', 'Common Pitfalls'],
        'code_type': 'Language-specific examples',
    },
    'ml_model': {
        'description': 'Skills about implementing ML models and algorithms',
        'sections': ['Algorithm Overview', 'Architecture', 'Implementation (PyTorch)', 'Training Loop', 'Evaluation', 'Common Pitfalls'],
        'code_type': 'PyTorch/scikit-learn with runnable classes',
    },
    'business_process': {
        'description': 'Skills about business operations and strategies',
        'sections': ['Overview', 'When to Use', 'Framework/Model', 'Implementation', 'Common Pitfalls', 'Verification Checklist'],
        'code_type': 'Python classes, templates, and calculators',
    },
    'software_pattern': {
        'description': 'Skills about software design patterns and practices',
        'sections': ['Pattern Overview', 'Problem', 'Solution', 'Implementation', 'Trade-offs', 'Common Pitfalls'],
        'code_type': 'Multi-language examples (Python, TypeScript, Rust)',
    },
    'networking_protocol': {
        'description': 'Skills about network protocols and infrastructure',
        'sections': ['Protocol Overview', 'How It Works', 'Implementation Considerations', 'Configuration', 'Security', 'Monitoring'],
        'code_type': 'Configuration files, Python scripts, CLI commands',
    },
    'agent_system': {
        'description': 'Skills about AI agent architectures and systems',
        'sections': ['System Overview', 'Architecture', 'Implementation', 'Communication', 'Safety', 'Common Pitfalls'],
        'code_type': 'Agent classes, communication protocols, message schemas',
    },
}
```

## Template Renderer

```python
class TemplateRenderer:
    """Render a skill template for a given category."""
    
    @staticmethod
    def render(category: str, skill_name: str, 
               description: str, tags: List[str]) -> str:
        template = TEMPLATE_CATALOG.get(category, TEMPLATE_CATALOG['business_process'])
        
        lines = ['---', f'name: {skill_name}', f'description: "{description}"',
                 'version: 1.0.0', f'category: {category}',
                 f'tags: {json.dumps(tags)}', '---']
        
        for section in template['sections']:
            lines.append(f'\n## {section}')
            lines.append(f'\nContent for {skill_name} — {section.lower()}.')
        
        return '\n'.join(lines)
```

## Verification Checklist

- [ ] Template selected matches skill domain
- [ ] Template sections customized for skill content (not generic)
- [ ] Code type appropriate for the domain
- [ ] Category assigned correctly
- [ ] Tags generated from template defaults + skill specifics
- [ ] Frontmatter complete and valid
- [ ] Template includes pitfalls and verification sections
