---
name: code-simplification
description: Use when refactoring code for clarity without changing behavior; code works but is harder to read, maintain, or extend than it should be; reviewing code that has accumulated unnecessary complexity; asked to simplify, clean up, or reduce the nesting of a function or module that already works, even when the code is pasted inline and nothing else needs to change.
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

# Code Simplification

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Refactoring code for clarity without changing behavior
- Code works but is harder to read, maintain, or extend than it should be
- Reviewing code that has accumulated unnecessary complexity
- Asked to simplify, clean up, or reduce the nesting of a function or module that already works, even when the code is pasted inline and nothing else needs to change

## When NOT to Use

- Simplification that requires modifying tests to pass (you likely changed behavior)
- "Simplified" code that is longer and harder to follow than the original
- Renaming things to match your preferences rather than project conventions
- Removing error handling because "it makes the code cleaner"
- Simplifying code you don't fully understand
- Batching many simplifications into one large, hard-to-review commit
- Refactoring code outside the scope of the current task without being asked

## Overview

Simplification means reducing complexity without altering behavior — not shrinking line count. The target is code a newcomer can understand faster than the original: fewer moving parts, clearer names, and the same outputs, side effects, error handling, and edge-case behavior as before. This is process-driven work that applies to any language; the test of every change is whether it makes the code easier to read, maintain, and extend.

## Core Principles

### Preserve Behavior Exactly

Change only how code expresses itself, never what it does. Inputs, outputs, side effects, error paths, and ordering must stay identical. If you cannot be certain a rewrite preserves behavior, leave it alone.

```
ASK BEFORE EVERY CHANGE:
→ Does this produce the same output for every input?
→ Does this maintain the same error behavior?
→ Does this preserve the same side effects and ordering?
→ Do all existing tests still pass without modification?
```

### Follow Project Conventions

"Simpler" means more consistent with the codebase, not more aligned with your own taste. First:

```
1. Read CLAUDE.md / project conventions
2. Study how neighboring code handles similar patterns
3. Match the project's style for:
   - Import ordering and module system
   - Function declaration style
   - Naming conventions
   - Error handling patterns
   - Type annotation depth
```

A rewrite that breaks house style is churn, not simplification.

### Prefer Clarity Over Cleverness

When a compact version requires a mental pause, prefer the explicit one:

```typescript
// UNCLEAR: Dense ternary chain
const label = isNew ? 'New' : isUpdated ? 'Updated' : isArchived ? 'Archived' : 'Active';

// CLEAR: Readable mapping
function getStatusLabel(item: Item): string {
  if (item.isNew) return 'New';
  if (item.isUpdated) return 'Updated';
  if (item.isArchived) return 'Archived';
  return 'Active';
}
```

```typescript
// UNCLEAR: Chained reduces with inline logic
const result = items.reduce((acc, item) => ({
  ...acc,
  [item.id]: { ...acc[item.id], count: (acc[item.id]?.count ?? 0) + 1 }
}), {});

// CLEAR: Named intermediate step
const countById = new Map<string, number>();
for (const item of items) {
  countById.set(item.id, (countById.get(item.id) ?? 0) + 1);
}
```

### Avoid Over-Simplifying

The failure mode of this skill is going too far:

- **Inlining too hard** — deleting a helper that gave a concept a name hurts readability
- **Merging unrelated logic** — two simple functions fused into one complex one is not simpler
- **Stripping abstraction that earns its place** — some exist for extensibility or testability
- **Optimizing for line count** — comprehension speed is the metric, not lines removed

### Scope to What Changed

Default to simplifying recently modified code. Drive-by refactors of untouched modules add diff noise and regression risk; widen scope only when asked.

## Process

### 1. Understand Before Touching

This is Chesterton's Fence: don't remove a fence until you know why it was built. Ask:

```
BEFORE SIMPLIFYING, ANSWER:
- What is this code's responsibility?
- What calls it? What does it call?
- What are the edge cases and error paths?
- Are there tests that define the expected behavior?
- Why might it have been written this way? (Performance? Platform constraint? Historical reason?)
- Check git blame: what was the original context for this code?
```

If you cannot answer these, keep reading; you are not ready to edit.

### 2. Spot Concrete Signals

**Structural complexity**

| Pattern | Signal | Simplification |
|---------|--------|----------------|
| Deep nesting (3+ levels) | Hard to follow control flow | Extract conditions into guard clauses or helpers |
| Long functions (50+ lines) | Multiple responsibilities | Split into focused functions with descriptive names |
| Nested ternaries | Needs a mental stack to parse | Replace with if/else chains, switch, or lookup objects |
| Boolean parameter flags | `doThing(true, false, true)` | Use options objects or separate functions |
| Repeated conditionals | Same `if` in several places | Extract a well-named predicate |

**Naming and readability**

| Pattern | Signal | Simplification |
|---------|--------|----------------|
| Generic names | `data`, `result`, `temp`, `val`, `item` | Name the content: `userProfile`, `validationErrors` |
| Abbreviations | `usr`, `cfg`, `btn`, `evt` | Spell it out unless universal (`id`, `url`, `api`) |
| Misleading names | A `get` function that also mutates state | Rename to reflect actual behavior |
| "What" comments | `// increment counter` above `count++` | Delete; the code says it |
| "Why" comments | `// Retry because the API is flaky under load` | Keep; the code can't say this |

**Redundancy**

