---
name: repository-documentation
description: Produce complete repo documentation sets; verify first.
version: 0.1.0
tags: [documentation, repository-maintenance]
related_skills: [verification-first-development]
---

# repository-documentation

Class-level skill: produce a complete, coherent documentation set for a repository, and verify that set against the repository's own checks before reporting it done.

## When to use
- The user asks for "complete, proper documentation" for a repo (PLAN, SPEC, TODO, AGENTS.md, HANDOVER, CONTRIBUTING, SECURITY, CHANGELOG, docs/adr, etc.).
- Any task whose deliverable is a documentation set, not a code change.

## Procedure (in order)
1. **Scope the state.** Read the repo: branch and clean status (git status), recent commits (git log), manifest (pyproject.toml / package.json / go.mod), README, and any pre-existing PLAN / SPEC / TODO / AGENTS / HANDOVER / docs/adr files. If a set already exists, extend it; do not duplicate it.
2. **Verify the artifact first.** Run the project's own checks before describing it: unit suite, static/type checks, format target. The docs must describe what is actually there and green.
3. **Pick the set.** Approve a target file set consistent with the class. For a repo deliverable the canonical set: PLAN.md (status / vision / goals / architecture / phases), SPEC.md (CLI schema / data model), TODO.md (prioritized backlog with acceptance criteria), AGENTS.md (agent conventions), HANDOVER.md (onboarding), CONTRIBUTING.md, SECURITY.md, CHANGELOG.md, docs/adr/ (index + one file per decision). If the repo's conventions differ, keep the structured core (status, goals, checks, verification by the project's own commands) and prune only what the repo does not use.
4. **Write.** Ground every claim in files you actually read. Describe behavior, not vibes. Each doc earns its place in the set; do not repeat the same content across files.
5. **Verify the set.** Run the structural checks in references/verification-checklist.md and re-run the project's own checks one final time; confirm the docs' claims (e.g., test counts) match actual output.
6. **Report.** State what exists now, what is verified, and what is left (pending items with status). Do not claim done without the run behind it.

## Always-on rules (standing user preferences for this class)
- "Properly proceed with all in order" = full implementation, no stubs, verification-first. The deliverable is a working artifact backed by real tool output, never a description of one.
- Docs describe real state including gaps (submodules not initialized, tests that are mock-only, CI absent, open items in TODO) — do not gloss over them.
- Concise prose; each doc earns its place in the set.

## Pitfalls
- **Never lint markdown with an AST parser (ast.parse, etc.).** AST is for code; markdown passes through it as one giant false token and reports fake "errors" (em-dashes, fences). Verify markdown structurally (fence balance) instead.
- **Never claim something is done without running the project's checks and matching the reported numbers to actual output.** If the docs' claims do not match the run, the docs are wrong.
- **For multi-line Python in the terminal, prefer a heredoc** ("python - <<'PY' ... PY") **over** "python -c" **with embedded quotes.** Bash rewrites single-quoted -c strings and $ expansion corrupts them.

## Support files
- references/verification-checklist.md — structural verification procedure for a documentation set (fence balance, link integrity, claim vs. actual, no stub declarations, current-state honesty).