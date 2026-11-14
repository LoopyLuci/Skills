---
name: oci-functions-troubleshoot
description: Use when asked to classify Fn CLI errors, deploy or invoke failures, OCIR auth and registry issues, app-limit symptoms, logs, tracing, metrics, or limits.
version: 2.0.0
author: LoopyLuci Community
license: UPL-1.0
platforms: [any]
metadata:
  hermes:
    tags: [oracle, oci, functions]
    source: oracle/skills
    adapted: true
---

# OCI Function Troubleshoot

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Asked to classify Fn CLI errors, deploy or invoke failures, OCIR auth and registry issues, app-limit symptoms, logs, tracing, metrics, or limits

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

A deterministic, diagnosis-first triage workflow for OCI Functions problems across setup, control plane, application creation, deployment, invocation, and observability. It isolates the most likely cause from error text, command output, or telemetry signals before anything is changed. Read-only checks are the default; context edits, Docker logins, app changes, redeploys, and infrastructure mutations happen only when the user explicitly asks for a fix, and mutating remediation is handed to `$oci-functions-deploy`.

## Output Contract

Answer in exactly this shape:

- `stage`: one of `setup_or_control_plane`, `create`, `deploy`, `invoke`, `observability_first`.
- `evidence`: 1–3 concrete facts drawn from the user's error text, command, config, logs, metrics, or limits.
- `most_likely_cause`: a single primary cause, or a ranked top-2 shortlist when confidence is low.
- `confidence`: `low`, `medium`, or `high`.
- `next_confirming_check`: the single best read-only check that narrows or confirms the cause.
- `smallest_safe_remediation`: the least invasive next action; with weak evidence this may be "collect more evidence with ...".
- `validation`: the follow-up step that proves the remediation worked.

## Triage

1. If the user supplies an exact error string, start with `references/error-patterns.md`.
2. Classify the issue by the failed action:
   - `setup_or_control_plane` — local Fn/OCI/OCIR/tooling/auth/context/policy problems that block normal app or function operations.
   - `create` — application creation failures.
   - `deploy` — `fn deploy`, image build or push, `func.yaml`, app config, subnet annotation, or registry-target failures.
   - `invoke` — runtime invocation, HTTP, image pull, timeout, memory, networking, detached delivery, or response-limit failures after a function has been deployed.
   - `observability_first` — the user starts from logs, traces, metrics, limits, or "why is this function unhealthy?"
3. If the stage is ambiguous, ask exactly one disambiguating question when a single missing fact would change it. Otherwise present the top two plausible stages in ranked order and continue with the best read-only confirming check.

## Minimum Facts

Capture these before diagnosing:

- Exact error text and HTTP status, if present.
- The command or action that failed.
- Region, compartment/profile, app name, and function name when known.
- Whether the problem is local, deploy-time, invoke-time, or telemetry-first.
- Which tooling is available: Fn CLI, OCI CLI, Docker, Logging, Monitoring, Tracing.

## Preferred Read-Only Checks

When tooling is available, prefer non-mutating checks:

- `fn inspect context`
- `fn list apps`
- `fn inspect app <app-name>`
- `fn inspect function <app-name> <function-name>`
- Read the local `func.yaml`.
- Inspect environment values that can override expected behavior, especially `FN_REGISTRY`.
- Read logs, traces, metrics, and limits before recommending edits.
- Use `DEBUG=1` or `OCI_GO_SDK_DEBUG=v` only for additional diagnostic signal, never as a first fix.

If tools or access are missing, stay docs-first: classify from the error text, use the phase reference file for likely causes, and use `references/error-patterns.md` when the text is the strongest clue.

## Workflow

### Setup or Control Plane

`references/setup-and-runtime.md` covers Fn CLI `401` and `404`, OCI key/passphrase/private-key format problems, wrong region/compartment/endpoint/app/function targets, IAM, policy, dynamic-group, or network-resource authorization failures, Docker registry unauthorized failures, and stale CLI behavior.

Read-only sequence: inspect active Fn context values; verify the intended OCI profile, compartment, and region match the failing target; confirm the registry host derived from the context. For `404`, separate endpoint or name mismatches from IAM/policy or compartment-targeting issues before suggesting reconfiguration.

### Application Creation

`references/create.md` covers create-time failures. Focus on documented service-limit style failures such as maximum application count; whether the request reaches the intended compartment and region; whether IAM or compartment targeting is wrong when the error is not clearly limit-shaped; and whether the smallest safe path is reuse, cleanup, or a limit increase request.

### Deployment

`references/deploy.md` covers `fn deploy` failures, image build/push/registry auth problems, `func.yaml` schema issues, wrong application context or missing subnet annotations, architecture mismatch symptoms, and identity-domain or federated OCIR username issues.

Check in this order: active Fn context and target app; local `func.yaml`; effective registry target including `FN_REGISTRY`; app annotations and subnet/network assumptions; whether the failure is local build, image push, or service-side deploy; `fn version` when architecture or stale-client symptoms are plausible.

