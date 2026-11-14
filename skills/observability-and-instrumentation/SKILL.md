---
name: observability-and-instrumentation
description: Use when adding logging, metrics, tracing, or alerting; shipping any feature that runs in production and you need evidence it works; production issues are reported but you can't tell what happened from the available data.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [software-development, engineering, agent-skills, observability, monitoring]
    source: addyosmani/agent-skills
    adapted: true
---

# Observability and Instrumentation

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Adding logging, metrics, tracing, or alerting
- Shipping any feature that runs in production and you need evidence it works
- Production issues are reported but you can't tell what happened from the available data

## When NOT to Use

- A feature PR with retries, queues, or external calls and zero new telemetry
- Log lines built by string interpolation instead of structured fields
- No correlation/request ID — each log line is an orphan
- One log stream fed by a scheduler, a webhook, and manual runs, with no field naming which one produced the line
- Metrics labeled with user IDs, raw URLs, or error message text (cardinality bomb)
- Latency tracked as an average with no percentiles
- Alerts that fire daily and get acknowledged without action
- Alerts on causes (CPU, memory) paging humans while user-facing error rate is unmonitored
- Secrets, tokens, or full request bodies appearing in logs
- "It works on my machine" as the only evidence a production feature is healthy

## Overview

Code you cannot observe is code you cannot operate. Observability means answering "what is the system doing and why?" from outside, using telemetry the code emits; instrumentation is not a post-launch add-on but something written alongside the feature, the way tests are. A feature that ships without telemetry turns the first user-reported bug into archaeology instead of a query. The sequence below moves from the questions on-call will actually ask, through logs, metrics, traces, and alerts, to verifying that the telemetry itself works.

## 1. Define "Working" Before Instrumenting

Telemetry with no question behind it is noise. Write down the two to four questions an on-call engineer will ask about this feature before adding any signal:

```
FEATURE: checkout payment retry
QUESTIONS ON-CALL WILL ASK:
1. What fraction of payments succeed on first attempt vs after retry?
2. When a payment fails permanently, why? (provider error? timeout? validation?)
3. Is the payment provider slower than usual?
→ Every signal below must help answer one of these.
```

If you cannot name the questions, you are not ready to instrument; you would log everything and learn nothing.

## 2. Match Each Question to a Signal

| Signal | Answers | Cost profile | Example |
|---|---|---|---|
| **Structured log** | "What happened in this specific case?" | Per-event; grows with traffic | `payment_failed` with provider error code |
| **Metric** | "How often / how fast, in aggregate?" | Fixed per series; cheap to query | p99 latency of provider calls |
| **Trace** | "Where did time go across services?" | Per-request; usually sampled | One slow checkout, broken down by hop |

Rule of thumb: metrics tell you **that** something is wrong, traces tell you **where**, logs tell you **why**.

## 3. Structured Logging

Log events, not prose. Each line is a JSON object with a stable event name plus machine-readable fields:

```typescript
// BAD: string interpolation — unqueryable, inconsistent
logger.info(`Payment ${id} failed for user ${userId} after ${n} retries`);

// GOOD: stable event name + structured fields
logger.warn({
  event: 'payment_failed',
  paymentId: id,
  provider: 'stripe',
  errorCode: err.code,
  attempt: n,
}, 'payment failed');
```

Log levels, used consistently:

| Level | Meaning | On-call action |
|---|---|---|
| `error` | Invariant broken; someone may need to act | Investigate |
| `warn` | Degraded but handled (retry succeeded, fallback used) | Watch for trends |
| `info` | Significant business event (order placed, job finished) | None |
| `debug` | Diagnostic detail | Off in production by default |

Correlation IDs are mandatory. Generate or accept a request ID at the system boundary and attach it to every log line, span, and outbound call; without it a single request cannot be reconstructed from interleaved logs:

```typescript
// Express: child logger per request, ID propagated downstream
app.use((req, res, next) => {
  req.id = req.headers['x-request-id'] ?? crypto.randomUUID();
  req.log = logger.child({ requestId: req.id });
  res.setHeader('x-request-id', req.id);
  next();
});
```

**Name the entry point when several of them write to one log.** A correlation ID identifies a run but says nothing about which code path started it. A scheduler tick, a replay endpoint, and a manual CLI run reaching the same job produce interchangeable lines in one sink, so attribution falls back to elimination — cross-reading the scheduler history, the process table, a deploy log — an argument that holds only while those external records still exist. Stamp the entry point where the run starts, beside the correlation ID, and propagate both identically:

