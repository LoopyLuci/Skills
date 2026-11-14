---
name: software-factory
description: Use when working with shared language for designing a software factory: the tasks it runs and the services it plugs into.
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

# Software Factory

> **Adapted for the LoopyLuci Skills collection** from [mattpocock/skills](https://github.com/mattpocock/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Shared language for designing a software factory: the tasks it runs and the services it plugs into

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

The shared vocabulary for designing a **software factory**: a system of agents that turns tickets, PRs, and schedules into merged code, deployed on infrastructure the user chooses. Use these terms and only these when discussing a factory; when the user reaches for a word under *Avoid*, name the canonical term.

## Tasks and runs

**Task** — a kind of work the factory performs, defined once and run many times: review, explore, implement, ratchet. It may act on a ticket, a PR, or the codebase as a whole. *Avoid*: job, workflow, action — a CI vendor's workflow file and its jobs are where a task is wired up, not the task.

**Trigger** — the event that starts a run: a change in the ticket tracker or git host, a clock in the orchestrator, or another run.

**Run** — one execution of a task on one runner, from trigger to finish, treated as a black box. A run triggers further runs directly, through orchestrator logic, or by changing the tracker or git host. A run never waits for a human: it ends, and the human's later change triggers a new run. *Avoid*: session.

**Runner** — the disposable machine a run executes on. Nothing on it survives the run even when the machine is long-lived; a run's only memory of earlier runs is the tracker, the git host, and the orchestrator. *Avoid*: server, host, box, compute, sandbox.

## Services

**Ticket tracker** — where tickets live and the factory's human interface: humans file work, talk to agents in comments, and their edits trigger runs. *Avoid*: issue tracker, ticket manager, project board.

**Ticket source** — anything outside the factory that creates tickets in the tracker: a feedback button, a monitor, an error tracker, an inbox. *Avoid*: data source, trigger source, intake.

**Git host** — where branches, PRs, and reviews live. *Avoid*: code host, forge, repo.

**Orchestrator** — receives triggers, starts runs on runners, and records which runs are queued, in flight, or finished. *Avoid*: dispatcher, scheduler, control plane.

**Observability platform** — where runners send logs, traces, and status so a human can see what happened inside each run. Optional: the product filling the runner or orchestrator slot often shows enough on its own, and a run never decides on it until something writes it into the tracker or git host. *Avoid*: observability, logs, monitoring, dashboard.

## Designing a factory

A design has two halves: the **services** (slots filled with products) and the **tasks** whose runs move work through them. Start from the user's problem, not from the factory — untriaged tickets, PRs waiting for automated review, a stricter automated check to migrate to, bugs nobody reads. When the user names a problem or does not know what to build, read `EXAMPLE-TASKS.md`.

### Start slow

Every trigger is an accelerator; accelerators without brakes make a slop cannon. Three brakes:

- **Automated checks** — deterministic gates (types, lint, tests) that every run must pass.
- **Automated review** — a separate run that reads the diff cold against the codebase's standards and the ticket, when there is one.
- **Human review** — a human reads the PR before it merges; what it catches becomes new automated checks and sharper automated review.

Add one automated trigger at a time, throttled at first (one bug report in ten, a clock once a day), with human review on every PR. Open the throttle as the brakes earn trust, and cap every loop of runs at a few tries before a human.

### Fill every slot

Each service is a slot; one product can fill several slots, and one server can host several services.

| Service | All on GitHub | Linear tickets | Own tracker |
| --- | --- | --- | --- |
| Ticket tracker | GitHub Issues | Linear | own app |
| Ticket source | feedback button | feedback button, monitor | feedback button, monitor |
| Git host | GitHub | GitHub | GitHub |
| Orchestrator | GitHub Actions | own server + database | own app |
| Runner | Actions runner | Actions, E2B, Daytona, or a VPS | own app, or sandboxes |
| Observability platform | none — Actions run pages suffice | an LLM tracing platform | own app |

When the user is choosing a product for a slot, read that slot's survey for orientation, then research the current options yourself: `TICKET-TRACKERS.md`, `GIT-HOSTS.md`, `RUNNERS.md`, `OBSERVABILITY-PLATFORMS.md`. Buy the services and build the tasks — the tasks carry the user's design, the services are generic. Favour an off-the-shelf ticket tracker: it is robust, people already know it, and outside users are easy to let in.

### Question every task

For each task answer: (1) what triggers it; (2) what it does and which services it reads and writes; (3) what it triggers next; (4) where a human re-enters; (5) what stops two runs doing the same work. For each ticket source answer: what stops it filing the same ticket twice. A design is finished when every slot names a product (or a deliberate none for observability) and every task and ticket source has an answer to every question.

## Verification

- [ ] Canonical terms used; avoided terms not used.
- [ ] Every service slot filled with a product or a deliberate none.
- [ ] Every task and ticket source answered all applicable questions.
- [ ] Triggers throttled initially, with brakes in place.

## Related Skills in This Repo

- [pr](../pr/SKILL.md) — Use when writing a PR body.
- [writing-for-agents](../writing-for-agents/SKILL.md) — Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.
- [chief-of-staff](../chief-of-staff/SKILL.md) — Use when working with pursue a long-running goal in a single session by co-ordinating suba...
- [retro](../retro/SKILL.md) — Use when conducting a retrospective on a coding session.

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [mattpocock/skills](https://github.com/mattpocock/skills)
- Path: `_sources/mattpocock_skills/skills/in-progress/software-factory/SKILL.md`
- License: MIT — Copyright (c) 2026 Matt Pocock
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
