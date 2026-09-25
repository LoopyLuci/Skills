---
name: skill-database-management
description: "Operate a Hermes skill database repo at scale."
version: 0.1.0
author: LoopyLuci Community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [skills, database, sync, bulk, validation, enrichment, hermes, automation]
    related_skills: []
---

# Skill Database Management

Manage a Hermes Agent skill database repository — a GitHub repo of 10,000+ SKILL.md files that syncs bidirectionally with local Hermes instances. Covers setup, bulk generation, validation, enrichment, and issue remediation at scale.

## When to Use

- Setting up a GitHub repo as a shared skill database across multiple Hermes machines
- Bulk-generating hundreds of skills with proper frontmatter and domain-specific content
- Validating a large skill repo for format compliance
- Enriching boilerplate/template skills with real, domain-specific content
- Fixing malformed YAML, duplicate tags, name mismatches, and structural issues at scale
- Syncing skills bidirectionally between Hermes local store and a GitHub repo

Don't use for: single-skill authoring (use `hermes-agent-skill-authoring`), personal skill management, or in-repo Hermes bundled skills.

## Prerequisites

- Hermes Agent installed with `skills.external_dirs` or `skills.tap` support
- GitHub repo cloned locally (e.g., `Z:\Projects\Skills\LoopyLuci-skills`)
- Python 3.11+ with stdlib only (no external deps)
- Git + `gh` CLI authenticated

## Procedure

### 1. Initial Setup (one-time)

Clone repo and configure Hermes to read skills from it:

```bash
# Clone
git clone https://github.com/LoopyLuci/Skills.git ~/LoopyLuci-skills

# Option A: external_dirs (recommended for read-only access)
# Add to ~/.hermes/config.yaml:
#   skills:
#     external_dirs:
#       - ~/LoopyLuci-skills/skills

# Option B: tap (for hub-managed updates)
hermes skills tap add LoopyLuci/Skills
# Edit ~/.hermes/.hub/taps.json: {"taps": [{"repo": "LoopyLuci/Skills", "path": "skills/"}]}
```

### 2. Bidirectional Sync (cron job)

Create a sync script and schedule it via Hermes cron:

```bash
# scripts/sync-skills.sh — pulls origin, bidirectional sync, commits, pushes
# Run hourly via Hermes cron (see `cronjob` tool, schedule="every 1h")
```

The sync strategy:
1. `git fetch origin` + `git reset --hard origin/main` (remote is authoritative)
2. Repo → Hermes: copy newer-or-missing skills from repo to `~/.hermes/skills/`
3. Hermes → Repo: copy newer-or-missing skills from Hermes to repo
4. Commit + push if changes exist

Key: use `cp -u` (copy-if-newer) or compare `st_mtime` — never delete orphans automatically.

### 3. Bulk Skill Generation

Use a generator script to create hundreds of properly-formatted skills:

```bash
# scripts/skill-generator/generate_skill.py --name <kebab-name> --description "..." --tags a,b --apply
# scripts/skill-generator/bulk_generate.py skills.json --apply
```

Each generated skill gets:
- Proper YAML frontmatter: `name`, `description`, `version`, `author`, `license`, `platforms`, `metadata.hermes.tags`
- Category-specific body (different templates for software, security, cloud, data, AI)
- Trigger section, core concepts, workflow, tools, best practices, pitfalls

Category auto-detection from name keywords (e.g., `aws-*` → cloud, `react-*` → software).

### 4. Validation

Run format checker across all skills:

```bash
python scripts/skill-generator/validate_skill.py
```

Checks:
- Frontmatter starts with `---`, closes properly, parses as YAML
- `name`, `description` present; name matches directory
- `metadata.hermes.tags` exists (or flat `tags:`)
- Body has content (>100 chars)

Expected output: `Valid: N, With warnings: 0, With errors: 0`.

### 5. Content Enrichment

Upgrade boilerplate skills to real content:

```bash
python scripts/skill-generator/generate_skill.py enrich --apply
```

Detects boilerplate by marker patterns:
- New format: "Document decisions and rationale (ADRs, memos)"
- Old format: "## Overview", "## When to Use", "## Key Approaches", "1. Define requirements"

Rewrites body with domain-specific content while preserving frontmatter.

### 6. Issue Remediation

Common issues and fixes:

| Issue | Fix |
|-------|-----|
| Flat `tags:` + nested `metadata.hermes.tags` | Delete flat `tags:` line |
| `description` before `---` | Rebuild frontmatter |
| Missing `version`/`author` | Add defaults (1.0.0, LoopyLuci Community) |
| Tag case issues (e.g., `MLOps`) | Lowercase all tags |
| Stray directories | Remove (not skill directories) |
| Duplicate `## Trigger` from enrichment | Remove appended sections, keep original |

## Pitfalls

1. **Parsing nested YAML with regex.** A regex-based YAML parser fails on nested structures like `metadata: {hermes: {tags: [...]}}`. Use a proper parser with an indent stack — track `(dict, indent_level)` and pop when indent decreases.

2. **Enrichment appending to real content.** Before appending `## Trigger`/`## Core Concepts`, check if the body already has those sections or `## Overview`/`## When to Use`. Enrichment should replace boilerplate, not duplicate existing structure.

3. **git reset --hard on sync.** Using `git reset --hard origin/main` before sync prevents merge conflicts but discards local-only commits. Ensure the sync script commits local changes BEFORE pulling, or use `git merge` instead if multiple machines push frequently.

4. **Flat vs nested tags.** Two valid formats exist in curated skills: flat `tags: [a, b]` and nested `metadata.hermes.tags: [a, b]`. Hermes only loads the nested form. Normalize to nested when both exist — never keep both (YAML parsers may crash on duplicate keys).

5. **CRLF on Windows.** Git may warn "LF will be replaced by CRLF". This is cosmetic — the file content is correct. Add a `.gitattributes` with `*.md text eol=lf` if warnings are problematic.

6. **Validator false positives.** Some curated skills intentionally have short bodies or use `## Overview`/`## When to Use` instead of `## Trigger`/`## Core Concepts`. A validator should treat both section sets as valid, not flag them as errors.

7. **10,000+ file git operations.** `git add -a` on 10,000+ files is slow. Use `.gitignore` for generated artifacts and consider `git add skills/` only (not scripts/ or root).

## Verification

```bash
# Validate all skills pass
python scripts/skill-generator/validate_skill.py
# Expected: Valid: N, errors: 0

# Check sync is current
git log --oneline -1
# Expected: latest commit matches origin

# Spot-check enriched skill
cat skills/docker-best-practices/SKILL.md | head -30
# Expected: proper frontmatter, ## Trigger section present
```