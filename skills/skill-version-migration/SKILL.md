---
name: skill-version-migration
description: Update skills when underlying tools, APIs, or syntax change.
---

# Skill Version Migration

**Trigger**: Use when you discover a skill's commands are outdated, a tool has a breaking version change, or an API has been deprecated.

## Migration Triggers

```markdown
SKILL MIGRATION NEEDED when you notice:

1. Commands fail with "deprecated" or "unknown flag"
   → Tool CLI changed (e.g., docker-compose → docker compose)

2. URLs return 404/301
   → API endpoints moved or restructured

3. Configuration format changed
   → YAML keys renamed, TOML instead of INI

4. Default behavior changed
   --force → --yes  |    HTTPS not HTTP  |    v2 not v1

5. New best practices available
   Multi-stage builds, security scanners, OIDC instead of keys
```

## Migration Checklist

```markdown
□ Identify all outdated patterns in the skill
□ Find the CURRENT equivalent (docs, --help, web search)
□ Update commands and syntax
□ Update version/flags/config keys
□ Update any URLs or endpoints
□ Update examples
□ Add a "Version note" in the skill body
□ Bump version in frontmatter
□ Test the updated commands
```

## Common Migration Patterns

### CLI Command Renames
```yaml
# OLD (deprecated)
docker-compose up -d
kubectl run myapp --image=nginx
heroku create myapp

# NEW (current)
docker compose up -d
kubectl create deployment myapp --image=nginx
# replaced by: flyctl launch, railway, render, etc.
```

### Configuration Format Changes
```yaml
# Old format
build:
  args:
    NODE_ENV: production

# New format
args:
  - NODE_ENV=production
```

### API Endpoint Changes
```yaml
# Old GitHub API
/api/v3/repos/:owner/:repo

# New (still v3, but some v4 endpoints now preferred)
GraphQL: github-api-usage skill covers this
```

## Version Tracking in Frontmatter

```yaml
---
name: docker-compose-patterns
version: 2.1.0
last_tested: 2026-07-29
tested_with:
  docker: v27.0
  compose: v2.29
---
# Note: This skill uses `docker compose` (v2 syntax).
# For v1, replace with `docker-compose`.
```

## Bulk Migration

```bash
#!/bin/bash
# Migrate all skills: docker-compose → docker compose
SKILLS_DIR="${1:-skills}"
count=0
for skill in "$SKILLS_DIR"/*/SKILL.md; do
    if grep -q "docker-compose" "$skill" 2>/dev/null; then
        sed -i 's/docker-compose/docker compose/g' "$skill"
        echo "  Updated: $skill"
        ((count++))
    fi
done
echo "Migrated $count skills"
```

## Pitfalls
- **Breaking changes require context**: Don't just replace text — the entire approach might need updating
- **Partial migration**: Updating 80% of a skill and missing 20% creates a confusing hybrid
- **Version bumping**: Just bumping the version number without meaningful changes is misleading
- **Multi-version support**: Some skills need to support multiple tool versions — use notes, not replacement
- **Test after migration**: Always run a key command from the skill to verify it works

## Verification
```bash
# Quick check for deprecated patterns in all skills
grep -rn "docker-compose\|kubectl run [^-]\|--wait-only\|deprecated" skills/ 2>/dev/null
```
