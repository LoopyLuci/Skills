---
name: technical-writing-patterns
description: "Use when writing technical documentation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [technical-writing, documentation, API-docs, README, style-guide, Diátaxis]
    related_skills: [swagger-openapi-patterns, api-design-and-documentation, documentation-generation, codebase-onboarding]
---

# Technical Writing Patterns

Writing clear technical documentation — from documentation frameworks (Diátaxis) through API docs, README structure, style guides, and documentation testing.

## When to Use

- Writing developer documentation and API references
- Creating README files for open source projects
- Building internal knowledge base and runbooks
- Documenting architecture decisions (ADRs)
- Testing documentation for correctness

## Documentation Framework

```python
DOC_FRAMEWORKS = {
    'diataxis': 'Tutorials (learning-oriented), How-to guides (task-oriented), Explanation (understanding), Reference (information)',
    'docs_as_code': 'Documentation in markdown, version-controlled, reviewed like code',
    'adr': 'Architecture Decision Records — lightweight, timestamped decisions',
}

class DocGenerator:
    """Generate documentation from code."""
    
    @staticmethod
    def readme_template() -> str:
        return """# Project Name
Brief description — what, why, who.

## Installation
```bash
pip install project
```

## Quick Start
```python
from project import Client
client = Client()
result = client.do_thing()
```

## API Reference
### `Client.do_thing(param1, param2)`
Does a thing with params.

## Contributing
See CONTRIBUTING.md

## License
MIT
"""
    
    @staticmethod
    def check_docs_completeness(repo_path: str) -> List[str]:
        missing = []
        essentials = ['README.md', 'LICENSE', 'CONTRIBUTING.md', 'CHANGELOG.md']
        for doc in essentials:
            if not os.path.exists(os.path.join(repo_path, doc)):
                missing.append(doc)
        return missing
```

## Verification Checklist

- [ ] README includes what, why, quick start, API reference
- [ ] Documentation follows Diátaxis or similar framework
- [ ] Code examples are tested (doctest or integration tests)
- [ ] ADRs documented for key architectural decisions
- [ ] API documentation generated and up-to-date
- [ ] Documentation is versioned (matches software versions)
- [ ] Style guide consistent (tone, terminology, formatting)
- [ ] Documentation review as part of PR process
- [ ] Searchable (headers, keywords, tags)
