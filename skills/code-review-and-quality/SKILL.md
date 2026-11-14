---
name: code-review-and-quality
description: Use when reviewing code written by yourself, another agent, or a human; you need to assess code quality across multiple dimensions before it enters the main branch; asked to review a diff or a pull request, even when the diff is pasted inline and the review looks quick to do from reading it.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [software-development, engineering, agent-skills, code-review, quality]
    source: addyosmani/agent-skills
    adapted: true
---

# Code Review and Quality

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Reviewing code written by yourself, another agent, or a human
- You need to assess code quality across multiple dimensions before it enters the main branch
- Asked to review a diff or a pull request, even when the diff is pasted inline and the review looks quick to do from reading it

## When NOT to Use

- PRs merged without any review
- Review that only checks if tests pass (ignoring other axes)
- "LGTM" without evidence of actual review
- Security-sensitive changes without security-focused review
- Large PRs that are "too big to review properly" (split them)
- No regression tests with bug fix PRs
- Review comments without severity labels — makes it unclear what's required vs optional
- Accepting "I'll fix it later" — it never happens
- A refactor that moves code around without reducing the number of concepts a reader must hold
- A change that grows an already-large file instead of decomposing it
- New conditionals scattered into unrelated code paths (a missing abstraction)
- A bespoke helper that duplicates an existing canonical one, or feature logic placed in a shared module
- A bulk "bump dependencies" PR with no changelog review and no per-package isolation
- A lockfile change that's hand-edited, uncommitted, or merged without reviewing its diff

## Overview

Every change gets a review before it merges — authored by you, another agent, or a human. The review weighs five axes (correctness, readability, architecture, security, performance) and labels each finding by severity so authors know what is mandatory and what is optional. The approval bar is improvement, not perfection: approve when a change clearly makes the codebase healthier and follows project conventions, even if it isn't written the way you would have written it.

## The Five Axes

### Correctness

Does the change do what it claims? Confirm it matches the spec, handles edges (null, empty, boundaries), covers error paths, passes tests that actually assert the right things, and avoids off-by-one errors, races, and inconsistent state.

### Readability

Could another engineer understand this without the author? Names should be descriptive and consistent (not bare `temp`/`data`/`result`), control flow direct, and related code grouped. Remove dead artifacts (`_unused`, backwards-compat shims, `// removed` comments) and simplify clever tricks. A conditional bolted onto an unrelated flow, or repeated conditionals over the same shape, signals a missing model or dispatcher — that is design debt, not a nit.

### Architecture

Does it fit the system? Follow existing patterns unless a new one is justified, keep module boundaries clean, share duplicated logic, and keep dependencies acyclic. Judge refactors by the concepts a reader must hold: if a "cleaner" version holds the same count, it relocated complexity instead of reducing it — prefer the shape where whole branches, modes, or layers disappear, and prefer deleting an abstraction over polishing it. Keep feature-specific logic out of shared modules, reuse canonical helpers instead of near-duplicates, and replace gratuitous `any`/casts/silent fallbacks with explicit type boundaries.

### Security

Does it introduce vulnerabilities? Validate and sanitize input, keep secrets out of code, logs, and version control, enforce authentication/authorization, parameterize SQL, encode output against XSS, use trusted dependencies, and treat external data as untrusted until validated at the boundary. Deeper guidance lives in `security-and-hardening`.

### Performance

Does it create bottlenecks? Hunt for N+1 queries, unbounded loops or fetches, synchronous work that belongs async, redundant UI re-renders, missing pagination, and large allocations in hot paths. Profiling depth lives in `performance-optimization`.

## Structural Remedies

Never stop at "this is complex" — name the move. Swap conditional chains for typed models or dispatchers, collapse duplicate branches into one flow, split orchestration from business logic, move feature logic into the package that owns it, reuse the canonical helper, make a type boundary explicit, delete pass-through wrappers that obscure rather than clarify, and extract helpers or split large files. Pick whichever option removes moving parts instead of redistributing them.

## Change Sizing

Focused changes review faster, merge sooner, and deploy safer:

```
~100 lines changed   → Good. Reviewable in one sitting.
~300 lines changed   → Acceptable if it's a single logical change.
~1000 lines changed  → Too large. Split it.
```

Watch total file size, not just diff size: a small diff that pushes a file past roughly 1000 total lines is a signal to decompose before adding. One change is a single self-contained modification addressing one thing, with its tests, leaving the system functional — a slice of a feature, not the whole thing. Wholesale deletions and automated refactors are exempt because the reviewer verifies intent rather than every line. Keep refactoring and behavior changes in separate submissions; incidental renames may ride along at the reviewer's discretion.

