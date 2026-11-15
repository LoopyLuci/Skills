# LoopyLuci Skills

A curated collection of **10,107 AI agent skills** built for [Hermes Agent](https://hermes-agent.nousresearch.com/) and compatible with any agent that supports the [agentskills.io](https://agentskills.io/) open standard.

Skills cover every major domain — software development, data/AI, cybersecurity, cloud, business, science, healthcare, engineering, creative, education, government, and more — across **5,789 distinct tags**. The repository holds **12,800+ tracked files** (~60 MB of skill content) and loads skills on demand.

> Counts on this page are read from the repository. The collection grows as skills
> sync in from connected Hermes instances; regenerate the per-skill index with
> `python -m ci --only build && python scripts/generate-docs-index.py`.

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/LoopyLuci/Skills.git ~/LoopyLuci-skills
cd ~/LoopyLuci-skills

# Option A — external skills directory (recommended; read-only scan)
# Add to ~/.hermes/config.yaml:
#   skills:
#     external_dirs:
#       - ~/LoopyLuci-skills/skills

# Option B — skill tap (hub-managed updates)
hermes skills tap add LoopyLuci/Skills
hermes skills tap list

# Option C — install a single skill by URL
hermes skills install https://raw.githubusercontent.com/LoopyLuci/Skills/main/skills/<skill-name>/SKILL.md

# Option D — inspect installed skills and browse what is available
hermes skills list
hermes skills browse
```

No per-skill install is required for Options A and B: every skill is available
immediately as a slash command.

---

## Repository Layout

```
.
├── skills/                      # 10,107 skill directories (flat)
│   └── <skill-name>/
│       ├── SKILL.md             # required — the skill itself
│       ├── references/          # optional — supporting docs
│       ├── scripts/             # optional — helper scripts
│       ├── templates/           # optional — output templates
│       ├── assets/              # optional — images, data
│       ├── agents/              # optional — subagent definitions
│       └── examples/            # optional — worked examples
├── scripts/                     # tooling: generator, import, sync, docs
│   ├── skill-generator/         # skill creation/validation/enrichment
│   ├── import-upstream-skills.py# import skills from upstream repos
│   ├── prep-customization.py    # build the customization work list
│   ├── assemble-custom-skills.py# assemble rewritten skills
│   ├── generate-docs-index.py   # regenerate docs/skills-index.md
│   └── sync-*.py|.sh            # Hermes ↔ repo synchronisation
├── ci/                          # local on-device CI/CD pipeline
│   ├── stages/                  # preflight, static, skills, tests, build, smoke, deploy
│   ├── hooks/                   # git pre-commit / pre-push
│   ├── config.json              # thresholds, allowlists, patterns
│   └── README.md                # pipeline documentation
├── tests/                       # stdlib unittest suite for the pipeline
├── docs/
│   └── skills-index.md          # every skill, grouped by category
├── _sources/                    # upstream clones used by the importer (git-ignored)
└── dist/                        # index + release archive (git-ignored)
```

---

## Finding a Skill

1. **Complete index** — [docs/skills-index.md](docs/skills-index.md) lists all 10,107
   skills with descriptions, grouped by category and linked to each `SKILL.md`.
2. **Machine-readable** — `dist/skills-index.json` (built by `python -m ci --only build`)
   carries name, title, description, tags, license, source, and file/byte counts.
3. **By tag** — search frontmatter `metadata.hermes.tags`, e.g.
   `grep -rl "tags:.*kubernetes" skills --include=SKILL.md`.
4. **By name** — skills are flat: `skills/<name>/SKILL.md`.
5. **Installed view** — `hermes skills list` and `hermes skills browse`.

---

## Skill Format Specification

### Directory structure

Each skill is a directory named exactly like its frontmatter `name`:

```
skills/<skill-name>/
├── SKILL.md          # required
├── references/       # optional
├── scripts/          # optional
├── templates/        # optional
├── assets/           # optional
├── agents/           # optional
└── examples/         # optional
```

### `SKILL.md` frontmatter

```yaml
---
name: skill-name              # required — kebab-case, must match the directory
description: Use when ...     # required — one sentence, ideally <= 120 chars
version: 1.0.0                # required — semver
author: LoopyLuci Community   # required
license: MIT                  # required — SPDX identifier (see License below)
platforms: [any]              # required — [linux, macos, windows, any]
metadata:
  hermes:
    tags: [tag1, tag2]        # required — 2-5 lowercase tags recommended
    source: owner/repo        # required for adapted skills (attribution)
    adapted: true             # marks a skill rewritten from an upstream source
---
```

### Body structure

```markdown
# Skill Title

One-sentence summary of what the skill does.

> Adapted notice (adapted skills only)

## Trigger
- Conditions that activate this skill

## When NOT to Use
- Conditions that belong to another skill

## Core Sections...
### ...

## Related Skills in This Repo
- [other-skill](../other-skill/SKILL.md) — description

## Adaptation Notes          # adapted skills only
- ...

## Source & Attribution      # adapted skills only
- Upstream, path, license, retrieval date
```

### Tag guidelines

- Lowercase, kebab-case for multi-word tags: `machine-learning`, `data-engineering`.
- 2–5 tags is the norm (the repo median is 3; the CI check requires at least one).
- Be specific: `postgresql` over `database`, `react` over `frontend`.
- Reuse existing tags for consistency — the CI pipeline flags self-referential tags.

---

## Categories

Counts below come from [docs/skills-index.md](docs/skills-index.md).

| Category | Skills |
| --- | --- |
| Software Development & Engineering | 2,603 |
| Science, Research & Healthcare | 1,639 |
| Business, Product & Management | 1,536 |
| General & Other | 1,441 |
| Data Science, AI & Machine Learning | 852 |
| Cloud & Infrastructure | 596 |
| Engineering & Manufacturing | 597 |
| Creative, Design & Media | 426 |
| Cybersecurity | 264 |
| Education & Personal Development | 129 |
| Government, Law & Public Policy | 24 |
| **Total** | **10,107** |

The most common tags are `biotech` (574), `business` (443), `data` (388), `email`
(388), `management` (355), `backend` (350), `cloud` (320), `engineering` (318),
`security` (315), and `finance` (310).

---

## Local CI/CD Pipeline

A fully custom, on-device pipeline — **stdlib-only, no third-party Python
packages**. See [ci/README.md](ci/README.md) for the full reference.

```bash
python -m ci --full      # every stage
python -m ci --fast      # preflight, static, skills, tests
python -m ci --only skills tests
python -m ci --list      # show the plan
python -m ci --full --push
```

| Stage | What it does |
| --- | --- |
| `preflight` | Python version, git branch/commit/dirty state, remote, free disk, tool availability, config sanity |
| `static` | `compileall`; `ruff`; secret, bare-`except`, oversize-file and JSON scans (working tree only) |
| `skills` | Parallel validation of every `skills/*/SKILL.md` — frontmatter, name/dir match, license, tags, attribution, cross-links, support files, duplicates, upstream overlap |
| `tests` | `unittest` discovery with hard timeout and flaky rerun |
| `build` | `dist/skills-index.json` + release archive |
| `smoke` | Artifact integrity: index parses, counts match, samples parse, archive verified |
| `deploy` | Remote reachability + receipt; pushes only with `--push` on a clean tree |

Typical runtime on this repository: **~21 s full**, **~9.5 s fast** across
10,107 skills and ~12,800 working-tree files.

Safety features: PID lock with stale takeover, per-command timeouts with
process-tree kill, change-aware stage selection, JSON reports with history and
pruning, and a flaky-test rerun that separates flakes from real failures.

### Automation

```bash
python -m ci.install_hooks     # pre-commit (preflight+static) + pre-push (fast)
python -m ci.watch             # poll watcher; runs --fast on change
python -m ci.watch --once      # single run, for schedulers
```

Scheduled jobs (Hermes cron, delivering locally):

- `skills-sync-hermes-repo` — every 30 m, Hermes ↔ repo sync.
- `skills-ci-fast` — every 60 m, fast pipeline.
- `skills-ci-full-daily` — daily at 03:00, full pipeline including build/archive.

---

## Upstream Import & Customization

59 skills are adapted from six upstream community repositories rather than
copied. The pipeline lives in `scripts/`; full details in
[docs/IMPORTING.md](docs/IMPORTING.md).

| Upstream | Skills |
| --- | --- |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 23 |
| [oracle/skills](https://github.com/oracle/skills) | 19 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 7 new (34 already present) |
| [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills) | 7 |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | 1 |
| [Forward-Future/loopy](https://github.com/Forward-Future/loopy) | 2 |

Each adapted skill carries a rewritten description, derived Trigger and
When-NOT-to-Use sections, a condensed/restructured body, real cross-links into
this repo, adaptation notes, and license-correct attribution. The CI pipeline
flags any adapted skill that drifts back toward verbatim upstream text.

---

## Automatic Sync

The repository syncs bidirectionally with Hermes Agent instances on a schedule
(currently every 30 minutes):

```bash
./scripts/sync-from-hermes.sh            # dry run
./scripts/sync-from-hermes.sh --apply    # copy changes in
./scripts/sync-from-hermes.sh --force    # sync, commit, and push
```

Other sync helpers: `scripts/sync-bidirectional.py`, `scripts/sync-skills-fast.py`,
`scripts/sync-hermes-windows.py`, `scripts/sync-machine.py`.

---

## Tests

`tests/` contains the stdlib `unittest` suite for the pipeline itself — validation
rules and orchestration units. It runs as the `tests` stage:

```bash
python -m unittest discover -s tests -t . -v
```

27 tests cover frontmatter parsing, every skill rule, planning, change selection,
locking, pruning, and the secret-scanning heuristics.

---

## Skill Generator Toolkit

```bash
# Generate one skill
python scripts/skill-generator/generate_skill.py generate \
  --name my-skill --description "Does X" --tags python,cli [--category CAT] --apply

# Bulk generate from a JSON file ([{"name","description","tags"}, ...])
python scripts/skill-generator/generate_skill.py bulk skills.json --apply

# Validate one skill
python scripts/skill-generator/generate_skill.py validate skills/my-skill

# Enrich boilerplate skills with real content
python scripts/skill-generator/generate_skill.py enrich --apply
```

`scripts/skill-generator/` also ships `README.md` and `SKILL-FORMAT.md`.

---

## Contributing

1. **Add a skill** — use the generator, or create `skills/<name>/SKILL.md` by hand
   following the format above.
2. **Validate** — run `python -m ci --fast` (or `python -m ci --only skills`).
3. **Commit** — the pre-commit hook runs preflight + static automatically.
4. **Push** — the pre-push hook runs the fast pipeline; it must be green.

Bulk additions and upstream imports are welcome as pull requests.

---

## License & Attribution

- **MIT** — 10,088 skills, including all adapted skills from MIT-licensed upstreams.
- **UPL-1.0** — 19 skills derived from [oracle/skills](https://github.com/oracle/skills)
  (Copyright (c) 2025 Oracle and/or its affiliates).

Adapted skills retain their upstream license and credit the source repository,
path, and copyright holder in a `Source & Attribution` section; the CI pipeline
requires that attribution and flags missing or altered licenses.

---

## Documentation Map

| Document | Contents |
| --- | --- |
| [docs/skills-index.md](docs/skills-index.md) | Every skill, grouped by category, with descriptions |
| [ci/README.md](ci/README.md) | Pipeline stages, CLI, automation, configuration |
| [docs/IMPORTING.md](docs/IMPORTING.md) | Upstream import and customization workflow |
| [scripts/skill-generator/SKILL-FORMAT.md](scripts/skill-generator/SKILL-FORMAT.md) | Generator-specific format notes |
| [Hermes Agent docs](https://hermes-agent.nousresearch.com/docs) | Host agent documentation |
