---
name: constraint-driven-development
description: Use when no quality bar is written down, when the user says "set up constraints" or "define our standards", when the user wants dimensions they care about — accessibility, web performance, coverage — set up as enforced constraints, when an agent keeps silencing checks or skipping tests to get to green, when you need a coverage or performance threshold and don't know what number to pick, or when an agent writes more code than anyone will read.
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

# Constraint-Driven Development

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- No quality bar is written down, when the user says "set up constraints" or "define our standards", when the user wants dimensions they care about — accessibility, web performance, coverage — set up as enforced constraints, when an agent keeps silencing checks or skipping tests to get to green, when you need a coverage or performance threshold and don't know what number to pick, or when an agent writes more code than anyone will read

## When NOT to Use

- The interview ran past four questions, or produced a config the user can't explain
- A budget was set that the codebase fails today, with no plan to reach it
- A dimension was written into CONSTRAINTS.md with a number but no tool behind it
- A checker was hand-rolled when a de facto one exists, so the team's existing config is ignored
- Every constraint is checked by the project's own test suite, with no external opinion
- `CONSTRAINTS.md` changed in the same commit as the feature that was failing
- An exception has no owner, or an expiry more than a year out
- The agent proposed relaxing a threshold instead of fixing the code
- Slow checks landed in the edit loop and someone has started passing `--no-verify`
- Nobody has opened `CONSTRAINTS.md` since it was written

## Overview

Other skills describe what good looks like; this one writes **this project's** bar down with numbers, in `CONSTRAINTS.md`, so it outlives the session and can be checked mechanically. The reason it matters: when you wrote the code, reading it told you whether it was good, but an agent writes more in an afternoon than you will read that week, so judgement moves out of your head and into checks that run around the loop. Spec-driven development says what to build; test-driven development proves it works; constraint-driven development defines "good enough to ship" before anyone argues about it in a pull request.

## When to apply

- Starting a project or significant feature with no written quality bar.
- The user asks to set up constraints, add quality gates, define standards, or stop the agent shipping junk.
- An agent produces volume nobody reads line by line.
- CI has checks but nobody can say which block a merge.
- Coverage, performance, or accessibility numbers get argued per PR instead of decided once.
- About to run an autonomous loop where the only guard is a test suite the agent also wrote.

Do not apply when a `CONSTRAINTS.md` already exists and is not changing (read and follow it), for one-off scripts and spikes, when the user wants a review (`code-review-and-quality`) or a CI pipeline (`ci-cd-and-automation`), or for pre-product-market-fit code with a two-week life (the floor is still worth it, the rest is not).

## Loading constraints

The interview needs a live user; do not run it in non-interactive contexts. If constraints are missing there, apply the Floor below, say that you did, and flag the rest for a human.

## Step 1: detect before asking

