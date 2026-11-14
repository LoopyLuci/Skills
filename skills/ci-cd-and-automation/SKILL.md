---
name: ci-cd-and-automation
description: Use when setting up or modifying build and deployment pipelines; you need to automate quality gates, configure test runners in CI, or establish deployment strategies.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [software-development, engineering, agent-skills, devops, ci-cd, automation]
    source: addyosmani/agent-skills
    adapted: true
---

# CI/CD and Automation

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Setting up or modifying build and deployment pipelines
- You need to automate quality gates, configure test runners in CI, or establish deployment strategies

## When NOT to Use

- No CI pipeline in the project
- CI failures ignored or silenced
- Tests disabled in CI to make the pipeline pass
- Production deploys without staging verification
- No rollback mechanism
- Secrets stored in code or CI config files (not secrets manager)
- Long CI times with no optimization effort

## Overview

Automate quality gates so no change reaches production without passing lint, types, tests, and build. CI/CD is the enforcement mechanism for every other skill: it catches what humans and agents miss, consistently, on every change.

- **Shift left.** Catch problems as early as possible — a lint-stage bug costs minutes, a production bug costs hours. Static analysis before tests, tests before staging, staging before production.
- **Faster is safer.** Smaller batches and more frequent releases reduce risk: three changes are easier to debug than thirty, and frequent releases build confidence in the release process itself.

## The quality gate pipeline

```
Pull request opened
  → lint (eslint, prettier)
  → type check (tsc --noEmit)
  → unit tests (jest/vitest)
  → build
  → integration (API/DB)
  → e2e (optional: Playwright/Cypress)
  → security audit (npm audit)
  → bundle size check
  → ready for review
```

No gate can be skipped. If lint fails, fix lint rather than disabling the rule; if a test fails, fix the code rather than skipping the test.

## GitHub Actions examples

Basic pipeline:

```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npx tsc --noEmit
      - run: npm test -- --coverage
      - run: npm run build
      - run: npm audit --audit-level=high
```

With database integration tests:

```yaml
  integration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: ci_user
          POSTGRES_PASSWORD: ${{ secrets.CI_DB_PASSWORD }}
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready --health-interval 10s
          --health-timeout 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npx prisma migrate deploy
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
      - run: npm run test:integration
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
```

Even for CI-only databases, keep credentials in secrets rather than hardcoding them — it builds good habits and stops test credentials leaking elsewhere.

E2E:

```yaml
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npm run build
      - run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

## Feeding failures back to the agent

The value of CI with agents is the feedback loop: copy the failure output, hand it to the agent with the specific error and an instruction to fix and verify locally, then push again. Lint failures → run the autofix and commit; type errors → read the location and fix the type; test failures → follow the debugging skill; build errors → check config and dependencies.

## Deployment strategies

**Preview deployments** — every PR gets a preview for manual testing:

```yaml
deploy-preview:
  runs-on: ubuntu-latest
  if: github.event_name == 'pull_request'
  steps:
    - uses: actions/checkout@v4
    - run: npx vercel --token=${{ secrets.VERCEL_TOKEN }}
```

**Feature flags** decouple deployment from release: ship code without enabling it, roll back without redeploying, canary 1% → 10% → 100%, and run A/B tests.

```typescript
if (featureFlags.isEnabled('new-checkout-flow', { userId })) {
  return renderNewCheckout();
}
return renderLegacyCheckout();
```

Lifecycle: create → enable for testing → canary → full rollout → remove the flag and its dead code. Flags that live forever become debt, so set a cleanup date at creation.

**Staged rollout** — merge to main → automatic staging deploy → manual verification → production deploy (manual trigger or automatic after staging) → monitor for 15 minutes → roll back on errors, otherwise done.

**Rollback plan** — every deployment must be reversible:

```yaml
name: Rollback
on:
  workflow_dispatch:
    inputs:
      version: { description: 'Version to rollback to', required: true }
jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - name: Rollback deployment
        env:
          VERSION: ${{ inputs.version }}
        run: npx vercel rollback "$VERSION"
```

Pass the input through `env`; never interpolate it into the script (shell injection).

## Environment management

`.env.example` committed as a template; `.env` never committed; `.env.test` committed with no real secrets; CI secrets in the platform's secrets store; production secrets in the deployment platform or a vault. CI should never hold production secrets.

## Automation beyond CI

**Dependabot/Renovate** keeps dependencies fresh:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule: { interval: weekly }
    open-pull-requests-limit: 5
```

**Build Cop** — designate an owner responsible for keeping CI green, whose job when the build breaks is to fix or revert (not the author of the breaking change). Prevents broken builds accumulating while everyone assumes someone else will fix them.

**PR checks** — require at least one approval, require status checks to pass, block force-pushes to main, and auto-merge once checks and approval are satisfied.

## CI optimization

When the pipeline passes 10 minutes, apply in order of impact: cache the package-manager cache (via `setup-node`'s `cache` or `actions/cache`, not `node_modules`); run lint/typecheck/test/build as parallel jobs; use path filters to skip unrelated jobs (docs-only PRs skip e2e); shard test suites across matrix runners; move slow tests off the critical path to a schedule; use larger runners for CPU-heavy builds.

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm run lint
  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npx tsc --noEmit
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm test -- --coverage
```

## Red flags

- No CI pipeline at all
- CI failures ignored or silenced; tests disabled to make the pipeline pass
- Production deploys without staging verification
- No rollback mechanism
- Secrets in code or CI config rather than a secrets manager
- Long CI with no optimization effort

## Verification

- [ ] All quality gates present (lint, types, tests, build, audit).
- [ ] Pipeline runs on every PR and push to main.
- [ ] Failures block merge via branch protection.
- [ ] CI results feed back into the development loop.
- [ ] Secrets live in the secrets manager, not in code.
- [ ] Deployment has a rollback mechanism.
- [ ] Test suite completes in under 10 minutes.

## Related Skills in This Repo

- [code-review-and-quality](../code-review-and-quality/SKILL.md) — Use when reviewing code written by yourself, another agent, or a human; you need to assess...
- [api-and-interface-design](../api-and-interface-design/SKILL.md) — Use when designing APIs, module boundaries, or any public interface; creating REST or Grap...
- [git-workflow-and-versioning](../git-workflow-and-versioning/SKILL.md) — Use when making any code change; committing, branching, resolving conflicts, splitting unc...
- [context-engineering](../context-engineering/SKILL.md) — Use when starting a new session, when agent output quality degrades, when switching betwee...
- [local-cicd-pipeline](../local-cicd-pipeline/SKILL.md) — Build local CI/CD pipelines with preflight, tests, deploy.
- [devops-troubleshooting](../devops-troubleshooting/SKILL.md) — Use when troubleshooting devops.
- [devops-optimization](../devops-optimization/SKILL.md) — Use when optimizing devops systems.

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Upstream anti-patterns retained as the When-NOT-to-Use list.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- Path: `_sources/addyosmani_agent-skills/skills/ci-cd-and-automation/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
