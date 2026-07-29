---
name: skill-cross-agent-portability
description: Make skills work across Hermes, Codex, and other agents.
---

# Skill Cross-Agent Portability

**Trigger**: Use when creating or adapting skills to work with multiple AI coding agents beyond Hermes.

## The agentskills.io Standard

Skills follow the [agentskills.io](https://agentskills.io/specification) standard: `SKILL.md` file with YAML frontmatter inside a named directory. Supported by Hermes, Codex, Claude Code (partial), and Cline.

```yaml
---
name: my-skill
description: Use when deploying apps with Docker and Kubernetes.
---
```

## Agent Compatibility

| Agent | Skill format | How to load | Notes |
|-------|-------------|-------------|-------|
| **Hermes** | `skills/<name>/SKILL.md` | `/skill-name` | Full support |
| **Codex** | `skills/<name>/SKILL.md` | Codex skills hub | agentskills.io |
| **Claude Code** | `CLAUDE.md` | Project files | No dynamic loading |
| **Cline** | `.clinerules/` | File-based | Manual setup |

## Writing Portable Skills

```markdown
DO use:
- Standard agentskills.io frontmatter
- Descriptions under 60 chars
- Plain markdown, no agent-specific syntax
- Exact shell commands
- Standard tool names

DON'T use:
- `/skill-name` slash commands (only Hermes)
- `fallback_for_toolsets` or Hermes YAML extensions
- `skill_manage`, `delegate_task`, `execute_code` assumptions
- Hermes cron/delegate features
```

## Adding Agent-Specific Metadata Safely

```yaml
---
name: deploy-k8s
description: Deploy apps to Kubernetes with Helm.
metadata:
  hermes:
    tags: [kubernetes, helm]
    config:
      - key: deploy.namespace
        default: default
---
```

Non-Hermes agents ignore `metadata.hermes`. This makes the skill portable.

## Loading by Agent

| Agent | How skills are accessed |
|-------|------------------------|
| Hermes | `/skill-name`, `skills_list()`, bundles, cron |
| Codex | Skills hub → points to `skills/` directory |
| Claude Code | Manual merge into `CLAUDE.md` (always loaded) |
| Cline | Manual copy to `.clinerules/` directory |

## Portability Check

```bash
grep -n "skill_manage\|delegate_task\|execute_code" "skills/*/SKILL.md" && \
  echo "⚠️  Contains Hermes-specific tools"
grep -c "^/" "skills/*/SKILL.md" && \
  echo "⚠️  Contains slash commands"
```

## Pitfalls
- **Feature assumptions**: Not all agents have terminal, web_search, or image generation — keep skills tool-agnostic
- **Slash command addiction**: Writing skills that rely on Hermes-only features limits their reach
- **Dynamic loading expectation**: Claude Code/Cline don't have on-demand loading — users manually include
- **Format divergence**: Hermes `metadata.hermes.*` is safely ignored by others but adds noise

## Verification
```bash
grep -qE "skill_manage|delegate_task|execute_code|cronjob" "skills/$name/SKILL.md" || \
  echo "Portable ✓"
```
