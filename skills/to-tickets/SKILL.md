---
name: to-tickets
description: Use when breaking a spec into actionable tickets or issues for implementation
tags: [tickets, issues, planning, agile, project-management]
related_skills: [to-spec, triage, qa]
---

# To Tickets

Break a specification into actionable, granular tickets. Each ticket represents a single unit of work with clear acceptance criteria.

## Process
1. **Review the spec** - understand the full scope
2. **Identify independent units** of work that can be done separately
3. **Declare blocking edges** - what each ticket depends on and what depends on it
4. **Write acceptance criteria** for each ticket
5. **Order by dependency chain** - blockers first

For local tracking, use one file per ticket under `.scratch/<feature>/issues/`.
For real trackers, use native blocking links between issues.

## Common Pitfalls

- **Tickets that are too large**: A ticket should represent a single unit of work. If it cannot be completed in one sitting, split it.
- **Tickets without blocking edges declared**: Each ticket should declare what it blocks and what blocks it. Without this, parallel work is impossible to coordinate.
- **Missing acceptance criteria**: Every ticket needs clear, testable acceptance criteria. 'Works as expected' is not acceptance criteria.

## Verification Checklist

- [ ] Each ticket is a single unit of work
- [ ] Blocking edges declared for each ticket
- [ ] Acceptance criteria are clear and testable
- [ ] Tickets ordered by dependency chain