Never ask what you can read. Before the first question, gather language and stack (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`), the test runner (dev dependencies, `test` script, existing tests), existing linters (`eslint.config.*`, `biome.json`, `.ruff.toml`), coverage today (`coverage/` or one suite run), CI (`.github/workflows/`, `.gitlab-ci.yml`), and the agent harness (`.claude/`, `.codex/`, `AGENTS.md`). Report the findings in two lines, then ask only what is left.

## Step 2: four questions, each with a default

One question at a time, and "I don't know" is a complete answer because every question has a default.

1. **Beyond the floor, what should be enforced?** coverage on new code, security scanning, performance budgets, accessibility, architecture boundaries. Default: coverage and security scanning (a test runner exists and user input is handled). Note the cost: performance and accessibility need a running URL; architecture needs a rules file.
2. **When a check fails mid-task, block or warn?** Default: block — a warning nobody reads is a warning. A gentler start is blocking the floor and warning on everything else for two weeks.
3. **Target numbers, or measure today and hold that line?** Default: measure and hold (a ratchet), since invented numbers get ignored.
4. **Slowest check you will tolerate before the agent hands work back?** Default: about 90 seconds at task end, unlimited in CI.

Stop at four; a twelve-question intake produces a config nobody understands.

## Step 3: write CONSTRAINTS.md

One file at the repo root, readable by any agent on any harness, and visible in review when changed.

```markdown
# Constraints

Last reviewed: 2026-08-08 by @addy

## Floor (always enforced, no setup required)

- No new suppression comments: `@ts-ignore`, `eslint-disable`, `# noqa`, `# type: ignore`
- No unimplemented stubs: `throw new Error("Not implemented")`, empty `catch {}`
- No skipped or deleted tests without a reason in the commit message
- No secrets in source
- This file does not get weakened to make a change pass

## Enforced with numbers

| Dimension | Rule | Checked by | Runs at |
|-----------|------|-----------|---------|
| Types | Zero type errors | `tsc --noEmit` | every edit |
| Lint | Zero errors from our config | `biome check` | every edit |
| Secrets | No secrets in source | `gitleaks dir . --redact` | every edit |
| Coverage | Changed lines ≥ 80% covered | `vitest run --coverage` + git diff | task end, CI |
| Security: code | Nothing at high or above | `npm run check:security` | CI |
| Security: deps | Nothing at high or above | `osv-scanner scan source -r .` | CI |
| Accessibility | Zero critical or serious | `npm run check:a11y` | preview deploy |
| Performance | LCP ≤ 2500ms, CLS ≤ 0.1 | `lighthouse $PREVIEW_URL --output=json` | preview deploy |

Every row names the command that produces the verdict; a number with
no command in that column is an aspiration, not a constraint.

## Measured, not yet enforced

| Metric | Today | Direction |
|--------|-------|-----------|
| Project coverage | 62.4% | must not fall |
| Bundle size (main) | 184 kB | must not grow |

## Exceptions

| ID | Rule | Path | Reason | Owner | Expires |
|----|------|------|--------|-------|---------|
| W1 | `no-explicit-any` | `src/legacy/**` | Rewrite tracked in ENG-441 | @addy | 2026-11-01 |
```

Then add one line to `AGENTS.md` and `CLAUDE.md`: `Read CONSTRAINTS.md before writing code. Do not weaken it to make a change pass.`

## Step 4: install what each dimension needs

Choosing a dimension means installing something; never leave a number with no mechanism, and prefer the de facto tool so the team's existing config keeps working.

| Dimension | Tool | Run | Gate on |
| --- | --- | --- | --- |
| Types (TS) | tsc | `tsc --noEmit` | any error |
| Types (Python) | mypy | `mypy .` | any error |
| Lint | existing config | `eslint .` / `biome check` / `ruff check` | any error |
| Coverage (JS) | Vitest/Jest | `vitest run --coverage` (or `jest --coverage`) | changed-line coverage |
| Coverage (Python) | pytest-cov | `pytest --cov --cov-report=lcov` | same |
| Security: code | Semgrep | `npm run check:security` | high or critical |
| Security: secrets | gitleaks | `gitleaks dir . --redact --no-banner` | any finding |
| Security: deps | osv-scanner | `osv-scanner scan source -r .` | high or above |
| Performance | Lighthouse | `lighthouse $URL --output=json --quiet` | LCP, CLS, score |
| Bundle | size-limit | `size-limit --json` | per-entry byte budget |
| Accessibility | axe-core | `npm run check:a11y` | zero critical or serious |
| Architecture | dependency-cruiser | `depcruise src` | any violation |
| Assertion quality | Stryker | `stryker run --mutate <changed files>` | mutation score |

Five pitfalls:

1. **`--redact` on gitleaks is not optional** — without it the matched secret lands in the transcript and can reach a log, summary, or commit. Report the rule and location, never the value.
2. **Lighthouse and axe need a URL.** If the project has nothing runnable (CLI, library, desktop app), say so and drop the dimension rather than inventing a check that cannot run.
3. **Scope expensive checks to the diff.** Whole-repo Stryker takes hours and gets switched off; changed files take under a minute. Semgrep likewise takes a path list.
4. **Coverage needs no second test run** — read the lcov the suite already writes and intersect with `git diff`.
5. **Semgrep registry rules are free to run; check the licence before redistributing them.** `opengrep` is a drop-in fork with the same rule format and JSON output.

`semgrep scan` and `axe` can exit 0 on findings, so copy `scripts/quality-gate.mjs` into the project's `scripts/` to enforce thresholds, and keep the scanner before `&&` so a failed scan stops the command.

Wire each check into a project script so it is reproducible without an agent:

```json
{
  "scripts": {
    "check:fast": "tsc --noEmit && eslint . && gitleaks dir . --redact --no-banner",
    "check:task": "npm run check:fast && vitest run --coverage",
    "check:security": "semgrep scan --config p/default --strict --json > semgrep-results.json && node scripts/quality-gate.mjs semgrep semgrep-results.json",
    "check:a11y": "axe \"$PREVIEW_URL\" --tags wcag2a,wcag2aa,wcag21aa --stdout > axe-results.json && node scripts/quality-gate.mjs axe axe-results.json",
    "check:full": "npm run check:task && npm run check:security && osv-scanner scan source -r ."
  }
}
```

The mapping matters more than the tools: `check:fast` after an edit, `check:task` when the agent thinks it is done, `check:full` in CI, `check:a11y` once the preview is reachable.

Before calling any row enforced, run its real command against a known violation and a clean control: the violation must fail, the control must pass, and scanner errors must fail too; for a severity threshold, also confirm a below-threshold finding passes. Generating a report does not enforce the number.

`CONSTRAINTS.md` is canonical (it carries the reason and shows up in review); the scripts are wrappers that must mirror it. If they drift, the file wins.

## Step 5: wire it to the lifecycle

Running everything everywhere is the biggest mistake: a check that stalls the agent gets switched off, and a switched-off gate is worse than none because the bar still looks like it exists.

| Phase | Command | Runs | Budget |
| --- | --- | --- | --- |
| BUILD | `/build` | Types, lint, secrets, floor | under 5s, changed files only |
| VERIFY | `/test` | Related tests, coverage on changed lines | under 90s |
| REVIEW | `/review` | Everything plus the guards below | minutes |
| SHIP | `/ship` | Direction checks, no regressions | CI |

Two rules keep it tolerable: scope to the diff (changed-line coverage is a number the agent can move; project coverage is one it inherited), and let cost decide placement (anything over a few seconds leaves the edit loop).

## Step 6: guard the bar itself

Agents do not craft clever loopholes; they hit a red check and take the cheapest road to green. Watch the diff for five moves at review time:

1. **The threshold moved** — a budget lowered, severity dropped, or a check removed from the fast stage; compare `CONSTRAINTS.md` against its branch-point state.
2. **A test got easier** — `.skip` added, a test file deleted, assertions pulled out of tests that stayed.
3. **A checker got silenced** — new `@ts-ignore` or `eslint-disable`; four suppressions deserve special attention because they switch off checks you rely on: `istanbul ignore` drops code from coverage, `Stryker disable` hides a surviving mutant, and `nosemgrep`/`gitleaks:allow` silence security findings.
4. **Work is unfinished** — a throwing stub, an empty `catch` turning failure into silence, a `TODO` where the implementation belongs.
5. **An exception appeared** — a new Exceptions row nobody discussed.

None of this needs tooling beyond `git diff`: tightening should be silent, loosening loud.

The floor has no de facto tool, so agents asked to enforce it tend to write checkers from scratch — and two agents write two different ones. Adapt the reference implementation in `references/floor-guard.md` (diff-scoped, exit `0`/`1`/`2`, patterns adaptable per ecosystem) rather than reinventing it, for the same reason each dimension names a de facto tool: the mechanism stays the same across runs and stacks.

Not all checks are equally circular. Rank by one question — can the agent make this pass by writing code that does not work? **External** checks (axe-core encodes WCAG, osv-scanner reads a vulnerability database, Lighthouse measures a real browser) cannot be argued with; **project** checks (your lint rules, your layer boundaries) have a human owner; **suite** checks (your own tests) are the most useful and the only genuinely circular ones. A bar made entirely of the third kind is worth less than one with an outside opinion — confirm at least one external constraint is present.

## Step 7: ratchets when you lack a number

Setting 80% coverage on a codebase at 62% produces a permanently red build and a team that learns to ignore red builds. The alternative needs no decision: record where you are and refuse to get worse. Put it in "Measured, not yet enforced" with today's number and a direction; every check compares against the recorded value, not an aspiration. When the number improves, update it; when it drops, that is the finding. This also answers a fair objection to training: models are rewarded for passing tests, which can be evaluated in seconds, while architectural rot appears over months and never reaches the weights — a ratchet is the missing penalty, written where the build can see it.

## Sane defaults

Chosen to be met by most codebases on day one:

| Constraint | Default | Why |
| --- | --- | --- |
| Coverage of changed lines | ≥ 80% | High enough to force a test, low enough to allow a config line |
| Project coverage | today's value, must not fall | Adoptable without argument |
| Mutation score | ≥ 60% to start | Typical for a never-mutated suite; 80% is mature |
| Dependency vulnerabilities | nothing at high or above | Below that is mostly noise |
| LCP / CLS | ≤ 2500 ms / ≤ 0.1 | Core Web Vitals "good" |
| Accessibility | zero critical or serious axe violations | Moderate and minor are often debatable |
| Exception lifetime | 90 days | Long enough to plan the fix, short enough to remember |
| Ratchet tolerance | 0.5% | Absorbs drift when an unrelated file moves the number |

State the number and its rationale together; a threshold without a reason gets deleted by the next person who hits it.

## Verification

- [ ] `CONSTRAINTS.md` exists with a floor, numbered rows, and an exceptions table.
- [ ] Every numbered row names a command that actually produces the verdict.
- [ ] Each command proven to fail on a violation and pass on a clean control.
- [ ] Checks mapped to build/task/full phases and scoped to the diff where expensive.
- [ ] At least one external constraint present; suppressions and skips diff-reviewed.
- [ ] Ratchets recorded with today's value and a direction.

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
- Path: `_sources/addyosmani_agent-skills/skills/constraint-driven-development/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
