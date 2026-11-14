---
name: deprecation-and-migration
description: Use when removing old systems, APIs, or features; migrating users from one implementation to another; migrating a database schema in production, such as renaming or dropping a column without downtime (expand/contract); deciding whether to maintain or sunset existing code.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [software-development, engineering, agent-skills]
    source: addyosmani/agent-skills
    adapted: true
---

# Deprecation and Migration

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Removing old systems, APIs, or features
- Migrating users from one implementation to another
- Migrating a database schema in production, such as renaming or dropping a column without downtime (expand/contract)
- Deciding whether to maintain or sunset existing code

## When NOT to Use

- Deprecated systems with no replacement available
- Deprecation announcements with no migration tooling or documentation
- "Soft" deprecation that's been advisory for years with no progress
- Zombie code with no owner and active consumers
- New features added to a deprecated system (invest in the replacement instead)
- Deprecation without measuring current usage
- Removing code without verifying zero active consumers
- A schema change and the code that depends on it shipped in the same deploy
- A column renamed or dropped in place rather than via expand/contract
- A migration merged with no tested down path, or a backfill that locks the table

## Overview

Code is a liability, not an asset: every line carries maintenance cost — bugs, dependency updates, security patches, onboarding. Deprecation is the discipline of removing code that no longer earns its keep; migration is moving users safely from old to new. Most teams build well and remove poorly; this skill closes that gap.

## Core principles

- **Code is a liability.** Its value is the functionality it provides, not the code itself. Where the same function can be delivered with less code or better abstractions, the old code should go.
- **Hyrum's Law makes removal hard.** With enough users, every observable behavior becomes depended on — including bugs and undocumented side effects. Deprecation therefore needs active migration, not just announcement.
- **Plan deprecation at design time.** When building something new, ask how it would be removed in three years. Clean interfaces, feature flags, and a small surface area make later removal far easier.

## Deciding whether to deprecate

1. Does it still provide unique value? If yes, maintain it; if no, continue.
2. How many consumers depend on it? Quantify the migration scope.
3. Does a replacement exist? If not, build one first — never deprecate without an alternative.
4. What is each consumer's migration cost? Trivially automated means do it; manual and expensive means weigh it against maintenance cost.
5. What is the ongoing cost of *not* deprecating? Security risk, engineer time, complexity opportunity cost.

## Advisory versus compulsory

| Type | When | Mechanism |
| --- | --- | --- |
| **Advisory** | Migration optional; old system stable | Warnings, docs, nudges; users move on their own timeline |
| **Compulsory** | Security issues, blocked progress, or unsustainable maintenance | Hard deadline, plus migration tooling, docs, and support |

Default to advisory. Use compulsory only when cost or risk justifies forcing migration — and then provide tooling, documentation, and support rather than just announcing a date.

## Migration process

1. **Build the replacement.** It must cover all critical use cases, have docs and a migration guide, and be proven in production rather than merely theoretically better.
2. **Announce and document.** Status, replacement, removal date, reason, and a concrete migration guide with steps and examples.
3. **Migrate incrementally.** One consumer at a time: identify touchpoints, switch to the replacement, verify behavior matches, remove old references, confirm no regressions. **Churn rule:** if you own the infrastructure being deprecated, you are responsible for migrating your users — or shipping backward-compatible updates that need no migration.
4. **Remove the old system** only after every consumer has moved: verify zero active usage from metrics, logs, and dependency analysis; remove code, tests, docs, and config; remove the deprecation notices.

## Migration patterns

**Strangler** — run old and new in parallel, shifting traffic incrementally (0% → 10% canary → 50% → 100%), then remove the old system.

**Adapter** — translate old-interface calls to the new implementation so consumers keep their existing calls while the backend moves:

```typescript
class LegacyTaskService implements OldTaskAPI {
  constructor(private newService: NewTaskService) {}

  getTask(id: number): OldTask {
    const task = this.newService.findById(String(id));
    return { id: Number(task.id), title: task.title, done: task.status === 'done' };
  }
}
```

**Feature flag** — switch consumers one at a time:

```typescript
function getTaskService(userId: string): TaskService {
  return featureFlags.isEnabled('new-task-service', { userId })
    ? new NewTaskService()
    : new OldTaskService();
}
```

**Database schema (expand/contract)** — schema changes are the riskiest migration because data cannot be rolled back by reverting a deploy. Coupling the schema change to the code change means that during rollout, old and new code run together and one queries a column that no longer exists. Never change a column in place; migrate in additive phases so both versions stay valid:

```
EXPAND ──────────────→ MIGRATE ──────────────→ CONTRACT
add the new column,    backfill existing rows,  once no code reads the
nullable, alongside    dual-write old+new from  old column, drop it in
the old one            the app                  a later, separate deploy
```

Renaming `name` to `full_name`, step by step: (1) expand — add `full_name` nullable and deploy; (2) dual-write both on every insert/update; (3) backfill `name → full_name` in batches to avoid locking; (4) switch reads to `full_name` while still writing both; (5) contract — stop writing `name`, then drop it in a separate later deploy. Each step is independently deployable and reversible.

Rules: additive first, destructive last and alone; every migration has a tested `down` path written and run before merge; backfill in throttled batches off the hot path; build large indexes without blocking writes (for example Postgres `CREATE INDEX CONCURRENTLY`); decouple with a feature flag when cutover is risky.

## Zombie code

Zombie code is nobody's responsibility but everybody's dependency: no commits in six months yet active consumers, no assigned maintainer, failing tests nobody fixes, vulnerable dependencies nobody updates, docs referencing systems that no longer exist. Either assign an owner and maintain it properly, or deprecate it with a concrete migration plan — limbo is not an option.

## Red flags

- Deprecating without a replacement
- Announcements with no migration tooling or documentation
- Advisory deprecation that has lingered for years with no progress
- Zombie code with active consumers and no owner
- New features added to a deprecated system
- Deprecating without measuring current usage
- Removing code before verifying zero active consumers
- Schema change and its dependent code shipped in the same deploy
- Renaming or dropping a column in place instead of expand/contract
- A migration merged with no tested down path, or a backfill that locks the table

## Verification

After a deprecation:

- [ ] Replacement production-proven and covers all critical use cases.
- [ ] Migration guide exists with concrete steps and examples.
- [ ] All active consumers migrated, verified by metrics/logs.
- [ ] Old code, tests, docs, and config fully removed; no references remain.
- [ ] Deprecation notices removed.

After a schema migration:

- [ ] Shipped in additive phases (expand → backfill → contract), not one in-place edit.
- [ ] Old and new code both valid against the schema at every step.
- [ ] Every migration has a tested down path; backfills run in throttled batches.
- [ ] Destructive steps ship in their own deploy after nothing references the old shape.

## Related Skills in This Repo

- [code-review-and-quality](../code-review-and-quality/SKILL.md) — Use when reviewing code written by yourself, another agent, or a human; you need to assess...
- [ci-cd-and-automation](../ci-cd-and-automation/SKILL.md) — Use when setting up or modifying build and deployment pipelines; you need to automate qual...
- [api-and-interface-design](../api-and-interface-design/SKILL.md) — Use when designing APIs, module boundaries, or any public interface; creating REST or Grap...
- [git-workflow-and-versioning](../git-workflow-and-versioning/SKILL.md) — Use when making any code change; committing, branching, resolving conflicts, splitting unc...

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Upstream anti-patterns retained as the When-NOT-to-Use list.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- Path: `_sources/addyosmani_agent-skills/skills/deprecation-and-migration/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
