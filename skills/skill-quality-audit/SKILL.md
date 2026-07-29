---
name: skill-quality-audit
description: Audit skills for correctness, freshness, and usefulness.
---

# Skill Quality Audit

**Trigger**: Use when reviewing a skill for correctness, checking if it's up to date, or assessing whether it's still useful.

## Audit Dimensions

```markdown
Score each dimension 1-10:

DIMENSION       | WHAT TO CHECK                  | MIN PASS
----------------|--------------------------------|---------
Accuracy        | Do the commands/APIs still work?| 7/10
Completeness    | Are all steps included?         | 6/10
Clarity         | Is the trigger obvious?         | 7/10
Conciseness     | Could it say the same in fewer? | 5/10
Freshness       | Is it updated for current tools?| 6/10
Discoverability | Would the agent find it?        | 7/10

OVERALL = average of all dimensions
PASS ≥ 6.5  |  NEEDS WORK 4-6.5  |  FAIL < 4
```

## Accuracy Check

```markdown
For each critical command in the skill:
1. Is the CLI syntax still current?
   - Check: `command --help` vs what the skill says
   - Flag: deprecated flags, renamed subcommands
2. Is the API endpoint still valid?
   - Check: current docs vs skill's URL
   - Flag: 301/404 endpoints
3. Are the package versions still supported?
   - Check: package current version vs skill's version
   - Flag: EOL versions, security vulnerabilities
```

## Freshness Check

```markdown
Check the skill version and last update:

1. Look at version in frontmatter
2. Check `.usage.json` for last_used_at
3. Check git history (if in a tap repo)
4. Test a key command

SIGNS OF STALE SKILL:
- Uses `docker-compose` (now `docker compose`)
- References `master` branch (now `main`)
- Uses Python 3.8 or older
- Dockerfile doesn't use multi-stage builds
- References deprecated cloud provider CLIs
```

## Completeness Check

```markdown
A complete skill should have:

✅ Trigger condition ("Use when...")
✅ Numbered steps
✅ Exact commands (not descriptions of commands)
✅ Pitfalls section
✅ Verification section
✅ Connected skills (if relevant)

MISSING ANY? → Flag for improvement
```

## Discoverability Check

```markdown
A discoverable skill has:

✅ Description ≤60 chars, starts with trigger
✅ Description is UNIQUE (no similar descriptions)
✅ Category matches the domain
✅ Tags are specific (not just "general")
✅ Name matches common task terminology

HARD CHECK:
  skills_list():
    Can you guess what this skill does from its description alone?
  
  If NO → description needs work.
```

## Automated Audit

```bash
#!/bin/bash
# Quick audit of all skills in a directory
SKILLS_DIR="${1:-skills}"

echo "=== Skill Audit ==="
for skill in "$SKILLS_DIR"/*/; do
    name=$(basename "$skill")
    desc=$(head -5 "$skill/SKILL.md" | grep "^description:" | cut -d: -f2- | xargs)
    desc_len=$(echo -n "$desc" | wc -c)
    has_pitfalls=$(grep -c "^## Pitfalls" "$skill/SKILL.md")
    has_verify=$(grep -c "^## Verification" "$skill/SKILL.md")
    step_count=$(grep -c "^[0-9]\. " "$skill/SKILL.md")
    
    status="✅"
    [ "$desc_len" -gt 60 ] && status="❌" && echo "  LONG DESC: $name ($desc_len chars)"
    [ "$has_pitfalls" -eq 0 ] && echo "  ⚠️  No pitfalls: $name"
    [ "$has_verify" -eq 0 ] && echo "  ⚠️  No verification: $name"
    [ "$step_count" -eq 0 ] && echo "  ⚠️  No numbered steps: $name"
done
```

## Quality Triage

```markdown
After audit, classify each issue:

CRITICAL (fix now):
- Broken commands that would fail
- Security vulnerabilities in instructions
- Incorrect API endpoints or URLs

MAJOR (fix this week):
- Missing pitfalls the user would hit
- Incomplete steps that would cause confusion
- Description >60 chars (hidden from routing)

MINOR (fix when convenient):
- Could use more examples
- Formatting improvements
- Additional reference files

TRIVIAL (maybe never):
- Extra context that's nice but not needed
- Alternative approaches that cover edge cases
```
