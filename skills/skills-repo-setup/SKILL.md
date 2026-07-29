---
name: skills-repo-setup
description: Set up a GitHub skills tap repo with two-way Hermes sync.
---

# Skills Repo Setup

**Trigger**: Use when setting up a GitHub-hosted skills repository that syncs bidirectionally with Hermes Agent's local skills.

## What this does

Converts a local Hermes skills backup into a properly structured, consumable GitHub skills repository:
1. Flattens the `category/skill-name/SKILL.md` structure into `skills/<skill-name>/SKILL.md`
2. Creates a README with consumption instructions (tap, external_dirs, URL install)
3. Creates a sync script that copies new/updated skills from Hermes → repo
4. Sets up a cron job for periodic automatic sync
5. Configures Hermes `external_dirs` to consume the repo's skills

## Procedure

### 1. Restructure repo for tap compatibility

```python
# Run from the repo root
import shutil, re, os
from pathlib import Path

REPO = Path('.')
SKILLS = REPO / 'skills'
SKILLS.mkdir(exist_ok=True)

for sk in list(REPO.glob('**/SKILL.md')):
    if '.git' in sk.parts or 'skills/' in str(sk):
        continue
    name = sk.parent.name
    tgt = SKILLS / name / 'SKILL.md'
    tgt.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(sk, tgt)
    for sub in ('references','templates','scripts','assets','examples'):
        src = sk.parent / sub
        if src.is_dir():
            shutil.copytree(src, tgt.parent / sub, dirs_exist_ok=True)

# Remove old dirs
for d in list(REPO.iterdir()):
    if d.is_dir() and d.name not in ('.git','skills','scripts'):
        shutil.rmtree(d)
```

### 2. Remove Hermes internal files

Files to remove from git tracking (add to .gitignore):
- `.bundled_manifest`
- `.curator_state`
- `.usage.json`
- `.usage.json.lock`
- `IDEA.md`

### 3. Create README.md with usage instructions

Include sections for:
- **Hermes tap**: `hermes skills tap add owner/repo` + path config
- **External dir**: `skills.external_dirs: [path/skills]` in config.yaml
- **Other agents**: Clone and point at `skills/`

### 4. Create sync script (`scripts/sync-from-hermes.sh`)

Must handle:
- Windows path resolution (`%LOCALAPPDATA%/hermes/skills`)
- Stripping category prefix from `category/skill/SKILL.md`
- `cmp -s` + `diff -rq` for change detection
- Supporting files (references/, templates/, scripts/, etc.)
- Dry-run mode (`--apply` flag)
- `git add && commit && push` on changes

Key snippet for the main loop:
```bash
while IFS= read -r skill_file; do
    norm_skill_file="$(echo "$skill_file" | sed 's|\\|/|g')"
    rel_path="${norm_skill_file#$norm_skills_dir/}"
    parts_count="$(echo "$rel_path" | tr '/' '\n' | wc -l)"
    if [ "$parts_count" -eq 2 ]; then
        skill_name="$(echo "$rel_path" | cut -d/ -f1)"
    elif [ "$parts_count" -eq 3 ]; then
        skill_name="$(echo "$rel_path" | cut -d/ -f2)"
    fi
    # ... cmp, copy, supporting dirs, git commit
done
```

### 5. Set up cron job

```bash
# Copy script to Hermes scripts dir
cp scripts/sync-from-hermes.sh ~/AppData/Local/hermes/scripts/sync-skills-to-github.sh

# Create a wrapper that sets REPO_DIR
cat > ~/AppData/Local/hermes/scripts/sync-skills-to-github.sh << 'EOF'
#!/usr/bin/env bash
REPO_DIR="/d/Projects/Skills"
cd "$REPO_DIR" && exec bash "$REPO_DIR/scripts/sync-from-hermes.sh" --apply
EOF

# Register cron
hermes cron-job create \
  --name skills-sync-to-github \
  --schedule "every 6h" \
  --script sync-skills-to-github.sh \
  --no-agent \
  --deliver local
```

### 6. Configure Hermes consumption

In `config.yaml`:
```yaml
skills:
  external_dirs:
    - D:\Projects\Skills\skills
```

Or for taps, edit `~/.hermes/.hub/taps.json`:
```json
{"taps": [{"repo": "LoopyLuci/Skills", "path": "skills/"}]}
```

## Pitfalls

- **Windows path confusion**: Bash/MSYS uses `/c/Users/...` paths, cron scripts need absolute paths
- **Slow file comparison**: `cmp -s` on 1,000+ files on MSYS takes 5+ minutes — cron runs in background
- **CRLF warnings**: Git on Windows warns about LF→CRLF conversion for shell scripts — harmless, set `.gitattributes` if needed
- **Tap path depth**: Flat `skills/<name>/SKILL.md` works; category nesting `skills/<cat>/<name>/SKILL.md` does NOT work with tap's one-level scan
- **External dir precedence**: Local `~/.hermes/skills/<name>` overrides external `skills/<name>` when names collide

## Verification

```bash
# Verify skill count
ls skills/ | wc -l

# Verify frontmatter parsing
head -5 skills/*/SKILL.md | grep "^name:" | wc -l

# Verify supporting files preserved
find skills -type d | grep -E "(references|templates|scripts)" | head -5

# Test sync in dry-run
bash scripts/sync-from-hermes.sh

# Test external dirs — skills show in Hermes
hermes chat -q "list 5 skills you have available"
```
