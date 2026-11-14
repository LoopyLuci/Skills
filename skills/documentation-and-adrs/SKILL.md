---
name: documentation-and-adrs
description: Use when you need to document an architecture decision (ADR) or the reasoning behind a design choice, when changing public APIs, shipping features, when docs may be stale or out of sync with the code they describe, when working out which module docs are still accurate, or when setting up a check so docs cannot silently go out of date again.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [software-development, engineering, agent-skills, documentation, adr]
    source: addyosmani/agent-skills
    adapted: true
---

# Documentation and ADRs

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- You need to document an architecture decision (ADR) or the reasoning behind a design choice, when changing public APIs, shipping features, when docs may be stale or out of sync with the code they describe, when working out which module docs are still accurate, or when setting up a check so docs cannot silently go out of date again

## When NOT to Use

- Architectural decisions with no written rationale
- Public APIs with no documentation or types
- README that doesn't explain how to run the project
- Commented-out code instead of deletion
- TODO comments that have been there for weeks
- No ADRs in a project with significant architectural choices
- Documentation that restates the code instead of explaining intent
- A change log that has been rewritten rather than appended to
- A doc called current when the commit order of the doc and its code could not be determined

## Overview

Documentation earns its keep by recording *why*: the context, constraints, and trade-offs behind a decision. Code shows what was built; docs explain why it was built that way and what was rejected instead. That reasoning is what future humans and agents cannot reconstruct from the source alone, so capture it at the moment it is still cheap to record.

## Architecture Decision Records (ADRs)

ADRs hold the rationale for significant technical decisions and are the highest-value documentation you can produce.

### When to Write One

- Selecting a framework, library, or other major dependency
- Designing a data model or database schema
- Choosing an authentication strategy
- Settling an API architecture (REST vs. GraphQL vs. tRPC)
- Picking build tools, hosting platforms, or infrastructure
- Any decision that would be expensive to reverse

### Match the Existing Convention First

Before adding an ADR, inspect the repository for an established convention: existing ADRs, project instructions, and ADR tooling or configuration such as an `.adr-dir` file. An established convention overrides the defaults below. Concretely, match:

- **Location and format** — `docs/adr/*.md`, `Documentation/Decisions/*.rst`, a MADR layout, an `adr-tools` setup, and so on. Reuse the directory, extension, and markup already in use.
- **Numbering and naming** — continue the current sequence and filename pattern (`ADR-004-Title.rst`, `0004-title.md`, …). Never restart at 001 or introduce a second scheme.
- **Section headings** — adopt the project's heading set rather than imposing this template.

If the available evidence conflicts, surface the conflict instead of quietly starting another scheme. Apply the default below only when no convention can be established.

### Template

Default location is `docs/decisions/` with sequential numbering, unless the project already standardizes elsewhere:

```markdown
# ADR-001: Use PostgreSQL for primary database

## Status
Proposed | Accepted | Superseded by ADR-XXX | Deprecated

## Date
2025-01-15

## Context
We need a primary database for the task management application. Key requirements:
- Relational data model (users, tasks, teams with relationships)
- ACID transactions for task state changes
- Support for full-text search on task content
- Managed hosting available (for small team, limited ops capacity)

## Decision
Use PostgreSQL with Prisma ORM.

## Alternatives Considered

### MongoDB
- Pros: Flexible schema, easy to start with
- Cons: Our data is inherently relational; would need to manage relationships manually
- Rejected: Relational data in a document store leads to complex joins or data duplication

### SQLite
- Pros: Zero configuration, embedded, fast for reads
- Cons: Limited concurrent write support, no managed hosting for production
- Rejected: Not suitable for multi-user web application in production

### MySQL
- Pros: Mature, widely supported
- Cons: PostgreSQL has better JSON support, full-text search, and ecosystem tooling
- Rejected: PostgreSQL is the better fit for our feature requirements

## Consequences
- Prisma provides type-safe database access and migration management
- We can use PostgreSQL's full-text search instead of adding Elasticsearch
- Team needs PostgreSQL knowledge (standard skill, low risk)
- Hosting on managed service (Supabase, Neon, or RDS)
```

