---
name: obsidian-cli
description: Use when the user asks to interact with their Obsidian vault, manage notes, search vault content, perform vault operations from the command line, or develop and debug Obsidian plugins and themes.
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

# Obsidian CLI

> **Adapted for the LoopyLuci Skills collection** from [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- The user asks to interact with their Obsidian vault, manage notes, search vault content, perform vault operations from the command line, or develop and debug Obsidian plugins and themes

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Drive a running Obsidian instance from the command line with the `obsidian` CLI — read, create, search, and manage notes, tasks, and properties, plus a develop/debug surface for plugins and themes.

## Before using the CLI

Run `obsidian help` to confirm availability. If it is missing, point the user to https://help.obsidian.md/cli to enable it. The command ships with the Obsidian installer; do not install the unrelated npm package `obsidian-cli`. If it cannot find Obsidian, ask the user to open the desktop app and retry — in a sandboxed shell the same message can mean the sandbox blocked the CLI's local socket. On WSL, run `Obsidian.com` from the Windows install folder rather than `Obsidian.exe`: the `.com` console wrapper prints output, while the `.exe` exits silently.

The CLI exits `0` even when a command fails, so read its output before claiming success. Quote parameters for the current shell, and pass note text as literal argument data — never as executable shell syntax.

## Syntax

`obsidian help` lists every command and stays current; full docs live at https://help.obsidian.md/cli.

**Parameters** take a value with `=`, quoted when they contain spaces:

```bash
obsidian create name="My Note" content="Hello world"
```

**Flags** are valueless booleans:

```bash
obsidian create name="My Note" open overwrite
```

Use `overwrite` only when replacing an existing file is intended. Opening is opt-in (`open`, plus `newtab` for a new tab); there is no `silent` flag.

In `content=`, `\n` becomes a newline and `\t` a tab. Every occurrence is converted, with no escape, so text such as LaTeX `\theta` or a path `C:\notes` is corrupted — write content containing backslashes, or longer than about 4 KB, directly to the note's file instead.

A dot in a file name starts an extension, so include the extension when the name contains one: `create name="Meeting 2026.11.06.md"`, `rename name="v1.2 notes.md"`, `move to="Archive 2026.10/Note.md"`.

## Targeting

`file=<name>` resolves like a wikilink — name only, `.md` optional, other types needing their extension (e.g. `file="Projects.base"`); aliases do not resolve. `path=<path>` is the exact path from the vault root, e.g. `folder/note.md`. Without either, the active file is used.

Without `vault=`, commands target the vault containing the current directory, then the most recently focused vault. `vault=<name>` works only as the first parameter and is ignored elsewhere:

```bash
obsidian vault="My Vault" search query="test"
```

Use it when the user has selected a vault; if the target is unclear and there are several, ask before changing files.

## Common patterns

```bash
obsidian read file="My Note"
obsidian create name="New Note" template="Template"
obsidian create name="New Note" content="# Hello" open
obsidian append file="My Note" content="New line"
obsidian rename path="folder/note.md" name="New name"
obsidian move path="folder/note.md" to="archive/"
obsidian delete path="folder/note.md"
obsidian search query="search term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
obsidian tags sort=count counts
obsidian backlinks file="My Note"
```

Prefer `rename` and `move` over filesystem `mv` or `obsidian eval` so Obsidian can update links. If other notes link to the file and automatic internal-link updates are disabled, Obsidian prompts in a dialog and the command waits. `delete` moves the file to trash; pass `permanent` only when the user asks. Prefer `create` and `append` over `eval` for writing bodies. Add `total` to list commands for a count.

`--copy`, `--json`, `--md`, `--tsv`, and `--csv` work only **after** the command name. Placed before it — or before `vault=` — they fail, typically as `Command "--copy" not found`, because the first token is treated as the command. Put `vault=` first and double-dash options last:

```bash
obsidian tasks todo total --copy
obsidian vault="My Vault" search query="TODO" --copy
obsidian tasks todo format=json
```

## Plugin development

Enable console capture once with `obsidian dev:debug on` so messages from the reload are kept, then iterate:

1. **Reload** — `obsidian plugin:reload id=my-plugin`
2. **Check for errors** — `obsidian dev:errors` (fix and repeat from 1)
3. **Verify visually** — `obsidian dev:screenshot`, then `obsidian dev:dom selector=".workspace-leaf" text`
4. **Check console output** — `obsidian dev:console level=error`

`dev:screenshot` saves to a temporary file and prints its path; a relative `path=` saves inside the vault. Other developer commands:

```bash
obsidian eval code="app.vault.getFiles().length"
obsidian dev:css selector=".workspace-leaf" prop=background-color
obsidian dev:mobile on
```

Run `obsidian help` for the remaining developer commands, including CDP and debugger controls.

## Verification

- [ ] CLI present and Obsidian running; output read rather than assumed.
- [ ] Correct targeting (`file=`/`path=`/`vault=`) for the selected vault.
- [ ] Output options placed after the command name.
- [ ] No backslash-bearing or >4 KB content passed through `content=`.
- [ ] Plugin reload → errors → visual → console loop completed.

## Related Skills in This Repo

- [obsidian-bases](../obsidian-bases/SKILL.md) — Use when working with .base files, creating database-like views of notes, or when the user...
- [json-canvas](../json-canvas/SKILL.md) — Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, or w...
- [obsidian-markdown](../obsidian-markdown/SKILL.md) — Use when working with .md files in Obsidian, or when the user mentions wikilinks, callouts...
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
- Path: `_sources/obsidianmd_obsidian-skills/plugins/obsidian/skills/obsidian-cli/SKILL.md`
- License: MIT — Copyright (c) 2026 Steph Ango (@kepano)
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
