---
name: secrets-management
description: "Store rotate API keys env files vault and 1Password CLI"
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
