---
name: documentation-generation
description: "Generate README API docs from code and tests"
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
