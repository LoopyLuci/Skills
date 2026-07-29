#!/usr/bin/env python3
"""
skill_batch_create.py — Create skills in batches from a structured JSON plan.

Usage:
    python scripts/skill_batch_create.py --plan plan.json
    python scripts/skill_batch_create.py --plan plan.json --dry-run
    python scripts/skill_batch_create.py --generate-plan --domain python --count 20

Plan JSON format:
{
  "batch_name": "python-ecosystem",
  "description": "String",
  "skills": [
    {
      "name": "python-async-patterns",
      "description": "Use when implementing async Python patterns.",
      "category": "software-development",
      "tags": ["python", "async", "asyncio", "coroutines"],
      "template": "language-patterns",
      "related": ["python-decorators-advanced", "concurrency-parallelism"],
      "level": "intermediate"
    }
  ]
}
"""

import json, os, sys, shutil, argparse
from datetime import datetime

HERMES_SKILLS = os.path.expandvars(r'$LOCALAPPDATA/hermes/skills')

# ── Templates ──────────────────────────────────────────────────────────────
TEMPLATES = {
    "language-patterns": """---
name: {{name}}
description: "{{description}}"
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [{{tag_string}}]
    related_skills: [{{related_string}}]
---

# {{title}}

## When to Use

## Core Patterns

```python
# Example
```

## Common Pitfalls

## Verification Checklist
- [ ] Implementation verified

## See Also
""",

    "framework-patterns": """---
name: {{name}}
description: "{{description}}"
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [{{tag_string}}]
    related_skills: [{{related_string}}]
---

# {{title}}

## When to Use

## Setup

## Core Patterns

## Common Pitfalls

## Verification Checklist

## See Also
""",

    "business-process": """---
name: {{name}}
description: "{{description}}"
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [{{tag_string}}]
    related_skills: [{{related_string}}]
---

# {{title}}

## When to Use

## Framework

## Implementation

## Common Pitfalls

## Verification Checklist

## See Also
""",
}

def generate_skill(skill_def: dict, dry_run: bool = False) -> dict:
    """Generate a single skill from its definition."""
    name = skill_def["name"]
    category = skill_def.get("category", "productivity")
    template_name = skill_def.get("template", "business-process")
    template = TEMPLATES.get(template_name, TEMPLATES["business-process"])
    
    tag_string = ", ".join(f'"{t}"' for t in skill_def.get("tags", [name.split("-")[0]]))
    related_string = ", ".join(skill_def.get("related", []))
    title = name.replace("-", " ").title()
    description = skill_def["description"]
    
    content = template
    content = content.replace("{{name}}", name)
    content = content.replace("{{description}}", description)
    content = content.replace("{{tag_string}}", tag_string)
    content = content.replace("{{related_string}}", related_string)
    content = content.replace("{{title}}", title)
    
    if dry_run:
        return {"name": name, "category": category, "status": "simulated", "size": len(content)}
    
    skill_dir = os.path.join(HERMES_SKILLS, category, name)
    os.makedirs(skill_dir, exist_ok=True)
    
    with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
        f.write(content)
    
    return {"name": name, "category": category, "status": "created", "path": skill_dir}


def generate_plan(domain: str, count: int) -> list:
    """Auto-generate a batch plan for a domain."""
    prefixes = {
        "python": ["async", "decorator", "generator", "typing", "testing", "logging", 
                   "serialization", "context-manager", "metaclass", "descriptor"],
        "react": ["hooks", "context", "render", "performance", "testing", "forms",
                  "state", "animation", "portal", "refs"],
        "kubernetes": ["pod", "deployment", "service", "ingress", "configmap", "secret",
                       "rbac", "hpa", "network-policy", "helm"],
    }
    words = prefixes.get(domain, [f"{domain}-pattern"])
    plans = []
    for i in range(min(count, len(words))):
        plans.append({
            "name": f"{domain}-{words[i]}-patterns",
            "description": f"Use when implementing {domain} {words[i]} patterns.",
            "category": "software-development",
            "tags": [domain, words[i]],
            "template": "language-patterns",
            "related": [],
            "level": "intermediate"
        })
    return plans


def main():
    parser = argparse.ArgumentParser(description="Batch create Hermes skills")
    parser.add_argument("--plan", help="Path to JSON plan file")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without writing")
    parser.add_argument("--generate-plan", help="Auto-generate plan for a domain (e.g., python)")
    parser.add_argument("--count", type=int, default=10, help="Skills to generate")
    args = parser.parse_args()
    
    if args.generate_plan:
        skills = generate_plan(args.generate_plan, args.count)
        plan = {"batch_name": f"{args.generate_plan}-ecosystem", "skills": skills}
        print(json.dumps(plan, indent=2))
        return
    
    if not args.plan:
        parser.print_help()
        return
    
    with open(args.plan) as f:
        plan = json.load(f)
    
    results = []
    for skill_def in plan["skills"]:
        result = generate_skill(skill_def, args.dry_run)
        results.append(result)
        
    created = [r for r in results if r["status"] == "created"]
    sys.stderr.write(f"Batch '{plan.get('batch_name', 'unnamed')}': "
                     f"{len(created)} created, "
                     f"{len(results) - len(created)} simulated\n")

if __name__ == "__main__":
    main()
