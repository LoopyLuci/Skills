---
name: writing-for-agents
description: Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [software-development, engineering, productivity]
    source: mattpocock/skills
    adapted: true
---

# Writing For Agents

> **Adapted for the LoopyLuci Skills collection** from [mattpocock/skills](https://github.com/mattpocock/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Creating or editing skills, or modifying AGENTS.md or CLAUDE.md

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

How to write any document an agent consumes — a skill, an `AGENTS.md`/`CLAUDE.md`, or a doc reached by a pointer. Packaging differs; the writing does not, because the agent runs the same *process* every time rather than producing the same output. For skills specifically, also read `SKILL-MECHANICS.md` for frontmatter, invocation choice, and router skills.

## Context pointers

A **context pointer** is a reference held in context that names out-of-context material and encodes the condition for reaching it. A skill's description is one; a line in `AGENTS.md` naming a doc is the same object. The pointer's *wording*, not its target, decides how reliably the agent reaches the material. A must-have target behind a weakly worded pointer is a variance bug — sharpen the wording first, and inline the material only if sharpening fails.

A pointer does two jobs: state what the material is, and list the **branches** that should trigger reaching it (a branch is a distinct case the document handles). Every word of an always-loaded pointer costs on every turn, so prune it harder than the body:

- **Front-load the leading word** — that is where the triggering work happens.
- **One trigger per branch** — synonyms that rename one branch are one branch written twice; collapse them.
- **Cut identity the body already carries.**

## The two loads

- **Context load** — the cost of always-loaded material on the agent's window: an `AGENTS.md` line, a skill description, anything present every turn, spending tokens and attention whether or not it fires.
- **Cognitive load** — the cost on the human of knowing which documents exist and when to reach for each. The human is the index. This is not a cost to minimise: it is the price of human agency. Spend it where human judgement matters, remove it where it does not.

Material reached only through a pointer escapes context load at the price of the pointer's line; material with no pointer rides entirely on cognitive load.

## Information hierarchy

Documents contain **steps** (ordered actions the agent performs) and **reference** (definitions, rules, facts consulted on demand). The two mix freely. The core decision is where each piece sits on the hierarchy, ranked by how immediately the agent needs it:

1. **In-file step** — what the agent does, in order.
2. **In-file reference** — consulted on demand; often a legitimate flat peer-set (every rule of a review on one rung), which is fine, not a smell.
3. **Disclosed reference** — pushed into a separate file, reached by a context pointer, loaded only when it fires. Ranges from a sibling file to fully external reference anywhere.

Push too little down and the top bloats; push too much and you hide material the agent needs. That tension is the whole decision.

**Progressive disclosure** is the move down the ladder so the top stays legible. It is not mainly a token optimisation — it protects the hierarchy. Branching is the cleanest test: inline what every branch needs, push behind a pointer what only some branches reach. When a document has steps, in-file reference that should be disclosed buries them and makes attending to them a coin flip — a variance lever, not just a legibility one.

**Co-location** is the within-file companion: the ladder decides *how far down* a piece sits, co-location decides *what sits beside it*. Keep a concept's definition, rules, and caveats under one heading so reading one part brings its neighbours. The test: the document should read like documentation written for the agent. Grouped material does; scattered material does not. (Different from duplication, which repeats one meaning in two places; scattering fragments one meaning across many.)

**Sprawl** is the failure mode: a document too long even when every line is live and unique. Attention thins, and every extra line is one more to keep relevant. The cure is the ladder — disclose reference behind pointers and split by branch or sequence.

## Steps and completion criteria

Every step ends on a **completion criterion**: the condition that tells the agent the work is done. Two properties make it a lever:

- **Clarity** — can the agent tell done from not-done? A vague bound ("understanding reached") invites **premature completion**: ending the step early, attention sliding to *being done*. The visible **post-completion steps** supply the pull; the criterion's clarity is the resistance. Defend in order: sharpen the bound first (local and cheap); only if it stays irreducibly fuzzy *and* you observe the rush, hide the later steps by splitting the sequence. Hiding works only across a real context boundary (a hand-off or subagent dispatch); an inline call leaves later steps in context and clears nothing.
- **Demand** — how much it requires. "Every modified model accounted for" forces thoroughness where "produce a change list" does not. Demand drives **legwork** (the digging latent in the wording, not written as its own step) and is not step-bound: "every rule applied" binds a flat reference body just as "every step done" binds a sequence, which is how an all-reference document still carries an exhaustiveness bar.

The strongest criteria are both checkable and exhaustive.

## When to split

Splitting one document into two spends one of the two loads, so split only when the cut earns it:

- **By sequence** — split a run of steps where the post-completion steps tempt the agent to rush the one in front of it. Keeping them out of view drives more legwork. Beware the reverse: merging sequences exposes each step's later steps to what follows, inviting premature completion.
- **By invocation** (skill-specific) — see `SKILL-MECHANICS.md`.

## Leading words

A **leading word** is a compact concept already living in the model's pretraining that the agent thinks with while running the document (*lesson*, *fog of war*, *tracer bullets*). Repeated as a token, never as a sentence, it accumulates a distributed definition and anchors a region of behaviour in few tokens by recruiting priors the model already holds. Coining your own works only if you define it clearly; a made-up word recruits no priors, so you pay in definition tokens what a pretrained word gives free. Reach for an existing word first.

It anchors twice. In the body (*execution*), the agent reaches for the same behaviour every time the word appears, and inside flat reference it focuses attention on a class of thing to look for. In a pointer (*invocation*), when the same word lives in your prompts, docs, and codebase, the agent links that shared language to the material and reaches it more reliably.

Hunt for refactors that leading words enable — a triad spelled out at three sites, a pointer spending a sentence to gesture at one idea:

- "fast, deterministic, low-overhead" → *tight* (a *tight* loop).
- "a loop you believe in" → *red*, turning a fuzzy gate into a binary observable state.

You win twice: fewer tokens and a sharper hook. Assume every document carries restatements that leading words retire.

**Negation** is the failure mode beside this lever: steering by prohibition drags the forbidden behaviour into context and makes it *more* available. "Don't think of an elephant" and the elephant is all there is — the negation is a weak modifier the strongly-activated concept overruns, so the ban half-reads as an instruction to do the thing. Prompt the **positive** instead ("write one-line comments") so the banned behaviour is never spoken. A prohibition earns its place only as a hard guardrail you cannot phrase positively, and even then pair it with the positive target.

## Pruning

- Keep each meaning in a **single source of truth** so changing behaviour is a one-place edit. **Duplication** costs maintenance and tokens and inflates a meaning's prominence past its real rank. (The accidental inverse of a leading word, which repeats a token on purpose, never the meaning.)
- The **environment** is a source of truth too (`package.json` scripts, config files, directory layout, `--help` output); a document that restates it is a **cache**, earning its load only when the lookup is expensive. Cache what the agent cannot find by looking — the unwritten convention, the reason behind a choice, the gotcha no config confesses. Leave one-file, one-command lookups to the environment, where they cannot go stale.
- Check every line for **relevance**: does it still bear on what the document does? A line loses relevance by never bearing on the task (mere exposition, or a branch that should be disclosed) or by going stale. Shorter documents are easier to keep relevant. Without pruning, the default fate is **sediment** — stale layers that settle because adding feels safe and removing feels risky.
- Hunt **no-ops** sentence by sentence: an instruction the model already obeys by default pays load to say nothing. The test — does it change behaviour versus the default? — is model-relative, not reader-relative: two people disagreeing about a no-op disagree about the default, and settle it by running the document, not by debate. When a sentence fails, delete the whole sentence rather than trim it. The test also grades leading words: a word too weak to beat the default ("be thorough" when the agent is already thorough-ish) is a no-op, and the fix is a stronger word ("relentless"), not a different technique.

## Verification

- [ ] Every pointer states what the material is and lists its branches, with the leading word up front.
- [ ] Steps end on checkable, exhaustive completion criteria.
- [ ] Reference that only some branches need sits behind a pointer.
- [ ] No duplication, no sediment, no no-ops.
- [ ] Prohibitions paired with a positive target.

## Related Skills in This Repo

- [pr](../pr/SKILL.md) — Use when writing a PR body.
- [software-factory](../software-factory/SKILL.md) — Use when working with shared language for designing a software factory: the tasks it runs ...
- [chief-of-staff](../chief-of-staff/SKILL.md) — Use when working with pursue a long-running goal in a single session by co-ordinating suba...
- [retro](../retro/SKILL.md) — Use when conducting a retrospective on a coding session.

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [mattpocock/skills](https://github.com/mattpocock/skills)
- Path: `_sources/mattpocock_skills/skills/productivity/writing-for-agents/SKILL.md`
- License: MIT — Copyright (c) 2026 Matt Pocock
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
