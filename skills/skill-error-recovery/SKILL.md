---
name: skill-error-recovery
description: Recover when a skill's instructions fail at runtime.
---

# Skill Error Recovery

**Trigger**: Use when following a skill's steps and a command fails, an error occurs, or the expected output doesn't appear.

## Error Classification

| Error type | Example | Recovery strategy |
|-----------|---------|------------------|
| **Command not found** | `docker-compose: command not found` | Check installation, use v2 syntax |
| **Permission denied** | `Permission denied (publickey)` | Check credentials, SSH keys, tokens |
| **API changed** | `flag provided but not defined` | Tool was updated — adjust command |
| **Wrong context** | `Not in a git repository` | Check working directory |
| **Missing dependency** | `ModuleNotFoundError` | Install missing package |
| **Network error** | `Could not resolve host` | Check connectivity, retry |
| **Version mismatch** | `requires >=3.8 but you have 3.7` | Check version requirements |

## Recovery Decision Tree

```
Command from skill failed
        │
   ┌────▼──────────────┐
   │ Known error?       │
   │ (listed in skill's │──YES──► Apply skill's pitfall fix
   │ Pitfalls section)  │
   └────┬──────────────┘
        │ NO
   ┌────▼──────────────┐
   │ Is error in the   │
   │ command syntax,   │──YES──► Adjust to current version
   │ not the approach? │
   └────┬──────────────┘
        │ NO
   ┌────▼──────────────┐
   │ Is approach       │
   │ fundamentally     │──YES──► Switch to different approach
   │ wrong?            │
   └────┬──────────────┘
        │ NO
   ┌────▼──────────────┐
   │ Unfamiliar error  │──YES──► Use general debugging skill
   └────┬──────────────┘
        │
   └──► Report: patch the skill with this fix
```

## Common Error Patterns

### Pattern 1: Deprecated CLI
```markdown
SKILL SAYS: docker-compose up -d
ERROR:      'docker-compose' is not recognized

FIX:        docker compose up -d
            (v2 removed the hyphen)
ACTION:     Patch the skill
```

### Pattern 2: Missing Setup Step
```markdown
SKILL SAYS: aws s3 sync ./dist s3://bucket
ERROR:      Unable to locate credentials

FIX:        Run `aws configure` first, or set env vars
MISSING:    Skill didn't mention authentication
ACTION:     Add setup prerequisites to the skill
```

### Pattern 3: Wrong Directory/Context
```markdown
SKILL SAYS: cargo test
ERROR:      could not find `Cargo.toml`

FIX:        cd to the correct project directory first
MISSING:    Skill assumed you were in the right dir
ACTION:    Add `cd` step or context assumption to skill
```

## Recovery Resources

```markdown
When the skill doesn't have the fix, try:

1. ERROR MESSAGE → search terms
   - Copy the exact error and search skills
   - `web_search` the error message

2. --help flag
   - `command --help` for current syntax
   - Compare with skill's syntax

3. Fallback skills
   - Load systematic-debugging
   - Load a sibling skill (different approach, same goal)

4. General knowledge
   - Apply general debugging principles
   - Adapt the skill's approach to the real error
```

## When to Patch the Skill

```markdown
PATCH immediately if:
- The error is caused by tool evolution (not environment)
- Multiple users would hit the same issue
- The fix is a simple command substitution

DON'T PATCH if:
- The error is environment-specific (Python 3.7 on this machine)
- The error is user-specific (missing permissions)
- You're unsure if the fix is correct

PATCH with:
skill_manage(
  action="patch",
  name="skill-name",
  old_string="old-command",
  new_string="new-command"
)
```

## Pitfalls
- **Environment vs skill error**: Is the command wrong, or is your environment misconfigured? Check before patching
- **Multiple errors**: Fix one error at a time — fixing everything at once can mask the root cause
- **Partial success**: Some steps worked, some didn't — document what failed, not the whole skill
- **False positives**: The command ran without error but produced wrong output — harder to catch than crashes

## Verification
```markdown
After recovery:
- Does the corrected approach work?
- Should the skill be patched with the fix?
- Did I document the error for future reference?
```