| Strategy | How | When to use |
|----------|-----|-------------|
| **Stack** | Land a small change, base the next on it | Sequential dependencies |
| **By file group** | Separate changes that need different reviewers | Cross-cutting concerns |
| **Horizontal** | Ship shared code/stubs first, then consumers | Layered architecture |
| **Vertical** | Cut smaller full-stack slices of the feature | Feature work |

## Change Descriptions

Each change needs a description that stands alone in version-control history. First line: short, imperative, informative ("Delete the FizzBuzz RPC," not "Deleting the FizzBuzz RPC"). Body: what changed and why, including context and decisions invisible in the diff, links to bugs or benchmarks, and candor about shortcomings. Avoid "Fix bug," "Fix build," "Add patch," "Moving code from A to B," "Phase 1."

## Review Process

1. **Understand the intent** before reading code: what is the change for, which spec or task does it implement, and what behavior should change?
2. **Review tests first.** Do they exist, assert behavior over internals, cover edges, use descriptive names, and catch regressions? Prove the last point experimentally: invert one condition the change adds (drop a negation, swap `&&` for `||`), run the suite, then restore the file from a copy. A surviving mutant is a finding — name the missing test case. For project-wide mutation scoring see `constraint-driven-development`.
3. **Walk the implementation** file by file through all five axes.
4. **Categorize findings.** Check each candidate against the callers, guards, and tests that reach the changed code; discard anything they eliminate. Distinguish pre-existing defects from new regressions. Zero findings is legitimate — do not manufacture one. Order by leverage: correctness and security first, then structural regressions and missed simplifications, then everything else; one structural problem outweighs ten nits.
5. **Verify the verification.** Which tests ran, did the build pass, was there manual testing, screenshots, or before/after comparison?

Severity labels keep feedback actionable:

| Prefix | Meaning | Author action |
|--------|---------|---------------|
| *(no prefix)* | Required change | Must address before merge |
| **Critical:** | Blocks merge | Security vulnerability, data loss, broken functionality |
| **Nit:** | Minor, optional | Author may ignore — formatting, style preferences |
| **Optional:** / **Consider:** | Suggestion | Worth considering but not required |
| **FYI** | Informational only | No action needed — context for future reference |

## Multi-Model Review

Separate authoring from reviewing — different models fail differently:

```
Model A writes the code
    │
    ▼
Model B reviews for correctness and architecture
    │
    ▼
Model A addresses the feedback
    │
    ▼
Human makes the final call
```

Example prompt for a review agent:

```
Review this code change for correctness, security, and adherence to
our project conventions. The spec says [X]. The change should [Y].
Flag any issues as Critical, Required, Optional, or Nit.
```

## Dead Code

After refactors or implementation changes, find code that is now unreachable, list it explicitly, and ask before deleting — orphans confuse readers, but uncertain deletions belong to the owner:

```
DEAD CODE IDENTIFIED:
- formatLegacyDate() in src/utils/date.ts — replaced by formatDate()
- OldTaskCard component in src/components/ — replaced by TaskCard
- LEGACY_API_URL constant in src/config.ts — no remaining references
→ Safe to remove these?
```

## Speed, Disagreement, Honesty

Reviews shouldn't stall teams; the wait usually costs more than the context switch. Respond within one business day at most, aim for multiple rounds in a day, favor fast replies over fast approval, and ask authors to split oversized changes. Resolve disputes by hierarchy: facts and data first, style guides as authority on style, design judged on engineering principles rather than taste, and codebase consistency acceptable only when it doesn't degrade health. Don't bank on "I'll clean it up later" — require cleanup before submission, or a self-assigned bug when it can't fit this change.

Review honestly: reject rubber-stamp "LGTM"s, don't soften production-bound bugs, quantify impact when possible ("adds ~50ms per item" beats "might be slow"), push back on flawed approaches while proposing alternatives, defer gracefully when the author has fuller context, and critique the code, never the person.

## Dependencies

Every dependency is a liability. Before adding one: does the existing stack suffice, what's the bundle cost, is it maintained, does `npm audit` flag it, and is the license compatible? Prefer the standard library and existing utilities.

Upgrades get the same scrutiny — bulk "bump deps" changes are the worst offenders. Read the changelog rather than trusting semver, isolate one dependency per change so breakage is attributable and revertible, let the suite prove before and after (adding a test first where coverage is thin), review the lockfile diff because transitive changes dominate, and commit the lockfile without hand-editing it. Use `security-and-hardening` for audit triage and supply-chain verdicts; this workflow covers the upgrade mechanics.

## Checklist

