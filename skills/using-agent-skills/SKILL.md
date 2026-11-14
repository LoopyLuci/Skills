---
name: using-agent-skills
description: Use when starting a session, or when you need to decide which skill or workflow applies to the piece of work at hand.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [software-development, engineering, agent-skills, skills, meta]
    source: addyosmani/agent-skills
    adapted: true
---

# Using Agent Skills

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Starting a session, or when you need to decide which skill or workflow applies to the piece of work at hand

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

How to discover and invoke agent skills, and which workflow applies to the work at hand. Skills encode the processes senior engineers follow, organized by development phase.

## Choosing a skill

Map the task to a phase, then apply the matching skill:

```
Task arrives
    ├── Don't know what you want yet? ──────→ interview-me
    ├── Have a rough concept, need variants? → idea-refine
    ├── New project/feature/change? ──→ spec-driven-development
    ├── No quality bar written down? ──→ constraint-driven-development
    ├── Have a spec, need tasks? ──────→ planning-and-task-breakdown
    ├── Implementing code? ────────────→ incremental-implementation
    │   ├── UI work? ─────────────────→ frontend-ui-engineering
    │   ├── API work? ────────────────→ api-and-interface-design
    │   ├── Need better context? ─────→ context-engineering
    │   ├── Need doc-verified code? ───→ source-driven-development
    │   └── Stakes high / unfamiliar code? ──→ doubt-driven-development
    ├── Writing/running tests? ────────→ test-driven-development
    │   └── Browser-based? ───────────→ browser-testing-with-devtools
    ├── Something broke? ──────────────→ debugging-and-error-recovery
    ├── Reviewing code? ───────────────→ code-review-and-quality
    │   ├── Too complex? ─────────────→ code-simplification
    │   ├── Security concerns? ───────→ security-and-hardening
    │   └── Performance concerns? ────→ performance-optimization
    ├── Committing/branching? ─────────→ git-workflow-and-versioning
    ├── CI/CD pipeline work? ──────────→ ci-cd-and-automation
    ├── Deprecating/migrating? ────────→ deprecation-and-migration
    ├── Writing docs/ADRs? ───────────→ documentation-and-adrs
    ├── Adding logs/metrics/alerts? ───→ observability-and-instrumentation
    └── Deploying/launching? ─────────→ shipping-and-launch
```

## Operating behaviors

These apply at all times, across all skills.

1. **Surface assumptions.** Before non-trivial work, state them explicitly ("ASSUMPTIONS I'M MAKING: … → Correct me now or I'll proceed with these."). Wrong unchecked assumptions are the most common failure mode; surfacing them early is cheaper than rework.
2. **Manage confusion actively.** On inconsistency or unclear specs: stop, name the specific confusion, present the tradeoff or ask the clarifying question, and wait. Bad: silently picking an interpretation. Good: "I see X in the spec but Y in the existing code — which takes precedence?"
3. **Push back when warranted.** You are not a yes-machine. Name the problem, quantify the downside ("adds ~200 ms latency", not "might be slower"), propose an alternative, and accept an informed override. Sycophancy is a failure mode.
4. **Enforce simplicity.** Before finishing, ask: fewer lines? Are these abstractions earning their complexity? Would a staff engineer say "why didn't you just…"? If 1,000 lines do what 100 would, that is failure. Prefer the boring, obvious solution; cleverness is expensive.
5. **Maintain scope discipline.** Touch only what you were asked to. Do not remove comments you do not understand, clean up orthogonal code, refactor adjacent systems as a side effect, delete apparently unused code without approval, or add "useful" features outside the spec. Surgical precision, not unsolicited renovation.
6. **Verify, don't assume.** A task is not complete until verification passes, and "seems right" is never evidence — there must be tests, build output, or runtime data. Per-skill verification is the local check; the project-wide bar for every change is the Definition of Done (tests pass, no regressions, behavior verified at runtime, docs updated), which complements rather than replaces task acceptance criteria.

## Failure modes to avoid

1. Wrong assumptions unchecked
2. Plowing ahead when lost
3. Not surfacing inconsistencies you notice
4. Not presenting tradeoffs on non-obvious decisions
5. Sycophancy toward approaches with clear problems
6. Overcomplicating code and APIs
7. Modifying code or comments orthogonal to the task
8. Removing things not fully understood
9. Building without a spec because "it's obvious"
10. Skipping verification because "it looks right"

## Skill rules

