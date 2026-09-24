#!/usr/bin/env python3
"""
Skill Generator — Create properly formatted skills for LoopyLuci/Skills.

Usage:
  python generate_skill.py generate --name my-skill --description "Does X" --tags python,cli
  python generate_skill.py bulk skills.json --apply
  python generate_skill.py validate skills/my-skill/SKILL.md
  python generate_skill.py enrich --apply --category aws,docker
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path
from datetime import datetime

REPO_SKILLS = Path(r"Z:\Projects\Skills\LoopyLuci-skills\skills")

# Category-specific content templates
CATEGORY_TEMPLATES = {
    "software-development": {
        "concepts": [
            "Language-specific idioms and best practices",
            "Package/module organization",
            "Error handling and logging patterns",
            "Testing methodology (unit, integration, e2e)",
            "Build, lint, and format tooling",
        ],
        "workflow": [
            ("Setup", "Initialize project, install dependencies, configure tooling", "Working dev environment"),
            ("Implement", "Write core logic following idiomatic patterns", "Functional code with passing tests"),
            ("Test", "Write and run tests covering happy path and edge cases", "All tests pass, >80% coverage"),
            ("Review", "Self-review for code quality, performance, security", "Clean, documented production-ready code"),
            ("Deliver", "Commit, document, and verify end-to-end", "Working feature with tests and docs"),
        ],
        "tools": ["Language-specific package manager", "Test framework", "Linter/Formatter", "Build system", "Debugging tools"],
        "pitfalls": [
            ("Skipping error handling", "Silent failures", "Always handle errors explicitly"),
            ("Over-engineering", "Unnecessary complexity", "Add abstraction only when needed"),
            ("Missing tests", "Regression bugs", "Write tests alongside code"),
        ],
    },
    "security": {
        "concepts": [
            "Threat modeling and risk assessment",
            "Attack surface analysis",
            "Defense in depth",
            "Zero-trust architecture",
            "Compliance and audit requirements",
        ],
        "workflow": [
            ("Scope", "Define assets, threats, attack surface", "Documented scope with trust boundaries"),
            ("Assess", "Identify vulnerabilities, evaluate risk", "Prioritized findings with CVSS scores"),
            ("Remediate", "Apply secure-by-design fixes", "Vulnerabilities closed"),
            ("Verify", "Re-test and validate remediation", "Independent verification complete"),
            ("Document", "Record findings and lessons learned", "Audit-ready report"),
        ],
        "tools": ["Vulnerability scanners", "SAST/DAST tools", "SIEM platforms", "Pen-testing frameworks"],
        "pitfalls": [
            ("Scope creep", "Unclear boundaries", "Define scope explicitly"),
            ("Tool reliance without analysis", "False positives", "Manual validation required"),
        ],
    },
    "cloud": {
        "concepts": [
            "Infrastructure as Code (IaC)",
            "Well-Architected Framework",
            "Identity and access management",
            "Networking and security groups",
            "Cost optimization and tagging",
        ],
        "workflow": [
            ("Design", "Architecture review against WAF pillars", "Approved architecture diagram"),
            ("Implement", "IaC templates with least-privilege IAM", "Reviewable version-controlled infra"),
            ("Validate", "Security scan, cost estimate, plan review", "Clean plan within budget"),
            ("Deploy", "Apply with change management", "Deployed infrastructure matches plan"),
            ("Monitor", "Alarms, dashboards, cost alerts", "Full observability and cost allocation"),
        ],
        "tools": ["Terraform/Pulumi", "Cloud-native IaC", "Security scanning", "Cost management"],
        "pitfalls": [
            ("Manual console changes", "Configuration drift", "All changes through IaC"),
            ("Over-privileged IAM", "Blast radius risk", "Least privilege by default"),
        ],
    },
    "data": {
        "concepts": [
            "Data modeling (dimensional, normalized)",
            "ETL/ELT patterns and idempotency",
            "Data quality and validation",
            "Lineage and cataloging",
            "Privacy and data protection",
        ],
        "workflow": [
            ("Discover", "Profile data, assess quality", "Data profile report with quality scores"),
            ("Design", "Model for use case", "Approved data model"),
            ("Build", "Implement pipelines with testing", "Idempotent pipelines with quality checks"),
            ("Validate", "Reconcile, test business rules", "Validated data with quality metrics"),
            ("Operate", "Monitor, optimize, iterate", "Monitored pipelines with SLA tracking"),
        ],
        "tools": ["dbt", "Airflow/Prefect", "Spark/DuckDB", "Data catalogs"],
        "pitfalls": [
            ("No data quality gates", "Garbage in, garbage out", "Validate at every stage"),
            ("Monolithic pipelines", "Hard to debug", "Small idempotent tasks"),
        ],
    },
    "ai": {
        "concepts": [
            "Model selection and evaluation",
            "Feature engineering and data prep",
            "Training methodology",
            "Deployment and serving patterns",
            "Monitoring and drift detection",
        ],
        "workflow": [
            ("Frame", "Define problem, success metric, baseline", "Clear problem statement"),
            ("Explore", "EDA, feature analysis", "Understanding of data relationships"),
            ("Build", "Train models, track experiments", "Logged reproducible experiments"),
            ("Evaluate", "Test on holdout, check bias", "Evaluation report with confidence"),
            ("Deploy", "Serve with monitoring", "Production model with drift detection"),
        ],
        "tools": ["Experiment tracking", "Model registry", "Feature store", "Model serving"],
        "pitfalls": [
            ("Data leakage", "Overly optimistic metrics", "Strict temporal splits"),
            ("No monitoring", "Silent degradation", "Monitor prediction distribution"),
        ],
    },
}

DEFAULT_TEMPLATE = CATEGORY_TEMPLATES["software-development"]

CATEGORY_KEYWORDS = {
    "software-development": ["python", "javascript", "typescript", "rust", "java", "react", "angular", "vue", "node", "api", "backend", "frontend", "web", "app", "cli", "sdk", "library", "framework", "testing", "debug", "code", "programming"],
    "security": ["security", "pentest", "vulnerability", "incident", "threat", "crypto", "iam", "compliance", "audit", "malware", "forensics", "firewall", "encryption", "auth"],
    "cloud": ["aws", "azure", "gcp", "cloud", "terraform", "kubernetes", "k8s", "docker", "container", "infrastructure", "iac"],
    "data": ["data", "database", "sql", "etl", "pipeline", "warehouse", "lakehouse", "spark", "kafka", "airflow", "dbt", "analytics"],
    "ai": ["ai", "ml", "machine-learning", "deep-learning", "neural", "nlp", "computer-vision", "llm", "gpt", "transformer", "model"],
}


def detect_category(name):
    name_lower = name.lower()
    scores = {}
    for cat, kws in CATEGORY_KEYWORDS.items():
        scores[cat] = sum(1 for kw in kws if kw in name_lower)
    return max(scores, key=scores.get) if any(scores.values()) else "software-development"


def make_title(name):
    words = name.replace('-', ' ').split()
    return ' '.join(w.capitalize() for w in words)


def generate_body(name, description, tags, category):
    t = CATEGORY_TEMPLATES.get(category, DEFAULT_TEMPLATE)
    title = make_title(name)

    workflow = "\n".join(f"{i+1}. **{p}** — {w}\n   - Expected: {o}" for i, (p, w, o) in enumerate(t["workflow"]))
    tools = "\n".join(f"- {tool}" for tool in t["tools"])
    pitfalls = "\n".join(f"- **{m}** → {c} → {f}" for m, c, f in t["pitfalls"])
    concepts = "\n".join(f"- {c}" for c in t["concepts"])
    tag_str = ", ".join(tags)

    return f"""# {title}

