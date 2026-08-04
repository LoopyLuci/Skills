---
name: domain-modeling
description: Use when building or sharpening a project's domain model and recording ADRs
tags: [DDD, domain, modeling, ADR, architecture]
related_skills: [ubiquitous-language, codebase-design, domain-driven-design-tactical]
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. Challenge terms, invent edge-case scenarios, and write the glossary and decisions down the moment they crystallize.

## File structure
Most repos have a single context:

```
/
|- CONTEXT.md
|- docs/
|   |- adr/
|       |- 0001-event-sourced-orders.md
|       |- 0002-postgres-for-write-model.md
|- src/
```

Create files lazily - only when you have something to write.

## During the session
- Challenge against the glossary when the user uses a term that conflicts
- Capture edge cases: scenarios that stress the model
- Propose ADRs: record architectural decisions with context, decision, and consequences
- Tie concepts to code locations

## Common Pitfalls

- **Creating files before you have something to write**: Create CONTEXT.md and ADR files lazily - only when you have resolved terms or decisions to record. Empty files are noise.
- **Terms that conflict with existing glossary without flagging**: When the user uses a term that conflicts with what is in the glossary, stop and discuss the discrepancy.
- **Neglecting the single/multi-context distinction**: Most repos have one context, but some need CONTEXT-MAP.md. Applying single-context rules to a multi-context repo creates confusion.

## Code Examples

```markdown
# Example ADR
## ADR-0001: Event-Sourced Order Lifecycle

**Context:** Orders need full audit trail and the ability to replay
state after failures.

**Decision:** Model Order as an event stream:
- OrderCreated, ItemAdded, ItemRemoved, OrderSubmitted, OrderPaid
- Current state is folded from the stream
- No mutable state table

**Consequences:**
- (+) Full audit trail by design
- (+) Temporal queries are free
- (-) More complex read-model projection needed
```

## Verification Checklist

- [ ] CONTEXT.md created/updated with resolved terms
- [ ] ADRs recorded for architectural decisions
- [ ] Terminology conflicts resolved with user
- [ ] Single or multi-context structure determined
- [ ] Files created only when content exists to write
