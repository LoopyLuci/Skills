---
name: git-workflow-and-versioning
description: Use when making any code change; committing, branching, resolving conflicts, splitting uncommitted work in a messy working tree into clean atomic commits, opening or reviewing a pull request (PR), pushing to a remote, or when you need to organize work across multiple parallel streams; cutting a release, choosing a semantic version bump, tagging, or writing a changelog; asked to write a commit message or a changelog entry for a change, or to split a change into commits, even when the diff is pasted inline and the message seems easy to write from it.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [software-development, engineering, agent-skills, git, version-control]
    source: addyosmani/agent-skills
    adapted: true
---

# Git Workflow and Versioning

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Making any code change
- Committing, branching, resolving conflicts, splitting uncommitted work in a messy working tree into clean atomic commits, opening or reviewing a pull request (PR), pushing to a remote, or when you need to organize work across multiple parallel streams
- Cutting a release, choosing a semantic version bump, tagging, or writing a changelog
- Asked to write a commit message or a changelog entry for a change, or to split a change into commits, even when the diff is pasted inline and the message seems easy to write from it

## When NOT to Use

- Large uncommitted changes accumulating
- Commit messages like "fix", "update", "misc"
- Formatting changes mixed with behavior changes
- No `.gitignore` in the project
- Committing `node_modules/`, `.env`, or build artifacts
- Long-lived branches that diverge significantly from main
- Force-pushing to shared branches
- A breaking change shipped under a minor or patch version bump
- A release with no tag, or a version number hand-edited out of sync with the tag
- A user-facing release with no changelog entry, or a changelog that's just dumped commit messages

## Overview

Git is the safety net that makes fast agent-generated change survivable: commits are save points, branches are sandboxes, and history is documentation nobody has to write by hand. The discipline exists so no change is ever larger than what you can review, revert, or explain later. Route every code change through it.

## Commit Discipline

### Trunk-Based Development

Keep `main` deployable at all times and do real work in short-lived branches that merge back within 1-3 days. DORA research consistently ties trunk-based development to high-performing teams, and long-lived dev branches are hidden costs: they diverge, conflict, and delay integration.

```
main ──●──●──●──●──●──●──●──●──●──  (always deployable)
        ╲      ╱  ╲    ╱
         ●──●─╱    ●──╱    ← short-lived feature branches (1-3 days)
```

- Every day a dev branch lives, it accrues merge risk; release branches are acceptable when you must stabilize while `main` moves forward.
- Prefer deploying incomplete work behind a feature flag over parking it on a branch for weeks.
- Teams committed to gitflow may keep the branching model, but they still owe the commit discipline here — the discipline carries more weight than the strategy.

### Commit Early, Commit Often

Give each successful increment its own commit:

```
Work pattern:
  Implement slice → Test → Verify → Commit → Next slice

Not this:
  Implement everything → Hope it works → Giant commit
```

Because commits are save points, a broken change costs one increment, not the whole session.

### Atomic Commits

One logical thing per commit, so every entry in the log stands alone:

```
# Good: Each commit is self-contained
git log --oneline
a1b2c3d Add task creation endpoint with validation
d4e5f6g Add task creation form component
h7i8j9k Connect form to API and add loading state
m1n2o3p Add task creation tests (unit + integration)

# Bad: Everything mixed together
git log --oneline
x1y2z3a Add task feature, fix sidebar, update deps, refactor utils
```

### Messages That Explain Why

```
# Good: Explains intent
feat: add email validation to registration endpoint

Prevents invalid email formats from reaching the database.
Uses Zod schema validation at the route handler level,
consistent with existing validation patterns in auth.ts.

# Bad: Describes what's obvious from the diff
update auth.ts
```

Standard shape:

```
<type>: <short description>

<optional body explaining why, not what>
```

- `feat` — new feature
- `fix` — bug fix
- `refactor` — change that neither fixes a bug nor adds a feature
- `test` — adding or updating tests
- `docs` — documentation only
- `chore` — tooling, dependencies, config

### Separate Concerns

Keep formatting out of behavior changes and refactors out of features; each change type deserves its own commit, ideally its own PR:

```
# Good: Separate concerns
git commit -m "refactor: extract validation logic to shared utility"
git commit -m "feat: add phone number validation to registration"

# Bad: Mixed concerns
git commit -m "refactor validation and add phone number field"
```

Splitting makes both changes easier to review, revert, and read in history. Small cleanups such as a variable rename may ride along inside a feature commit at reviewer discretion.

### Size Your Changes

