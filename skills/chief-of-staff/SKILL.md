---
name: chief-of-staff
description: Use when working with pursue a long-running goal in a single session by co-ordinating subagents.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [software-development, engineering, in-progress]
    source: mattpocock/skills
    adapted: true
---

# Chief Of Staff

> **Adapted for the LoopyLuci Skills collection** from [mattpocock/skills](https://github.com/mattpocock/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Pursue a long-running goal in a single session by co-ordinating subagents

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Drive a long-running goal inside one session by coordinating subagents and schedules, while deliberately improving the environment the next task will run in.

## Two tracks

You are the Directly Responsible Individual for the goal, and you are expected to think further ahead than usual. Hold both tracks at once:

- **Tactical** — how the immediate task gets finished.
- **Strategic** — how the environment changes so the *next* task does better.

## Schedules

Where the harness allows, propose recurring schedules that advance the goal.

## Subagents

Do all work in subagents to protect your own context window. Use background agents so you can keep talking to the user, and start every subagent with a fresh context. Keep subagent communication sparse: share **context pointers** (research notes, prior commits, wiki pages) rather than restating information a pointer already reaches.

## Wiki

Persist durable knowledge in a wiki — a folder of interlinked markdown pages that outlives the session. Context-only knowledge is lost at compaction; the wiki carries it into the next session. Look for a shared wiki the user or other agents already maintain and write into it, following its conventions where they differ. Only if none exists, agree a location with the user before the first write.

- `index.md` lists every page with a link and a one-line summary, grouped by category.
- Every other page covers one thing — a decision, a recurring problem, a subsystem, a user preference — and links to related pages.
- Sources (issues, PRs, transcripts, subagent reports) are cited, never copied or edited.

Three operations keep it alive:

- **Ingest** — when you learn something durable (a decision, a user correction, a subagent finding), update every page it touches plus the index, not just a new page.
- **Query** — before deciding, read `index.md` and the pages it points to; if the answer is worth keeping, file it.
- **Lint** — periodically look for contradictions, orphan pages, missing links, and claims newer sources have overtaken; propose this as a schedule.

### Write history, not the present

The wiki is a historical record and never claims to describe how things are now, because it cannot keep up with the code.

- Date every claim: "On 2026-10-13, the team decided..."
- When a claim concerns code, cite the commit it held at, with its repository: "As of `owner/repo@abc1234`, `retro` loads `writing-for-agents` in step 1."
- Never write "currently", "now", or "is" about code without a date or commit beside it.
- When something changes, add a new dated claim and mark the old one superseded; do not rewrite the old one.

## Procedures

Some procedures live in sibling skills. To run one, read its `SKILL.md` relative to this skill's directory and follow it.

- **Retro** (`../retro/SKILL.md`) — run a retro on roughly one in five subagent sessions, including those dispatched by `implement-spec`; start with the sessions where something went wrong. Replace retro's final step with your own judgement about which candidates are worth pursuing, then pursue them.
- **Large chunks of work** — write a spec with `../to-spec/SKILL.md`, break it into tickets with `../to-tickets/SKILL.md`, publish both to the issue tracker, then implement them with `../implement-spec/SKILL.md`.

## Strategic view

Before anything else, consider how the agents' environment could improve. Agents do best in a **pit of success**:

- APIs and functions that are tightly constrained.
- Lint rules that force correctness.
- `CODING_STANDARDS.md` files that let reviewers enforce good practice.

They also need the right **data sources**: logs from critical running processes (dev or production), access to test-environment databases, and browser access for clicking and screenshots when it helps.

Finally, build environments and codebases that obey the **"no workarounds"** rule: no one-off hacks that bypass established process, and any deviation from convention fixed proactively, before feature work. Be relentless — treat every user message as a prompt to look for these improvements.

## Verification

- [ ] Subagents used for all execution; own context reserved for coordination.
- [ ] Wiki updated for every durable finding, with dated claims.
- [ ] At least one environment improvement identified per piece of work.

## Related Skills in This Repo

- [pr](../pr/SKILL.md) — Use when writing a PR body.
- [software-factory](../software-factory/SKILL.md) — Use when working with shared language for designing a software factory: the tasks it runs ...
- [writing-for-agents](../writing-for-agents/SKILL.md) — Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.
- [retro](../retro/SKILL.md) — Use when conducting a retrospective on a coding session.

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [mattpocock/skills](https://github.com/mattpocock/skills)
- Path: `_sources/mattpocock_skills/skills/in-progress/chief-of-staff/SKILL.md`
- License: MIT — Copyright (c) 2026 Matt Pocock
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
