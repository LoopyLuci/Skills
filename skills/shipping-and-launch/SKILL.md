---
name: shipping-and-launch
description: Use when preparing to deploy to production, or when asking what needs to be in place before shipping; you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a rollback strategy.
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

# Shipping and Launch

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Preparing to deploy to production, or when asking what needs to be in place before shipping
- You need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a rollback strategy

## When NOT to Use

- Deploying without a rollback plan
- No monitoring or error reporting in production
- Big-bang releases (everything at once, no staging)
- Feature flags with no expiration or owner
- No one monitoring the deploy for the first hour
- Production environment configuration done by memory, not code
- "It's Friday afternoon, let's ship it"
- Error budget exhausted but feature work continues unchanged

## Overview

A launch is only done when it can be observed, measured, and undone. This skill structures that into three disciplines: a pre-launch bar (quality, security, performance, accessibility, infrastructure, docs), a staged rollout that decouples deploying from releasing, and a monitoring/rollback setup so regressions surface on dashboards rather than in user complaints. Treat every deployment as carrying risk, and make reversibility part of the plan rather than an improvisation at 3 a.m.

## Pre-Launch Checklist

Six areas must be green before anything reaches production. Checkbox status tracks completion; a red item blocks the deploy.

### Code Quality

- [ ] Full test suite passes (unit, integration, e2e)
- [ ] Build clean, no new warnings
- [ ] Lint and type checks pass
- [ ] Change reviewed and approved
- [ ] No unresolved TODOs that should have been handled here
- [ ] Debug statements (`console.log` and equivalents) out of production code
- [ ] Error handling covers expected failure modes

### Security

- [ ] No secrets in code or version control
- [ ] Dependency audit (`npm audit`, `pip-audit`, `cargo audit`) shows no critical/high findings
- [ ] Input validation on all user-facing endpoints
- [ ] Authentication and authorization enforced
- [ ] Security headers set (CSP, HSTS, etc.)
- [ ] Rate limiting on auth endpoints
- [ ] CORS restricted to specific origins, never wildcard

### Performance

- [ ] Core Web Vitals inside "Good" thresholds
- [ ] No N+1 queries on critical paths
- [ ] Images compressed, responsively sized, lazily loaded
- [ ] Bundle size within budget
- [ ] Appropriate indexes on database queries
- [ ] Caching for static assets and repeated queries

### Accessibility

- [ ] Full keyboard operation for interactive elements
- [ ] Screen reader conveys content and structure
- [ ] Contrast meets WCAG 2.1 AA (4.5:1 text)
- [ ] Focus managed correctly for modals and dynamic regions
- [ ] Error messages descriptive and tied to their fields
- [ ] Zero axe-core or Lighthouse a11y violations

### Infrastructure

- [ ] Production environment variables configured
- [ ] Database migrations applied or ready to apply
- [ ] DNS and SSL configured
- [ ] CDN serving static assets
- [ ] Logging and error reporting wired up
- [ ] Health check endpoint present and responding

### Documentation

- [ ] README reflects any new setup requirements
- [ ] API docs current
- [ ] ADRs written for architectural decisions
- [ ] Changelog updated
- [ ] User-facing docs updated where applicable

## Feature Flags

Flags let code land inert, then turn on for a controlled audience:

```typescript
// Feature flag check
const flags = await getFeatureFlags(userId);

if (flags.taskSharing) {
  // New feature: task sharing
  return <TaskSharingPanel task={task} />;
}

// Default: existing behavior
return null;
```

Lifecycle:

```
1. DEPLOY with flag OFF     → Code is in production but inactive
2. ENABLE for team/beta     → Internal testing in production environment
3. GRADUAL ROLLOUT          → 5% → 25% → 50% → 100% of users
4. MONITOR at each stage    → Watch error rates, performance, user feedback
5. CLEAN UP                 → Remove flag and dead code path after full rollout
```

Rules: every flag has an owner and an expiration date; remove it within two weeks of full rollout; avoid nesting flags (combinations explode); exercise both on and off states in CI.

## Staged Rollout

### Sequence

```
1. DEPLOY to staging
   └── Full test suite in staging environment
   └── Manual smoke test of critical flows

2. DEPLOY to production (feature flag OFF)
   └── Verify deployment succeeded (health check)
   └── Check error monitoring (no new errors)

3. ENABLE for team (flag ON for internal users)
   └── Team uses the feature in production
   └── 24-hour monitoring window

4. CANARY rollout (flag ON for 5% of users)
   └── Monitor error rates, latency, user behavior
   └── Compare metrics: canary vs. baseline
   └── 24-48 hour monitoring window
   └── Advance only if all thresholds pass (see table below)

5. GRADUAL increase (25% -> 50% -> 100%)
   └── Same monitoring at each step
   └── Ability to roll back to previous percentage at any point

6. FULL rollout (flag ON for all users)
   └── Monitor for 1 week
   └── Clean up feature flag
```

### Decision Thresholds