### Invocation

`references/invoke.md` covers request or response size limits, throttling, detached delivery, event-triggered retries, client disconnect, image pull, DNS, timeout, memory, syslog, security-attribute, dynamic-group failures, and subnet, DHCP, resolver, or service-availability failures.

Check in this order: exact HTTP code and service error text; whether the error occurs before code starts, during init, during execution, or after execution but before delivery completes; logs first for code/runtime clues; traces next when dependency timing or call path is unclear; metrics next for error rate, latency, concurrency, and invoke-type trends; limits last when the symptom suggests capacity pressure.

### Observability First

Use `references/observability.md` when the user starts from symptoms rather than one failing command. Default sequence: logs (did the function run, is application logging enabled), tracing (dependency timing, latency, call path when enabled), metrics (execution failure vs throttling vs detached delivery vs latency vs capacity), limits (do create or invoke failures align with service limits), debug flags (`DEBUG=1` or `OCI_GO_SDK_DEBUG=v`) only when reproducing locally or when request/SDK detail is still missing.

## Reference Map

| Concern | File |
|---|---|
| setup / control-plane issues | `references/setup-and-runtime.md` |
| app creation issues | `references/create.md` |
| deployment issues | `references/deploy.md` |
| invocation issues | `references/invoke.md` |
| logs, traces, metrics, limits, debug flags | `references/observability.md` |
| exact strings to likely causes | `references/error-patterns.md` |
| reusable prompt patterns | `references/example-prompts.md` |

## Guardrails

- Diagnose and isolate first. Do not mutate local context, Docker auth, app config, deployed state, or infrastructure unless the user explicitly asks for a fix.
- When the user does ask for a fix, finish the diagnosis summary first and hand the mutating repair work to `$oci-functions-deploy`.
- Never open with a mutating fix when a read-only check could narrow the cause.
- A `404` is not automatically an endpoint or name problem; treat IAM, policy, compartment targeting, dynamic groups, and network-resource authorization as first-class alternatives.
- Do not call a deploy issue code-related until registry, app, client version, and network context are checked.
- Do not call an invoke issue platform-related until logs, traces, and metrics are checked.
- Treat `FN_REGISTRY`, active Fn context, app annotations, tracing availability, and service limits as common hidden causes.
- With only a partial symptom, ask for the exact error text or failing command before escalating to broad remediation.
- With partial evidence, give a ranked shortlist of plausible causes instead of one overconfident root cause.

## Verification

- [ ] The answer includes all seven contract fields (`stage`, `evidence`, `most_likely_cause`, `confidence`, `next_confirming_check`, `smallest_safe_remediation`, `validation`).
- [ ] The stage matches the failed action, or a single disambiguating question was asked when it could not be determined.
- [ ] Diagnosis rested on read-only checks (or documented error-text classification when tooling was unavailable).
- [ ] No Fn context edit, Docker login, app change, redeploy, or infrastructure mutation ran without explicit user approval.
- [ ] When a fix was requested, the diagnosis was completed and the mutation was routed through `$oci-functions-deploy`.
- [ ] `validation` names a concrete check that would prove the remediation worked.

## Sources

- [Troubleshooting OCI Functions](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionstroubleshooting.htm)
- [Issues deploying applications and functions](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionstroubleshooting_topic-Issues-deploying-applications-and-functions.htm)
- [Issues invoking functions](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionstroubleshooting_topic-Issues-invoking-functions.htm)
- [Storing and Viewing Function Logs](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsexportingfunctionlogfiles.htm)
- [Function Metrics](https://docs.oracle.com/en-us/iaas/Content/Functions/Reference/functionsmetrics.htm)
- [Functions QuickStart on Local Host](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsquickstartlocalhost.htm)

## Related Skills in This Repo

- [apexlang-inventory](../apexlang-inventory/SKILL.md) — Use when working with provides an overview of APEX application components, APEXlang syntax...
- [oke-troubleshooter](../oke-troubleshooter/SKILL.md) — Use when the user wants to diagnose or root-cause issues with an OCI Kubernetes Engine clu...
- [oke-gva-deployer](../oke-gva-deployer/SKILL.md) — Use when the user asks to enable, deploy, or configure Generic VNIC Attachment (GVA) for O...
- [oci-functions-deploy](../oci-functions-deploy/SKILL.md) — Use when asked to validate/install Fn, OCI CLI, and Docker, configure or create Fn context...
- [serverless-computing-patterns](../serverless-computing-patterns/SKILL.md) — Use when building serverless applications and functions.
- [bash-scripting-advanced](../bash-scripting-advanced/SKILL.md) — Use when writing advanced bash scripts.
- [azure-functions-troubleshooting](../azure-functions-troubleshooting/SKILL.md) — Use when applying azure functions troubleshooting.

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [oracle/skills](https://github.com/oracle/skills)
- Path: `_sources/oracle_skills/oci/functions/oci-functions-troubleshoot/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
