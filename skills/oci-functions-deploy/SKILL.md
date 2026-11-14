---
name: oci-functions-deploy
description: Use when asked to validate/install Fn, OCI CLI, and Docker, configure or create Fn contexts, validate OCI session and Docker registry auth from Fn context values, choose or create a Functions application, scaffold Java, Python, or Node functions, and deploy them.
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

# OCI Functions Deploy

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Asked to validate/install Fn, OCI CLI, and Docker, configure or create Fn contexts, validate OCI session and Docker registry auth from Fn context values, choose or create a Functions application, scaffold Java, Python, or Node functions, and deploy them

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Local macOS/Linux workstation flow for OCI Functions: validate or install `fn`, `oci`, and Docker; configure Fn contexts; verify OCI session and registry auth; pick or create an application; scaffold and deploy Java, Python, or Node functions. Windows automation and OCI Cloud Shell are out of scope — handle those manually rather than reusing this flow blind. Additional OCI Functions runtimes exist but are not scaffolded or deployed automatically here.

Resolve every value with this precedence: explicit user values from chat or script flags, then the active Fn context, then values derived from already-resolved inputs, then OCI/CLI defaults.

Execution modes: `interactive` gathers confirmations through terminal prompts; `agent-mediated` confirms per command and single-use, requiring `CONFIRM_RESPONSE=yes`, a matching `CONFIRM_ACTION_ID`, and the nonce emitted for that exact mutation in `CONFIRM_NONCE`.

## Read versus mutate

`read` — dependency checks, context inspection, session validation, registry auth inspection, app listing, dry-run validation: run without confirmation. `mutate` — install/start, context create/update, Docker login, app creation, advanced network creation, `fn init`, `fn deploy`: require confirmation. When a command is ambiguous, treat it as mutating.

| Step | Class | Confirm |
| --- | --- | --- |
| Dependency, context, session, registry-auth checks | read | no |
| Install missing `fn`/`oci`/`docker`, start Docker | mutate | yes |
| Create/update Fn context, Docker login | mutate | yes |
| Create Functions app, advanced network creation | mutate | yes |
| `fn init`, `fn deploy` | mutate | yes |

## Confirmation interface

Mutating scripts use `confirm_gate.sh --description <text> [--display <text>] [--cwd <path>] [--stdin-env <env>] [--nonce <nonce>] [--machine-readable] -- <argv...>`.

Run argv directly rather than through `bash -c`; use `--cwd` instead of embedding `cd … && …`; use `--stdin-env` for `docker login --password-stdin`. Agent-mediated approvals are single-use — replaying an action id and nonce after a successful mutation is invalid. Interactive prompts mint a fresh 128-bit nonce per mutation so the same command can be approved again later. Descriptions and caller display text are shell-escaped for review, but execution always uses the original argv array.

Linux Fn installation resolves the latest non-draft, non-prerelease GitHub release before confirmation, binds the approval to that release's canonical asset URL and GitHub SHA-256 digest, and revalidates metadata, digest, and binary version before privileged install; it never executes a downloaded shell installer. That path needs `curl`, `python3`, and `sha256sum` or `shasum` — install a missing prerequisite first. Verified installation still trusts the official `fnproject/cli` repository and release publisher.

## Function name rules

A name counts as `provided` only when the user explicitly names it ("name it…", "call it…", "function name is…", or `--function-name`). Descriptive phrases such as "hello world function", "sample function", or "python function" describe intent and must never become a name automatically, and a descriptive phrase must never be slugified into one without asking. Suggesting a derived name is fine; using it requires explicit confirmation.

States: `missing` (nothing explicit or prompted yet), `explicit` (named in chat or via `--function-name` with `--function-name-source explicit`), `prompted` (gathered or confirmed through a prompt). Pass `--function-name` to `build_and_deploy.sh` only when the state is `explicit` or `prompted`; if a likely name was inferred from prose, keep `missing` and ask.

## Workflow