1. Check for an applicable skill before starting — skills exist to prevent common mistakes.
2. Skills are workflows, not suggestions: follow the steps in order, never skip verification.
3. Several skills can apply in sequence (for example `idea-refine` → `spec-driven-development` → `planning-and-task-breakdown` → `incremental-implementation` → `test-driven-development` → `code-review-and-quality` → `code-simplification` → `shipping-and-launch`).
4. When in doubt, start with a spec: non-trivial work without one begins with `spec-driven-development`.

## Lifecycle sequence

For a full feature, the typical order is:

```
 1. interview-me                      → what the user actually wants
 2. idea-refine                       → sharpen the vague idea
 3. spec-driven-development           → requirements and acceptance criteria
 4. planning-and-task-breakdown       → verifiable chunks
 5. context-engineering               → load the right context
 6. source-driven-development         → verify against official docs
 7. incremental-implementation        → build slice by slice
 8. observability-and-instrumentation → instrument as you build (parallel to 7–9)
 9. doubt-driven-development          → cross-examine non-trivial decisions in flight
10. test-driven-development           → prove each slice works
11. code-review-and-quality           → review before merge
12. code-simplification               → reduce complexity, preserve behavior
13. git-workflow-and-versioning       → clean commit history
14. documentation-and-adrs            → record decisions
15. deprecation-and-migration         → retire old systems safely
16. shipping-and-launch               → deploy safely
```

Not every task needs every skill; a bug fix may only need `debugging-and-error-recovery` → `test-driven-development` → `code-review-and-quality`.

## Quick reference

| Phase | Skill | Summary |
| --- | --- | --- |
| Define | interview-me | Surface what the user wants before any plan, spec, or code |
| Define | idea-refine | Divergent then convergent refinement of ideas |
| Define | spec-driven-development | Requirements and acceptance criteria before code |
| Plan | planning-and-task-breakdown | Decompose into small, verifiable tasks |
| Build | incremental-implementation | Thin vertical slices, each tested before expanding |
| Build | source-driven-development | Verify against official docs before implementing |
| Build | doubt-driven-development | Adversarial fresh-context review of non-trivial decisions |
| Build | context-engineering | Right context at the right time |
| Build | frontend-ui-engineering | Production-quality, accessible UI |
| Build | api-and-interface-design | Stable interfaces with clear contracts |
| Verify | test-driven-development | Failing test first, then make it pass |
| Verify | browser-testing-with-devtools | Chrome DevTools MCP for runtime verification |
| Verify | debugging-and-error-recovery | Reproduce → localize → fix → guard |
| Review | code-review-and-quality | Five-axis review with quality gates |
| Review | code-simplification | Preserve behavior while reducing complexity |
| Review | security-and-hardening | OWASP prevention, input validation, least privilege |
| Review | performance-optimization | Measure first, optimize only what matters |
| Ship | git-workflow-and-versioning | Atomic commits, clean history |
| Ship | ci-cd-and-automation | Automated quality gates on every change |
| Ship | deprecation-and-migration | Retire old systems and migrate users safely |
| Ship | documentation-and-adrs | Document the why, not just the what |
| Ship | observability-and-instrumentation | Structured logs, RED metrics, traces, symptom-based alerts |
| Ship | shipping-and-launch | Pre-launch checklist, monitoring, rollback plan |

## Verification

- [ ] The applicable skill was identified before work began.
- [ ] Assumptions surfaced and confusion resolved rather than guessed.
- [ ] Verification evidence produced, not assumed.
- [ ] Scope limited to the request.

## Related Skills in This Repo

- [code-review-and-quality](../code-review-and-quality/SKILL.md) — Use when reviewing code written by yourself, another agent, or a human; you need to assess...
- [ci-cd-and-automation](../ci-cd-and-automation/SKILL.md) — Use when setting up or modifying build and deployment pipelines; you need to automate qual...
- [api-and-interface-design](../api-and-interface-design/SKILL.md) — Use when designing APIs, module boundaries, or any public interface; creating REST or Grap...
- [git-workflow-and-versioning](../git-workflow-and-versioning/SKILL.md) — Use when making any code change; committing, branching, resolving conflicts, splitting unc...
- [writing-great-skills](../writing-great-skills/SKILL.md) — Reference for writing and editing skills well — the vocabulary and principles that make a ...
- [skill-inventory-management](../skill-inventory-management/SKILL.md) — Use when auditing, pruning, or consolidating skills.
- [skill-discovery](../skill-discovery/SKILL.md) — Use when discovering, designing, or developing skills.

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- Path: `_sources/addyosmani_agent-skills/skills/using-agent-skills/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