```
~100 lines  → Easy to review, easy to revert
~300 lines  → Acceptable for a single logical change
~1000 lines → Split into smaller changes
```

Target about 100 lines per commit/PR. Past roughly 1000 lines, split before submitting — see `code-review-and-quality` for breakdown strategies.

## Branching

```
main (always deployable)
  │
  ├── feature/task-creation    ← One feature per branch
  ├── feature/user-settings    ← Parallel work
  └── fix/duplicate-tasks      ← Bug fixes
```

Branch from `main` (or the team default), keep the branch short-lived, delete it after merge, and prefer feature flags to long branches for unfinished features.

```
feature/<short-description>   → feature/task-creation
fix/<short-description>       → fix/duplicate-tasks
chore/<short-description>     → chore/update-deps
refactor/<short-description>  → refactor/auth-module
```

## Worktrees for Parallel Agents

```bash
# Create a worktree for a feature branch
git worktree add ../project-feature-a feature/task-creation
git worktree add ../project-feature-b feature/user-settings

# Each worktree is a separate directory with its own branch
# Agents can work in parallel without interfering
ls ../
  project/              ← main branch
  project-feature-a/    ← task-creation branch
  project-feature-b/    ← user-settings branch

# When done, merge and clean up
git worktree remove ../project-feature-a
```

Use worktrees to run several agents on different branches at once: each directory owns its branch, no switching is needed, a failed experiment is just a deleted directory, and nothing leaks until you merge.

## Save Point Pattern

```
Agent starts work
    │
    ├── Makes a change
    │   ├── Test passes? → Commit → Continue
    │   └── Test fails? → Revert to last commit → Investigate
    │
    ├── Makes another change
    │   ├── Test passes? → Commit → Continue
    │   └── Test fails? → Revert to last commit → Investigate
    │
    └── Feature complete → All commits form a clean history
```

You never lose more than one increment of work. If an agent wanders off, `git reset --hard HEAD` drops you back to the last good state.

## Change Summaries

Report the shape of every modification in three parts:

```
CHANGES MADE:
- src/routes/tasks.ts: Added validation middleware to POST endpoint
- src/lib/validation.ts: Added TaskCreateSchema using Zod

THINGS I DIDN'T TOUCH (intentionally):
- src/routes/auth.ts: Has similar validation gap but out of scope
- src/middleware/error.ts: Error format could be improved (separate task)

POTENTIAL CONCERNS:
- The Zod schema is strict — rejects extra fields. Confirm this is desired.
- Added zod as a dependency (72KB gzipped) — already in package.json
```

The summary catches wrong assumptions early and hands reviewers a map of the change. The "didn't touch" section earns its place most: it demonstrates scope discipline rather than unsolicited renovation.

## Pre-Commit Hygiene

Run all five steps before committing:

```bash
# 1. Check what you're about to commit
git diff --staged

# 2. Ensure no secrets (lists matching file names only — any output means review them)
git diff --staged -i -G'password|secret|api_key|token' --name-only

# 3. Run tests
npm test

# 4. Run linting
npm run lint

# 5. Run type checking
npx tsc --noEmit
```

Automate the routine parts with git hooks:

```json
// package.json (using lint-staged + husky)
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

## Generated Files

- Commit generated files only when the project expects them (`package-lock.json`, Prisma migrations).
- Exclude build output (`dist/`, `.next/`), environment files (`.env`), and IDE config (`.vscode/settings.json` unless shared).
- Maintain a `.gitignore` covering at least `node_modules/`, `dist/`, `.env`, `.env.local`, `*.pem`.

## Debugging with Git

```bash
# Find which commit introduced a bug
git bisect start
git bisect bad HEAD
git bisect good <known-good-commit>
# Git checkouts midpoints; run your test at each to narrow down

# View what changed recently
git log --oneline -20
git diff HEAD~5..HEAD -- src/

# Find who last changed a specific line
git blame src/services/task.ts

# Search commit messages for a keyword
git log --grep="validation" --oneline
```

## Release and Versioning

Commits track change for you; a version number tracks it for everyone who consumes your code. The moment another team, a published package, or a deployed client depends on what you ship, "latest on main" stops answering "what am I running, and is it safe to upgrade?" A version plus a changelog is the contract that answers.

### Semantic Versioning

```
  MAJOR  breaking change — consumers must change their code to upgrade
  MINOR  new functionality, backward-compatible — safe to upgrade
  PATCH  bug fix, backward-compatible — safe to upgrade