1. **Dependencies.** `scripts/preflight_check.sh --runtime <java|python|node>` detects `fn`, `oci`, and Docker. Install missing tools with `scripts/install_missing.sh --tool <fn|oci|docker>`, and start a stopped daemon with `--tool docker-daemon` — each behind confirmation.
2. **Fn context.** `fn inspect context` is the primary source for `oracle.profile`, `oracle.compartment-id`, `api-url`, and `registry`. If the context is missing or incomplete, collect only the gaps and run `scripts/configure_context.sh` (the deliberate mutation path for applying explicit overrides). Support `oracle.image-compartment-id` only when the user supplies it or an existing context carries it.
3. **OCI session.** Validate using the profile from the Fn context. On a retryable security-token error, prompt and retry with `security_token` auth before reporting failure; stop if auth stays invalid. Any nonzero CLI exit is `error` unless the command succeeded and an empty result positively proved absence.
4. **Docker registry.** Derive the registry host from the context `registry` and run a live, non-mutating probe before claiming auth is valid. Treat cached credentials as `cached`, not `valid`, when the probe cannot confirm them. If auth is missing or still insufficient, prompt for OCIR credentials and run `scripts/configure_context.sh --ocir-username … --ocir-auth-token …` or an equivalent login.
5. **Application.** Run `scripts/discover_state.sh` once prerequisites are valid, then list Functions apps in the context compartment. If apps exist, ask explicitly whether to reuse one or create a new one; reuse keeps the chosen name/id. Resolve user-selected names by fetching OCI JSON and comparing `display-name` exactly — never interpolate names into JMESPath, and stop on duplicate exact matches rather than picking arbitrarily. Creation supports 1–3 subnet OCIDs, an optional shape (`GENERIC_X86`, `GENERIC_ARM`, `GENERIC_X86_ARM`), and optional NSG attachment; shape and NSG are create-only, so do not silently ignore them on a reuse path. Do not infer VCN/subnet creation from ordinary app selection. Enter the advanced network branch only when the user explicitly asks for network setup or explicitly opts into infrastructure creation; non-interactive creation needs an explicit branch flag plus explicit topology, names, and CIDRs. Do not claim to auto-validate registry/subnet regional alignment — surface it as a manual check when explicit network inputs mix with an existing registry. If `app_name` matches an existing app but `app_choice` was never stated, prompt interactively and fail non-interactively; never silently reuse.
6. **Scaffold.** Ask for the function name unless explicitly given, and for the runtime if not explicit (scope: `java`, `python`, `node`). Run `scripts/build_and_deploy.sh --runtime <runtime> --app <app-name> --function-dir <path> --function-name <name> --function-name-source <explicit|prompted>`. Scaffolding runs `fn init` only after prerequisites and app choice are complete. Derive a default directory only after the name is confirmed. If the target directory exists, is non-empty, and lacks `func.yaml`, stop and ask for a different directory rather than running `fn init` in place.
7. **Deploy.** Run `fn deploy` only after successful scaffolding. On failure, surface it and stop — never rewrite image references automatically. If the push to OCIR fails, call out repository-compartment and auto-create edge cases, and recommend pre-creating the repository or setting `oracle.image-compartment-id` when the output points that way.

## Confirmation and collection order

Use `scripts/confirm_gate.sh` for mutating commands only; read-only steps run automatically. In non-interactive runs, mutations proceed only with explicit per-command approval, and `CONFIRM_RESPONSE=yes` without a matching action id and nonce is invalid.

Prompt for missing values only after discovery, in this order: dependency install/start approvals; missing Fn context values; security-token retry approval; OCIR login inputs (only if not logged in); the reuse-versus-create decision when apps exist; app inputs (only if creating); advanced-network approval and inputs (only on explicit opt-in); function name and runtime (only if not provided), preserving name provenance.

## Machine-readable contract

Lowercase snake_case only. With `--machine-readable`, helper scripts emit only `key=value` lines on stdout, move human logs to stderr, and downstream parsers rely on documented keys only; keys are validated as lowercase snake case and values containing control characters are rejected.

State families: `dependency_{fn,oci,docker,java,mvn,python3,node,npm}_state` = `found|missing`; `docker_daemon_state` = `running|stopped|missing|error`; `fn_context_state` = `found|missing|incomplete|error`; `apps_state`/`vcns_state` = `found|empty|error`; `app_state` = `found|missing|incomplete|error`; `oci_cli_state`/`compartment_state`/`discovery_state`/`network_state` = `found|missing|error`; `oci_auth_state`/`docker_registry_auth_state`/`ocir_auth_state`/`docker_registry_auth_probe_state` = `valid|cached|missing|error`; `confirm_state` = `approved|skipped|error`; `app_action`/`deploy_action` = `reuse|create|deploy|skip|error`; `deploy_preflight_state` = `passed|skipped`; `install_state` = `success|error`; `function_name_state` = `explicit|prompted|missing`.

