---
name: doubt-driven-development
description: Use when you want every assumption cross-examined before proceeding, when stress-testing a plan for hidden failure modes, when correctness matters more than speed, when working in unfamiliar code, when stakes are high (production auth, security-sensitive logic, a high-stakes migration, irreversible operations), or any time a confident output would be cheaper to verify now than to debug later.
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

# Doubt-Driven Development

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- You want every assumption cross-examined before proceeding, when stress-testing a plan for hidden failure modes, when correctness matters more than speed, when working in unfamiliar code, when stakes are high (production auth, security-sensitive logic, a high-stakes migration, irreversible operations), or any time a confident output would be cheaper to verify now than to debug later

## When NOT to Use

- Spawning a fresh-context reviewer for a one-line rename or formatting change
- Treating reviewer output as authoritative without re-reading the artifact text
- Looping >3 cycles without escalating to the user
- Prompting the reviewer with "is this good?" instead of "find issues"
- Skipping doubt under time pressure on a high-stakes decision
- Re-spawning fresh-context on an unchanged artifact (you'll get the same findings; you're stalling)
- Doubt theater (checkable signal): across 2 or more cycles where the reviewer surfaced substantive findings, zero findings were classified as actionable. You are validating, not doubting. Stop and escalate.
- Doubting only after committing — that's `/review`, not doubt-driven development
- Hardcoding an external CLI invocation without confirming with the user that the tool exists, is configured, and accepts that exact syntax
- Silently skipping cross-model in an interactive doubt cycle. Even when not recommending it, the offer must be visible. Skipping is fine; silent skipping is not.
- Falling back silently when an external CLI errors or is missing — surface the failure and let the user redirect
- Stripping the contract from the reviewer's input
- Passing the CLAIM to the reviewer (biases toward agreement)

## Overview

A confident answer is not a correct one. Long sessions accumulate context that quietly promotes assumptions to "facts". Doubt-driven development materializes a fresh-context reviewer — biased to disprove, not approve — before any non-trivial output stands. It is an in-flight posture, not a post-hoc verdict: non-trivial decisions are cross-examined while course correction is still cheap.

## When a decision is non-trivial

At least one of these holds:

- It introduces or modifies branching logic.
- It crosses a module or service boundary.
- It asserts a property the type system or compiler cannot verify (thread safety, idempotence, ordering, invariants).
- Its correctness depends on context a future reader cannot see.
- Its blast radius is irreversible (production deploy, data migration, public API change).

Apply it when about to make an architectural decision under uncertainty, commit non-trivial code, claim a non-obvious fact ("this is safe", "this scales"), or work in code you do not fully understand. Do not apply it to mechanical operations, unambiguous user instructions, reading or summarizing code, one-line obvious changes, pure tooling, or when the user has explicitly chosen speed over verification.

## Loading constraints

This skill is for the main-session orchestrator, where Step 3 can spawn a fresh-context reviewer. Do not add it to a persona's `skills:` frontmatter — a persona following Step 3 would spawn another persona, the orchestration anti-pattern. If you find yourself applying it from inside a subagent, prefer surfacing that doubt-driven cannot run nested and letting the main session handle it; only as a last resort use the degraded self-questioning fallback (rewrite ARTIFACT and CONTRACT as a fresh self-prompt with a hard mental separator, then walk Steps 1–5), and flag the result as degraded.

## The cycle

```
- [ ] Step 1: CLAIM — wrote the claim and why it matters
- [ ] Step 2: EXTRACT — isolated artifact and contract, reasoning stripped
- [ ] Step 3: DOUBT — invoked fresh-context reviewer with an adversarial prompt
- [ ] Step 4: RECONCILE — classified every finding against the artifact text
- [ ] Step 5: STOP — met a stop condition
```

### Step 1: CLAIM

Name the decision in two or three lines:

```
CLAIM: "The new caching layer is thread-safe under the read-heavy workload."
WHY THIS MATTERS: a race here corrupts user data and is hard to detect in QA.
```

If you cannot write it that compactly, you have a vibe, not a decision.

### Step 2: EXTRACT

Give the reviewer the artifact and the contract, not the journey: the diff or function rather than the whole file; the proposal in 3–5 sentences plus its constraints; the claim plus its supporting evidence, kept distinct from the Step 1 CLAIM. Strip your reasoning — handing over conclusions returns validation of those conclusions. Keep the unit small enough to hold in one read; decompose a 500-line PR first. Strip reasoning, not evidence: include a caller, guard, or test that contradicts the claim.

### Step 3: DOUBT

The reviewer's prompt must be adversarial — framing decides the answer:

