---
name: secrets-management
description: Store rotate API keys env files vault and 1Password CLI
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [secrets, management]
---

# Secrets Management

## .env File Pattern
```bash
# .env (never committed)
DATABASE_URL=postgres://user:pass@localhost/db
API_KEY=sk-abc123

# Load in Python
from dotenv import load_dotenv
load_dotenv()
import os
db_url = os.environ["DATABASE_URL"]
```

## 1Password CLI
```bash
op item get "My API Key" --field credential
export API_KEY=$(op item get "My API Key" --field credential)
```

## Trigger

Activate this skill when the user mentions:
- secrets, management workflows or issues
- Building, fixing, or optimizing secrets management


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
