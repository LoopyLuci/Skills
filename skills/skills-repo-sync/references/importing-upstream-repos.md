# Importing Third-Party Skill Repos into a Curated Collection

Distinct from bidirectional sync (Hermes <-> your repo): this is bringing an
**external** skills repo into your collection as first-class, reformatted
entries. The bar is that the result must be recognisably yours, not a vendor
mirror.

## Procedure

1. **Clone into a git-ignored vendor dir**, e.g. `_sources/<owner>_<repo>/`.
   Add it to `.gitignore` so the vendor tree never enters history. Keep the
   clones: they are the overlap reference for later verification.
2. **Survey before writing.** Enumerate every `SKILL.md`, extract frontmatter
   `name`, description, title, and line count. Build:
   - a **work list** (JSON) with name, source, upstream path, title,
     description, tags, and batch number;
   - a **repo tag index** for cross-linking.
3. **Deduplicate before importing:**
   - collapse version-nested copies (`.../26.1/x` vs `.../26.2/x`) to the newest;
   - skip **container/index skills** — any `SKILL.md` whose directory holds
     child directories that also contain `SKILL.md` (umbrella pages);
   - skip explicit placeholders ("Placeholder for future ...").
4. **Skip name collisions** with skills you already have. Never overwrite an
   existing curated entry; report the skip.
5. **Adapt each skill** to your canonical frontmatter (name, description in
   trigger form, version, author, license, platforms, `metadata.hermes.tags`)
   and add: a Trigger section, a When-NOT-to-Use section, a Related Skills
   section (real cross-links into your collection), Adaptation Notes, and
   Source & Attribution with the upstream repo, path, **license**, and
   copyright holder.
6. **Carry supporting files** (`references/`, `scripts/`, `agents/`,
   `assets/`, `templates/`) next to the skill so relative links resolve.
7. **Verify** (see below), then commit on a branch, push, open a PR, merge.

## The differentiation bar

"Customised, not copied" means the body is **condensed and reworded**, not
paraphrased by a thesaurus:

- drop the upstream "When to Use" section (you generate a canonical Trigger);
- keep commands, paths, URLs, tables, and code blocks verbatim — they are
  functional reference data;
- rewrite the surrounding prose;
- add the new sections listed above.

**Measure it.** Compute, per skill, the longest common run of prose lines
against the upstream body (exclude fenced code blocks) and a similarity ratio.
A healthy result is a median run of a couple of lines and a mean similarity
well under 0.5. If one file stands out, rewrite it — do not ship it.

## Pitfalls

- **Container skills look like skills.** Detect them structurally (child dirs
  containing `SKILL.md`), not by name.
- **Version-nested duplicates silently double-import.** Dedupe by frontmatter
  name and keep the highest version.
- **Frontmatter `name` can differ from the directory name** (common in
  vendor repos). Key the work list by the frontmatter name, and validate
  `name == directory` on import.
- **Nested metadata is easy to mis-read.** Attribution and tags usually live
  under `metadata.hermes.*`; a validator that only checks top-level keys will
  false-positive. Search the raw frontmatter for `^\s+source:` /
  `^\s+tags:` as well as top-level.
- **Licenses differ per source.** Record each repo's actual license
  (MIT vs UPL-1.0 vs Apache-2.0) and its copyright line; do not assume MIT.
- **Native tools need native paths.** On an MSYS/Git-Bash host, `git -C
  /h/...` fails; pass `H:/...` (forward slashes) to git and other native
  binaries.
- **Large rewrites can outrun a rate-limited model.** Fanning a big rewrite
  out to many subagents on a metered/free provider can burn an hour and
  return nothing (HTTP 429). Keep batches small, or do the rewrites inline
  with file tools.
- **File-write guards.** An overwrite can be refused after a partial read;
  re-read the file or remove it before rewriting. Do not retry the identical
  write in a loop.

## Verification

- every entry parses, `name` matches its directory, required keys present;
- every cross-link target exists (build the name set once, check `../x/SKILL.md`);
- referenced support files exist in the skill dir or elsewhere in the repo;
- no nested `.git`/`__pycache__`; sizes within caps;
- no duplicate bodies/descriptions across the collection;
- overlap metric within bounds for every adapted skill;
- adapted entries carry a license-correct attribution block.