Companion fields include `*_error_reason` (`auth_or_permission`, `runtime_or_cli`, `network_or_transport`, or a documented specific reason), `oci_auth_error`, `fn_context_missing_keys`, `confirm_action_id`, `confirm_nonce`, `oci_auth_mode`, `oci_auth_retry_state`, `oci_profile`, `oci_profile_source`, `docker_registry_host`, `fn_context_name`, `fn_context_provider`, `fn_context_profile`, `fn_context_compartment_id`, `fn_context_api_url`, `fn_context_registry`, `fn_context_image_compartment_id`, `region`, `compartment_id`, `profile`, `app_id`, `app_name`, `apps_count`, `app_item_<n>`, `vcn_id`, `subnet_id`, `install_method`, `function_name`.

Hard rules: no uppercase env-style keys; never `unknown`; successful empty collections are `empty`; failed CLI/runtime operations are `error`.

## Decision table

| Target | found | missing/empty | error |
| --- | --- | --- | --- |
| VCN / subnet | Reuse only in the explicit advanced branch | Stay in the default flow; collect inputs only after branch approval | Stop, escalate |
| Functions app | Require an explicit reuse-versus-create decision | Create with confirmation; 1–3 subnets, optional shape/NSG | Stop, escalate |
| Fn context | Reuse active values unless explicitly overridden | Create or fill with confirmation | Stop, escalate |
| OCI session | Validate with `oracle.profile` | Retry with `security_token` after approval, then stop | Stop, escalate |
| OCIR login | Reuse after a live probe, else report `cached` | Prompt only if needed, then confirm | Stop, escalate |
| OCIR repo/compartment | Reuse when deploy succeeds | On push failure, surface auto-create and `oracle.image-compartment-id` | Stop, escalate |
| Function name | Reuse only when explicitly named | Ask and confirm; never infer from prose | Stop, ask again |

## Advanced network branch

Only after explicit approval to create or repair Functions networking. Prefer a private-first topology as a security baseline rather than an OCI requirement; keep subnets regional and private; use service-gateway routing to the Oracle Services Network for OCIR access in private topology, or an internet-gateway route (`0.0.0.0/0`) for public topology. Accept any egress shape that genuinely permits the required registry/service access rather than narrowing a valid broader rule, and treat CIDR sizing guidance as sizing advice, not a pass/fail gate. See `references/functions-vcn-requirements.md`, `references/cidr-sizing.md`, and `references/oci-functions-quickstart.md`.

## Runtime matrix and guardrails

Automated runtimes: `java` (needs `java`, `mvn`), `python` (needs `python3`), `node` (needs `node`, `npm`). `scripts/preflight_check.sh` validates dependencies, context completeness, session state, and registry auth before scaffolding. Run strict preflight before scaffold/deploy; `--skip-preflight` must still pass a confirmation gate carrying high-risk warning text. In `--machine-readable` mode emit only lowercase state lines on stdout, and emit `function_name_state` and `function_name` before scaffolding so inferred-name bugs show up in logs.

## Sources

- https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsquickstartlocalhost.htm
- https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionscreatingapps.htm
- https://docs.oracle.com/en-us/iaas/tools/oci-cli/latest/oci_cli_docs/cmdref/fn/application/create.html
- https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionscreatingvcn.htm
- https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionscidrblocks.htm
- https://docs.oracle.com/en-us/iaas/tools/oci-cli/latest/oci_cli_docs/cmdref/network/vcn/create.html
- https://docs.oracle.com/en-us/iaas/Content/Registry/Tasks/registrypushingimagesusingthedockercli.htm

## Verification

- [ ] Every mutation passed `confirm_gate.sh`; read-only steps ran freely.
- [ ] Value precedence respected; context values used unless explicitly overridden.
- [ ] Function name state `explicit` or `prompted` before scaffolding.
- [ ] App choice explicit; no silent reuse of a name-matched app.
- [ ] Machine-readable keys lowercase snake_case, no `unknown`.
- [ ] Deploy failures surfaced, not papered over with rewritten image references.

## Related Skills in This Repo

- [apexlang-inventory](../apexlang-inventory/SKILL.md) — Use when working with provides an overview of APEX application components, APEXlang syntax...
- [oke-troubleshooter](../oke-troubleshooter/SKILL.md) — Use when the user wants to diagnose or root-cause issues with an OCI Kubernetes Engine clu...
- [oke-gva-deployer](../oke-gva-deployer/SKILL.md) — Use when the user asks to enable, deploy, or configure Generic VNIC Attachment (GVA) for O...
- [oke-cluster-generator](../oke-cluster-generator/SKILL.md) — Use when the user asks to build, generate, create, design, or scaffold an OKE (OCI Kuberne...
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
- Path: `_sources/oracle_skills/oci/functions/oci-functions-deploy/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
