---
name: obsidian-headless
description: Use when the user wants to set up or run Obsidian Sync or Obsidian Publish on a server, in CI, or from a terminal, or change a vault's Sync or Publish settings.
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

# Obsidian Headless

> **Adapted for the LoopyLuci Skills collection** from [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- The user wants to set up or run Obsidian Sync or Obsidian Publish on a server, in CI, or from a terminal, or change a vault's Sync or Publish settings

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

`ob` runs Obsidian Sync and Obsidian Publish from the terminal, without the desktop app — suited to servers, CI, and sandboxes. It is in open beta. Note what it does not do: `ob` only syncs and publishes files; for reading or editing notes directly, edit files on disk (see the obsidian-markdown skill), and for controlling a running desktop app use the obsidian-cli skill instead. Docs: https://help.obsidian.md/headless

## Setup and Login

Check availability with `ob --help`. If missing, tell the user Obsidian Headless requires Node.js 22+ and offer `npm install -g obsidian-headless`. For any command's options, run `ob <command> --help`.

Sync and Publish each need an active subscription on the user's account. Most commands accept `--json` for machine-readable output.

`ob login` prints the current account when already authenticated. Otherwise it prompts for email, password, and a 2FA code — have the user run that step in their own terminal. Never ask for their password and never pass one via `--password`. `ob logout` clears stored credentials.

## Vault Paths

Commands act on the vault in the current directory, or the one passed with `--path`; always pass `--path` so the target is explicit. Before any command that changes remote state, confirm vault, site, and path from list or status output first.

## Sync

Never run the desktop app's Sync and Headless Sync against the same vault on the same device — they conflict. Ask the user to back up the vault folder before the first sync.

```bash
ob sync-list-remote                                  # remote vaults, including shared ones
ob sync-list-local                                   # vaults set up on this machine
ob sync-setup --vault "Research" --path ~/vaults/research
ob sync --path ~/vaults/research                     # sync once
ob sync --path ~/vaults/research --continuous        # keep syncing as files change
ob sync-status --path ~/vaults/research
ob sync-unlink --path ~/vaults/research              # disconnect and remove stored credentials
```

`--vault` takes a remote vault's name or ID. For an end-to-end encrypted vault, `sync-setup` prompts for the encryption password, so let the user enter it. `--device-name` labels this machine in version history. `--continuous` runs until stopped, so start it in the background or as a service.

Create a remote vault with `ob sync-create-remote --name "Research"`; add `--encryption e2ee` for end-to-end encryption or `--encryption standard` for managed encryption.

### Sync Settings

`ob sync-config --path <vault>` prints the vault's settings. Change them with:

- `--mode bidirectional|pull-only|mirror-remote` — `pull-only` ignores local changes and `mirror-remote` reverts them, so confirm before setting either.
- `--conflict-strategy merge|conflict`
- `--excluded-folders "Archive,Templates"`
- `--file-types image,audio,video,pdf,unsupported` for which attachment types to sync
- `--configs` for settings categories to sync, e.g. `app,appearance,core-plugin`
- `--config-dir` when the vault's configuration folder isn't `.obsidian`

An empty string clears a list option, e.g. `--excluded-folders ""`.

## Publish

```bash
ob publish-list-sites
ob publish-setup --site my-notes --path ~/vaults/research
ob publish --path ~/vaults/research --dry-run
ob publish --path ~/vaults/research --yes
```

`ob publish` includes only notes with `publish: true` in their properties; `--all` includes every file, so use it only when the user asks. Run `--dry-run` first and show the changes. Without `--yes`, `ob publish` waits for confirmation — pass `--yes` once the user approves, or for an unattended job they configured.

Create a site at `publish.obsidian.md/my-notes` with `ob publish-create-site --slug my-notes`.

Current settings print when these run with no options:

- `ob publish-config` — include/exclude folders via `--includes` / `--excludes`
- `ob publish-site-options` — site name, home page, navigation, theme, and other display options; see `ob publish-site-options --help` for the full list

`ob publish-unlink` disconnects the vault from its site.

## Verification

- [ ] `ob --help` works; Node.js 22+ present
- [ ] Logged-in account confirmed (`ob login`), credentials never handled by the agent
- [ ] `--path` supplied on every command
- [ ] Remote/local state confirmed from list or status output before any mutating command
- [ ] Desktop Sync not running concurrently on the same vault and device
- [ ] Vault backed up before first sync
- [ ] Publish dry-run shown to the user before `--yes`
- [ ] `--pull-only` / `--mirror-remote` mode changes confirmed explicitly

## Related Skills in This Repo

- [obsidian-bases](../obsidian-bases/SKILL.md) — Use when working with .base files, creating database-like views of notes, or when the user...
- [json-canvas](../json-canvas/SKILL.md) — Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, or w...
- [obsidian-markdown](../obsidian-markdown/SKILL.md) — Use when working with .md files in Obsidian, or when the user mentions wikilinks, callouts...
- [obsidian-cli](../obsidian-cli/SKILL.md) — Use when the user asks to interact with their Obsidian vault, manage notes, search vault c...
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
- Path: `_sources/obsidianmd_obsidian-skills/plugins/obsidian/skills/obsidian-headless/SKILL.md`
- License: MIT — Copyright (c) 2026 Steph Ango (@kepano)
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
