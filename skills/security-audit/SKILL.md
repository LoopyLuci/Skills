---
name: security-audit
description: Use when security questions, focused reviews, vulnerability research, security audits, or pen tests.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [security, auditing, appsec, vulnerability-research, audit, pentest]
    source: cloudflare/security-audit-skill
    adapted: true
---

# Security Audit

> **Adapted for the LoopyLuci Skills collection** from [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Security questions, focused reviews, vulnerability research, security audits, or pen tests

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Find vulnerabilities that cross a real trust boundary, then hand owners source evidence, safe reproduction, priority, and the smallest effective fix. This is a defensive, source-first workflow: a candidate without a concrete affected principal, resource, or security outcome is not a confirmed finding.

## Operating modes

Loading this skill is guidance by default and authorizes neither the full workflow nor file creation.

- **Guidance mode** — for security questions, focused reviews, methodology, triage, or investigating specific findings, use only the relevant parts. Do not run all six phases, create an output directory, or write artifacts. Focused agents may be launched; their results return to the current task.
- **Full audit mode** — when the user explicitly asks to audit or pen-test a codebase, requests a full/comprehensive/end-to-end review, or asks for report artifacts. Run all six phases and write the defined files.

If the request could mean either, ask one focused question before creating files or starting the workflow.

## Terminology and safety

Agent-neutral terms: **parent** coordinates the run and owns shared state; **task tool** is the platform's delegation mechanism; **`research` agent** explores source and verifies facts; **`general` agent** investigates broadly with bounded local execution. A `subagent_type:` heading names which role runs that work — preserve role, write-isolation, prompt, and independence boundaries when mapping to equivalent platform capabilities.

Source inspection is read-only. Run target-controlled builds, tests, processes, browsers, emulators, fuzzers, and fixture processing only inside an OS-enforced sandbox providing all of: no external network (isolated loopback only when local client/server traffic is needed); an empty environment populated from an explicit allowlist with safe values plus scratch-local `HOME`, temp dirs, and caches; a read-only target and toolchain with writes confined to the assigned `scratch/`; and explicit CPU, memory, process, file-size, disk, and wall-clock limits.

The agent may make a disposable source copy in `scratch/` when a build must write beside source. In guidance mode, retain no target-controlled files. In full audit mode, only trusted parent-side code may promote the minimum non-secret result to retained `artifacts/`, using the write-isolation procedure below. Never expose a retained output directory (other than the agent's own `scratch/`), another agent's directory, the host home, credentials, sockets, or shared services to target code. Do not install dependencies or let builds fetch them — use only what is already local. If a control cannot be enforced, do not execute target code: report the missing sandbox capability as a needs-validation blocker with a safe validation plan.

Use dummy principals, fixtures, and secrets. Never probe deployed endpoints, external services, shared infrastructure, production identities, other users' data, or live control planes; do not test availability against a live or shared process, publish artifacts, alter releases, spend paid quota, or go beyond the minimum local effect needed to establish a defect. If the decisive fact lies outside source or the sandbox, report it as needing validation.

## Full audit setup

Resolve before reconnaissance: the absolute **skill directory**; the absolute **target** repository root; a stable **repo name** from the directory or local Git remote; an **output directory** outside the target (default `~/security-audit-skill/<repo-name>/run-<N>`, the next unused integer) — use a directory inside the target only when the user explicitly selects it and the parent verifies version control ignores the whole directory, otherwise stop and request an external path; and the **source ref** (reviewed commit and whether the worktree is dirty — unreviewed generated or modified files are not another revision).

### Write isolation

The parent creates and solely writes the shared run files: `run-metadata.json`, `architecture.md`, `coverage-ledger.json`, `findings.json`, `REPORT.md`, `FINDINGS-DETAIL.md`, `NEEDS-VALIDATION.md`. Each hunter or verifier gets a unique root under `<output-dir>/agents/<agent-id>/` with separate `scratch/` and `artifacts/`. Agent IDs match `^[a-z0-9][a-z0-9_-]{0,63}$` and must not be Windows device names (`con`, `prn`, `aux`, `nul`, `com1`–`com9`, `lpt1`–`lpt9`); lowercase prevents case-fold collisions. The agent and every target-controlled process write only to `scratch/`; retained `artifacts/` is parent-owned, never exposed to the sandbox, and writable only by trusted promotion code. Agents may not change shared files, target source, retained artifacts, or another agent's directory. Do not use `/tmp` or the host home as a writable fallback.

Before execution the parent opens and retains trusted, non-inheritable descriptors for each agent's `scratch/` and `artifacts/` roots and records an allowlist of expected scratch-relative artifact files with per-file and cumulative byte limits; those descriptors are never passed to the agent or sandbox. After the sandbox and its processes terminate, trusted parent-side code promotes each allowlisted file separately: validate the relative path (reject absolute, empty, `.`, `..`, or symlinked components); walk each parent component from the retained scratch-root descriptor with no-follow directory-relative operations, never reopening by path; open the leaf no-follow and nonblocking; `fstat` a regular file with link count exactly one within the recorded limits; re-enforce limits while reading from that descriptor; copy exactly the verified size, re-`fstat`, and reject any changed identity, type, link count, or size; walk the destination parents from the retained artifacts-root descriptor no-follow, requiring real directories and creating missing ones exclusively before verifying no-follow; create the destination leaf exclusively without following links and verify it is a regular file with link count one; copy from the verified source descriptor without reopening either path; use race-safe equivalents on non-POSIX systems; never recursively copy or glob scratch, extract an archive into artifacts, or promote a symlink, FIFO, socket, device, directory, hard link, changing file, or over-bound file; and if any check is unavailable or fails, discard the entry — retaining `needs_validation` with the exact promotion blocker if it is decisive evidence.

`HUNTING.md` and `VALIDATION-AND-REPORTING.md` carry this procedure as one identical fenced block for hunter and verifier prompts, stating the same rules in the same order.

For a reproduced check, record the command, exact test input, sandbox limits, and only the allowlisted environment variable names plus safe non-secret values needed to reproduce it. Never capture the ambient environment, inherited variables, credential values, authentication state, or unrelated host paths — launch from an empty environment rather than redacting afterward.

Before delegation, write `run-metadata.json` with at least `run_id`, `repo`, `target`, `source_ref`, `profile`, `scope_paths`, `budget` (null if unset), `execution_policy: "sandboxed-source-and-local-only"`, selected companion files, prior-run paths, shared-file owners, and `run_status: "in_progress"`. Update it only when those facts change; candidate state belongs in the ledger and `findings.json`.

## Planning: coverage, prior runs, profiles, budget

No single pass is complete. Build a deterministic coverage plan before hunting and update it after every agent result; `RECONNAISSANCE.md` defines the stable coverage units and `HUNTING.md` the coverage-critic waves. Only the parent updates the ledger.

If prior runs exist, read every compatible `coverage-ledger.json` and `findings.json` before planning. Compare the relevant current source with each prior record and unit — a prior source ref alone does not prove a path unchanged. Carry a prior `confirmed` record forward only when its relevant source and conditions are unchanged and its evidence still meets the current contract: link it to a current `planned` unit, preserve its fingerprint, exclude only that carried root cause from hunters, and send it through the current final verification path, where the Phase 3 verifier becomes the unit's assignment owner and moves it to `candidate`. When relevant source changed, create a current planned revalidation unit instead of excluding it; it stays confirmed only if current independent validation establishes the current path and result. Prior `needs_validation`, `deferred`, `blocked`, `out_of_scope`, and changed-source units are all current work — a still-external `needs_validation` record may be carried only after the current source trace is checked and linked by fingerprint to a current `planned` unit whose verifier supplies owner and evidence, keeping the unresolved blocker. Prior states never suppress a current unit. A prior same-source covered unit may inform priority but stays visible in the ledger, and a prior `rejected` record suppresses only the unchanged failed claim, not its unit's coverage. Read the prior profile and scope: a prior `quick` or scoped ledger contributes its recorded evidence and gaps, never an implied "the rest is fine." If no prior ledger exists, say so in the final coverage statement, and never imply one run exhausts the target.

Pick a profile from the request or propose one from the target's size and stakes; record `profile` and `scope_paths` in metadata and state it in the report. Default `standard`. **`quick`** — bounded pass for small targets, re-runs, or a first look: coarsen units to surface × boundary × attack class, run exactly one hunter wave then one final coverage critic, and use one fresh verifier per candidate for both validation and final record verification, with no follow-up hunter wave (critic discoveries become `deferred`). **`standard`** — the workflow as written. **`deep`** — high-stakes or large targets: split units per subsystem and lifecycle mode, run critic waves to a clean pass, keep candidate validation and final record verification as separate fresh agents, and give `prior_covered_same_source` units an independent second pass. A **scoped run** audits a subset (named paths, one subsystem, one companion domain, or a diff between two refs): seed units only for in-scope surfaces and record everything else `out_of_scope`, never `covered`, and present itself as partial coverage. Profiles change breadth and redundancy, never the evidence bar — never scale away the candidate gate, the source/local execution boundary, `needs_validation` discipline, schema validation, or independent verification of confirmed records.

Budget: one unit is roughly one hunter assignment; one surviving candidate is one or two verifier assignments depending on profile. Record `budget` in metadata as a maximum agent-invocation count across all phases. Apply the strict gate before launching any reconnaissance agent: reserve the four baseline reconnaissance calls, one final post-wave critic for `quick` (or one post-wave plus one distinct final-clean critic for `standard`/`deep`), and at least one verifier call; add focused reconnaissance only after re-applying the gate. If the budget cannot fund that minimum, launch nothing — ask for more budget, narrower scope, or a different profile; if unchanged, set `run_status: "incomplete"` with `incomplete_reason: "budget_cannot_fund_reconnaissance_and_reserves"` and report that no pass ran. Spend in order: count reconnaissance, post-wave critics, and the final-clean critic as invocations; reserve critics and validation before hunting (for `standard`/`deep`, reserve one post-wave plus one final-clean critic before every wave, and reserve roughly 30% of the remaining balance for verification); assign hunters in priority order until the hunting allowance is spent, then run the reserved post-wave critic while keeping the final-clean and validation reserves intact; before a later wave, reserve its new post-wave critic again, and if the remainder cannot cover the required critics and validation reserve, launch no hunters, mark that wave's units `deferred` with `budget_cannot_reserve_critics_and_validation`, and let the retained final-clean critic record the gap. Before wave 1, restate the estimate with seeded units, implied hunter count, mandatory critic calls, validation reserve, and whether the budget covers it; if clearly not, propose tighter scope or a coarser profile rather than silently thinning evidence. If later facts consume the final-critic reserve, launch no hunters, defer all planned work, set `run_status: "incomplete"` with `critic_budget_exhausted`, and make no complete-coverage claim. A strict budget can still be exceeded by an unexpectedly large candidate set or a material Phase 5 replacement needing another independent verifier: if the remainder cannot validate every candidate, stop hunting, validate in fingerprint order while budget permits, set `run_status: "incomplete"` with `validation_budget_exhausted`, and keep each unvalidated fingerprint linked to a `candidate` unit with that unresolved reason — never place an unvalidated candidate in `findings.json`, relabel it `needs_validation`, or call the run complete. Phase 6 may produce a partial report only if its first section states that candidate validation is incomplete and lists the affected fingerprints and units. Never exceed a user-set strict budget silently.

## Core principles

**Require a boundary and a result.** For every candidate, name the lower-trust principal, the accepted input or action, the intended control, the crossed boundary, the affected principal or resource, and the concrete observed or owner-observable result. Do not elevate a missing best practice, guessed deployment behavior, generic parser crash, or self-impact into a finding.

**Use bounded local evidence.** Static analysis establishes the source path; sandboxed local tests resolve behavior when all execution controls exist — a minimal function harness, an existing unit test, a small parser fixture, a dummy-tenant integration test, a locally rendered configuration, or a bounded isolated-loopback client. Stop at a wrong return value, an unauthorized dummy record, a sanitizer finding, a policy difference, or another minimum effect; do not extend beyond the minimum boundary result or produce persistence, post-fault, or concealment material.

**Respect source visibility.** Deployment controls, proxy behavior, provider settings, browser headers, identity policy, broker ACLs, packaging, and topology are real controls. If one is required and absent from the repository, assume neither presence nor absence — use `needs_validation` with the exact missing fact and a safe owner-observed or local plan.

**Separate priority from certainty.** Only `confirmed` records get severity. Likelihood and impact must reflect the demonstrated conditions and result, and overall severity cannot exceed demonstrated impact. `needs_validation` is a blocked, source-grounded boundary hypothesis with no severity. Anchors: **critical** — an unauthenticated actor gains code execution, full data-store access, or arbitrary account takeover; **high** — fully defeating an explicit control with real consequences (authentication bypass, cross-tenant read/write, stored script execution affecting other users, authenticated code execution, or unauthenticated remote stop of a shared service); **medium** — a real boundary violation with limited blast radius, uncommon preconditions, or a narrow resource set; **low** — disclosure of non-secret internals, or an effect needing sustained effort for minimal gain; **informational** — a confirmed but minimal-impact observation, useful mainly as a prerequisite in a larger finding. High versus medium: does the result fully defeat an explicit control for an action with real consequences, or only weaken it? If you cannot state the concrete damage, the severity is lower than it feels.

**Recommend the smallest effective source fix.** For each confirmed finding, identify the invariant the code must enforce and the narrowest source change that enforces it at the last trusted decision point. Prefer concrete repository-relative changes and regression tests over generic hardening advice. The audit describes fixes; it never modifies target source.

## Workflow

In full audit mode, follow all six phases in order:

1. **Reconnaissance** — map source, trust boundaries, local build paths, companion selections, prior evidence, and the initial deterministic coverage ledger (`RECONNAISSANCE.md`).
2. **Coverage-led hunting waves** — assign isolated hunters from the ledger and collect structured candidate results (`HUNTING.md`, `ATTACK-CLASSES.md`, selected domain companions).
3. **Candidate validation** — consolidate fingerprints and give every candidate to a fresh source verifier (`VALIDATION-AND-REPORTING.md`).
4. **Structured output** — write all final `confirmed`, `needs_validation`, and `rejected` records to `findings.json`; validate with `report-schema.json` and `validate-findings.cjs`, and validate the coverage claim with `validate-coverage-ledger.cjs`.
5. **Independent record verification** — fresh agents verify final source claims and reconcile corrections or state changes.
6. **Target-neutral report** — derive `REPORT.md`, `FINDINGS-DETAIL.md`, and `NEEDS-VALIDATION.md` from the final records, with no live-probe instructions.

End the run in exactly one of two terminal states: all Phase 6 artifacts written and both validators pass, or `run_status: "incomplete"` with its exact reason and the gap disclosed in the report. Never stop mid-phase.

## Anti-patterns

1. Checklist deviations presented as vulnerabilities.
2. Defense-in-depth advice with no reachable boundary violation.
3. Live or shared-environment testing where bounded local evidence is insufficient.
4. Guessing provider, proxy, browser, identity, or deployment behavior absent from source.
5. Treating intended same-principal authority or self-impact as a cross-boundary result.
6. Reporting a parser or runtime effect stronger than the observed effect.
7. Prose-only hunter results that cannot be deduplicated or verified.
8. Re-reporting carried same-source prior confirmed records, or using them as exemplars that anchor the hunt.
9. Assigning severity to `needs_validation` records.
10. Writing the report before independent verification, or letting prose and JSON disagree.

## Verification

- [ ] Mode confirmed; full workflow authorized only for an explicit request.
- [ ] Sandbox controls all present before any target code runs; otherwise a needs-validation blocker.
- [ ] Shared files parent-owned; agents write only to their `scratch/`, promotions validated.
- [ ] Coverage ledger current, prior runs reconciled, scoped or quick runs labeled partial.
- [ ] Budget gate applied; reserves intact; any overrun disclosed, never silent.
- [ ] Every candidate states boundary, affected principal/resource, and observed result.
- [ ] Severity only on `confirmed` records; `needs_validation` carries no severity.
- [ ] `findings.json` and the coverage ledger pass their validators.
- [ ] Report derived from final records after independent verification, with no live-probe instructions.

## Related Skills in This Repo

- [file-upload-security](../file-upload-security/SKILL.md) — Use when testing file upload.
- [directory-traversal-test](../directory-traversal-test/SKILL.md) — Use when testing directory traversal.
- [csrf-testing-method](../csrf-testing-method/SKILL.md) — Use when testing CSRF.

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill)
- Path: `_sources/cloudflare_security-audit-skill/skills/security-audit/SKILL.md`
- License: MIT — Copyright (c) 2025-2026 Cloudflare, Inc.
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