```

Treat the number as a promise and make the code match it. A patch that alters behavior consumers relied on is really a major wearing a disguise (Hyrum's Law — see `api-and-interface-design`). When unsure whether a change is breaking, assume it is: a surprising major is cheaper than a broken consumer.

### Tag the Release

A release is an immutable point in history, not a moving branch:

```bash
git tag -a v1.4.0 -m "Release 1.4.0"
git push origin v1.4.0
```

Derive the version from the tag instead of hand-editing it across files, so the artifact, tag, and changelog cannot drift apart.

### Changelog Written for Humans

A changelog is not `git log`: it is the curated, consumer-facing answer to "what changed, and do I care?", grouped by `Added / Changed / Fixed / Deprecated / Removed / Security`, newest first, with every entry phrased around user impact rather than internal mechanics.

```markdown
## [1.4.0] - 2025-06-12
### Added
- Bulk task import via CSV
### Fixed
- Timezone drift in recurring task due dates
### Deprecated
- `GET /v1/tasks/all` — use the paginated `GET /v1/tasks` (removal in 2.0)
```

Write the entry in the same change that makes the change, while the impact is fresh. Breaking changes carry a migration note and a deprecation window (`deprecation-and-migration`); actually shipping the release belongs to `shipping-and-launch`.

## Rationalizations to Reject

| Excuse | Reality |
|---|---|
| "I'll commit when the feature is done" | One giant commit cannot be reviewed, debugged, or reverted; commit each slice. |
| "The message doesn't matter" | Messages are documentation for future you and future agents. |
| "I'll squash it all later" | Squashing destroys the development narrative; keep commits clean from the start. |
| "Branches add overhead" | Short-lived branches prevent collisions; long-lived branches are the problem. |
| "I'll split this change later" | Large changes are harder to review, riskier to deploy, and harder to revert; split first. |
| "I don't need a .gitignore" | Not until production secrets land in history; set it up immediately. |
| "It's just a small fix, bump the patch" | Judge by what consumers observe: a relied-on behavior change is a major regardless of diff size. |
| "The changelog is just the commit log" | Commits serve you; the changelog serves consumers and is curated by impact. |
| "We'll write the changelog at release time" | By then the impact is reconstructed from memory and half is missing. |

## Red Flags

- Large uncommitted changes accumulating.
- Messages like `fix`, `update`, `misc`.
- Formatting changes mixed with behavior changes.
- Missing `.gitignore`, or one that lets in `node_modules/`, `.env`, or build artifacts.
- Long-lived branches significantly diverged from main.
- Force-pushing to shared branches.
- A breaking change shipped under a minor or patch bump.
- A release with no tag, or a version hand-edited out of sync with the tag.
- A user-facing release with no changelog entry, or a changelog that is dumped commit messages.

## Verification

For every commit:

- [ ] The commit does one logical thing.
- [ ] The message explains the why and follows the type convention.
- [ ] Tests pass before committing.
- [ ] No secrets appear in the diff.
- [ ] No formatting-only changes are mixed with behavior changes.
- [ ] `.gitignore` covers standard exclusions.

For every release (anything with consumers):

- [ ] Version bump matches the change: breaking → major, additive → minor, fix → patch.
- [ ] The release is tagged, and the version derives from the tag rather than a hand edit.
- [ ] The changelog has a curated, human-readable entry grouped by impact for this version.

## Related Skills in This Repo

- [code-review-and-quality](../code-review-and-quality/SKILL.md) — Use when reviewing code written by yourself, another agent, or a human; you need to assess...
- [ci-cd-and-automation](../ci-cd-and-automation/SKILL.md) — Use when setting up or modifying build and deployment pipelines; you need to automate qual...
- [api-and-interface-design](../api-and-interface-design/SKILL.md) — Use when designing APIs, module boundaries, or any public interface; creating REST or Grap...
- [context-engineering](../context-engineering/SKILL.md) — Use when starting a new session, when agent output quality degrades, when switching betwee...
- [advanced-version-control-git](../advanced-version-control-git/SKILL.md) — Use when using advanced git workflows and recovery.
- [skills-repo-sync](../skills-repo-sync/SKILL.md) — Sync skills between Hermes and a GitHub repo.
- [resolving-merge-conflicts](../resolving-merge-conflicts/SKILL.md) — Use when you need to resolve an in-progress git merge/rebase conflict.

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Upstream anti-patterns retained as the When-NOT-to-Use list.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- Path: `_sources/addyosmani_agent-skills/skills/git-workflow-and-versioning/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
