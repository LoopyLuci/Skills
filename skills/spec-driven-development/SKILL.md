---
name: spec-driven-development
description: Use when starting a new project, feature, or significant change and no specification exists yet; drafting a PRD or requirements document with objectives and scope, or when requirements are unclear, ambiguous, or only exist as a vague idea; a single requirement spans several independently testable capabilities and needs decomposing into a capability map of modules before specifying; evolving a shipped spec — scoping a V1, deferring ideas to a V2 backlog, or writing a follow-up spec for a change to an existing feature.
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

# Spec-Driven Development

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Starting a new project, feature, or significant change and no specification exists yet
- Drafting a PRD or requirements document with objectives and scope, or when requirements are unclear, ambiguous, or only exist as a vague idea
- A single requirement spans several independently testable capabilities and needs decomposing into a capability map of modules before specifying
- Evolving a shipped spec — scoping a V1, deferring ideas to a V2 backlog, or writing a follow-up spec for a change to an existing feature

## When NOT to Use

- Starting to write code without any written requirements
- Asking "should I just start building?" before clarifying what "done" means
- Implementing features not mentioned in any spec or task list
- Making architectural decisions without documenting them
- Skipping the spec because "it's obvious what to build"
- V1 requirements growing mid-implementation as new ideas get written straight into the spec
- Changing a shipped feature with no spec for the change because "the feature already has one"
- Writing the spec and starting the plan or code in the same turn
- One spec whose requirements span several independently testable capabilities
- Module boundaries or build order decided implicitly during implementation because no capability map was approved up front

A written specification is the shared source of truth for what is being built, why, and how completion gets judged. Writing it before any code forces assumptions into the open while they are still cheap to fix, and gives the human a concrete artifact to approve before implementation begins.

## The Gated Sequence

Four phases run in order, each approved by the human before the next starts. A scope check precedes them only when one request bundles several independently testable capabilities.

```
SPECIFY ──→ PLAN ──→ TASKS ──→ IMPLEMENT
   │          │        │          │
   ▼          ▼        ▼          ▼
 Human      Human    Human      Human
 reviews    reviews  reviews    reviews
```

### Scope Check

Most requests describe a single capability — skip straight to Specify. Decompose first when one requirement bundles capabilities that could ship and be verified separately, when acceptance criteria cluster into independent groups, or when cutting one capability would not require rewriting the others' requirements.

Propose a small capability map before writing any spec — a module table plus build order, nothing more:

```markdown
# Capability Map: [Initiative Name]

| Module id | Responsibility | Depends on |
|---|---|---|
| identity | Accounts, sessions, SSO | — |
| billing | Plans, invoices, payments | identity |
| notifications | Email and webhook fan-out | identity |
| reporting | Usage dashboards | billing, notifications |

Build order: identity → billing, notifications → reporting
```

Rules for the map:

- Module ids are kebab-case, chosen once, and never renamed mid-initiative; specs and downstream commands select work by id.
- Dependencies point one way with no cycles — if two modules need each other, they are one module.
- Interfaces live at the boundary: the map records that `billing` depends on `identity`, and the contract between them belongs in the provider module's spec.
- The human reviews module boundaries, dependency direction, and build order before any module spec is written.
- Then recurse per module: run Specify → Plan → Tasks → Implement for each module in dependency order, each with its own scoped spec saved as `SPEC-<module-id>.md`. Save the approved map at the project root; the map, not filename guessing, indexes what exists.

### Specify

Open with a high-level vision and ask clarifying questions until requirements are concrete.

List assumptions before writing any spec content, and invite correction:

```
ASSUMPTIONS I'M MAKING:
1. This is a web application (not native mobile)
2. Authentication uses session-based cookies (not JWT)
3. The database is PostgreSQL (based on existing Prisma schema)
4. We're targeting modern browsers only (no IE11)
→ Correct me now or I'll proceed with these.
```

Silently filling in ambiguous requirements defeats the spec's purpose; assumptions are the most dangerous form of misunderstanding.

Cover six core areas in the spec:

1. **Objective** — what is being built, who it is for, what success looks like.
2. **Commands** — full executable invocations with flags, not tool names alone.
3. **Project Structure** — where source, tests, and docs live.
4. **Code Style** — one real snippet beats three paragraphs; include naming and formatting rules.
5. **Testing Strategy** — framework, test locations, coverage expectations, which level addresses which concern.
6. **Boundaries** — three tiers: always do, ask first, never do.

```markdown
# Spec: [Project/Feature Name] — V[N]

## Objective
[What we're building and why. User stories or acceptance criteria.]

## Tech Stack
[Framework, language, key dependencies with versions]

## Commands
[Build, test, lint, dev — full commands]

## Project Structure
[Directory layout with descriptions]

## Code Style
[Example snippet + key conventions]

## Testing Strategy
[Framework, test locations, coverage requirements, test levels]

## Boundaries
- Always: [...]
- Ask first: [...]
- Never: [...]

## Success Criteria
[How we'll know this is done — specific, testable conditions]

## Out of Scope (Deferred)
[Ideas explicitly excluded from this version — the V2 backlog. One line each: what, and why it's deferred.]

## Open Questions
[Anything unresolved that needs human input]
```

