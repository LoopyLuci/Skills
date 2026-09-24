---
name: skills-repo-sync
description: "Sync skills between Hermes and a GitHub repo."
version: 1.0.0
author: agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [skills, sync, git, cron, github, automation]
---

# Skills Repo Sync

Bidirectional skill synchronization between a Hermes instance and a GitHub-backed skills repository, with automatic commit, push, and multi-machine sharing.

## When to Use

- User wants to share skills across multiple machines via a GitHub repo
- User wants Hermes to automatically commit and push skill changes
- User wants a cron job to keep a local repo folder in sync with Hermes skills
- User clones a skills repo and wants to connect it to their Hermes instance

## Procedure

### 1. Clone the repo (if not already present)

```bash
git clone git@github.com:<user>/Skills.git <repo-path>
```

### 2. Create the sync script

Place a Python script at `<repo>/scripts/sync-skills.py`. Key design points:

- **Resolve paths dynamically** — never hardcode drive letters or absolute paths that are machine-specific. Use `Path(__file__).resolve().parent.parent` for the repo root and `%LOCALAPPDATA%/hermes/skills` (Windows) or `$HERMES_HOME/skills` / `~/.hermes/skills` for Hermes.
- **Handle structural differences** — Hermes uses nested `category/skill/SKILL.md`; most repos use flat `skill/SKILL.md`. Flatten Hermes skills by iterating categories and subdirectories, keying by skill name.
- **Sync strategy** — mtime-based: newer file wins. Pull latest from origin first, then sync both directions, then commit and push.
- **Skip Hermes internals** — ignore `.archive`, `.curator_*`, `.usage.json`, `.hub`, `.locks`, and other dot-prefixed directories.
- **Support dirs** — copy `references/`, `templates/`, `scripts/`, `assets/`, `examples/` alongside each skill.

Usage modes:
```
python scripts/sync-skills.py           # dry run
python scripts/sync-skills.py --apply   # apply changes (commit only)
python scripts/sync-skills.py --force   # apply + push
```

### 3. Create a cron wrapper

The cron tool resolves script paths relative to `~/AppData/Local/hermes/scripts/`. Place a wrapper there that calls the main script with `--force`:

```python
# ~/AppData/Local/hermes/scripts/sync-cron.py
import os, subprocess, sys
from pathlib import Path

REPO_DIR = Path(r"C:\Users\<user>\Desktop\Skills")  # adjust per machine
script = REPO_DIR / "scripts" / "sync-skills.py"
env = os.environ.copy()
env["HERMES_HOME"] = str(Path(os.environ.get("LOCALAPPDATA", r"C:\Users\<user>\AppData\Local")) / "hermes")
result = subprocess.run([sys.executable, str(script), "--force"], cwd=str(REPO_DIR), env=env)
sys.exit(result.returncode)
```

### 4. Set up the cron job

Use `cronjob_manage` with:
- `action: create`
- `name: skills-sync-hermes-repo`
- `schedule: 30m` (or user preference)
- `no_agent: true` (script-only, no LLM needed)
- `script: sync-cron.py` (the wrapper from step 3)
- `workdir: <repo-path>` (so git operations run in the repo)
- `deliver: local` (silent unless errors)

### 5. Start the gateway

Cron jobs only fire when the Hermes gateway is running:
```
hermes gateway start
hermes gateway status
```

The gateway auto-starts on Windows login via a startup shortcut.

## Pitfalls

- **Hardcoded paths break cross-machine sync.** Existing repo scripts may be hardcoded to `D:\Projects\Skills` or `Z:\Projects\Skills\...` from other machines. Always use `Path(__file__).resolve()` and environment variables.
- **Cron scripts resolve relative to Hermes scripts dir.** The cron tool's `script` field resolves under `~/AppData/Local/hermes/scripts/`. Place wrappers there, not in the repo.
- **Cron jobs need the gateway running.** `no_agent: true` jobs fire via the scheduler, which requires the gateway process. If the gateway isn't running, jobs are saved but won't fire.
- **Git identity must be configured.** Commits fail with `Author identity unknown` if `user.name` and `user.email` aren't set. Run `git config --global user.name` and `git config --global user.email`.
- **Pull before sync to avoid conflicts.** Always `git fetch origin && git reset --hard origin/main` before syncing to ensure the repo is up to date.
- **Structural mismatch between Hermes and repo.** Hermes nests skills under categories (`skills/github/SKILL.md`); repos typically flatten (`skills/github/SKILL.md`). The sync script must flatten Hermes skills by iterating category directories.

## Verification

After setup, verify:
1. `hermes cron list` shows the job as active
2. `hermes gateway status` shows the gateway running
3. Run the sync wrapper manually: `python ~/AppData/Local/hermes/scripts/sync-cron.py`
4. Check GitHub for the commit with the sync message