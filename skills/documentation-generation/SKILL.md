---
name: documentation-generation
description: Generate README API docs from code and tests
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [documentation, generation]
---

# Documentation Generation

## README Structure
```markdown
# Project Name
## Overview
## Installation
## Usage
## API Reference
## Development
## Contributing
## License
```

## Auto-Generate
```bash
# Python docstrings to docs
pip install pdoc
pdoc src/myapp -o docs/

# OpenAPI docs
# FastAPI auto-generates at /docs
```

## Trigger

Activate this skill when the user mentions:
- documentation, generation workflows or issues
- Building, fixing, or optimizing documentation generation


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
