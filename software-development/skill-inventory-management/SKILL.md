---
name: skill-inventory-management
description: "Use when auditing, pruning, or consolidating skills."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skills, meta, inventory, audit, lifecycle, pruning]
    related_skills: [skill-development-workflow, skill-discovery, skill-architecture-planning, skill-testing-automation, meta-skill-patterns]
---

# Skill Inventory Management

Systematic process for auditing, pruning, consolidating, and maintaining the skill inventory over time. Skills accumulate sediment; this skill keeps the catalog clean, discoverable, and performant.

## When to Use

- Before creating a new skill — check if consolidation or pruning could free a slot
- On a quarterly audit cycle — inventory every skill, purge the stale
- When `skills_list()` returns more than ~80 skills — loading overhead grows linearly
- When a user says "I have too many skills" or "clean up my skills"
- After merging two skills — delete the originals with `absorbed_into`
- When you discover a skill is never loaded in practice

## Audit Process

### Phase 1: Full Inventory

```bash
skills_list()    # list all skills with categories
```

Group by category and assess each skill against:

| Criterion | Keep? | Action |
|-----------|-------|--------|
| Loaded in the last 30 days | ✅ Keep | — |
| Referenced by another skill's `related_skills` | ✅ Keep | — |
| Used by a cron job | ✅ Keep | — |
| Never loaded, no references | ❌ Prune candidate | Check with user first |
| Overlaps >70% with another skill | 🔀 Merge candidate | Consolidate, then delete originals |
| Description truncated poorly | 🔧 Patch | Rewrite first 57 chars |
| Stale commands/APIs | 🔧 Patch | Update content |

### Phase 2: Usage Analysis

Check `.usage.json` for load frequency:

```bash
cat $LOCALAPPDATA/hermes/skills/.usage.json | python -m json.tool
```

Look for skills with `"loads": 0` or very low counts. Cross-reference with `related_skills` chains: a skill that's referenced but never directly loaded still provides value as a cross-reference target.

### Phase 3: Duplicate Detection

Search for overlapping descriptions. Signal words for overlap:
- Same category + similar noun ("docker", "wsl2", "windows")
- Description starts with same trigger phrase
- Body overlaps >50% on inspection

### Phase 4: Pruning Workflow

For each stale skill:

1. **Check references**: Do any other skills list it in `related_skills`?
   - If yes, patch those skills first to remove the reference
   - Use: `skill_manage(action='patch', name='other-skill', old_string='- stale-skill', new_string='')`

2. **Check cron jobs**: Does any cron job reference it?
   - `cronjob(action='list')` — check attached skills
   - If yes, update the cron job to remove the reference

3. **Delete**:
   - If merging into another: `absorbed_into='umbrella-skill'`
   - If truly stale: `absorbed_into=''` (prune with no forwarding)

### Phase 5: Consolidation (Merge)

When two skills overlap heavily:

1. Identify the stronger/broader skill as the umbrella
2. Create or patch the umbrella to absorb the other's unique content
3. Delete the narrower skill with `absorbed_into='umbrella-skill'`
4. Update any cron jobs or related_skills that reference the deleted name

## Consolidation Patterns

### Absorption (1→1)

```bash
# Skill A absorbs Skill B's unique content, then B is deleted
skill_manage(action='patch', name='umbrella-skill',
    old_string='## Common Pitfalls',
    new_string='## Common Pitfalls\n\n### From merged skill (old-skill-name)\n- pitfall content here...')
skill_manage(action='delete', name='old-skill-name',
    absorbed_into='umbrella-skill')
```

### Umbrella Creation (N→1)

```bash
# Create a new broader skill, delete N narrow ones
skill_manage(action='create', name='broad-skill', content='...', category='...')
skill_manage(action='delete', name='narrow-skill-a', absorbed_into='broad-skill')
skill_manage(action='delete', name='narrow-skill-b', absorbed_into='broad-skill')
```

## Maintenance Schedule

| Frequency | Action |
|-----------|--------|
| Weekly | Check for skills created but never loaded |
| Monthly | Review skills_list() for naming inconsistencies |
| Quarterly | Full audit: prune, merge, patch stale content |
| Per-version | After major Hermes updates, verify all skills still work |

## Common Pitfalls

1. **Deleting a referenced skill** — always check `related_skills` and cron jobs first
2. **Accidental hard-delete** — use `absorbed_into=''` to signal intent; the curator may archive rather than delete
3. **Over-pruning** — a skill loaded once every 3 months for a critical task is still valuable
4. **Patching descriptions for truncation** — the system prompt index truncates at 57 chars; the full description is visible via `skill_view()` and `skills_list()`
5. **Merging without removing old references** — after merging, patch all skills that referenced the old name

## Verification Checklist

- [ ] Full inventory taken via `skills_list()`
- [ ] Usage data reviewed from `.usage.json`
- [ ] Duplicates identified and resolved
- [ ] Stale/pruned skills deleted with correct `absorbed_into`
- [ ] All `related_skills` references updated after deletions
- [ ] Cron jobs updated after deletions
- [ ] Final inventory count documented

## See Also

- skill-development-workflow — building and testing skills
- skill-discovery — discovering existing skills
- skill-testing-automation — automated skill validation
- meta-skill-patterns — design patterns for meta-skills
