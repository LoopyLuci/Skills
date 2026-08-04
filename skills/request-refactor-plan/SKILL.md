---
name: request-refactor-plan
description: Use when planning a refactor, requesting a refactoring RFC, or breaking refactors into commits
tags: [refactoring, planning, commits, GitHub, RFC]
related_skills: [improve-codebase-architecture, to-spec, codebase-design]
---

# Request Refactor Plan

Create a detailed refactor plan with tiny, safe commits via user interview, then file it as a GitHub issue. Follow Martin Fowler's advice: make each refactoring step as small as possible, so you can always see the program working.

## Steps

1. Ask the user for a long, detailed description of the problem and any potential ideas for solutions.
2. Explore the repo to verify their assertions and understand the current state.
3. Ask whether they have considered other options, and present alternatives.
4. Interview the user about the implementation. Be extremely detailed and thorough.
5. Hammer out the exact scope: what to change and what not to change.
6. Check for test coverage in the affected area. If insufficient, ask about testing plans.
7. Break the implementation into a plan of tiny commits.
8. Create a GitHub issue with the refactor plan template.

## Common Pitfalls

- **Skipping codebase verification**: Always verify the user's assertions about the codebase before planning. Misunderstandings compound into wrong plans.
- **Commits that are too large**: Each commit should leave the codebase in a working state. If a commit description spans multiple concerns, it is too big.
- **Insufficient test coverage**: Do not plan refactors in areas without test coverage without asking about testing strategy.

## Verification Checklist

- [ ] User's assertions verified against actual codebase
- [ ] Alternative options discussed with user
- [ ] Test coverage assessed for affected areas
- [ ] Implementation broken into tiny, working commits
- [ ] GitHub issue created with the refactor plan
