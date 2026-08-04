---
name: data-leakage-prevention-in-skills
description: "Use when creating skills. Prevent data leakage."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [privacy, data-leakage, security, pii, skill-authoring]
    related_skills: [privacy-by-design-skill-authoring, pii-detection-and-remediation]
---

# Data Leakage Prevention in Skills

## Overview
Safeguard against accidental personal data leakage when authoring Hermes skills. Ensures no PII (personally identifiable information), secrets, credentials, or sensitive data is embedded in SKILL.md content, template files, references, or script examples.

## When to Use
- Before creating any new skill
- When reviewing/editing existing skills for privacy compliance
- When a skill will process user data
- When writing example templates that might contain sample data

## The Risk: How Skills Leak Data

Skills can leak data through multiple vectors:
1. **Example content**: Templates with hardcoded names, emails, addresses, phone numbers
2. **Configuration files**: Scripts with embedded API keys, passwords, file paths
3. **Reference files**: Documents containing sample client data, screenshots with PII
4. **Code examples**: Python/bash scripts with hardcoded credentials or personal paths
5. **Frontmatter**: Description or metadata containing project names tied to personal identity
6. **Linked files**: Templates, scripts, or assets that contain real data instead of placeholders

## The Pre-Write Privacy Gate

**Always run through this checklist before writing ANY skill content:**

### Step 1: Identify Data Categories
For every field, variable, or example value, ask:
- Could this identify a real person or entity?

| Data Category | Examples in Skills | Safe Alternative |
|--------------|--------------------|------------------|
| Full names | "John Smith's API key" | "YOUR_API_KEY" or "example@example.com" |
| Email addresses | "john@company.com" in templates | "user@example.com" or "{{email}}" |
| Phone numbers | "(555) 123-4567" | "555-0100" or "+0-000-000-0000" |
| Physical addresses | "123 Main St, Anytown" | "123 Example St" or "[FULL_ADDRESS]" |
| Company names (personal context) | "John's Startup Inc." | "ACME Corp" or "Example Company" |
| API keys/tokens | Hardcoded keys in scripts | Environment variables or placeholders |
| File paths (personal) | "C:\Users\john\MyProject" | "$PROJECT_DIR" or relative paths |
| Database names | "john_customer_db" | "app_database" or "{{DB_NAME}}" |

### Step 2: Safe Placeholder Standards
Always use placeholders that are unmistakably generic:

```yaml
# BAD (contains PII-like patterns):
sample_api_key: "sk-live-abc123-john-smith-key"
client_email: "john.doe@company.com"
user_name: "John Smith"

# GOOD (generic placeholders):
api_key: "{{API_KEY}}"
email: "user@example.com"
name: "[FULL_NAME]"
```

### Step 3: Secret Management in Scripts
Never hardcode secrets in skill scripts. Always use:
```python
# BAD:
api_key = "sk-12345abcdef-John-Smith-key"
password = "mypassword123"

# GOOD:
import os
api_key = os.environ.get("API_KEY")
password = os.environ.get("PASSWORD")
# Or: raise ValueError("Set API_KEY environment variable")
```

### Step 4: Generic Example Data Templates
For templates, scripts, and reference files:
- Names: Use "Alice", "Bob", "Charlie" (common test names) or "User One"
- Emails: Use example.com, test.com, or company.example.com
- Addresses: Use "123 Example Street" with "Springfield" as city placeholder
- Phone: "+1-555-010-0000" pattern
- Companies: "ACME Corp", "Example Inc", "Globex Corporation"

## Privacy Review Process

### Before Skill Publication
1. Scan entire SKILL.md for PII patterns (use pii-detection-and-remediation skill)
2. Scan all linked files (references/, scripts/, templates/, assets/)
3. Check all example values, variable names, default configs
4. Verify no real API keys, tokens, or credentials are included
5. Ensure all placeholder patterns are generic and reusable

### For Data-Processing Skills
When a skill will handle actual user data:
1. Document what data the skill collects (explicit `## Privacy Impact` section)
2. Document what data the skill stores (none / temporary / persistent)
3. Document what data the skill transmits (external APIs, logging, etc.)
4. Include a `## Data Handling Notice` in the skill body

## Common Pitfalls
1. **Example credentials that look real** — "user@company.com" might be a real person's email
2. **Hardcoded file paths** — "C:\\Users\\John\\Documents\\ClientProject" reveals identity
3. **Test data from real life** — Using your own or clients' real data as examples
4. **"Realistic" placeholder patterns** — Fake names that happen to match real people
5. **Reference files with real data** — Screenshots, CSVs with real names/emails
6. **Embedding secrets in script examples** — "for demo purposes" keys that still work

## Verification Checklist
- [ ] No full names, emails, phones, addresses in any skill content
- [ ] All API keys/passwords replaced with `{{ENV_VAR}}` or `YOUR_KEY_HERE`
- [ ] File paths use env vars (`$PROJECT_DIR`) or relative paths
- [ ] All example data uses generic placeholders (example.com, Alice/Bob, etc.)
- [ ] Reference files scanned for hidden PII
- [ ] Scripts use `os.environ.get()` for secrets, never hardcoded
- [ ] Data-handling skills include Privacy Impact and Data Handling Notice sections