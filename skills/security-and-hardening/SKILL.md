---
name: security-and-hardening
description: Use when auditing an input handler for vulnerabilities, when handling user input, authentication, data storage, or external integrations, or when checking a login flow is safe against the OWASP Top Ten; building any feature that accepts untrusted data, manages user sessions or session cookies, or interacts with third-party services; auditing dependencies for known vulnerabilities, triaging package-manager audit findings, or assessing supply-chain risk in a new package; personal data or privacy compliance (GDPR, CCPA) is involved.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [software-development, engineering, agent-skills, security, hardening]
    source: addyosmani/agent-skills
    adapted: true
---

# Security and Hardening

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Auditing an input handler for vulnerabilities, when handling user input, authentication, data storage, or external integrations, or when checking a login flow is safe against the OWASP Top Ten
- Building any feature that accepts untrusted data, manages user sessions or session cookies, or interacts with third-party services
- Auditing dependencies for known vulnerabilities, triaging package-manager audit findings, or assessing supply-chain risk in a new package
- Personal data or privacy compliance (GDPR, CCPA) is involved

## When NOT to Use

- User input passed directly to database queries, shell commands, or HTML rendering
- A delete, move, or overwrite whose target comes from a payload, a config value, or another process's command line, guarded only by a shape check on the path
- Secrets in source code or commit history
- API endpoints without authentication or authorization checks
- Missing CORS configuration or wildcard (`*`) origins
- No rate limiting on authentication endpoints, or an in-memory limiter in front of more than one instance
- Stack traces or internal errors exposed to users
- Dependencies with known critical vulnerabilities, competing lockfiles at one installation boundary, non-reproducible installs, or blanket-approved scripts
- Server fetches user-supplied URLs without an allowlist (SSRF)
- LLM/model output passed into a query, the DOM, a shell, or `eval`
- Secrets, PII, or the full system prompt placed inside an LLM context window
- Personal data collected with no stated purpose, retention limit, or deletion path
- PII sent to analytics/ad/LLM vendors with no consent or data-processing agreement
- "Delete my account" that only flips a flag while the personal data lingers in stores and backups

## Overview

Treat every external input as hostile, every secret as sacred, and every authorization check as mandatory. Security is not a phase but a constraint on every line that touches user data, authentication, or external systems.

## Threat model first

Controls bolted on without a threat model are guesses. Spend five minutes thinking like an attacker:

1. **Map the trust boundaries** — anywhere untrusted data crosses in: HTTP requests, form fields, uploads, webhooks, third-party APIs, queues, and **LLM output**, plus values that look internal only because the OS delivered them (another process's command line or environment, filenames on a shared volume, a job-payload path). Trust follows who *wrote* a value, not which channel carried it.
2. **Name the assets** — credentials, PII, payment data, admin actions, money movement.
3. **Run STRIDE per boundary:**

| Threat | Ask | Mitigation |
| --- | --- | --- |
| Spoofing | Can someone impersonate a user or service? | Authentication, signature verification |
| Tampering | Can data change in transit or at rest? | Integrity checks, parameterized queries, HTTPS |
| Repudiation | Can an action be denied later? | Audit logging of security events |
| Information disclosure | Can data leak? | Encryption, field allowlists, generic errors |
| Denial of service | Can it be overwhelmed? | Rate limiting, size caps, timeouts |
| Elevation of privilege | Can a user gain rights they should not have? | Authorization checks, least privilege |

4. **Write abuse cases next to use cases** — for each feature ask how you would misuse it, and make that the first test.

If you cannot name a feature's trust boundaries, you are not ready to secure it (OWASP A06:2025 Insecure Design — most breaches begin in design, not code).

## Three tiers of rules

**Always do:** validate all external input at the boundary; parameterize every query and never concatenate input into SQL, NoSQL, or shell; encode output through framework auto-escaping; use HTTPS externally; hash passwords with bcrypt/scrypt/argon2; set CSP, HSTS, `X-Frame-Options`, and `X-Content-Type-Options`; use `httpOnly`, `secure`, `sameSite` session cookies; run the package manager's native audit against the committed lockfile before each release.

**Ask first:** new or changed authentication flows; storing new categories of sensitive data; new external integrations; CORS changes; upload handlers; rate-limit changes; elevated permissions or roles.

**Never:** commit secrets; log sensitive data; treat client-side validation as a boundary; disable security headers for convenience; use `eval()` or `innerHTML` with user data; store sessions in client-accessible storage; expose stack traces or internal errors to users.

## Hardening controls

Concrete implementations live in `references/hardening-patterns.md`; open the relevant section when you reach that code.

**Injection, XSS, access control.** Parameterize every query; never build SQL, NoSQL, or shell from input strings. Encode output via auto-escaping, and sanitize with an allowlist sanitizer if raw HTML is unavoidable. Check **authorization** on every request, not just authentication — the caller must own or be permitted on the specific resource (A01:2025, IDOR).

**Authentication and sessions.** Hash with bcrypt (≥12 rounds), scrypt, or argon2; the session secret comes from the environment. Cookies are `httpOnly`, `secure`, `sameSite: 'lax'` or `'strict'` (the CSRF defense — `'none'` sends the cookie cross-site), with a bounded `maxAge`.

**Headers, CORS, responses.** Security headers on every response; CSP starts at `default-src 'self'` and is tightened, never loosened. CORS is an explicit origin list from configuration, never `*` with credentials. Strip sensitive fields before responding, and keep error bodies generic while internals go to server logs.

**Validation and uploads.** Validate at the boundary with a schema — allowlisted shape, lengths, enums, formats — reject with 422 and structured details, and let downstream code use only the parsed typed value. For uploads, allowlist MIME types, cap size, and verify content by magic bytes; the extension proves nothing.

**SSRF.** Any user-influenced URL (webhooks, import-from-URL, image proxies, link previews) can be aimed inward. Allowlist scheme and host, resolve **all** DNS records and reject private or reserved addresses (loopback, link-local `169.254.169.254`, private, unique-local — IPv4 and IPv6), and forbid redirects. That still leaves a DNS-rebinding TOCTOU gap: for high-risk surfaces, pin the resolved IP or place a filtering agent in front.

**Destructive operations on derived paths.** A delete, move, or overwrite is only as safe as the value naming its target, and trust follows who *wrote* it — another process's command line is as attacker-controlled as a form field. A shape check proves well-formedness, not authorization. Before the call require all three: the resolved target (symlinks resolved) sits under an **allowlisted root**, it is at least one level **below** that root, and it carries **ownership evidence read before the operation**. On refusal, log the rejected target and stop; never fall back to a broader default path. See `references/hardening-patterns.md#destructive-operations-on-derived-paths` for why marker self-attestation and check/use races weaken this, and `references/security-checklist.md` for worked code.

**Rate limiting.** Limit the API generally and auth endpoints strictly (about 10 attempts per 15 minutes). Once more than one process serves traffic, in-memory counters silently become `max × instances` or never fire on serverless — back the limiter with a shared store.

**Secrets.** From the environment; `.env.example` committed with placeholders; real `.env*` and key material gitignored; grep the staged diff before committing. A secret that reaches a remote is compromised the moment it lands — rotate first, then purge history.

**Dependencies and supply chain.** (1) Find the installation boundary and manager: the workspace root owning the lockfile, or a nested project only when it sits outside that workspace; corroborate `packageManager`, lockfile, and CI, and stop on disagreement or competing lockfiles. (2) Block dependency scripts before first execution: bootstrap with scripts disabled or a documented fail-closed policy, inspect the pending script source, approve only the minimum, commit the policy, then verify with a clean frozen install — never blanket-approve. (3) Run the native audit against the committed lockfile before every release; triage critical/high by reachability and fix availability; never apply forced remediation automatically (`npm audit fix --force` can cross declared ranges) — preview, read changelogs, test each upgrade, and document deferrals with a reason and review date. (4) Audits match known advisories only, so a newly malicious or typosquatted package (`cross-env` vs `crossenv`) slips through — review new dependencies, lockfile diffs, and script-policy changes together for ownership, maintenance, release age, provenance, and the transitive graph; verify registry signatures where supported and treat their absence as a signal to investigate, not proof of compromise (A03:2025, LLM03). See the triage tree in `references/hardening-patterns.md#dependency-audit-triage`.

**Personal data and privacy.** Hardening asks "can an attacker read it?"; privacy asks "should we hold it at all, and for how long?" The cheapest data to protect, breach, and comply over is data you never collected. Classify fields as you add them (non-personal, PII, sensitive) and handle each class accordingly — you cannot protect or delete what you cannot find. Collect only against a stated purpose; keep PII out of telemetry. Set retention up front and then actually delete, including backups, caches, search indexes, and analytics copies. Support the data-subject rights your jurisdiction requires (GDPR, CCPA, and kin): export, correct, delete — design the schema so a user's data is findable and erasable. Consent gates collection and third-party sharing and is auditable; sending PII to an analytics, ad, or LLM vendor is sharing and needs a data-processing agreement. Make region a configurable policy, not a hardcoded assumption. See `references/hardening-patterns.md#data-classification`; run a privacy incident's postmortem with the debugging skill.

**AI/LLM features.** Map them to the OWASP Top 10 for LLM Applications (2025): model output is untrusted input (LLM05) — never into `eval`, SQL, a shell, `innerHTML`, or a file path; parse defensively, validate against a schema, then encode. Prompts can be hijacked (LLM01): untrusted text in context (a user message, a fetched page, a PDF) can carry instructions, and the system prompt is not a security boundary — enforce permissions in code. Keep secrets, other tenants' data, and the full system prompt out of the context window (LLM02, LLM07); scope tool permissions, validate every tool argument, and confirm destructive actions (LLM06); cap tokens, request rate, and recursion depth (LLM10); partition RAG embeddings per tenant and validate documents before indexing (LLM08). See `references/hardening-patterns.md#llm-output-handling`.

## Review

Before sign-off walk `references/security-checklist.md` — authentication, authorization, input, data protection and privacy, headers and CORS, dependencies and supply chain, AI/LLM, error handling, plus the OWASP quick-reference tables.

## Red flags

- Input reaching queries, shell commands, or HTML rendering unparameterized
- A delete/move/overwrite whose target comes from a payload, config value, or another process's command line, guarded only by a path-shape check
- Secrets in source or history; missing authentication or authorization on endpoints
- Missing CORS configuration or wildcard origins; no rate limiting on auth, or an in-memory limiter behind multiple instances
- Stack traces exposed; reachable critical/high dependency findings, competing lockfiles, non-reproducible installs, blanket-approved scripts
- User-supplied URLs fetched without an allowlist (SSRF)
- LLM output reaching a query, the DOM, a shell, or `eval`; secrets, PII, or the full system prompt inside an LLM context
- Personal data with no stated purpose, retention limit, or deletion path; PII sent to vendors without consent or a DPA
- "Delete my account" that flips a flag while data lingers in stores and backups

## Verification

- [ ] Native audit shows no unmitigated reachable critical/high findings; CI preserves the authoritative lockfile and blocks unreviewed dependency scripts.
- [ ] No secrets in source or git history.
- [ ] All user input validated at boundaries.
- [ ] Destructive filesystem operations resolve symlinks, then verify allowlisted root, minimum depth, and ownership.
- [ ] Authentication and authorization on every protected endpoint.
- [ ] Security headers present (check with browser DevTools); errors expose nothing internal.
- [ ] Rate limiting active on auth endpoints and backed by a shared store when multiple instances serve traffic.
- [ ] Server-side URL fetches validated against an allowlist (no SSRF).
- [ ] LLM output validated and encoded before use, where AI features exist.
- [ ] Personal data classified, minimized to a stated purpose, and given a retention limit.
- [ ] Deletion and export work end-to-end, including backups, caches, and analytics copies.

## Related Skills in This Repo

- [code-review-and-quality](../code-review-and-quality/SKILL.md) — Use when reviewing code written by yourself, another agent, or a human; you need to assess...
- [ci-cd-and-automation](../ci-cd-and-automation/SKILL.md) — Use when setting up or modifying build and deployment pipelines; you need to automate qual...
- [api-and-interface-design](../api-and-interface-design/SKILL.md) — Use when designing APIs, module boundaries, or any public interface; creating REST or Grap...
- [git-workflow-and-versioning](../git-workflow-and-versioning/SKILL.md) — Use when making any code change; committing, branching, resolving conflicts, splitting unc...
- [docker-security-hardening](../docker-security-hardening/SKILL.md) — Use when hardening Docker containers and images.
- [docker-security](../docker-security/SKILL.md) — Use when securing Docker containers.
- [windows-firewall-management](../windows-firewall-management/SKILL.md) — Use when configuring Windows Firewall via PowerShell.

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Upstream anti-patterns retained as the When-NOT-to-Use list.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- Path: `_sources/addyosmani_agent-skills/skills/security-and-hardening/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
