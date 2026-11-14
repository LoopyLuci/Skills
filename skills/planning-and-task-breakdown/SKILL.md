---
name: planning-and-task-breakdown
description: Use when you have a spec or clear requirements and need to break work into implementable tasks; a task feels too large to start, when you need to estimate scope, or when parallel work is possible.
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

# Planning and Task Breakdown

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- You have a spec or clear requirements and need to break work into implementable tasks
- A task feels too large to start, when you need to estimate scope, or when parallel work is possible

## When NOT to Use

- Starting implementation without a written task list
- Overwriting a `tasks/plan.md` or `tasks/todo.md` that still has unchecked tasks for different work, without asking
- Writing `tasks/todo.md` when the project has designated an external tracker (or scattering tasks across both)
- Tasks that say "implement the feature" without acceptance criteria
- No verification steps in the plan
- All tasks are XL-sized
- No checkpoints between tasks
- Dependency order isn't considered

## Overview

Turn a spec into small, ordered tasks that each carry acceptance criteria and a verification step. Well-broken work is the difference between an agent that delivers reliably and one that produces a tangled mess; every task should be implementable, testable, and verifiable inside a single focused session. Good breakdowns also expose hidden dependencies and give a human something concrete to review before code starts.

## Planning Process

### Step 1: Read-Only First Pass

Before writing any code, survey the ground:

- Read the spec and the relevant parts of the codebase
- Identify existing patterns and conventions
- Map dependencies between components
- Note risks and unknowns

Planning never writes code. Its output is a plan document at `tasks/plan.md` plus a task list in the task-list target (default `tasks/todo.md`) — not implementation.

### Step 2: Map the Dependency Graph

Show what builds on what:

```
Database schema
    │
    ├── API models/types
    │       │
    │       ├── API endpoints
    │       │       │
    │       │       └── Frontend API client
    │       │               │
    │       │               └── UI components
    │       │
    │       └── Validation logic
    │
    └── Seed data / migrations
```

Build in dependency order, foundations first.

### Step 3: Slice Vertically

Deliver complete feature paths rather than completing each layer across the whole app.

**Bad (horizontal slicing):**

```
Task 1: Build entire database schema
Task 2: Build all API endpoints
Task 3: Build all UI components
Task 4: Connect everything
```

**Good (vertical slicing):**

```
Task 1: User can create an account (schema + API + UI for registration)
Task 2: User can log in (auth schema + API + UI for login)
Task 3: User can create a task (task schema + API + UI for creation)
Task 4: User can view task list (query + API + UI for list view)
```

Each slice leaves working, testable functionality behind.

### Step 4: Write Each Task

Use this shape, whether it lands in markdown or an external tracker:

```markdown
## Task [N]: [Short descriptive title]

**Description:** One paragraph explaining what this task accomplishes.

**Acceptance criteria:**
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]

**Verification:**
- [ ] Tests pass: [the repository's focused-test command]
- [ ] Build succeeds: [the repository's build command]
- [ ] Manual check: [description of what to verify]

**Dependencies:** [Task numbers this depends on, or "None"]

**Files likely touched:**
- `src/path/to/file.ts`
- `tests/path/to/test.ts`

**Estimated scope:** [Small: 1-2 files | Medium: 3-5 files | Large: 5+ files]
```

### Step 5: Order and Insert Checkpoints

Arrange tasks so that:

1. Dependencies resolve before dependents start
2. Every task leaves the system working
3. Verification checkpoints land after every 2–3 tasks
4. High-risk tasks run early, to fail fast

Add checkpoints to the task list:

```markdown
## Checkpoint: After Tasks 1-3
- [ ] All tests pass
- [ ] Application builds without errors
- [ ] Core user flow works end-to-end
- [ ] Review with human before proceeding
```

## Sizing

| Size | Files | Scope | Example |
|------|-------|-------|---------|
| **XS** | 1 | Single function or config change | Add a validation rule |
| **S** | 1-2 | One component or endpoint | Add a new API endpoint |
| **M** | 3-5 | One feature slice | User registration flow |
| **L** | 5-8 | Multi-component feature | Search with filtering and pagination |
| **XL** | 8+ | **Too large — break it down further** | — |

Anything L or bigger should be split. Agents perform best on S and M. Break a task down when:

- It would take more than one focused session (~2+ hours of agent work)
- Acceptance criteria need more than three bullets
- It touches two or more independent subsystems (e.g. auth and billing)
- The title contains "and" (usually two tasks wearing one coat)

## Output Files

Create the `tasks/` directory if missing.