```typescript
// One helper for every entry point: the run's own logger carries both fields.
// `entryPoint`, not `source` — ECS reserves `source.*` for network fields.
export const runLog = (entryPoint: 'scheduler' | 'replay_endpoint' | 'cli', runId: string) =>
  logger.child({ entryPoint, requestId: runId });

// scheduler tick        -> runLog('scheduler', crypto.randomUUID())
// POST /jobs/:id/replay -> runLog('replay_endpoint', req.id)
// CLI invocation        -> runLog('cli', process.env.RUN_ID ?? crypto.randomUUID())
```

Both fields must cross the same boundaries as the correlation ID — queue metadata, HTTP headers — or a worker re-derives the entry point and guesses. A field that merely correlates with an entry point is a hint, not an attribution: anything that can invoke the job can reproduce it.

Never log secrets, tokens, passwords, or full PII. Telemetry pipelines are a classic data-leak path. Allowlist fields rather than logging whole request bodies.

## 4. Metrics

For request-driven services instrument **RED** on every endpoint and external dependency: **R**ate (requests/sec), **E**rrors (failure rate), **D**uration (latency histogram, never an average). For resources such as queues, pools, and hosts use **USE**: **U**tilization, **S**aturation, **E**rrors.

The vendor-neutral path is the OpenTelemetry metrics API. The example uses Prometheus' `prom-client` — one common backend, not the only one; RED/USE and cardinality rules are identical either way:

```typescript
import { Histogram } from 'prom-client';

const httpDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration',
  labelNames: ['method', 'route', 'status_class'],  // '2xx', not '200'
  buckets: [0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
});
```

Cardinality is the failure mode: every unique label combination is its own time series, so labels must come from small fixed sets (route template, status class, provider name). Never use user IDs, raw URLs, error messages, or other unbounded values as labels — those belong in logs and traces.

```
OK as label:    route="/api/tasks/:id"   status_class="5xx"   provider="stripe"
NEVER a label:  user_id, email, request_id, full URL, error message text
```

Track averages never, percentiles always: an average hides the one percent of users having a terrible time. Use histograms and read p50/p95/p99.

## 5. Distributed Tracing

Use OpenTelemetry; auto-instrumentation covers HTTP, gRPC, and common database clients with almost no code:

```typescript
// tracing.ts — must be imported before anything else
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

const sdk = new NodeSDK({
  serviceName: 'checkout-service',
  instrumentations: [getNodeAutoInstrumentations()],
});
sdk.start();
```

Wrap manual spans around meaningful internal units of work (`applyDiscounts`, `chargeProvider`) and attach the attributes on-call will filter by. Propagate context across every async boundary — HTTP headers, queue message metadata — or the trace dies at the gap. Sample head-based at a low rate by default, keeping 100% of errors if the backend supports tail sampling.

## 6. Alerting

Alert on symptoms users feel, not on causes:

```
SYMPTOM (page-worthy):           CAUSE (dashboard, not a page):
error rate > 1% for 5 min        CPU at 85%
p99 latency > 2s                 one pod restarted
queue age > 10 min               disk at 70%
```

Cause-based alerts fire when nothing is wrong and miss failures nobody predicted. Symptom-based alerts fire exactly when users are hurt, whatever the cause.

Every alert must satisfy four rules:

1. **Actionable.** If the correct response is "ignore it, it self-heals", delete the alert.
2. **Linked to a runbook** — even three lines: what it means, the first query to run, the escalation path.
3. **Threshold and duration justified** by the SLO or historical data, not a guess.
4. **Two severities only**: `page` (user-facing, act now) and `ticket` (degradation, act this week). A third tier becomes noise that trains people to ignore everything.

### Runbooks

Store runbooks in `docs/runbooks/`, named after the alert. Their job is to answer three questions without making the reader think: what is happening, what to check first, who to call if that does not resolve it.

Minimum viable runbook:

```markdown
# Runbook: High Error Rate on /api/tasks
**Means:** DB connection pool likely exhausted, or a bad deploy.
**First check:** `SELECT count(*) FROM pg_stat_activity WHERE backend_type = 'client backend';`
  — if count > pool limit, see Step 2. (Swap in the equivalent for your database.)
**Escalate to:** #db-oncall or engineering on-call rotation.
```

