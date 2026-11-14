---
name: interview-me
description: Use when an ask is underspecified ("build me X" without "for whom" or "why now"), when the user explicitly invokes ("interview me", "grill me", "are we sure?", "stress-test my thinking"), or when you catch yourself silently filling in ambiguous requirements before any plan, spec, or code exists.
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

# Interview Me

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- An ask is underspecified ("build me X" without "for whom" or "why now"), when the user explicitly invokes ("interview me", "grill me", "are we sure?", "stress-test my thinking"), or when you catch yourself silently filling in ambiguous requirements before any plan, spec, or code exists

## When NOT to Use

- Three or more questions in a single message: that's batching, not interviewing
- A question without your hypothesis attached: that's surveying, not committing
- Accepting "whatever you think is best" as a terminal answer
- Producing a spec, plan, or task list before the user has explicitly confirmed your restate
- Invoking tools or starting downstream work immediately upon intent confirmation instead of stopping the turn
- Questions framed as "what would be best practice?" instead of "what do you actually want?"
- The user gives a sophistication-signaling answer ("scalable", "clean", "modern") and you accept it without probing whether it's what they actually want
- Three or more rounds without your confidence visibly rising: you're asking the wrong questions, step back and reframe
- A confidence number below ~70% with no reason attached: the user can't help close the gap if they don't know what's missing
- Saving the intent doc before the user has confirmed (the doc itself implies a yes the user didn't give)
- Skipping the "Out of scope" line in the restate (silent disagreement about non-goals is half of misalignment)

## Overview

People rarely ask for what they actually want — they ask for the conventional artifact ("a dashboard," "make it faster") without the specifics that determine success. This skill closes that gap before any plan, spec, or code exists, because once building begins, switching costs rise and users rationalize the wrong thing into "good enough." It replaces silent assumption-filling with a one-question-at-a-time interview, each question carrying an explicit guess, until you can predict the user's reactions.

## Loading Constraint

A live, responsive user is required. Don't run this in CI pipelines, scheduled runs, `/loop`, or autonomous-loop contexts; if the ask is underspecified there, flag it as a blocker for the user instead of guessing.

## Step 1: State a Hypothesis With a Confidence Number

Before asking anything, write your best one-sentence read of what the user wants plus an honest confidence percentage:

```
HYPOTHESIS: You want a way to answer "how are we doing?" in standup, and "dashboard" was the convention that came to mind.
CONFIDENCE: ~30% — missing: who it's for, what "metrics" means in context, and what success looks like
```

The number forces honesty: if you can't predict the user's answers to your next three questions, the number is too high. Below ~70%, append a one-line reason naming what is still unresolved — this tells the user exactly what the interview must surface.

## Step 2: Ask One Question at a Time, Guess Attached

```
Q: <one focused question>
GUESS: <your hypothesis for the answer, with the reasoning that produced it>
```

Wait for the reaction before the next question. One at a time because the user can't react to hypotheses buried in a list, batches invite skim-reading, later questions often depend on earlier answers, and careful-thinking energy is finite. Attach a guess because people react to a wrong guess faster than they generate answers from scratch, it exposes your assumptions (the point of the exercise), and it keeps you visibly committed to a falsifiable position. Guard against polite agreement by being openly willing to be wrong, and occasionally guess in a direction you expect the user to push back on.

## Step 3: Detect "Want vs. Should Want"

The dangerous answers sound thoughtful rather than true. Watch for best-practice talk without specifics ("scalable," "clean architecture"), deference to convention ("the way most apps do it"), hedges ("I should probably…", "good engineering practice says…"), and buzzwords standing in for outcomes ("modern," "robust"). When you hear them, ask:

> *"If you didn't have to justify this to anyone, what would you actually want?"*

That single question often outperforms the previous five combined.

## Step 4: Restate Intent in the User's Own Words

At high confidence, write back your read — tight (5–8 lines), in their language, structured so the user can confirm or correct line by line:

```
Here's what I now think you want:

- Outcome:      <one line>
- User:         <one line — who benefits>
- Why now:      <one line — what changed>
- Success:      <one line — how we know it worked>
- Constraint:   <one line — the binding limit>
- Out of scope: <one line — what we're explicitly not doing>

Yes / no / refine?
```

"Out of scope" is mandatory — half of misalignment is silent disagreement about what is *not* being built.

## Step 5: Require an Explicit Yes

The gate is a clear "yes." Not yes: "Whatever you think is best" (delegation, not decision — re-ask with two concrete options), "Sounds good" (ambiguous — ask "Anything you'd refine?"), "Sure, let's go" (often a polite exit — same follow-up), or silence followed by "okay let's start" (the user gave up on the interview, not converged — stop and ask what you missed). Fold corrections in and restate until the yes is explicit.

## Step 6: End the Turn Immediately

On explicit confirmation:

1. Deliver the confirmed Statement of Intent.
2. Offer downstream paths — save it to `docs/intent/[topic].md`, draft a spec with `spec-driven-development`, or move to task planning after the spec.
3. **Stop the turn.** Invoke no tools and begin no downstream work; hand control back so the user chooses the next step.

## The 95% Stop Rule

You're done when you can answer yes to: *can I predict the user's reaction to the next three questions I would ask?* If yes, shared understanding exists — stop interviewing and produce the restate. If no, keep going. There's a floor: after several rounds without that predictive power, the gap is in the ask itself, not your questions. Say so — "I've asked X questions and I still can't predict your reactions. Something foundational is missing. Want to step back?" — instead of grinding.

## Output and Downstream Skills

The deliverable is the confirmed Statement of Intent; specs, plans, and task lists consume it downstream. Offer to persist it to `docs/intent/[topic].md` for multi-session projects or handoffs, but only after explicit confirmation.

Handoffs: `idea-refine` when the confirmed intent still needs scoping variations; `spec-driven-development` when it is concrete enough to write down; `planning-and-task-breakdown` sits two hops downstream (after the spec); `doubt-driven-development` occupies the opposite end of the timeline — post-decision artifact review versus this pre-decision extraction; `source-driven-development` is orthogonal (clarifying wants versus verifying framework facts).

## Red Flags

- Three or more questions in a single message — batching, not interviewing
- Questions without an attached hypothesis — surveying, not committing
- Accepting "whatever you think" as a terminal answer
- Producing a spec, plan, or task list before the user confirms your restate
- Invoking tools or starting downstream work right after confirmation instead of ending the turn
- Framing questions as "what's best practice?" instead of "what do you actually want?"
- Accepting sophistication-signaling answers without probing
- Three or more rounds with no visible confidence gain — reframe instead of repeating
- Confidence below ~70% with no reason attached — the user can't close a gap they can't see
- Saving the intent doc before confirmation, or omitting the "Out of scope" line

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The ask is clear enough" | If you can't state the desired outcome in one sentence right now, run Step 1 |
| "Asking too many questions wastes time" | Four to six targeted questions cost little; building the wrong thing costs the user dearly |
| "I'll figure it out as I build" | Switching costs after code exists are roughly 10x; discovery during implementation is rework |
| "'Whatever you think' means decide" | It's delegation; re-ask with two concrete options |
| "I should give them options to pick from" | Options suit users choosing between trade-offs, not users who don't know what they want; asking narrows, listing widens |
| "Attaching a guess leads them" | Leading is the point; the risk is sycophancy, mitigated by being visibly wrong sometimes |
| "We've talked enough, I get it" | Test it: predict their reaction to the next three questions |
| "The user said yes, we're done" | A yes after a vague restate or an open "sounds good" is hollow — restate concretely and re-confirm |

## Verification

- [ ] First turn stated an explicit hypothesis with a confidence number
- [ ] Every confidence number below ~70% carried a one-line reason naming what's still missing
- [ ] Questions went one at a time, each with the agent's guess attached
- [ ] At least one "what would you actually want if you didn't have to justify it?" probe ran after a sophistication- or convention-signaling answer
- [ ] Restate covered Outcome / User / Why now / Success / Constraint / Out of scope
- [ ] User confirmed with an explicit yes (not delegation, ambiguity, or silence)
- [ ] At the stop point, reactions to the next three questions were predictable
- [ ] The turn ended immediately on confirmation, with no tools or downstream work
- [ ] Any downstream handoff was framed around the confirmed intent, not the original underspecified ask

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
- Path: `_sources/addyosmani_agent-skills/skills/interview-me/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
