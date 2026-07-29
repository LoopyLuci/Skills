---
name: skills-repo-publishing
description: Publish agent skills as a GitHub tap for any agent to use.
---

# Skills Repo Publishing

**Trigger**: Use when publishing a collection of agent skills as a GitHub tap repo for other Hermes/agent users.

## Repo Layout

```
owner/skills-repo
├── skills/
│   ├── my-skill/
│   │   ├── SKILL.md              # Required — skill definition
│   │   ├── references/           # Additional docs
│   │   ├── templates/            # Output templates
│   │   └── scripts/              # Helper scripts
│   └── another-skill/
│       └── SKILL.md
├── README.md                     # Consumption instructions
├── .gitignore                    # No Hermes internal state
```

### SKILL.md Format (Required)
```yaml
---
name: my-skill
description: Trigger-based description under 60 chars ending with period.
tags: [git, version-control]
---
```

## Consuming the Tap

### Hermes Tap Method
```bash
hermes skills tap add owner/skills-repo
# Edit ~/.hermes/.hub/taps.json:
# {"taps": [{"repo": "owner/skills-repo", "path": "skills/"}]}
hermes skills install owner/skills-repo/<skill-name>
```

### Hermes External Dir Method
```yaml
# config.yaml
skills:
  external_dirs:
    - ~/skills-repo/skills
```

### Other Agents (Codex, Claude Code, Cline)
```bash
git clone https://github.com/owner/skills-repo.git
# Point agent's skills directory at ./skills-repo/skills/
```

## Category Metadata (Optional)

`skills.sh.json` at repo root:
```json
{
  "$schema": "https://skills.sh/schemas/skills.sh.schema.json",
  "groupings": [
    {"title": "Git & Version Control", "skills": ["git-branching", "git-rebase"]}
  ]
}
```

## .gitignore Template

```
.bundled_manifest
.curator_state
.usage.json
.usage.json.lock
IDEA.md
.DS_Store
Thumbs.db
__pycache__/
.venv/
.idea/
.vscode/
```

## Pitfalls
- **Flat skills/ required**: Tap scans one level deep — `skills/cat/name/SKILL.md` won't be found
- **Category in frontmatter**: Put category in YAML, not in the directory path
- **GitHub token**: For private taps, users need `GITHUB_TOKEN` in `.env`

## Verification
```bash
ls skills/ | wc -l                        # Skill count
head -5 skills/*/SKILL.md | grep "^name:" | wc -l  # Valid frontmatter
hermes skills tap add owner/skills-repo   # Test discovery
```