Add steps only when the first check is not enough to decide; five steps covering the three most common causes beats twenty steps covering every edge case and getting skimmed. Update the runbook while closing every incident that used it — a stale runbook builds false confidence, so fix wrong or missing steps before marking the incident resolved.

## 7. Verify the Telemetry Itself

Instrumentation is code and can be wrong. Trigger the paths and inspect actual output before calling the work done:

- Force an error in staging, find it in the logs by `requestId`, confirm fields are structured rather than `[object Object]`.
- Send test traffic; confirm metric series appear with expected labels and sane values.
- Follow one request across services in the tracing UI; no broken spans.
- Fire each new alert once (temporarily lowering the threshold); confirm it reaches the right channel and the runbook link works.

## Rationalizations to Reject

| Excuse | Reality |
|---|---|
| "I'll add logging after it works" | "After" becomes "after the first incident", the most expensive moment to discover you are blind. Instrument as you build. |
| "More logs = more observability" | Unstructured noise makes incidents slower, not faster. Three queryable events beat three hundred prose lines. |
| "console.log is fine for now" | Unstructured output cannot be filtered, correlated, or alerted on. The structured logger costs five minutes once. |
| "We can just look at the dashboards when something breaks" | Dashboards built without defined questions show everything except the answer. Start from on-call questions. |
| "Alert on everything important, we'll tune later" | A noisy pager trains people to ignore it; the tuning never happens, and the missed real page does. |
| "User ID as a metric label makes debugging easier" | It also makes your metrics backend fall over. High-cardinality lookups belong in logs and traces. |
| "Tracing is overkill for our two services" | Two services already raise cross-service latency questions logs cannot answer. Auto-instrumentation makes the cost trivial. |

## Red Flags

- A feature PR adds retries, queues, or external calls with zero new telemetry.
- Log lines built by string interpolation instead of structured fields.
- No correlation or request ID, leaving every log line an orphan.
- One log stream fed by a scheduler, a webhook, and manual runs, with no field naming which produced a given line.
- Metric labels carrying user IDs, raw URLs, or error message text (cardinality bomb).
- Latency tracked as an average with no percentiles.
- Alerts that fire daily and get acknowledged without action.
- Cause-based alerts (CPU, memory) paging humans while user-facing error rate is unmonitored.
- Secrets, tokens, or full request bodies appearing in logs.
- "It works on my machine" as the only evidence a production feature is healthy.

## Verification

After instrumenting a feature, confirm:

- [ ] The on-call questions for this feature are written down, and every signal maps to one of them.
- [ ] All log output is structured (JSON) with stable event names, and every line carries a correlation ID.
- [ ] Any log sink written by more than one entry point carries an entry-point field, set where the run starts and propagated with the correlation ID rather than inferred downstream.
- [ ] No secrets, tokens, or unredacted PII in any log line (spot-check actual output).
- [ ] RED metrics exist for every new endpoint and every external dependency, with bounded label sets.
- [ ] Latency is a histogram, and p95/p99 are queryable.
- [ ] A single request can be followed end-to-end in the tracing UI without broken spans.
- [ ] Every new alert is symptom-based, links to a runbook, and has been test-fired once.
- [ ] An induced failure in staging was located using telemetry alone, without reading the source.

An at-a-glance version of this list, including the pre-launch instrumentation gate, lives in `../../references/observability-checklist.md`.

## Related Skills in This Repo

- [code-review-and-quality](../code-review-and-quality/SKILL.md) — Use when reviewing code written by yourself, another agent, or a human; you need to assess...
- [ci-cd-and-automation](../ci-cd-and-automation/SKILL.md) — Use when setting up or modifying build and deployment pipelines; you need to automate qual...
- [api-and-interface-design](../api-and-interface-design/SKILL.md) — Use when designing APIs, module boundaries, or any public interface; creating REST or Grap...
- [git-workflow-and-versioning](../git-workflow-and-versioning/SKILL.md) — Use when making any code change; committing, branching, resolving conflicts, splitting unc...
- [logging-observability-patterns](../logging-observability-patterns/SKILL.md) — Use when implementing structured logging and observability.
- [docker-monitoring](../docker-monitoring/SKILL.md) — Use when monitoring Docker containers.
- [distributed-tracing-patterns-troubleshooting](../distributed-tracing-patterns-troubleshooting/SKILL.md) — Use when applying distributed tracing troubleshooting.

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Upstream anti-patterns retained as the When-NOT-to-Use list.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- Path: `_sources/addyosmani_agent-skills/skills/observability-and-instrumentation/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