| Metric | Advance (green) | Hold and investigate (yellow) | Roll back (red) |
|--------|-----------------|-------------------------------|-----------------|
| Error rate | Within 10% of baseline | 10-100% above baseline | >2x baseline |
| P95 latency | Within 20% of baseline | 20-50% above baseline | >50% above baseline |
| Client JS errors | No new error types | New errors at <0.1% of sessions | New errors at >0.1% of sessions |
| Business metrics | Neutral or positive | Decline <5% (may be noise) | Decline >5% |

Roll back immediately when: error rate exceeds 2x baseline, P95 latency rises over 50%, user-reported issues spike, data integrity is compromised, or a security vulnerability appears.

## Monitoring

### Signals to watch

```
Application metrics:
├── Error rate (total and by endpoint)
├── Response time (p50, p95, p99)
├── Request volume
├── Active users
└── Key business metrics (conversion, engagement)

Infrastructure metrics:
├── CPU and memory utilization
├── Database connection pool usage
├── Disk space
├── Network latency
└── Queue depth (if applicable)

Client metrics:
├── Core Web Vitals (LCP, INP, CLS)
├── JavaScript errors
├── API error rates from client perspective
└── Page load time
```

### Error Reporting

```typescript
// Set up error boundary with reporting
class ErrorBoundary extends React.Component<React.PropsWithChildren> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    // Report to error tracking service
    reportError(error, {
      componentStack: info.componentStack,
      userId: getCurrentUser()?.id,
      page: window.location.pathname,
    });
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback onRetry={() => this.setState({ hasError: false })} />;
    }
    return this.props.children;
  }
}

// Server-side error reporting
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  reportError(err, {
    method: req.method,
    url: req.url,
    userId: req.user?.id,
  });

  // Don't expose internals to users
  res.status(500).json({
    error: { code: 'INTERNAL_ERROR', message: 'Something went wrong' },
  });
});
```

### First-Hour Verification

Within an hour of launch:

```
1. Check health endpoint returns 200
2. Check error monitoring dashboard (no new error types)
3. Check latency dashboard (no regression)
4. Test the critical user flow manually
5. Verify logs are flowing and readable
6. Confirm rollback mechanism works (dry run if possible)
```

## Error Budget Gate

The error budget is the failure fraction your SLO permits; use remaining budget as an objective shipping gate:

```
Budget remaining > 20%  →  Ship normally; monitor closely
Budget remaining 0–20%  →  Slow rollouts only; no high-risk changes
Budget exhausted        →  Freeze feature work; focus entirely on reliability
Budget resets           →  Resume normal pace; bake in the fix that recovered it
```

Burn rate matters as much as the absolute error rate. A canary consuming budget faster than baseline pace is a hold signal, even when individual thresholds still look green.

## Rollback Plan

Write the plan before deploying:

```markdown
## Rollback Plan for [Feature/Release]

### Trigger Conditions
- Error rate > 2x baseline
- P95 latency > [X]ms
- User reports of [specific issue]

### Rollback Steps
1. Disable feature flag (if applicable)
   OR
1. Deploy previous version: `git revert <commit> && git push`
2. Verify rollback: health check, error monitoring
3. Communicate: notify team of rollback

### Database Considerations
- Migration [X] has a rollback: <verified command or runbook link>
- Data inserted by new feature: [preserved / cleaned up]

### Time to Rollback
- Feature flag: < 1 minute
- Redeploy previous version: < 5 minutes
- Database rollback: < 15 minutes
```

## Rationalizations to Reject

| Excuse | Reality |
|---|---|
| "It works in staging, it'll work in production" | Production data, traffic, and edge cases differ; monitor after deploy. |
| "We don't need feature flags for this" | Every change benefits from a kill switch, however simple it looks. |
| "Monitoring is overhead" | Without it you learn about problems from users, not dashboards. |
| "We'll add monitoring later" | Instrument before launch; invisible systems are undebuggable. |
| "Rolling back is admitting failure" | Rolling back is responsible engineering; shipping broken code is the failure. |
| "Error rate looks fine, keep shipping" | Check burn rate too; budget depletion is itself a hold signal. |

## Red Flags

- Deploying with no rollback plan
- No monitoring or error reporting in production
- Big-bang releases with no staging or phased exposure
- Feature flags without an owner or expiry
- Nobody watching the deploy during its first hour
- Production config remembered rather than codified
- Shipping late on a Friday because "it's small"
- Continuing feature work while the error budget is exhausted

## Verification

Before deploying:

- [ ] All checklist sections green
- [ ] Feature flag in place (when applicable)
- [ ] Rollback plan written and reachable
- [ ] Monitoring dashboards live
- [ ] Team notified about the deployment

After deploying:

- [ ] Health check returns 200
- [ ] Error rate at baseline
- [ ] Latency at baseline
- [ ] Critical user flow verified working
- [ ] Logs flowing
- [ ] Rollback path tested or confirmed ready

Standing requirement:

- [ ] Error budget policy defined: action at <20% remaining and at exhaustion

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
- Path: `_sources/addyosmani_agent-skills/skills/shipping-and-launch/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
