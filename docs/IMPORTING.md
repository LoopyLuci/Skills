# Upstream Import & Customization

How skills from external repositories are brought into this collection as
**adapted** skills — rewritten and restructured for this repo, never vendored as
verbatim copies.

## Why

Copying an upstream skill directory into `skills/` produces a mirror: no
attribution block, no cross-links into this repo, upstream framing, and no way
to tell it apart from the original. The pipeline below instead produces a skill
that is visibly this repository's own work while preserving the upstream's
substantive guidance.

## Sources

| Repository | License | Skills | Notes |
| --- | --- | --- | --- |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | MIT | 23 | Engineering workflow skills |
| [oracle/skills](https://github.com/oracle/skills) | UPL-1.0 | 19 | APEXLang, OCI OKE, Functions, IAM, DB |
| [mattpocock/skills](https://github.com/mattpocock/skills) | MIT | 7 new | 34 were already present and were left untouched |
| [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills) | MIT | 7 | Obsidian CLI, Bases, Canvas, Markdown |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | MIT | 1 | Security audit workflow |
| [Forward-Future/loopy](https://github.com/Forward-Future/loopy) | MIT | 2 | Loop discovery and execution |

Container/index skills (Oracle's `apex`, `apexlang`, `db`, `oci` umbrella files)
and the `fusion` placeholder are skipped — they are navigation pages, not skills.

## Layout

```
_sources/                       # shallow clones of each upstream repo (git-ignored)
scripts/adapted_bodies/         # intermediate rewritten bodies (git-ignored)
scripts/import-community-skills.py   # legacy fetch-and-enhance importer
scripts/import-upstream-skills.py    # clone-aware importer (writes skills/)
scripts/prep-customization.py        # builds the work list + tag index
scripts/assemble-custom-skills.py    # rebuilds skills/<name>/SKILL.md
scripts/customization-worklist.json  # per-skill metadata + batch assignment
scripts/customization-manifest.json  # what was assembled
scripts/imported-upstream-skills.json# import manifest (source, tags, support)
scripts/repo-tag-index.json          # tag -> skill names (for cross-links)
```

## Pipeline

### 1. Import — `scripts/import-upstream-skills.py`

```bash
python scripts/import-upstream-skills.py            # apply
python scripts/import-upstream-skills.py --dry-run  # report only
```

Clones live in `_sources/<owner>_<repo>/` (git-ignored). For each upstream
`SKILL.md` it:

- derives tags from the source and path (plus per-skill overrides),
- collapses versioned duplicates (Oracle `26.1` vs `26.2` → newest),
- skips container/umbrella skills and placeholders,
- skips anything already present in `skills/` (never overwrites),
- copies supporting files (`references/`, `scripts/`, `agents/`, `assets/`,
  `templates/`, `examples/`),
- writes the canonical frontmatter with `metadata.hermes.source`.

### 2. Prepare — `scripts/prep-customization.py`

```bash
python scripts/prep-customization.py
```

Builds `scripts/customization-worklist.json` (name, source, upstream path, title,
description, tags, size, batch) and `scripts/repo-tag-index.json` (tag → skills,
used to compute cross-links). Batches are balanced by line count for parallel work.

### 3. Rewrite — `scripts/adapted_bodies/<name>.md`

Each skill body is condensed and rewritten in original wording: the upstream
title and "when to use" sections are removed (the assembler derives canonical
ones), the prose is restructured, and all commands, paths, URLs, and tables are
preserved exactly. The intermediate bodies are git-ignored but kept on disk so
the assembly step is reproducible.

### 4. Assemble — `scripts/assemble-custom-skills.py`

```bash
python scripts/assemble-custom-skills.py
```

Rebuilds each `skills/<name>/SKILL.md` as:

```
frontmatter (trigger-form description, version 2.0.0, license-correct,
             tags, source, adapted: true)
# <Title>
> adapted notice
## Trigger
## When NOT to Use
<rewritten body>
## Related Skills in This Repo
## Adaptation Notes
## Source & Attribution
```

Related skills are computed: up to four peers from the same upstream, plus up to
three skills elsewhere in the repo that share a specific (non-generic) tag.

### 5. Document — `scripts/generate-docs-index.py`

```bash
python -m ci --only build          # refresh dist/skills-index.json
python scripts/generate-docs-index.py
```

Regenerates [docs/skills-index.md](../docs/skills-index.md).

## Customization rules (enforced by CI)

The `skills` stage of the pipeline fails on:

- missing `SKILL.md`, unparsable frontmatter, missing required keys;
- `name` not matching the directory;
- license outside the allowlist;
- missing or empty `tags`;
- adapted skill without `source` attribution;
- broken `../<name>/SKILL.md` cross-links;
- missing referenced support files;
- nested `.git`/`__pycache__`, oversize files/directories;
- duplicate bodies or duplicate title+description.

It warns when an adapted skill drifts back toward upstream: more than 20
consecutive verbatim prose lines or a similarity above 0.75 against the source
file in `_sources/`.

## Adding a new upstream

1. Add the repository to `SOURCES` in `scripts/import-upstream-skills.py`
   (and a license entry in `scripts/assemble-custom-skills.py`).
2. `python scripts/import-upstream-skills.py`
3. `python scripts/prep-customization.py`
4. Rewrite the new bodies into `scripts/adapted_bodies/`.
5. `python scripts/assemble-custom-skills.py`
6. `python -m ci --full` — must be green.
7. `python scripts/generate-docs-index.py`

## Verification

```bash
python -m ci --full          # all seven stages
python -m ci --only skills   # skill rules only
```

Reports land in `ci/reports/` (JSON + `history.jsonl`) and logs in `ci/logs/`.