{description}

## Trigger

Activate this skill when the user mentions:
- {tag_str.replace(',', ', ')} workflows or issues
- Building, fixing, or optimizing {title.lower()}
- Questions about {tags[0] if tags else 'the domain'} best practices

## Core Concepts

{concepts}

## Step-by-Step Workflow

{workflow}

## Tools & Technologies

{tools}

## Best Practices

- Document decisions and rationale (ADRs, design docs, runbooks)
- Version everything - code, configs, data, and documentation
- Test incrementally; never claim passing without verification
- Respect domain-specific regulations and ethical standards
- Measure outcomes with meaningful metrics

## Common Pitfalls

{pitfalls}

## Tags

`{tag_str}`

---

*LoopyLuci/Skills - {datetime.now().strftime('%Y-%m-%d')}*
"""


def generate_skill(name, description, tags, category=None, apply=False):
    if category is None:
        category = detect_category(name)

    skill_dir = REPO_SKILLS / name
    if skill_dir.exists():
        return {"status": "exists", "name": name}

    frontmatter = {
        "name": name,
        "description": description,
        "version": "1.0.0",
        "author": "LoopyLuci Community",
        "license": "MIT",
        "platforms": ["any"],
        "metadata": {"hermes": {"tags": tags}},
    }

    body = generate_body(name, description, tags, category)

    if apply:
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            "---\n" + yaml_dump(frontmatter) + "---\n\n" + body, encoding="utf-8"
        )

    return {"status": "created" if apply else "dry-run", "name": name, "category": category}





def validate_skill(skill_path):
    path = Path(skill_path)
    if not path.exists():
        return [f"File not found: {path}"]

    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return ["Missing YAML frontmatter"]

    end = content.find("---", 3)
    if end == -1:
        return ["Missing closing --- for frontmatter"]

    body = content[end+3:].strip()
    if len(body) < 200:
        return [f"Body too short ({len(body)} chars) - likely placeholder"]

    issues = []
    required_sections = ["## Trigger", "## Core Concepts"]
    for section in required_sections:
        if section not in body:
            issues.append(f"Missing section: {section}")

    return issues


def enrich_skill(skill_path):
    path = Path(skill_path)
    if not path.exists():
        return False

    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False

    end = content.find("---", 3)
    if end == -1:
        return False

    frontmatter = content[3:end].strip()
    body = content[end+3:].strip()

    # Detect boilerplate (two formats)
    new_format_markers = [
        "Document decisions and rationale (ADRs, memos)",
        "Version everything — code, configs, data, and docs",
        "Skipping discovery and jumping to solutions",
    ]
    old_format_markers = [
        "## Overview",
        "## When to Use",
        "## Key Approaches",
        "## Common Pitfalls",
        "## Verification Checklist",
        "1. Define requirements",
        "2. Choose tools",
        "3. Implement modular",
    ]
    
    new_score = sum(1 for m in new_format_markers if m in body)
    old_score = sum(1 for m in old_format_markers if m in body)
    
    is_boilerplate = new_score >= 2 or old_score >= 3
    if not is_boilerplate:
        return False

    name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else path.parent.name

    desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
    description = desc_match.group(1).strip() if desc_match else f"Skill for {name}"

    tags_match = re.search(r'tags:\s*\[(.+?)\]', frontmatter)
    tags = [t.strip() for t in tags_match.group(1).split(",")] if tags_match else ["general"]

    category = detect_category(name)
    new_body = generate_body(name, description, tags, category)

    new_content = f"---\n{frontmatter}\n---\n\n{new_body}"
    path.write_text(new_content, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    gen = subparsers.add_parser("generate")
    gen.add_argument("--name", required=True)
    gen.add_argument("--description", required=True)
    gen.add_argument("--tags", required=True)
    gen.add_argument("--category")
    gen.add_argument("--apply", action="store_true")

    bulk = subparsers.add_parser("bulk")
    bulk.add_argument("input")
    bulk.add_argument("--apply", action="store_true")

    val = subparsers.add_parser("validate")
    val.add_argument("path")

    enr = subparsers.add_parser("enrich")
    enr.add_argument("--category")
    enr.add_argument("--apply", action="store_true")
    enr.add_argument("--path")

    args = parser.parse_args()

    if args.command == "generate":
        tags = [t.strip() for t in args.tags.split(",")]
        result = generate_skill(args.name, args.description, tags, args.category, args.apply)
        print(json.dumps(result, indent=2))

    elif args.command == "bulk":
        # ... bulk processing
        pass

    elif args.command == "validate":
        issues = validate_skill(args.path)
        if issues:
            print(f"Validation issues ({len(issues)}):")
            for i in issues:
                print(f"  - {i}")
        else:
            print(f"Valid: {args.path}")

    elif args.command == "enrich":
        if args.path:
            result = enrich_skill(args.path)
            print(f"Enriched: {result}")
        else:
            cat_filter = [c.strip() for c in args.category.split(",")] if args.category else None
            skills = sorted(REPO_SKILLS.iterdir())
            enriched = 0
            for skill_dir in skills:
                if not skill_dir.is_dir():
                    continue
                skill_md = skill_dir / "SKILL.md"
                if not skill_md.exists():
                    continue
                if cat_filter and skill_dir.name.split("-")[0].lower() not in cat_filter:
                    continue
                if not args.apply:
                    content = skill_md.read_text(encoding="utf-8")
                    if "Skipping discovery and jumping to solutions" in content:
                        enriched += 1
                else:
                    if enrich_skill(skill_md):
                        enriched += 1
            print(f"{'Would enrich' if not args.apply else 'Enriched'}: {enriched}")


if __name__ == "__main__":
    main()
