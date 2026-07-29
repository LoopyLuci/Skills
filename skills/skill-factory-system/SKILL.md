---
name: skill-factory-system
description: "Use when autonomously discovering and creating skills."
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meta, skill-factory, batch-create, landscape, auto-discovery, quality]
    related_skills: ["skill-content-optimization", "skill-gap-analysis", "skill-test-generation", "meta-skill-patterns", "skill-analytics-usage-tracking"]
---

# Skill Factory System

Autonomous skill discovery and creation system. Load this skill and use its companion scripts (in `scripts/`) for batch creation, landscape analysis, bulk management, and external discovery.

## Quick Start

```bash
# 1. Discover gaps
python scripts/skill_landscape.py --analyze gaps

# 2. Batch create from gaps
python scripts/skill_batch_create.py --plan batch_plan.json

# 3. Score quality
python scripts/skill_quality_score.py --all

# 4. Auto-link cross-references
python scripts/skill_auto_related.py --all
```

## Available Tools

| Script | Function |
|--------|----------|
| `skill_batch_create.py` | Create 20-50 skills from structured JSON plan |
| `skill_landscape.py` | Analyze ecosystem coverage, detect gaps |
| `skill_bulk_manage.py` | Move, tag, validate skills in bulk |
| `skill_quality_score.py` | Score skill quality (0-100) with detailed report |
| `skill_auto_related.py` | Auto-generate related_skills from tag overlap |
| `skill_discover.py` | Discover skill opportunities from external signals |
| `skill_templates/` | Template files for different skill categories |

## Templates Available

| Template | Best For |
|----------|----------|
| `language-patterns` | Programming language skills |
| `framework-patterns` | Framework/library skills |
| `business-process` | Business and strategy skills |
| `security-test` | Pen-testing and security skills |
| `ml-model` | ML/AI model skills |
| `infrastructure-tool` | DevOps/cloud/infra skills |

## Verification Checklist

- [ ] `scripts/` directory populated with all tool scripts
- [ ] `skill_templates/` directory populated with template files
- [ ] Each script has `--help` flag
- [ ] Batch plan JSON schema defined
- [ ] Quality scoring thresholds configured
