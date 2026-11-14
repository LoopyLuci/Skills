---
name: implement-spec
description: Use when implementing the result of /to-spec and /to-tickets in code.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [software-development, engineering]
    source: mattpocock/skills
    adapted: true
---

# Implement Spec

> **Adapted for the LoopyLuci Skills collection** from [mattpocock/skills](https://github.com/mattpocock/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Implement the result of /to-spec and /to-tickets in code

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Implements a spec and its associated tickets in code. The spec comes with tickets describing the work; those tickets form a task graph with blocking relationships, so at any moment there is a frontier of unblocked tickets ready to be picked up. Everything lands on one integration branch, each ticket resolved the way the issue tracker closes work.

## Preliminaries

The issue tracker should have been provided alongside the spec. If it wasn't, tell the user to run `/setup-matt-pocock-skills` before continuing.

## Workflow

1. **Read the spec and tickets** to understand the task graph — nodes plus their blocking edges.

2. **(Optional) Exploration subagent.** When tickets require codebase or external-documentation research, send an exploration subagent. Make sure it can write files: it saves markdown notes to a directory outside the repo that every future subagent can read. This keeps implementers focused on implementation rather than exploration.

3. **Create the integration branch.** If the tracker closes work via PRs, or the user asks for one, open a draft PR after the first merge in step 5 (a branch with no commits ahead of main cannot open one), marked as closing the spec and tickets.

4. **One fresh implementer subagent per ticket**, each in its own worktree on its own branch. Each implementer:
   - confirms its worktree is based on the integration branch before starting, resetting onto it if not;
   - calls the Skill tool with `tdd` to build the ticket;
   - merges the integration branch tip into its own branch before reporting done.

5. **Merge completed work** onto the integration branch with a **merger subagent**.

6. **Expand the frontier.** If new tickets became available, launch more implementers on them — this is where concurrency pays off.

7. **Code review once all tickets are complete:** call the Skill tool with `code-review` on the integration branch, then fix everything it raised in a single fresh implementer subagent.

8. **Close out.** If a draft PR exists, mark it ready for review. Otherwise resolve each ticket the way the tracker closes work and report the integration branch.

9. **Clean up** all implementer worktrees.

## Operating Notes

- Tickets are a graph, not a checklist; always work from the current frontier of unblocked items.
- Give every subagent a fresh context window.
- Keep subagent communication sparse. Share **context pointers** — to the spec, tickets, research notes, previous commits — instead of duplicating information those pointers already carry.
- Run implementer subagents in the background wherever possible for maximum concurrency.

## Verification

- [ ] Spec and ticket graph both read; frontier identified before first implementation
- [ ] Integration branch created and used as the base for every implementer worktree
- [ ] Each ticket built via the `tdd` skill and based on the current integration-branch tip
- [ ] Every merged change landed on the integration branch (merger subagent)
- [ ] Newly unblocked tickets detected and dispatched
- [ ] `code-review` run on the integration branch after all tickets; every finding fixed
- [ ] Draft PR marked ready, or tickets closed through the tracker's mechanism
- [ ] All implementer worktrees removed

## Related Skills in This Repo

- [pr](../pr/SKILL.md) — Use when writing a PR body.
- [software-factory](../software-factory/SKILL.md) — Use when working with shared language for designing a software factory: the tasks it runs ...
- [writing-for-agents](../writing-for-agents/SKILL.md) — Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.
- [chief-of-staff](../chief-of-staff/SKILL.md) — Use when working with pursue a long-running goal in a single session by co-ordinating suba...

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [mattpocock/skills](https://github.com/mattpocock/skills)
- Path: `_sources/mattpocock_skills/skills/engineering/implement-spec/SKILL.md`
- License: MIT — Copyright (c) 2026 Matt Pocock
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