### Lifecycle

```
PROPOSED → ACCEPTED → (SUPERSEDED or DEPRECATED)
```

Old ADRs stay in place — they preserve historical context. When a decision changes, write a new ADR that references and supersedes the old one rather than editing the original.

## Inline Documentation

### Explain Why, Not What

```typescript
// BAD: Restates the code
// Increment counter by 1
counter += 1;

// GOOD: Explains non-obvious intent
// Rate limit uses a fixed window that opens on the first request after the
// previous one expires, not on a clock schedule. Known gap: a client can spend
// the full limit just before a reset and again just after (2x in a moment)
if (now - windowStart > WINDOW_SIZE_MS) {
  counter = 0;
  windowStart = now;
}
```

### Skip Comments That Add Nothing

```typescript
// Don't comment self-explanatory code
function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// Don't leave TODO comments for things you should just do now
// TODO: add error handling  ← Just add it

// Don't leave commented-out code
// const oldImplementation = () => { ... }  ← Delete it, git has history
```

### Record Known Traps Where They Live

```typescript
/**
 * IMPORTANT: This function must be called before the first render.
 * If called after hydration, it causes a flash of unstyled content
 * because the theme context isn't available during SSR.
 *
 * See ADR-003 for the full design rationale.
 */
export function initializeTheme(theme: Theme): void {
  // ...
}
```

## API Documentation

For public APIs (REST, GraphQL, library interfaces), document inline with the types where possible:

```typescript
/**
 * Creates a new task.
 *
 * @param input - Task creation data (title required, description optional)
 * @returns The created task with server-generated ID and timestamps
 * @throws {ValidationError} If title is empty or exceeds 200 characters
 * @throws {AuthenticationError} If the user is not authenticated
 *
 * @example
 * const task = await createTask({ title: 'Buy groceries' });
 * console.log(task.id); // "task_abc123"
 */
export async function createTask(input: CreateTaskInput): Promise<Task> {
  // ...
}
```

For REST surfaces, describe the contract with OpenAPI/Swagger:

```yaml
paths:
  /api/tasks:
    post:
      summary: Create a task
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateTaskInput'
      responses:
        '201':
          description: Task created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '422':
          description: Validation error
```

## README Structure

Every project needs a README covering at least this ground:

```markdown
# Project Name

One-paragraph description of what this project does.

## Quick Start
1. Clone the repo
2. Install dependencies: `npm install`
3. Set up environment: `cp .env.example .env`
4. Run the dev server: `npm run dev`

## Commands
| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm test` | Run tests |
| `npm run build` | Production build |
| `npm run lint` | Run linter |

## Architecture
Brief overview of the project structure and key design decisions.
Link to ADRs for details.

## Contributing
How to contribute, coding standards, PR process.
```

## Changelog Maintenance

Record shipped features as appended entries grouped by kind:

```markdown
# Changelog