If the project already uses OpenSpec or another specification system, keep that artifact format and storage convention instead of creating a duplicate `SPEC.md`; this workflow owns clarification and approval gates, the external tool owns representation.

Reframe vague instructions into measurable success criteria:

```
REQUIREMENT: "Make the dashboard faster"

REFRAMED SUCCESS CRITERIA:
- Dashboard LCP < 2.5s on 4G connection
- Initial data load completes in < 500ms
- No layout shift during load (CLS < 0.1)
→ Are these the right targets?
```

Once the spec is saved, summarize it, list Open Questions, and ask for approval — then end the turn immediately. Do not start planning, invoke task breakdown, or write code in the same turn. Planning begins only after the human approves the spec in a later turn.

### Plan

Turn the approved spec into an implementation plan: major components and their dependencies, implementation order, risks and mitigations, what can run in parallel, and verification checkpoints between phases. Keep the plan reviewable enough that the human can approve the approach or name exactly what to change.

Save it to `tasks/plan.md` (creating `tasks/` if needed) and record the task list where the planning workflow designates — by default `tasks/todo.md`. Downstream commands expect these defaults.

### Tasks

Break the plan into discrete pieces: each completable in one focused session, each with explicit acceptance criteria and a verification step, ordered by dependency rather than perceived importance, and touching no more than roughly five files.

```markdown
- [ ] Task: [Description]
  - Acceptance: [What must be true when done]
  - Verify: [How to confirm — test command, build, manual check]
  - Files: [Which files will be touched]
```

### Implement

Execute tasks one at a time using incremental delivery and test-first practice, loading only the relevant spec sections and source files at each step rather than flooding context with the entire spec.

## Keeping the Spec Alive

The spec is a living document, not a one-time artifact:

- Update it before implementing whenever decisions change, and reflect scope additions or cuts in it.
- Commit it beside the code, and link each PR back to the spec section it implements.

## Versions and Follow-Up Changes

A spec describes one version. Label it in the title (`# Spec: Invoice Pipeline — V1`) so "that belongs in V2" becomes an objective call rather than a mid-build judgment.

Ideas that miss this version go under **Out of Scope (Deferred)** — captured, not lost. During implementation, anything absent from the spec's requirements is out of scope, even when it sits in the Deferred list. An idea arriving mid-build gets parked there; re-scoping happens between versions, not during one.

Changes to shipped work get a delta spec rather than an edit of the original. Cover only what changes:

```markdown
# Spec Delta: [Change Name]

Status: proposed

## Objective
[The change and why. Which deferred item or new requirement this implements.]

## Current Behavior
[What exists today — link the relevant section of the original spec.]

## New Behavior
[What will be true after the change.]

## Success Criteria
[Specific, testable conditions — including what must NOT change.]

## Boundaries
[Only deltas from the original spec's boundaries; everything else inherits.]
```

Save it next to the original (for example `SPEC-postgres-migration.md` beside `SPEC.md`) and run the same gated workflow. One change per delta spec keeps each plan/build cycle small and reviewable. After it ships, fold the outcome back into the original spec so it stays the source of truth for what exists, and flip the delta's `Status:` line to `implemented`.

## Objections and Answers

| Objection | Response |
|---|---|
| "This is simple, no spec needed" | Simple work needs short specs, not none; acceptance criteria still matter. |
| "I'll write it after coding" | That is documentation, not specification; clarity must come before code. |
| "The spec slows us down" | Fifteen minutes of spec prevents hours of rework. |
| "Requirements change anyway" | Hence a living document; a stale spec still beats none. |
| "The user knows what they want" | Clear requests carry implicit assumptions; the spec exposes them. |
| "Good idea, fold it into this spec" | Mid-build growth is how V1 slips; park it under Deferred. |
| "The feature has a spec, I'll edit it" | Shipped specs describe what exists; changes get a delta spec and the original is updated afterward. |
| "It's one big feature, splitting is overhead" | Independently testable clusters mean a monolithic spec forces every task to reason over the whole contract; a ten-line capability map is cheaper. |
| "I'll decompose during planning" | Planning slices tasks inside an already oversized artifact; module boundaries must be fixed before specifying. |

## Verification

Before implementation begins:

- [ ] The spec covers all six core areas (a delta spec covers only affected areas — at minimum objective, success criteria, and boundary deltas).
- [ ] The human reviewed and approved the spec.
- [ ] The turn ended after saving the spec; approval arrived in a later turn.
- [ ] Success criteria are specific and testable.
- [ ] Always / Ask First / Never boundaries are defined.
- [ ] The spec is saved to a repository file.
- [ ] Cut ideas appear under Out of Scope (Deferred), not dropped or quietly included.
- [ ] Changes to shipped specs use a delta spec referencing the original, not a rewrite.
- [ ] Multi-capability requests have an approved capability map (module ids, dependency direction, build order) before any module spec was written.
- [ ] Every module spec traces to a module id in the approved map.

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
- Path: `_sources/addyosmani_agent-skills/skills/spec-driven-development/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
