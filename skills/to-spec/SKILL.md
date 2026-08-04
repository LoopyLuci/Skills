---
name: to-spec
description: Use when turning a design discussion into a formal specification document
tags: [specification, documentation, design, planning, requirements]
related_skills: [to-tickets, to-questionnaire, design-an-interface]
---

# To Spec

Turn a design discussion into a formal specification document. Capture requirements, acceptance criteria, and design decisions in a structured format.

## Process
1. **Extract requirements** from the conversation
2. **Define acceptance criteria** for each requirement (must be testable)
3. **Document design decisions** with rationale
4. **Write the spec** to a file in the project
5. **Validate** with the user before proceeding to implementation

The spec serves as the source of truth that tickets are created from and code is reviewed against.

## Common Pitfalls

- **Spec that is too detailed too early**: High-level specs should leave room for implementation decisions. Over-specifying creates friction.
- **Spec that is too vague to implement**: Acceptance criteria must be testable. 'Fast enough' without a number is not an acceptance criterion.
- **Writing spec without user verification**: Always validate the spec with the user before moving to tickets. A spec that does not match what they wanted creates rework.

## Verification Checklist

- [ ] Requirements captured from discussion
- [ ] Acceptance criteria are testable
- [ ] Design decisions documented with rationale
- [ ] Spec validated with user
- [ ] Spec saved to project docs directory
