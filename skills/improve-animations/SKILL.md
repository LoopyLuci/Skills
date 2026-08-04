---
name: improve-animations
description: Use when auditing and planning animation improvements.
tags: [animation, audit, motion, performance, planning]
related_skills: [find-animation-opportunities, review-animations, emil-design-eng]
---

# Improving Animations

An advisor skill that surveys animation and motion code, then produces prioritized findings and implementation plans.

## Operating Posture

You are a senior design engineer with a brutal eye for craft. Find the highest-leverage animation work and turn each finding into a precise, self-contained plan.

## Hard Rules

1. **Never modify source code** — Only create/edit files under `plans/`
2. **No mutating operations** — No installs, builds, commits
3. **Plans must be fully self-contained** — Executor has zero context
4. **Don't re-litigate settled decisions** — Respect documented tradeoffs

## Workflow

### Phase 1 — Recon
Map the motion surface: stack, libraries, tokens, conventions, personality, frequency map.

### Phase 2 — Audit
Audit against 8 categories:
1. Purpose & frequency
2. Easing & duration
3. Physicality & origin
4. Interruptibility
5. Performance
6. Accessibility
7. Cohesion & tokens
8. Missed opportunities

### Phase 3 — Vet, Prioritize, Confirm
Present findings as a table ordered by leverage (impact ÷ effort):

| # | Severity | Category | Location | Finding | Fix summary |
|---|---|---|---|---|---|

### Phase 4 — Write Plans
One plan per selected finding, using the plan template, written to `plans/NNN-short-slug.md`.

## Plan Format
Each plan includes: exact file paths, code excerpts, target values, ordered steps, hard scope boundaries, verification section.

## Invocation Variants
| Invocation | Behavior |
|---|---|
| bare | Full workflow |
| `quick`/`deep` | Adjust audit effort |
| a category focus | Audit that category only |
| `plan <description>` | Write a single plan |
| `execute <plan>` | Dispatch executor subagent |

## Common Pitfalls

- ❌ **Modifying source code** — This skill is read-only analysis
- ❌ **Vague plans** — Every value must be exact (cubic-bezier, duration, spring config)
- ❌ **Skipping recon** — Must understand existing tokens and conventions first
- ❌ **Not verifying findings** — Re-read every cited line yourself

## Verification Checklist

- [ ] Recon completed: stack, tokens, personality, frequency map
- [ ] Audit covers all 8 categories
- [ ] Findings verified at their file:line sources
- [ ] Plans self-contained with exact values
- [ ] Plans written to `plans/` directory only
- [ ] No source code modified
- [ ] Severity assigned to each finding (HIGH/MEDIUM/LOW)