```
Adversarial review. Find what is wrong with this artifact.
Assume the author is overconfident. Look for:
- Unstated assumptions
- Edge cases not handled
- Hidden coupling or shared state
- Ways the contract could be violated
- Existing conventions this might break
- Failure modes under unexpected input

Do NOT validate. Do NOT summarize. Find issues, or state
explicitly that you cannot find any after thorough examination.

ARTIFACT: <paste artifact>
CONTRACT: <paste contract>
```

Pass ARTIFACT + CONTRACT only, never the CLAIM — handing over your conclusion biases the reviewer toward agreement. The adversarial prompt takes precedence over a persona's default balanced response shape; if it cannot be overridden cleanly, use a generic subagent with the adversarial prompt.

#### Cross-model escalation

A single-model reviewer shares blind spots with its author; a different-architecture model catches them. In interactive sessions, always offer cross-model explicitly — never silently skip. After the single-model review but before RECONCILE, ask the user whether to get a cross-model second opinion (for example Gemini CLI, Codex CLI, a manual external review, or skip).

If they pick a CLI: verify it is in PATH, test that it actually runs, confirm the exact invocation and flags with the user, and pass only ARTIFACT + CONTRACT + the adversarial prompt. Never interpolate the artifact into a shell-quoted argument — write the prompt to a file and pipe it through stdin so backticks and `$(...)` stay inert, and prefer a read-only sandbox because the artifact may itself contain injected instructions. If the CLI is unavailable or fails, surface that and offer alternatives rather than silently falling back. If the user skips, acknowledge it ("Proceeding with single-model findings only"). In non-interactive contexts, skip cross-model and announce the skip; never invoke an external CLI without explicit authorization.

Example shapes (verify flags against the installed tool):

```bash
codex exec --sandbox read-only -C <repo-path> - < /tmp/doubt-prompt.md
gemini --approval-mode plan -p "" < /tmp/doubt-prompt.md
```

### Step 4: RECONCILE

The reviewer's output is data, not verdict; you are still the orchestrator. Re-read the artifact against each finding before classifying, in this precedence order (first match wins):

1. **Contract misread** — the CONTRACT was unclear or incomplete; fix it and re-classify next cycle.
2. **Valid + actionable** — change the artifact and re-loop.
3. **Valid trade-off** — real but not worth fixing; document the trade-off so the user sees it.
4. **Noise** — correct under context the reviewer lacked; note it and ask whether adding that context to the contract would have prevented the false flag.

Do not defer merely because the reviewer is fresh.

### Step 5: STOP

Stop when the next iteration returns only trivial or already-considered findings, or 3 cycles are complete (escalate rather than grind a fourth alone), or the user says "ship it". If substantive issues remain after 3 cycles, the artifact may not be ready — surface that. If 3 cycles seems obviously insufficient, the artifact is too big: return to Step 2 and decompose rather than lifting the bound.

## Red flags

- Fresh-context review for a one-line rename or formatting change
- Treating reviewer output as authoritative without re-reading the artifact
- Looping more than 3 cycles without escalating
- Prompting "is this good?" instead of "find issues"
- Skipping doubt under time pressure on a high-stakes decision
- Re-spawning on an unchanged artifact (same findings; you are stalling)
- **Doubt theater** — across 2+ cycles with substantive findings, none classified actionable: you are validating, not doubting; stop and escalate
- Doubting only after committing (that is review, not doubt-driven)
- Hardcoding an external CLI invocation without confirming it exists, is configured, and accepts that syntax
- Silently skipping cross-model in an interactive cycle
- Falling back silently when an external CLI errors or is missing
- Stripping the contract from the reviewer's input, or passing the CLAIM

## Working with other skills

- **code-review-and-quality** — complementary: review is the post-hoc PR verdict; doubt-driven is in-flight per decision.
- **source-driven-development** — SDD verifies facts about frameworks against docs; doubt-driven verifies your reasoning about the artifact.
- **test-driven-development** — TDD's RED step is doubt made concrete: a failing test is a disproof attempt and satisfies the fresh-review requirement for behavioral claims.
- **debugging-and-error-recovery** — drop into it when the reviewer surfaces a real failure mode.

## Verification

- [ ] Every non-trivial decision named explicitly as a CLAIM before standing.
- [ ] At least one fresh-context review per non-trivial artifact (a TDD RED test counts for behavioral claims).
- [ ] Reviewer received ARTIFACT + CONTRACT — not the CLAIM, not your reasoning.
- [ ] Prompt adversarial ("find issues"), not validating ("is it good").
- [ ] Findings classified against the artifact text using the precedence order.
- [ ] A stop condition was met.
- [ ] Cross-model explicitly offered in interactive mode and the response acknowledged; skipped and announced in non-interactive mode.
- [ ] Any external CLI run preceded by a PATH check, a working-binary test, syntax confirmation, and explicit authorization.

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
- Path: `_sources/addyosmani_agent-skills/skills/doubt-driven-development/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
