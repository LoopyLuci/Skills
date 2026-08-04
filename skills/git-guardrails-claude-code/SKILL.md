---
name: git-guardrails-claude-code
description: Use when adding git safety hooks to prevent destructive operations in Claude Code
tags: [git, safety, hooks, Claude-Code, guardrails]
related_skills: [setup-pre-commit, git-hooks-workflow, git-config-essentials]
---

# Git Guardrails Claude Code

Set up Claude Code hooks that block dangerous git commands (push, reset --hard, clean, branch -D) before they execute.

## What gets blocked
- `git push` (all variants including --force)
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .`

## Setup steps
1. Ask scope: project-only (.claude/settings.json) or all projects (~/.claude/settings.json)
2. Copy the hook script to the appropriate location
3. Make it executable (chmod +x)
4. Add PreToolUse hook to settings.json
5. Verify by triggering a blocked command

> **Note**: This skill is designed for Claude Code's hook system. For Hermes Agent, adapt to use git config aliases or pre-commit hooks instead.

## Common Pitfalls

- **Missing execute permission on the hook script**: The block-dangerous-git.sh script must be chmod +x or it silently won't run.
- **Installing globally when project-only is appropriate**: Global hooks affect all Claude Code sessions. Only install globally if the user explicitly wants that.
- **Not testing the guardrails after installation**: Verify by triggering one of the blocked commands and confirming it is intercepted.

## Verification Checklist

- [ ] Scope confirmed (project or global)
- [ ] Hook script copied to correct location
- [ ] chmod +x applied to hook script
- [ ] Hook added to settings.json (PreToolUse)
- [ ] Guardrails verified with a test command