- **Plan document:** always a markdown file at `tasks/plan.md`. Design decisions, risks, and open questions don't map cleanly onto tracker issues.
- **Task list:** recorded in the task-list target (below).

**Never clobber an incomplete plan.** Before writing `tasks/plan.md` or `tasks/todo.md`, check whether they already exist with unchecked tasks:

- Same work being replanned → update the existing files in place
- Different work → stop and ask. Unchecked tasks may be mid-build in another session; do not delete, overwrite, or rename anything. Present the conflict and let the user choose (finish the old plan, explicitly discard it, or point elsewhere).

The same caution applies to an external tracker: never bulk-close or delete another plan's open items to make room for yours.

### Task List Target

One place records tasks and checkpoints, defined here once:

- **Default: a checklist-style markdown file at `tasks/todo.md`.** This is what `/build` and downstream tooling expect unless the project says otherwise.
- **External tracker:** if project rules (`CLAUDE.md`, `AGENTS.md`) or the user designate one (GitHub Issues, Jira, Linear, `bd`/beads), create one item per task instead of `tasks/todo.md`. Map the Step 4 structure onto its fields — acceptance criteria and verification in the body, dependencies via its linking mechanism (`bd dep add`, "blocked by", etc.). Record checkpoints as tracker items too, or as a checklist in the plan document if the tracker has no equivalent.

When using an external tracker, note it in `tasks/plan.md` ("Tasks tracked in Linear project FOO") so later steps know where to look, and keep the plan's Task List section as an ordered index of IDs or links rather than a duplicate checklist.

## Plan Document Template

```markdown
# Implementation Plan: [Feature/Project Name]

Source spec: [path to the spec this plan was generated from, e.g. SPEC.md or SPEC-<change>.md; omit if no spec]

## Overview
[One paragraph summary of what we're building]

## Architecture Decisions
- [Key decision 1 and rationale]
- [Key decision 2 and rationale]

## Task List

### Phase 1: Foundation
- [ ] Task 1: ...
- [ ] Task 2: ...

### Checkpoint: Foundation
- [ ] Tests pass, builds clean

### Phase 2: Core Features
- [ ] Task 3: ...
- [ ] Task 4: ...

### Checkpoint: Core Features
- [ ] End-to-end flow works

### Phase 3: Polish
- [ ] Task 5: ...
- [ ] Task 6: ...

### Checkpoint: Complete
- [ ] All acceptance criteria met
- [ ] Ready for review

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [High/Med/Low] | [Strategy] |

## Open Questions
- [Question needing human input]
```

With an external tracker, keep the Task List section as an ordered index of item IDs or links instead of a duplicate checklist.

## Parallelization

When multiple agents or sessions are available:

- **Safe to parallelize:** independent feature slices, tests for shipped features, documentation
- **Must stay sequential:** database migrations, shared-state changes, dependency chains
- **Needs coordination:** features sharing an API contract — fix the contract first, then parallelize

## Rationalizations to Reject

| Excuse | Reality |
|---|---|
| "I'll figure it out as I go" | That path ends in a tangle and rework; ten minutes of planning saves hours. |
| "The tasks are obvious" | Write them anyway; explicit lists surface hidden dependencies and forgotten edges. |
| "Planning is overhead" | Planning *is* the task; implementation without a plan is typing. |
| "I can hold it all in my head" | Context windows are finite; written plans survive compaction and session boundaries. |
| "The old `tasks/plan.md` is stale, I'll replace it" | Unchecked tasks may be mid-build elsewhere; overwriting destroys state that exists nowhere else. Stop and ask. |

## Red Flags

- Starting implementation without a written task list
- Overwriting `tasks/plan.md` or `tasks/todo.md` with unchecked tasks for different work, without asking
- Writing `tasks/todo.md` when the project designates an external tracker (or scattering tasks across both)
- Vague tasks like "implement the feature" with no acceptance criteria
- No verification steps anywhere in the plan
- Every task sized XL
- No checkpoints between phases
- Dependencies ignored in ordering

## Verification

Before implementation begins:

- [ ] Every task has acceptance criteria
- [ ] Every task has a verification step
- [ ] Dependencies identified and ordered correctly
- [ ] Tasks recorded in the task-list target (default `tasks/todo.md`)
- [ ] No pre-existing incomplete plan overwritten without explicit confirmation
- [ ] No task touches more than ~5 files
- [ ] Checkpoints exist between major phases
- [ ] A human reviewed and approved the plan

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
- Path: `_sources/addyosmani_agent-skills/skills/planning-and-task-breakdown/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
