---
name: json-canvas
description: Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, or when the user mentions Canvas files in Obsidian.
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

# JSON Canvas Skill

> **Adapted for the LoopyLuci Skills collection** from [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Working with .canvas files, creating visual canvases, mind maps, flowcharts, or when the user mentions Canvas files in Obsidian

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Create and edit JSON Canvas files (`.canvas`) with nodes, edges, groups, and connections, following the [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/).

## File structure

```json
{
  "nodes": [],
  "edges": []
}
```

`nodes` and `edges` are optional arrays. Array order sets z-index: the first node is the bottom layer, the last is the top.

## Workflows

**Create a canvas.** Write the base structure, generate a unique 16-character hex ID per node, add nodes with `id`, `type`, `x`, `y`, `width`, `height`, add edges whose `fromNode`/`toNode` reference valid node IDs, then validate.

**Add a node.** Parse the existing file, generate an ID that collides with nothing, pick a position 50–100 px clear of existing nodes, append the node, optionally add edges, then validate.

**Connect two nodes.** Generate a unique edge ID, set `fromNode`/`toNode`, optionally set `fromSide`/`toSide` and `label`, append, then validate.

**Edit.** Parse, locate by `id`, change attributes, write back, then re-validate ID uniqueness and edge integrity.

## Nodes

Generic attributes:

| Attribute | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | Yes | string | Unique 16-char hex identifier |
| `type` | Yes | string | `text`, `file`, `link`, or `group` |
| `x`, `y` | Yes | integer | Top-left position in pixels |
| `width`, `height` | Yes | integer | Size in pixels |
| `color` | No | canvasColor | Preset `"1"`–`"6"` or hex |

Text nodes add `text` (Markdown):

```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 0, "y": 0, "width": 400, "height": 200,
  "text": "# Hello World\n\nThis is **Markdown** content."
}
```

Use `\n` for line breaks in JSON strings — never the literal `\\n`, which Obsidian renders as `\` and `n`. Escape inner double quotes as `\"`; unescaped quotes break the parse and the canvas fails to render. When generating canvas JSON programmatically, always use a JSON serializer rather than string concatenation. Write `.canvas` files directly — `obsidian create content=` turns every `\n` into a raw newline and breaks the JSON.

File nodes add `file` and optional `subpath` (starting with `#` for a heading or block):

```json
{
  "id": "a1b2c3d4e5f67890",
  "type": "file",
  "x": 500, "y": 0, "width": 400, "height": 300,
  "file": "Attachments/diagram.png"
}
```

Link nodes add `url`:

```json
{
  "id": "c3d4e5f678901234",
  "type": "link",
  "x": 1000, "y": 0, "width": 400, "height": 200,
  "url": "https://obsidian.md"
}
```

Group nodes are visual containers; place children inside their bounds and add optional `label`, `background`, and `backgroundStyle` (`cover`, `ratio`, `repeat`):

```json
{
  "id": "d4e5f6789012345a",
  "type": "group",
  "x": -50, "y": -50, "width": 1000, "height": 600,
  "label": "Project Overview",
  "color": "4"
}
```

## Edges

| Attribute | Required | Default | Description |
| --- | --- | --- | --- |
| `id` | Yes | — | Unique identifier |
| `fromNode`, `toNode` | Yes | — | Source and target node IDs |
| `fromSide`, `toSide` | No | — | `top`, `right`, `bottom`, or `left` |
| `fromEnd` | No | `none` | `none` or `arrow` |
| `toEnd` | No | `arrow` | `none` or `arrow` |
| `color` | No | — | Line color |
| `label` | No | — | Text label |

```json
{
  "id": "0123456789abcdef",
  "fromNode": "6f0ad84f44ce9c17",
  "fromSide": "right",
  "toNode": "a1b2c3d4e5f67890",
  "toSide": "left",
  "toEnd": "arrow",
  "label": "leads to"
}
```

## Colors

| Preset | Color |
| --- | --- |
| `"1"` | Red |
| `"2"` | Orange |
| `"3"` | Yellow |
| `"4"` | Green |
| `"5"` | Cyan |
| `"6"` | Purple |

Preset values are intentionally undefined — applications use their own brand colors. Hex strings are also accepted.

## IDs and layout

IDs are 16-character lowercase hex strings (64-bit random), e.g. `6f0ad84f44ce9c17`. Coordinates may be negative (the canvas is infinite), `x` increases right and `y` increases down, and position is the top-left corner. Space nodes 50–100 px apart, leave 20–50 px padding inside groups, and align to a 10 or 20 px grid.

| Node type | Width | Height | CJK width (×1.5) |
| --- | --- | --- | --- |
| Small text | 200–300 | 80–150 | 300–450 |
| Medium text | 300–450 | 150–300 | 450–675 |
| Large text | 400–600 | 300–500 | 600–900 |
| File preview | 300–500 | 200–400 | 450–750 |
| Link preview | 250–400 | 100–200 | 375–600 |

CJK characters are wider than Latin; multiply the width by about 1.5× for primarily Chinese, Japanese, or Korean content to avoid cramped layouts.

## Validation checklist

1. All `id` values unique across nodes and edges.
2. Every `fromNode`/`toNode` references an existing node.
3. Required per-type fields present (`text`, `file`, or `url`).
4. `type` is `text`, `file`, `link`, or `group`.
5. `fromSide`/`toSide` are `top`, `right`, `bottom`, or `left`.
6. `fromEnd`/`toEnd` are `none` or `arrow`.
7. Colors are `"1"`–`"6"` or valid hex.
8. Double quotes in `text` and `file` are escaped as `\"`.
9. JSON parses.

Failures usually mean duplicate IDs, dangling edge references, or malformed strings (especially unescaped newlines).

## References

- [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/)
- [JSON Canvas GitHub](https://github.com/obsidianmd/jsoncanvas)
- `references/EXAMPLES.md` — full canvases: mind maps, project boards, research canvases, flowcharts.

## Related Skills in This Repo

- [obsidian-bases](../obsidian-bases/SKILL.md) — Use when working with .base files, creating database-like views of notes, or when the user...
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
- Path: `_sources/obsidianmd_obsidian-skills/plugins/obsidian/skills/json-canvas/SKILL.md`
- License: MIT — Copyright (c) 2026 Steph Ango (@kepano)
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
