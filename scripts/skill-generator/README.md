# LoopyLuci Skills — Skill Generator Toolkit

Tools for creating, validating, bulk-generating, and enriching skills in the LoopyLuci/Skills repository.

## Quick Start

```bash
# Generate a single skill
python scripts/skill-generator/generate_skill.py generate \
  --name my-new-skill \
  --description "Brief description of what this skill does" \
  --tags python,cli,automation \
  --apply

# Bulk generate from JSON
python scripts/skill-generator/bulk_generate.py skills-to-add.json --apply

# Validate all skills
python scripts/skill-generator/validate_skill.py

# Enrich boilerplate skills with real content
python scripts/skill-generator/generate_skill.py enrich --apply
```

## Tools

### `generate_skill.py` — Single Skill Generator

```bash
python generate_skill.py generate \
  --name <kebab-case-name> \
  --description "<description>" \
  --tags tag1,tag2,tag3 \
  [--category software-development|security|cloud|data|ai] \
  [--apply]
```

- `--apply` creates the skill (default: dry-run)
- Auto-detects category from name keywords
- Generates category-specific content (different templates for software, security, cloud, data, AI)
- Creates proper YAML frontmatter + structured body

### `bulk_generate.py` — Bulk Generator

```bash
python bulk_generate.py skills.json --apply
python bulk_generate.py skills.csv --format csv --apply
```

Input formats:
- **JSON**: `[{"name": "...", "description": "...", "tags": [...]}, ...]`
- **CSV**: `name,description,tags` (comma-separated)

### `validate_skill.py` — Quality Checker

```bash
python validate_skill.py                      # Validate all
python validate_skill.py skills/my-skill     # Validate one
```

Checks:
- Required frontmatter fields (`name`, `description`, `version`, `author`, `license`, `metadata`)
- Name matches directory
- Tags are lowercase
- Body has required sections (`## Trigger`, "## Core Concepts")
- Body is substantive (>100 chars)

### `generate_skill.py enrich` — Content Enrichment

```bash
python generate_skill.py enrich --apply           # All skills
python generate_skill.py enrich --category aws --apply  # Filter by prefix
python generate_skill.py enrich --path skills/my-skill/SKILL.md  # Single
```

Rewrites boilerplate/template content with domain-specific content:
- Detects boilerplate by marker patterns
- Parses skill name for domain keywords
- Generates unique content using category templates
- Preserves existing frontmatter

## Skill Format

See `SKILL-FORMAT.md` for the complete specification.

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | kebab-case, matches directory |
| `description` | ✅ | ≤120 chars, one sentence |
| `version` | ✅ | semver (1.0.0) |
| `author` | ✅ | Name or handle |
| `license` | ✅ | SPDX (MIT, Apache-2.0) |
| `platforms` | ✅ | `[any]` or `[linux, macos, windows]` |
| `metadata.hermes.tags` | ✅ | 2-5 lowercase tags |

### Body Sections

| Section | Required | Content |
|---------|----------|---------|
| Title (`# ...`) | ✅ | Title Case from name |
| `## Trigger` | ✅ | When to activate |
| `## Core Concepts` | ✅ | Domain fundamentals |
| `## Step-by-Step Workflow` | ✅ | Phased approach |
| `## Tools & Technologies` | ❌ | Specific tools |
| `## Best Practices` | ❌ | Patterns that work |
| `## Common Pitfalls` | ❌ | Mistakes and fixes |
| `## Related Skills` | ❌ | Cross-references |

## Categories with Specialized Content

- **software-development** — Setup → Implement → Test → Review → Deliver
- **security** — Scope → Assess → Remediate → Verify → Document
- **cloud** — Design → Implement → Validate → Deploy → Monitor
- **data** — Discover → Design → Build → Validate → Operate
- **ai** — Frame → Explore → Build → Evaluate → Deploy
- **design**, **creative**, **business**, **marketing**, **science** — General templates

## Best Practices

1. Use `--apply` only after reviewing dry-run output
2. Run `validate_skill.py` after generation to catch issues
3. Use `enrich` to upgrade boilerplate skills
4. Keep descriptions ≤120 characters
4. Use 3-5 descriptive tags
5. Test that `name` matches directory name exactly
