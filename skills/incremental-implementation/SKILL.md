---
name: incremental-implementation
description: Use when implementing any feature or change that touches more than one file, or when picking up the next task from a plan; rolling a change out behind a feature flag, when you're about to write a large amount of code at once, or when a task feels too big to land in one step.
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

# Incremental Implementation

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Implementing any feature or change that touches more than one file, or when picking up the next task from a plan
- Rolling a change out behind a feature flag, when you're about to write a large amount of code at once, or when a task feels too big to land in one step

## When NOT to Use

- More than 100 lines of code written without running tests
- Multiple unrelated changes in a single increment
- "Let me just quickly add this too" scope expansion
- Skipping the test/verify step to move faster
- Build or tests broken between increments
- Large uncommitted changes accumulating
- Building abstractions before the third use case demands it
- Touching files outside the task scope "while I'm here"
- Creating new utility files for one-time operations
- Running the same build/test command twice in a row without any intervening code change

Large changes land reliably when delivered as thin vertical slices: implement one piece, test it, verify it, commit, then expand. Each increment leaves the system working and testable, so a failure never buries itself inside hundreds of unfinished lines.

## The Cycle

```
┌──────────────────────────────────────┐
│                                      │
│   Implement ──→ Test ──→ Verify ──┐  │
│       ▲                           │  │
│       └───── Commit ◄─────────────┘  │
│              │                       │
│              ▼                       │
│          Next slice                  │
│                                      │
└──────────────────────────────────────┘
```

For each slice: implement the smallest complete piece; test it (run the suite, or write a test if none exists); verify the slice behaves as expected; commit with a descriptive message; move on carrying forward rather than restarting.

## How to Slice

**Vertical slices (preferred)** — one complete path through the stack per slice:

```
Slice 1: Create a task (DB + API + basic UI)
    → Tests pass, user can create a task via the UI

Slice 2: List tasks (query + API + UI)
    → Tests pass, user can see their tasks

Slice 3: Edit a task (update + API + UI)
    → Tests pass, user can modify tasks

Slice 4: Delete a task (delete + API + UI + confirmation)
    → Tests pass, full CRUD complete
```

**Contract-first** — when backend and frontend develop in parallel, define the contract as Slice 0, build each side against it, then integrate and test end-to-end.

**Risk-first** — prove the riskiest or most uncertain piece first. If that slice fails, you learn it before investing in the rest.

## Rules

### Simplicity first

Before coding, ask what the simplest thing that could work is. Afterwards, check whether it can be shorter, whether the abstractions earn their complexity, whether a senior engineer would ask "why didn't you just…", and whether it serves the current task or hypothetical future ones.

```
SIMPLICITY CHECK:
✗ Generic EventBus with middleware pipeline for one notification
✓ Simple function call

✗ Abstract factory pattern for two similar components
✓ Two straightforward components with shared utilities

✗ Config-driven form builder for three forms
✓ Three form components
```

Three similar lines beat a premature abstraction. Ship the naive, obviously-correct version; optimise only after tests prove correctness.

### Scope discipline

Touch only what the task requires. Do not clean up adjacent code, refactor imports in untouched files, delete comments you do not fully understand, add features because they seem useful, or modernise syntax in files you are only reading. Notice improvements outside scope, but note them rather than fixing them:

```
NOTICED BUT NOT TOUCHING:
- src/utils/format.ts has an unused import (unrelated to this task)
- The auth middleware could use better error messages (separate task)
→ Want me to create tasks for these?
```

### One thing per increment

Each increment changes one logical thing. Adding a component, refactoring an existing one, and updating build config are three commits, not one.

### Always compilable

After every increment the project builds and existing tests pass; never leave the codebase broken between slices.

### Feature flags for incomplete work

When a feature is not ready for users but increments must merge:

```typescript
// Feature flag for work-in-progress
const ENABLE_TASK_SHARING = process.env.FEATURE_TASK_SHARING === 'true';

if (ENABLE_TASK_SHARING) {
  // New sharing UI
}
```

### Safe defaults

New code defaults to conservative behaviour — opt-in rather than opt-out:

```typescript
// Safe: disabled by default, opt-in
export function createTask(data: TaskInput, options?: { notify?: boolean }) {
  const shouldNotify = options?.notify ?? false;
  // ...
}
```

### Rollback-friendly

Every increment should revert independently: prefer additive changes, keep modifications to existing code minimal and focused, pair migrations with rollback migrations, and split deletions from replacements into separate commits.

## Directing an Agent

State the slice boundary explicitly:

```
"Let's implement Task 3 from the plan.

Start with just the database schema change and the API endpoint.
Don't touch the UI yet — we'll do that in the next increment.

After implementing, run the repository's test and build commands to
verify nothing is broken."
```

## Per-Increment Checks

Run the repository's own commands after each increment:

- [ ] The change does one thing and does it completely.
- [ ] Existing tests pass (`npm test`, `./gradlew test`, `pytest`, ...).
- [ ] The build succeeds.
- [ ] Type checking passes where the stack has one (`npx tsc --noEmit`, `mypy`, ...).
- [ ] Linting passes.
- [ ] The new functionality works as expected.
- [ ] The change is committed with a descriptive message.

Re-run a command only after code that could affect it has changed; repeating a green command adds no information.

## Objections and Answers

| Objection | Response |
|---|---|
| "I'll test at the end" | Bugs compound; a defect in Slice 1 makes Slices 2–5 wrong. |
| "Faster to do it all at once" | It feels faster until a break hides among 500 changed lines. |
| "Too small to commit separately" | Small commits are free; large ones hide bugs and hurt rollbacks. |
| "Add the feature flag later" | Incomplete features should not be user-visible; add the flag now. |
| "This refactor is small enough to include" | Mixed refactors make features harder to review and debug; separate them. |
| "Run the build again to be sure" | Re-running unchanged code adds nothing; re-run after edits. |

## Verification

- [ ] Each increment was tested and committed individually.
- [ ] The full test suite passes.
- [ ] The build is clean.
- [ ] The feature works end-to-end as specified.
- [ ] No uncommitted changes remain.

Per-increment checks are the local gate; the project-wide Definition of Done is the final bar every increment must clear.

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
- Path: `_sources/addyosmani_agent-skills/skills/incremental-implementation/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