## [1.2.0] - 2025-01-20
### Added
- Task sharing: users can share tasks with team members (#123)
- Email notifications for task assignments (#124)

### Fixed
- Duplicate tasks appearing when rapidly clicking create button (#125)

### Changed
- Task list now loads 50 items per page (was 20) for better UX (#126)
```

## Documentation for Agents

Agents consume project docs heavily, so treat these as load-bearing:

- **CLAUDE.md / rules files** — encode conventions so agents follow them
- **Spec files** — keep current so agents build the intended thing
- **ADRs** — let agents see past reasoning instead of re-deciding settled questions
- **Inline gotchas** — stop agents from walking into known traps

## Prose Review

Once the technical content checks out, review the writing for the people who will read it. Rewording must never change the decision or its limits.

1. Identify what must survive editing: names, numbers and units, commands, paths, links, conditions, trade-offs, and uncertainty. Verify each against the code and decision context, and flag anything you cannot substantiate.
2. Cut stock openings, promotional adjectives, and repeated summaries; replace them with the concrete information the reader needs. Do not swap an unsupported claim for an invented example or a stronger guarantee. Keep necessary technical repetition and the project's established terminology.
3. Diff the edited document against the original and its sources. Restore any lost qualifier or caveat, confirm commands and code examples still behave as documented, and raise unresolved factual questions explicitly instead of smoothing them over.

## Documentation Drift

A doc that was accurate when written still reads as authoritative after the code moves on. Decide staleness from version control, not from how confident the prose sounds:

```bash
code=$(git log -1 --format=%H -- src/rate-limiter.js)
doc=$(git log -1 --format=%H -- docs/rate-limiter.md)
if [ "$code" = "$doc" ]; then echo "current: changed together"
elif git merge-base --is-ancestor "$doc" "$code"; then echo "stale: code changed after the doc"
elif git merge-base --is-ancestor "$code" "$doc"; then echo "current: doc changed after the code"
else echo "can't tell"; fi
```

Unordered history — divergent branches, a rebase, a shallow clone — yields "can't tell". Report it that way and never label such a doc current.

When correcting a doc that carries a changelog, append a dated entry explaining the correction. Do not rewrite or collapse earlier entries: git preserves the old text, but the log is the only surviving record of the reasons.

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "The code is self-documenting" | Code states what happened; it cannot state why, what alternatives lost, or which constraints applied. |
| "We'll document once the API stabilizes" | Documenting speeds stabilization — the doc is the first test of the design. |
| "Nobody reads docs" | Agents do, future engineers do, and so will you in three months. |
| "ADRs are overhead" | Ten minutes spent on an ADR saves a two-hour re-debate six months later. |
| "Comments go stale" | Comments about *why* stay stable; comments about *what* go stale, which is why you only write the former. |
| "I'll tidy the changelog while I'm here" | Git holds the old text; the log holds the reasoning. Rewriting it destroys the only copy of both. |

## Red Flags

- Architectural decisions with no recorded rationale
- Public APIs lacking documentation or types
- A README that never explains how to run the project
- Commented-out code left in place of deletion
- TODO comments that have survived for weeks
- No ADRs in a project with significant architectural choices
- Docs that restate code instead of explaining intent
- A changelog that was rewritten rather than appended to
- A doc declared current when commit order between it and its code could not be determined

## Verification

- [ ] An ADR exists for every significant architectural decision
- [ ] README covers quick start, commands, and an architecture overview
- [ ] API functions carry parameter and return type documentation
- [ ] Known gotchas are documented inline at the point they matter
- [ ] No commented-out code remains
- [ ] Rules files (CLAUDE.md etc.) are current and accurate
- [ ] Prose edits preserved source details, trade-offs, and qualifiers without adding unsupported guarantees
- [ ] Changelogs were appended to, not rewritten
- [ ] A doc whose staleness could not be determined is reported as "can't tell", not as current

## Related Skills in This Repo

- [code-review-and-quality](../code-review-and-quality/SKILL.md) — Use when reviewing code written by yourself, another agent, or a human; you need to assess...
- [ci-cd-and-automation](../ci-cd-and-automation/SKILL.md) — Use when setting up or modifying build and deployment pipelines; you need to automate qual...
- [api-and-interface-design](../api-and-interface-design/SKILL.md) — Use when designing APIs, module boundaries, or any public interface; creating REST or Grap...
- [git-workflow-and-versioning](../git-workflow-and-versioning/SKILL.md) — Use when making any code change; committing, branching, resolving conflicts, splitting unc...
- [writing-skills](../writing-skills/SKILL.md) — Use when creating, editing, or testing agent skills
- [technical-writing-patterns](../technical-writing-patterns/SKILL.md) — Use when writing technical documentation.
- [technical-documentation](../technical-documentation/SKILL.md) — Use when writing technical documentation for projects.

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Upstream anti-patterns retained as the When-NOT-to-Use list.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- Path: `_sources/addyosmani_agent-skills/skills/documentation-and-adrs/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
