---
name: triage
description: Use when triaging incoming issues, feature requests, or bugs for prioritization
tags: [triage, issues, prioritization, bugs, workflow]
related_skills: [qa, to-tickets, wayfinder]
---

# Triage

Triage incoming issues, feature requests, and bug reports. Classify, prioritize, and route each item to the appropriate workflow.

## Process
1. **Classify**: Bug (something is broken), Feature (new capability), Enhancement (improve existing), Question (user needs information)
2. **Prioritize** (P0-P3): P0 blocks release or affects all users, P1 major impact with difficult workaround, P2 moderate impact with workaround, P3 minor or nice-to-have
3. **Route**: Assign labels, add to milestone, assign owner if known
4. **Check for duplicates** before filing new issues

## Out of scope for triage
Some items may be out of scope for the current project. Maintain a clear definition of what belongs and what does not.

## Common Pitfalls

- **Prioritizing without understanding impact**: Urgency without understanding user impact leads to wrong priorities. Always assess severity through the user's eyes.
- **Missing duplicate detection**: Before creating a new issue, search for existing ones. Duplicates fragment the conversation.
- **Triage without routing**: Every triaged item should go somewhere - a milestone, a project board, or at minimum a label. Unrouted items get lost.

## Verification Checklist

- [ ] Issue classified (bug/feature/enhancement/question)
- [ ] Priority assigned (P0-P3)
- [ ] Duplicate check performed
- [ ] Labels applied appropriately
- [ ] Issue routed to milestone or project board
