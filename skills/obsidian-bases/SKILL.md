---
name: obsidian-bases
description: Use when working with .base files, creating database-like views of notes, or when the user mentions Bases, table views, card views, kanban boards, filters, or formulas in Obsidian.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [note-taking, obsidian, productivity]
    source: obsidianmd/obsidian-skills
    adapted: true
---

# Obsidian Bases Skill

> **Adapted for the LoopyLuci Skills collection** from [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Working with .base files, creating database-like views of notes, or when the user mentions Bases, table views, card views, kanban boards, filters, or formulas in Obsidian

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Create and edit Obsidian Bases (`.base` files) — database-like views of your notes with filters, formulas, summaries, and table, card, list, map, and kanban presentations.

## Workflow

1. Create a `.base` file containing valid YAML.
2. Add `filters` to choose which notes appear, by tag, folder, property, or date.
3. Optionally define computed properties under `formulas`.
4. Add one or more views (`table`, `cards`, `list`, `map`, `kanban`) with `order` listing the properties to show.
5. Validate: confirm the YAML parses, and that every referenced property and formula exists. The usual failures are unquoted strings containing YAML-special characters, mismatched quotes inside formulas, and referencing `formula.X` without defining `X`.
6. Test in Obsidian: a YAML error points at the quoting rules below; a file that does not open as a base at all means Bases is off under Settings → Core plugins.

## Schema

```yaml
# Global filters apply to every view in the base.
filters:
  and:
    - 'status == "active"'
    - not:
        - 'file.hasTag("archived")'

# Computed properties, usable across views.
formulas:
  formula_name: 'expression'

# Display names and settings. Note properties need the `note.` prefix here.
properties:
  note.property_name:
    displayName: "Display Name"
  formula.formula_name:
    displayName: "Formula Display Name"
  file.ext:
    displayName: "Extension"

# Custom summary formulas.
summaries:
  custom_summary_name: 'values.mean().round(3)'

views:
  - type: table | cards | list | map | kanban
    name: "View Name"
    limit: 10                    # optional
    groupBy:                     # optional
      property: property_name
      direction: ASC | DESC
    groupOrder:                  # optional: only these groups, in this order
      - value_one
      - null                     # files with no value for the groupBy property
    sort:                        # optional; multiple keys applied in order
      - property: property_name
        direction: ASC | DESC
    filters:                     # view-specific; same structure as global filters
      and:
        - 'status == "active"'
    order:                       # properties to display, in order
      - file.name
      - property_name
      - formula.formula_name
    summaries:                   # map a property to a summary formula
      property_name: Average
```

## Filters

Filters narrow results and can be global or per-view. A filter is either a single expression or a recursive object with exactly one key — `and`, `or`, or `not`.

```yaml
filters: 'status == "done"'

filters:
  and:
    - 'status == "done"'
    - 'priority > 3'

filters:
  or:
    - 'file.hasTag("book")'
    - 'file.hasTag("article")'

filters:
  not:
    - 'file.hasTag("archived")'

filters:
  or:
    - file.hasTag("tag")
    - and:
        - file.hasTag("book")
        - file.hasLink("Textbook")
    - not:
        - file.hasTag("book")
        - file.inFolder("Required Reading")
```

| Operator | Meaning |
| --- | --- |
| `==`, `!=` | equals, not equal |
| `>`, `<`, `>=`, `<=` | comparisons |
| `&&` | logical and |
| `\|\|` | logical or |
| `!` | logical not |

## Properties

Three kinds: note properties from frontmatter (`note.author`, or bare `author`), file metadata (`file.name`, `file.mtime`, …), and formula properties (`formula.my_formula`). In `order`, `filters`, `groupBy`, and `sort` a note property may be bare or prefixed; in the top-level `properties:` section always write `note.author`, because Obsidian ignores a bare key there and shows the raw name as the column header.

| Property | Type | Description |
| --- | --- | --- |
| `file.name` | String | File name |
| `file.basename` | String | File name without extension |
| `file.path` | String | Full path |
| `file.folder` | String | Parent folder path |
| `file.ext` | String | Extension |
| `file.size` | Number | Size in bytes |
| `file.ctime` / `file.mtime` | Date | Created / modified time |
| `file.tags` | List | All tags in the file |
| `file.links` | List | Internal links |
| `file.backlinks` | List | Files linking here — slow in large vaults and not refreshed on vault changes; prefer reversing the lookup with `file.links` |
| `file.embeds` | List | Embeds in the note |
| `file.properties` | Object | All frontmatter properties; not refreshed on vault changes |
| `file.file` | File | File object, usable only in specific functions |

`this` refers to the base file itself in the main content area, to the embedding file when embedded, and to the active file in the sidebar.

## Formulas

Formulas are expressions defined under `formulas`:

```yaml
formulas:
  total: "price * quantity"
  status_icon: 'if(done, "✅", "⏳")'
  formatted_price: 'if(price, price.toFixed(2) + " dollars")'
  created: 'file.ctime.format("YYYY-MM-DD")'
  days_old: '(now() - file.ctime).days'
  days_until_due: 'if(due_date, (date(due_date) - today()).days, "")'
```

Common functions (full type-by-type reference in `references/FUNCTIONS_REFERENCE.md`):

| Function | Signature | Purpose |
| --- | --- | --- |
| `date()` | `date(string): date` | Parse `YYYY-MM-DD HH:mm:ss` |
| `now()` / `today()` | `→ date` | Current date-time / current date at midnight |
| `if()` | `if(cond, then, else?)` | Conditional |
| `duration()` | `duration(string): duration` | Parse a duration string |
| `file()` | `file(path): file` | Get a file object |
| `link()` | `link(path, display?): Link` | Build a link |

Subtracting two dates yields a **Duration**, not a number. Read a numeric field first, then apply number functions: `(date(due) - today()).days` works, while `((date(due) - today()) / 86400000).round(0)` errors because Duration supports neither division nor `.round()`/`.floor()`/`.ceil()` directly. Duration fields are `.days`, `.hours`, `.minutes`, `.seconds`, `.milliseconds`.

Date arithmetic accepts unit suffixes `y`/`year(s)`, `M`/`month(s)`, `d`/`day(s)`, `w`/`week(s)`, `h`/`hour(s)`, `m`/`minute(s)`, `s`/`second(s)`:

```yaml
"now() + \"1 day\""       # tomorrow
"today() + \"7d\""        # a week from today
"(now() - file.ctime).days"
```

## Views

**Table** — `order` lists columns; `summaries` maps a property to a summary formula.

```yaml
views:
  - type: table
    name: "My Table"
    order: [file.name, status, due_date]
    summaries:
      price: Sum
      count: Average
```

**Cards** — a visual gallery:

```yaml
views:
  - type: cards
    name: "Gallery"
    order: [file.name, cover_image, description]
```

**List** — minimal rows:

```yaml
views:
  - type: list
    name: "Simple List"
    order: [file.name, status]
```

**Kanban** (Obsidian 1.14+) — requires `groupBy`; `groupOrder` fixes which columns appear and in what order, with `null` for files lacking the value. Dragging a card writes that property back to the note. Only Markdown notes move, except when grouping by `file.folder`, where a move relocates the file. Grouping by a formula or a non-folder file property makes cards and columns immovable and blocks creating notes from a column.

```yaml
views:
  - type: kanban
    name: "Projects"
    groupBy: { property: note.status, direction: ASC }
    groupOrder: [Planned, In progress, Done]
    order: [file.name, due_date]
```

**Map** — needs latitude/longitude properties and the Maps community plugin.

## Sorting

Each sort entry names a `property` and an uppercase `direction` (`ASC`/`DESC`); any other value, or a sort written as a string, is silently ignored. Entries apply in order — the first is the primary key, later ones break ties. Text sorts A→Z / Z→A, numbers 0→9 / 9→0, dates old→new / new→old. Any property type may be used, including `formula.*` and `file.*`.

```yaml
sort:
  - property: due
    direction: ASC
  - property: file.name
    direction: ASC
```

## Built-in summaries

`Average`, `Min`, `Max`, `Sum`, `Range`, `Median`, `Stddev` (numbers); `Earliest`, `Latest`, `Range` (dates); `Checked`, `Unchecked` (booleans); `Empty`, `Filled`, `Unique` (any).

## Verification

- [ ] YAML parses with no errors.
- [ ] Every referenced property and formula exists; note properties prefixed in `properties:`.
- [ ] Filter operators and nesting valid.
- [ ] Duration values accessed through a numeric field before rounding.
- [ ] View renders correctly in Obsidian, including kanban `groupBy` constraints.

## Related Skills in This Repo

- [json-canvas](../json-canvas/SKILL.md) — Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, or w...
- [obsidian-markdown](../obsidian-markdown/SKILL.md) — Use when working with .md files in Obsidian, or when the user mentions wikilinks, callouts...
- [obsidian-cli](../obsidian-cli/SKILL.md) — Use when the user asks to interact with their Obsidian vault, manage notes, search vault c...
- [knap](../knap/SKILL.md) — Use when the user asks to apply a Knap template, turn JSON or CSV data into notes, batch-g...
- [obsidian-vault](../obsidian-vault/SKILL.md) — Use when searching, creating, or managing notes in an Obsidian vault
- [obsidian-note-taking-workflow](../obsidian-note-taking-workflow/SKILL.md) — Use when implementing Obsidian workflows.
- [obsidian](../obsidian/SKILL.md) — Read, search, create, and edit notes in the Obsidian vault.

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills)
- Path: `_sources/obsidianmd_obsidian-skills/plugins/obsidian/skills/obsidian-bases/SKILL.md`
- License: MIT — Copyright (c) 2026 Steph Ango (@kepano)
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
