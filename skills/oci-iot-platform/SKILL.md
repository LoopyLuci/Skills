---
name: oci-iot-platform
description: Use when requests involve OCI IoT bootstrap, digital twin inspection, safe lifecycle operations, or translating OCI IoT docs and samples into concrete commands.
version: 2.0.0
author: LoopyLuci Community
license: UPL-1.0
platforms: [any]
metadata:
  hermes:
    tags: [oracle, oci]
    source: oracle/skills
    adapted: true
---

# OCI IoT Platform

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Requests involve OCI IoT bootstrap, digital twin inspection, safe lifecycle operations, or translating OCI IoT docs and samples into concrete commands

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

Oracle Cloud Infrastructure (OCI) Internet of Things Platform connects devices to cloud resources through domains, digital twin models, adapters, instances, and relationships. This skill explores, creates, and troubleshoots those resources, and turns OCI IoT documentation and samples into concrete commands. It favors read-only discovery first, small verified mutations, and CLI workflows — with MCP treated as an optional accelerator rather than a dependency.

## Quick start

1. Confirm the work targets OCI IoT Platform.
2. Gather minimal context before emitting commands: `IOT_DOMAIN_ID` when available, `OCI_CLI_PROFILE`, `OCI_CLI_AUTH` (e.g. `security_token`) if the chosen profile needs it, `OCI_REGION` if it cannot be derived from the domain, and the intended operation — inspect, create, update, delete, or publish test telemetry.
3. Work in this order: discover the domain and current state, inspect the relevant model/adapter/twin, check local CLI capability with `oci ... --help` when newer filters or gateway/raw-command options are involved, make the smallest required change, then verify with a fresh read.

## Default workflow

1. Begin with read-only OCI CLI discovery.
2. Use `scripts/derive_domain_context.sh` when the user has only `IOT_DOMAIN_ID`.
3. Consult [references/platform-surface.md](references/platform-surface.md) for orientation on OCI IoT resource families, data flow, connectivity types, and which surface fits.
4. Use [references/cli-workflows.md](references/cli-workflows.md) for control-plane actions: domains and domain groups, digital twin models, adapters, instances, relationships, work requests, and HTTPS publish examples.
5. Use [references/mcp-optional-use.md](references/mcp-optional-use.md) only when an OCI IoT MCP server is already present in the environment. CLI remains the fallback; never require MCP for public workflows.
6. Use [references/resilience-guidance.md](references/resilience-guidance.md) for large or ambiguous list operations, SDK/CLI command-shape drift, gateway-aware topology, relationship source/target diagnosis, work-request failures, publish rejection triage, raw-command final-state validation, and cleanup/rollback planning.
7. Use [references/modeling-guidance.md](references/modeling-guidance.md) for DTDL authoring or adapter payload design.
8. Use [references/data-access.md](references/data-access.md) only when the user explicitly needs Data API, ORDS, direct database access, or APEX-oriented workflows.
9. Use [references/release-validation.md](references/release-validation.md) before calling the skill package ready to share publicly.

## Bundled resources

- `scripts/derive_domain_context.sh` derives region, device host, data host, domain group OCID, and the short IDs later commands use.
- `scripts/twin_tools.py` provides `last-known`, `offline`, and `telemetry-template`.
- Templates: [model.temperature-sensor.template.json](templates/model.temperature-sensor.template.json), [adapter.default.template.json](templates/adapter.default.template.json), [instance.template.json](templates/instance.template.json), [publish-curl.template.sh](templates/publish-curl.template.sh).
- [references/platform-surface.md](references/platform-surface.md) explains how domains, domain groups, models, adapters, twins, relationships, work requests, raw commands, and data access fit together.
- [references/resilience-guidance.md](references/resilience-guidance.md) keeps operator responses bounded, active-resource focused, and explicit about final-state evidence.
- [references/mcp-optional-use.md](references/mcp-optional-use.md) describes optional OCI IoT MCP tool families, gateway-aware helper behavior, Data API wrappers, and safety rules.

## Guardrails

- Do not assume internal tenancy names, profiles, network access patterns, or private tooling.
- Treat Oracle product docs and official samples as the source of truth for platform behavior.
- Prefer read-only commands first and verify current state before recommending mutations.
- After any suggested create/update/delete, immediately include a verification command.
- Bound large reads with filters and `--limit` before reaching for `--all`.
- Treat asynchronous acceptance — including raw-command `202` — as incomplete until final state is verified.
- For digital twin instance creation, never use `INDIRECT` as a shortcut around auth setup. Use `INDIRECT` only when the user explicitly asks for a gateway/downstream topology or supplies a gateway routing requirement; otherwise clarify connectivity or proceed with `DIRECT` when a publishing device is implied.
- Keep MCP guidance optional — MCP installation or private bootstrap is never part of the public workflow.
- When MCP is already available, treat it as an accelerator for joined context, selector resolution, bounded pagination, gateway topology, Data API summaries, and polling; stay ready to fall back to CLI/SDK.
- Keep device publishing auth modes distinct: vault-secret-backed basic auth vs. certificate-based mTLS.
- Do not imply OCI IoT is a general-purpose MQTT broker.
- Keep examples redacted and tenant-neutral.

## Output style

For every task return:

1. The exact command sequence, with placeholders filled or called out.
2. The key IDs, state, or timestamps that matter.
3. The next verification step.

## Verification

- [ ] Domain context derived (region, hosts, domain group OCID) before control-plane commands.
- [ ] Each mutation paired with a verification command that re-reads final state.
- [ ] Asynchronous operations (including raw-command `202`) confirmed at final state before reporting success.
- [ ] Large list reads bounded with filters and `--limit`; `--all` used deliberately.
- [ ] Device auth mode identified (basic vs. mTLS) before publish steps.
- [ ] CLI help checked (`oci ... --help`) when using newer filters or gateway/raw-command options.
- [ ] Response contains the command sequence, the key IDs/state/timestamps, and the next verification step.
- [ ] Public-facing guidance keeps MCP optional and never depends on private tooling.

## Authoritative references

- Oracle IoT service docs: `https://docs.oracle.com/en-us/iaas/Content/internet-of-things/home.htm`
- OCI CLI IoT command reference: `https://docs.oracle.com/en-us/iaas/tools/oci-cli/latest/oci_cli_docs/cmdref/iot.html`
- Oracle sample repository: `https://github.com/oracle-samples/oci-iot-samples`

## Related Skills in This Repo

- [apexlang-inventory](../apexlang-inventory/SKILL.md) — Use when working with provides an overview of APEX application components, APEXlang syntax...
- [oke-troubleshooter](../oke-troubleshooter/SKILL.md) — Use when the user wants to diagnose or root-cause issues with an OCI Kubernetes Engine clu...
- [oke-gva-deployer](../oke-gva-deployer/SKILL.md) — Use when the user asks to enable, deploy, or configure Generic VNIC Attachment (GVA) for O...
- [oci-functions-deploy](../oci-functions-deploy/SKILL.md) — Use when asked to validate/install Fn, OCI CLI, and Docker, configure or create Fn context...

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [oracle/skills](https://github.com/oracle/skills)
- Path: `_sources/oracle_skills/oci/iot-platform/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
