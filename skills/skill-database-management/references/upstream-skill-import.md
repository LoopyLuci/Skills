# Upstream Skill Import — Algorithm and Templates

Depth for step 6 of SKILL.md. Reimplement or audit `scripts/import-upstream-skills.py`.

## Discovery and filtering

- Walk `rglob("SKILL.md")`, skip any path containing `.git`.
- Container test: `any(child.is_dir() and (child / "SKILL.md").exists() for child in skill_dir.iterdir())`.
- Placeholder test: description starts with "Placeholder for future".
- Version key: max over path segments matching `\d+(\.\d+)?` of `major*100 + minor`; dedupe by `name`, keep the highest.

## Frontmatter normalization

Canonical template. `metadata.hermes.source` carries attribution; preserve unknown upstream keys such as `argument-hint` rather than dropping them.

```
---
name: <name>
description: <single-line description>
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
<extra upstream keys>

metadata:
  hermes:
    tags: [<tags>]
    source: <owner>/<repo>
---

<body verbatim>
```

## Tag derivation

`tags = base_tags(source) + slug(parent_segments) + overrides(name)`, deduped, order preserved.

- `parent_segments = rel.parts[:-2]` — exclude the filename and the skill's own directory.
- Drop noise segments (`skills`, `plugins`, `obsidian`) and version-like segments.
- Keep tags topical; never the skill's own name.

## Support files

Copy every entry in the skill directory except `SKILL.md` and `.git` (directories recursively, ignoring `.git` and `__pycache__`). Record the copied names in the manifest and verify manifest == disk.

## Verification recipe

- Every imported `SKILL.md` parses, `name` matches its directory, description non-empty, tags non-empty, `source` present.
- Manifest support list equals the actual sibling entries.
- No nested `.git` under any imported skill.
- `git status --short` shows only the expected new dirs plus the importer and manifest; `_sources/` absent (ignored).

## Worked example: oracle/skills

Nested `apex/apexlang/26.1/*` and `26.2/*` plus umbrellas `apex`, `apexlang`, `db`, `oci`. Result: containers dropped (6), version duplicates collapsed (4), 19 real skills imported. `apexlang-generation` exists only in 26.1, so it survives as the sole candidate for that name.
