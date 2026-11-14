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

## Customization pass (never vendor a copy)

Raw import is step one. This repo's convention is a condensed, restructured adaptation
in original wording, so read one already-adapted skill in the target repo before writing
and match its shape. The user's bar: nothing directly copied, everything customized and
improved, upstream attribution retained.

Pipeline, in order:
1. `scripts/prep-customization.py` — builds the work list (name, source, source_dir,
   upstream_path, title, description, tags, line count, batch) and indexes existing repo
   tags into `scripts/repo-tag-index.json`. Balance skills into batches by line count.
2. Rewrite each body into `scripts/adapted_bodies/<name>.md` (git-ignored intermediate).
3. `scripts/assemble-custom-skills.py` — rebuilds `skills/<name>/SKILL.md` with canonical
   frontmatter plus generated sections.

Rewrite contract per body:
- Markdown only: no YAML frontmatter, no top-level `# Title` (the assembler adds it).
- Omit the upstream "When to Use" / "When NOT to Use" sections; the assembler derives
  canonical Trigger and When-NOT-to-Use from the upstream description and anti-patterns.
- Open with an original 2-4 sentence overview; keep the upstream's own headings where they
  earn their place; close with a Verification/Checklist section.
- Reword all explanatory prose. Preserve fenced code, commands, paths, URLs, identifiers,
  and table information exactly — functional reference data is exempt from the
  no-verbatim rule.
- Do not invent tools, commands, or facts; match the original's level of detail.

Assembly output, after the body:
- `## Trigger` — bullets parsed from the upstream description's "Use when / Use for"
  clauses; fall back to the whole description when none exist.
- `## When NOT to Use` — bullets lifted from upstream anti-pattern sections (when-not,
  red flags, rationalizations, pitfalls); fall back to a scope reminder if none.
- `## Related Skills in This Repo` — same-source peers first, then repo skills ranked by
  shared tags. Exclude generic tags (`productivity`, `engineering`,
  `software-development`, `automation`, `agent-skills`, `agent-workflow`, `ai-agents`,
  `general`, `tools`) from matching, or every skill cross-links to unrelated ones.
- `## Adaptation Notes` — what changed.
- `## Source & Attribution` — upstream URL, path, license + copyright holder, date.
- Frontmatter: version 2.0.0, `metadata.hermes.source` and `adapted: true`, and the
  per-source license. Licenses differ by upstream (most MIT; oracle is UPL-1.0) — read
  each source repo's LICENSE and record holder and year; never assume MIT.

Differentiation check (run after assembly, before commit):
- Longest common contiguous line run between rewritten body and upstream body, computed
  on prose only (strip fenced code blocks first), plus a difflib similarity ratio.
- Expect a low median run and no long runs; rewrite any outlier instead of shipping it.
  A subagent-written batch can still copy long spans, so measure rather than eyeball.
- Also verify: frontmatter parses, exactly one H1 outside code fences, every required
  section present, and every `../<skill>/SKILL.md` cross-link resolves to a real skill.

Orchestration note: if a delegated fan-out fails on provider rate limits, finish the
remaining rewrites directly in the main session instead of re-dispatching the same batch.
A failed child may still have written some files — diff the output directory against the
work list before redoing anything.
