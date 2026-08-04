---
name: community-skill-harvesting
description: Import external skill repos into your skills library.
---

# Community Skill Harvesting

**Trigger**: Use when importing existing SKILL.md files from public GitHub skill repos into your personal or organization skills repository.

## When to Use

- Expanding your skills library by sourcing from known community repos
- Curating the best skills from `mattpocock/skills`, `anthropics/skills`, `emilkowalski/skills`, `MiniMax-AI/skills`, `slavingia/skills`, `google/skills`
- Creating a merged, deduplicated repository from multiple upstream sources
- Setting up a one-time bulk import from a new upstream repo

**Not for** single skill installs via `hermes skills install <url>`.

## Key Sources

| Repo | Skills | Focus |
|------|--------|-------|
| `mattpocock/skills` | ~39 | Engineering methodology, TDD, code review |
| `anthropics/skills` | ~17 | Claude API, MCP, document creation |
| `emilkowalski/skills` | 8 | Design engineering, animation, UI |
| `MiniMax-AI/skills` | 17 | Dev frameworks, shaders, music |
| `slavingia/skills` | 10 | Entrepreneur methodology |
| `google/skills` | ~80 | GCP, GKE, BigQuery, Firebase |

**Non-harvestable**: `vercel-labs/skills` (CLI tool), `openai/skills` (deprecated), `awesome-openclaw-skills` (index only).

**Recently discovered harvestable**:

| Repo | Skills | Focus |
|------|--------|-------|
| `obra/superpowers` | ~12 | Agent workflows, brainstorming, git worktrees, code review |
| `vercel/skills` | 1 | `find-skills` — skill discovery helper |


## Procedure

### 1. Survey

```bash
curl -s "https://api.github.com/repos/owner/repo/contents/skills" | \
  python3 -c "import sys,json; [print(d['name']) for d in json.load(sys.stdin) if d['type']=='dir']"
```

### 2. Build Import Map

```python
SOURCES = {
    "source/repo": {
        "category": ["skill1", "skill2"],
    },
}
```

### 3. Fetch and Enhance

```python
from urllib.request import urlopen

def fetch_skill(repo, path, name):
    url = f"https://raw.githubusercontent.com/{repo}/main/skills/{path}/SKILL.md"
    with urlopen(url, timeout=15) as r:
        return r.read().decode("utf-8")

enhanced = f"""---
name: {name}
description: {desc}
source: {repo}
tags: [engineering]
metadata:
  hermes:
    tags: [engineering, design-patterns]
---

{body}
"""
```

### 4. Handle Name Collisions

```python
NAME_ALIASES = {
    "prototype": {"mattpocock/skills": "prototype-solution"},
}
mapped = NAME_ALIASES.get(name, {}).get(repo, name)
```

### 5. Fetch Supporting Files

```python
for sub in ["references", "templates", "scripts", "assets", "examples"]:
    url = f"https://api.github.com/repos/{repo}/contents/skills/{path}/{sub}"
    try:
        with urlopen(url, timeout=10) as r:
            for e in json.loads(r.read()):
                if e["type"] == "file" and e["name"] != "SKILL.md":
                    # download e["download_url"] to target/sub/e["name"]
                    pass
    except:
        pass
```

### 6. Process in Parallel (for 50+ skills)

For large hauls (50+ skills across multiple repos), dispatch parallel subagents:

```python
from hermes_tools import delegate_task

# Split skills across 4 agents (~25 skills each)
batches = [
    skills[0:25], skills[25:50],
    skills[50:75], skills[75:100],
]
for batch in batches:
    delegate_task(
        goal=f"Read, enhance, and install {len(batch)} skills into Hermes Agent...",
        role="leaf",
    )
# Results deliver back when all complete — do not poll.
```

Each subagent gets isolated context and terminal session. The final summaries
arrive as messages in the conversation.

### 7. Verify Counts

```bash
ls skills/ | wc -l
# Confirm expected total: existing + imported = final count
```

```bash
python scripts/import-community-skills.py
git add -A && git commit -m "Import N skills from {sources}" && git push
```

## Pitfalls

- **GitHub rate limits**: 60/hr unauthenticated; 5000/hr with `GITHUB_TOKEN`
- **Repo clone naming conflicts**: Multiple repos may all be named `skills/`. Always clone with a named target dir: `git clone --depth 1 <url> <repo-name>-skills`
- **MSYS2/git-bash path persistence**: In git-bash, `cd "$WORKDIR"` changes don't persist between command invocations. Always use explicit absolute paths (`/c/Users/...`) rather than relative `cd` state.
- **False-positive skill detection**: A `SKILL.md` filename doesn't guarantee real skill content. Filter by: has frontmatter (`---`), has substantive body (>200 chars), has sections (`## `), has meaningful description. Reject non-skill files like CHANGELOG.md, CONTEXT.md, templates, LICENSE files.
- **Repo structure varies**: Flat vs categorized — adjust paths per source
- **License compliance**: Preserve licenses and add `source:` attribution
- **Name collisions**: Check all names before bulk import
- **Stale content**: Re-check upstream quarterly
- **Branch naming**: Some repos use `master` not `main`
- **Idempotency of frontmatter enhancement**: Re-running `enhance_frontmatter` on already-enhanced content duplicates `metadata:` blocks if the entire old metadata subtree isn't dropped — orphaned nested keys (e.g. `related_skills:` under `hermes:`) survive the filter and a new `metadata:` block gets appended on every run. **Always** drop the complete indented subtree under `metadata:` (every following line indented more than `metadata:` itself), not just lines matching `hermes:`/`tags:`/`category:` by name. Verify by round-tripping: `enhance(content) == enhance(enhance(content))`.

## Verification

```bash
ls skills/ | wc -l
grep -l "^source:" skills/*/SKILL.md | wc -l
python3 -c "from pathlib import Path; n=[d.name for d in Path('skills').iterdir() if d.is_dir()]; print([x for x in set(n) if n.count(x)>1] or 'OK')"
```

## Supporting Files

- `references/enhancement-pipeline.md` — Adding Hermes format (trigger, procedure, pitfalls, verification) to imported skills. Documents known bugs: body changes lost when FM updated, false-positive "How to" detection, and proper section matching patterns.
- `references/source-definitions.md` — Full source map and path mappings for all harvested repos.
- `references/resume-from-local-clones.md` — **When GitHub raw fetches are flaky or interrupted**, resume the import from a local staging clone directory instead of re-fetching online. Iterate `rglob("SKILL.md")` over each cloned repo dir, apply `enhance_frontmatter`, and verify idempotency via round-trip equality before writing. The staging dir acts as a checkpoint: if the import is interrupted midway, re-running picks up exactly where it left off (existing target files are skipped).
- `scripts/import_community_skills.py` — The bulk import script. Run from repo root.
- `scripts/resume_skill_import.py` — Resumable import script that reads from local clones (no network fetches), applies frontmatter enhancement idempotently, and copies supporting files (references/templates/scripts/assets/examples).

## Related Skills

- `skills-repo-setup` — Structural repo setup for GitHub
- `skill-factory-system` — Batch skill creation from trend analysis
- `hermes-agent-skill-authoring` — Authoring individual SKILL.md files
