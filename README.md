# LoopyLuci Skills

A curated collection of **1,028+ AI agent skills** built for [Hermes Agent](https://hermes-agent.nousresearch.com/) and compatible with any agent that supports the [agentskills.io](https://agentskills.io/) open standard.

These skills cover: software development, ML/AI, networking, security, creative tools, productivity, DevOps, system administration, and more — designed to be loaded on-demand by AI agents.

---

## How to Use

### With Hermes Agent

#### Option A: Clone + External Directory (recommended)

```bash
git clone https://github.com/LoopyLuci/Skills.git ~/LoopyLuci-skills
```

Then add to your `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - ~/LoopyLuci-skills/skills
```

All skills are instantly available as `/skill-name` slash commands. No install per skill needed.

#### Option B: Skill Tap (hub-managed updates)

```bash
hermes skills tap add LoopyLuci/Skills
```

Then edit `~/.hermes/.hub/taps.json` to set the path to root:

```json
{
  "taps": [
    {"repo": "LoopyLuci/Skills", "path": "skills/"}
  ]
}
```

Then install individual skills:

```bash
hermes skills search <query>
hermes skills install LoopyLuci/Skills/<skill-name>
```

#### Option C: Direct URL Install

```bash
hermes skills install https://raw.githubusercontent.com/LoopyLuci/Skills/main/skills/<skill-name>/SKILL.md
```

### With Other Agents

Most AI coding agents (Claude Code, Codex, Cline, Aider) support the [agentskills.io](https://agentskills.io/) format. Clone the repo and point your agent at the `skills/` directory:

```bash
git clone https://github.com/LoopyLuci/Skills.git
# Then configure your agent to scan ./Skills/skills/
```

---

## Structure

```
LoopyLuci/Skills/
├── skills/                        # All skills (flat, one directory per skill)
│   ├── blocklist-manager/
│   │   ├── SKILL.md               # Skill definition (required)
│   │   ├── references/            # Additional documentation
│   │   ├── templates/             # Output templates
│   │   └── scripts/               # Helper scripts
│   ├── git-workflow-optimization/
│   │   └── SKILL.md
│   ├── kubernetes-deployment/
│   │   └── SKILL.md
│   ├── ... 1,028+ skills
├── scripts/
│   └── sync-from-hermes.sh        # Sync script (maintainer use)
├── README.md                      # This file
└── .gitignore
```

---

## Automatic Updates

This repository is synced from Hermes Agent's local skill library. Skills added or modified in Hermes are automatically committed and pushed here.

To sync changes back to your local Hermes (pull from repo):

```bash
cd ~/LoopyLuci-skills && git pull
```

---

## Skill Format

Each skill follows the [agentskills.io](https://agentskills.io/specification) standard:

```yaml
---
name: my-skill
description: Brief description, ~60 chars
tags: [python, automation]
---
```

Full format details at the [Hermes Skills Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills).

---

## License

MIT — free to use, share, and contribute.