| Pattern | Signal | Simplification |
|---------|--------|----------------|
| Duplicated logic | Same 5+ lines repeated | Extract a shared function |
| Dead code | Unreachable branches, unused vars, commented-out blocks | Remove once confirmed dead |
| Useless wrappers | Pass-through with no added value | Inline and call the underlying function |
| Over-engineering | Factory-for-a-factory, strategy-with-one-strategy | Replace with the direct approach |
| Redundant assertions | Casting an already-inferred type | Drop the assertion |

### 3. Apply Incrementally

One simplification at a time, tests after each:

```
FOR EACH SIMPLIFICATION:
1. Make the change
2. Run the test suite
3. If tests pass → commit (or continue to next simplification)
4. If tests fail → revert and reconsider
```

Keep refactor commits separate from feature or bugfix commits; a PR that does both is really two PRs. If a refactor would exceed roughly 500 lines, reach for automation (codemods, AST transforms) instead of hand-editing.

### 4. Evaluate the Whole

Afterward, compare before and against:

```
COMPARE BEFORE AND AFTER:
- Is the simplified version genuinely easier to understand?
- Did you introduce any new patterns inconsistent with the codebase?
- Is the diff clean and reviewable?
- Would a teammate approve this change?
```

If the result is harder to read or review, revert. Not every attempt succeeds.

## Language Notes

TypeScript / JavaScript:

```typescript
// SIMPLIFY: Unnecessary async wrapper
// Before
async function getUser(id: string): Promise<User> {
  return await userService.findById(id);
}
// After
function getUser(id: string): Promise<User> {
  return userService.findById(id);
}

// SIMPLIFY: Verbose conditional assignment
// Before
let displayName: string;
if (user.nickname) {
  displayName = user.nickname;
} else {
  displayName = user.fullName;
}
// After
const displayName = user.nickname || user.fullName;

// SIMPLIFY: Manual array building
// Before
const activeUsers: User[] = [];
for (const user of users) {
  if (user.isActive) {
    activeUsers.push(user);
  }
}
// After
const activeUsers = users.filter((user) => user.isActive);

// SIMPLIFY: Redundant boolean return
// Before
function isValid(input: string): boolean {
  if (input.length > 0 && input.length < 100) {
    return true;
  }
  return false;
}
// After
function isValid(input: string): boolean {
  return input.length > 0 && input.length < 100;
}
```

Python:

```python
# SIMPLIFY: Verbose dictionary building
# Before
result = {}
for item in items:
    result[item.id] = item.name
# After
result = {item.id: item.name for item in items}

# SIMPLIFY: Nested conditionals with early return
# Before
def process(data):
    if data is not None:
        if data.is_valid():
            if data.has_permission():
                return do_work(data)
            else:
                raise PermissionError("No permission")
        else:
            raise ValueError("Invalid data")
    else:
        raise TypeError("Data is None")
# After
def process(data):
    if data is None:
        raise TypeError("Data is None")
    if not data.is_valid():
        raise ValueError("Invalid data")
    if not data.has_permission():
        raise PermissionError("No permission")
    return do_work(data)
```

React / JSX:

```tsx
// SIMPLIFY: Verbose conditional rendering
// Before
function UserBadge({ user }: Props) {
  if (user.isAdmin) {
    return <Badge variant="admin">Admin</Badge>;
  } else {
    return <Badge variant="default">User</Badge>;
  }
}
// After
function UserBadge({ user }: Props) {
  const variant = user.isAdmin ? 'admin' : 'default';
  const label = user.isAdmin ? 'Admin' : 'User';
  return <Badge variant={variant}>{label}</Badge>;
}

// SIMPLIFY: Prop drilling through intermediate components
// Before — consider whether context or composition solves this better.
// This is a judgment call — flag it, don't auto-refactor.
```

## Rationalizations to Reject

| Excuse | Reality |
|---|---|
| "It works, no need to touch it" | Hard-to-read code will be hard to fix when it breaks; simplify now or pay later on every change. |
| "Fewer lines is always simpler" | A one-line nested ternary beats nothing over a five-line if/else. Comprehension speed decides. |
| "I'll quickly simplify this unrelated code too" | Unscoped edits make noisy diffs and regressions you never intended. |
| "The types make it self-documenting" | Types document structure, not intent; a good name explains *why* better than a signature explains *what*. |
| "This abstraction might be useful later" | Speculative abstractions are complexity with no current value. Remove; re-add when needed. |
| "The original author must have had a reason" | Check git blame, but accumulated complexity often has no reason — it's residue from iteration under pressure. |
| "I'll refactor while adding this feature" | Mixed changes are harder to review, revert, and read in history. Split them. |

## Red Flags

- Tests had to be modified to pass (behavior likely changed)
- The "simplified" version is longer and harder to follow
- Renames match personal preference instead of project conventions
- Error handling removed because it looked messy
- Code simplified that isn't fully understood
- Many simplifications bundled into one unreviewable commit
- Refactoring outside the task's scope unasked

## Verification

After a simplification pass:

- [ ] All existing tests pass unchanged
- [ ] Build succeeds with no new warnings
- [ ] Linter/formatter passes
- [ ] Each simplification is small and reviewable
- [ ] Diff contains no unrelated changes
- [ ] Style matches project conventions (checked against CLAUDE.md or equivalent)
- [ ] No error handling removed or weakened
- [ ] No dead code left behind (unused imports, unreachable branches)
- [ ] A reviewer would call the result a net improvement

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
- Path: `_sources/addyosmani_agent-skills/skills/code-simplification/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