```
## Review: [PR/Change title]

### Context
- [ ] I understand what this change does and why

### Correctness
- [ ] Change matches spec/task requirements
- [ ] Edge cases handled
- [ ] Error paths handled
- [ ] Tests cover the change adequately

### Readability
- [ ] Names are clear and consistent
- [ ] Logic is straightforward
- [ ] No unnecessary complexity

### Architecture
- [ ] Follows existing patterns
- [ ] No unnecessary coupling or dependencies
- [ ] Appropriate abstraction level
- [ ] Refactors reduce complexity rather than relocate it
- [ ] No feature logic in shared modules; file stays within a healthy size

### Security
- [ ] No secrets in code
- [ ] Input validated at boundaries
- [ ] No injection vulnerabilities
- [ ] Auth checks in place
- [ ] External data sources treated as untrusted

### Performance
- [ ] No N+1 patterns
- [ ] No unbounded operations
- [ ] Pagination on list endpoints

### Verification
- [ ] Tests pass
- [ ] Build succeeds
- [ ] Manual verification done (if applicable)

### Verdict
- [ ] **Approve** — Ready to merge
- [ ] **Request changes** — Issues must be addressed
```

Detailed references: `../../references/security-checklist.md`, `../../references/performance-checklist.md`.

## Common Rationalizations

| Claim | Counter |
|-------|---------|
| "It works, that's good enough" | Unreadable or insecure working code compounds debt. |
| "I wrote it, so it's correct" | Authors miss their own assumptions; every change benefits from fresh eyes. |
| "We'll clean it up later" | Later rarely arrives; the review is the gate — require cleanup now. |
| "AI-generated code is probably fine" | It needs more scrutiny, not less — confident and plausible even when wrong. |
| "The tests pass, so it's good" | Necessary but insufficient; tests miss architecture, security, and readability problems. |
| "The refactor makes it cleaner" | Relocation isn't reduction; fewer concepts held by the reader is the real test. |
| "It's a small addition to this file" | Small diffs still grow files and bolt branches onto unrelated flows; judge the result. |
| "It's just a version bump" | It's a behavior change you didn't write; read the changelog. |
| "I'll upgrade everything in one PR" | Bulk bumps hide the culprit; isolation keeps cause and revert clean. |

## Red Flags

- Merged PRs with no review, or reviews that only check whether tests pass
- "LGTM" without evidence; security-sensitive changes without security-focused review
- Oversized PRs that resist proper review (split them)
- Bug fixes shipped without regression tests
- Comments lacking severity labels; accepted "fix it later" promises
- Refactors that relocate rather than reduce concepts; files grown without decomposition
- Conditionals scattered into unrelated paths; near-duplicate helpers; feature logic in shared modules
- Bulk dependency bumps with no changelog review; hand-edited, uncommitted, or unreviewed lockfiles

## Verification

- [ ] All Critical findings resolved
- [ ] Every Required (no-prefix) finding resolved or explicitly deferred with justification
- [ ] Tests pass and the build succeeds
- [ ] The verification story is documented (what changed, how it was checked)
- [ ] Dependency upgrades reviewed against their changelogs, isolated per package, verified by green suites, with lockfile diffs inspected

**Presumptive blockers** — surface each and propose the simpler design, escalating to Required only when the change actively makes structure worse: refactors that relocate complexity instead of reducing it; changes that push a file past the size boundary without decomposition; feature logic added to shared modules; near-duplicates of existing canonical helpers; and silent fallbacks masking unclear invariants.

## Related Skills in This Repo

- [ci-cd-and-automation](../ci-cd-and-automation/SKILL.md) — Use when setting up or modifying build and deployment pipelines; you need to automate qual...
- [api-and-interface-design](../api-and-interface-design/SKILL.md) — Use when designing APIs, module boundaries, or any public interface; creating REST or Grap...
- [git-workflow-and-versioning](../git-workflow-and-versioning/SKILL.md) — Use when making any code change; committing, branching, resolving conflicts, splitting unc...
- [context-engineering](../context-engineering/SKILL.md) — Use when starting a new session, when agent output quality degrades, when switching betwee...
- [requesting-code-review](../requesting-code-review/SKILL.md) — Pre-commit review: security scan, quality gates, auto-fix.
- [receiving-code-review](../receiving-code-review/SKILL.md) — Use when receiving and integrating feedback from code reviews
- [github-code-review](../github-code-review/SKILL.md) — Review PRs: diffs, inline comments via gh or REST.

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Upstream anti-patterns retained as the When-NOT-to-Use list.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- Path: `_sources/addyosmani_agent-skills/skills/code-review-and-quality/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
