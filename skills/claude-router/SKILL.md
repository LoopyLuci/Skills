---
name: claude-router
description: Claude Router and Orchestration. Picks the right model (Haiku, Sonnet or Opus) for every piece of delegated work by its complexity, and plans how multi-part work is split across subagents, separate sessions, worktrees and background tasks, then verified. Use this whenever you are about to spawn a subagent or Agent, start or propose another session, fan work out in parallel, hand off a task, choose a model for an API call or pipeline step, or the user asks to delegate, route, orchestrate, parallelize, "use the right model", save cost, or speed up a large task, even if they don't name a model.
version: 1.0.0
author: LoopyLuci
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [meta, agents, orchestration, routing, models]
---

# Claude Router and Orchestration

Two jobs: **route** each piece of work to the cheapest model that will do it well, and **orchestrate** the pieces so they run in the right place, in parallel where they can, and come back verified.

The reason to bother: a model one tier too big wastes money and time on every token; one tier too small wastes a whole attempt and the review that catches it. Routing well means matching the model to what the work actually demands, not to how important the task feels.

## 1. Route: pick the model

Judge the work by what it needs from the model, not by its size or the user's urgency.

| Tier | Use for | Signals |
|---|---|---|
| **Haiku** | Mechanical and read-only work | Searching or sweeping files, reading logs, listing or summarizing what exists, running a known command and reporting the result, renames and other edits with an exact recipe, formatting, extraction into a fixed shape, classification into given labels |
| **Sonnet** | Well-scoped implementation | A feature or fix with a clear spec and known files, dependency upgrades, writing tests for existing behaviour, refactors with a stated goal, docs from code, debugging with a reproduction in hand, most single-repository coding |
| **Opus** | Judgement across many parts | Architecture and design, plans other agents will follow, debugging with no reproduction or across systems, security-sensitive review, ambiguous requirements, work where a subtle mistake is expensive and hard to spot, synthesis of conflicting sources |

Tie-breakers:
- **Ambiguity beats size.** A huge but mechanical change is Haiku or Sonnet; a two-line fix whose cause is unknown is Opus.
- **Who checks the result?** If the output will be verified mechanically (tests, a build, a diff you will read), a cheaper tier is safer. If nobody will check it closely, go one tier up.
- **Escalate, don't guess high.** Starting a well-scoped task on Sonnet and escalating to Opus on a real failure costs less than starting everything on Opus. Escalate with the failure in the brief ("Sonnet tried X and hit Y"), never by re-sending the same brief.
- **Never route down on a correctness-critical step**: secrets, money, deletions, migrations, security review, anything outward-facing.
- **Name the model every time.** Delegated work otherwise inherits the current model, which is usually the most expensive one in the room.

Model ids change; use the ones the environment lists (the system prompt or the model picker) rather than ids from memory. See `references/environments.md` for how each environment takes a model.

## 2. Decide where each piece runs

Before splitting anything, ask whether it should be split at all. Delegation has a fixed cost: a cold start, a brief to write, and a result to check. Quick things (a question, a read, one edit, a handful of tool calls) stay inline.

| Shape of the piece | Where it goes |
|---|---|
| Needed to answer the user in this turn, and self-contained (search, review, a test run, a demo) | A **subagent**: its result comes back to you |
| A task of its own that outlives this turn and ends in something of its own (a branch, a PR, a change in another repository) | A **separate session**, in its own worktree if it writes code |
| Long-running command with nothing to decide meanwhile (a build, a test suite, a commit with slow hooks, a training run) | A **background task**; carry on with other work and react when notified |
| Depends on decisions made in this conversation and is short | **Inline**, or a fork that inherits the context |

Parallelism rules:
- Run pieces in parallel only when none needs another's result, none touches another's files, and none must land in the same change as another.
- **One writer per set of files.** Two agents editing the same files lose work silently. Give writers separate worktrees or separate folders.
- A final step that only checks the finished work (tests, a review) runs last, after the pieces are merged.

## 3. Write the brief

A delegated agent starts cold: it has none of this conversation. The brief is the whole of what it knows, so it must stand alone.

Every brief has:
1. **The task**, in your own words: what to build or find, not "based on the above".
2. **Where**: the files, folders, branch, repository and machine, by exact path.
3. **What done looks like**: the commands that must pass, the files that must exist, what to report back.
4. **Constraints learned the hard way**: hooks that take minutes (run commits in the background), lockfile checks, secret scanners that flag realistic fake values, drives that must not be used, anything the user insisted on.
5. **Context**: why the work matters and how it fits, for the session to make sensible calls on its own.

Keep secrets out of briefs. Point to where a secret lives (an environment variable, a credential store), never paste its value.

See `references/brief-template.md` for a fill-in template and a worked example.

## 4. Verify what comes back

A report is a claim, not proof. Before telling the user something is done:
- Read the diff or the files, run the tests, or check the branch, PR or artifact yourself.
- Check that it did what the brief asked, not a neighbouring task.
- Watch for silent failures: a background command that exited 0 while a hook blocked the commit; a push that "succeeded" for one branch and failed for another; a test skipped instead of passed.
- When a piece failed, re-route with what you learned (a tier up, a sharper brief, or do it inline), not the same brief again.

## 5. Report the routing

When you delegate, tell the user in one line per piece what went where and on which model, for example: "Edge Worker step 2 → its own session on Sonnet (well-scoped build); the skill design stays here (design work)". This lets them correct a routing call before it costs anything.

## Worked examples

**"Upgrade the site to SvelteKit 3 to clear the audit"** → a separate session on **Sonnet** in its own worktree: a well-scoped upgrade with a clear finish line (audit clean, build and tests pass). Its PR is its own deliverable.

**"Why did two runs of the same model score 52 and 47?"** → **inline on Opus**: no reproduction yet, needs judgement across the eval, retrieval and sampling. Comparing the two result files case by case is mechanical, so it can go to a **Haiku** subagent if the files are large.

**"Find every place we call the old client"** → a **Haiku** subagent: a read-only sweep whose result you need now.

**"Design the plugin architecture, then implement the three adapters"** → the design **inline on Opus**; then three **Sonnet** sessions in parallel, one per adapter, each in its own worktree, each brief carrying the design; a final test run after merging.

**"Commit this"** in a repository whose pre-commit hook takes eight minutes → a **background task** (no model choice needed); keep working and check its output when notified, because a blocked hook still exits 0 in some setups.
