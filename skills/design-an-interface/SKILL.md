---
name: design-an-interface
description: Use when designing an API, exploring interface options, or comparing module shapes
tags: [design, architecture, API, sub-agents, review]
related_skills: [codebase-design, improve-codebase-architecture, to-spec]
---

# Design An Interface

Generate multiple radically different interface designs for a module using parallel sub-agents. Based on "Design It Twice" from "A Philosophy of Software Design": your first idea is unlikely to be the best.

## Workflow

### 1. Gather Requirements
Before designing, understand:
- What problem does this module solve?
- Who are the callers? (other modules, external users, tests)
- What are the key operations?
- Any constraints? (performance, compatibility, existing patterns)
- What should be hidden inside vs exposed?

### 2. Generate Designs (Parallel Sub-Agents)
Spawn 3+ sub-agents simultaneously. Each must produce a radically different approach.

Assign each agent a different constraint:
- Agent 1: "Minimize method count - aim for 1-3 methods max"
- Agent 2: "Maximize flexibility - support many use cases"
- Agent 3: "Optimize for the most common case"
- Agent 4: "Take inspiration from a specific paradigm/library"

### 3. Present Designs
Show each design with its interface signature, usage examples, hidden complexity, and trade-offs.

### 4. Compare and Select
Compare designs side by side. Ask: which is deepest? Easiest to use? Most maintainable? Pick one or hybridize.

> **Note**: This skill is deprecated in the original source. Consider using `codebase-design` for deep module vocabulary instead.

## Common Pitfalls

- **Over-designing before understanding requirements**: Jumping to interface designs without first gathering requirements leads to designs that don't solve the actual problem. Always complete the requirements checklist first.
- **Sub-agent designs too similar**: If spawned sub-agents produce similar designs, you lose the benefit of radical comparison. Enforce different constraints per agent.
- **Ignoring what callers actually need**: Designing interfaces without understanding who calls them and how leads to mismatched abstractions.

## Code Examples

```typescript
// Minimal interface approach
interface UserStore {
  get(id: string): Promise<User>;
  set(user: User): Promise<void>;
}

// Flexible approach
interface UserStore {
  find(query: UserQuery): Promise<User[]>;
  findOne(query: UserQuery): Promise<User | null>;
  create(data: CreateUserDTO): Promise<User>;
  update(id: string, data: Partial<User>): Promise<User>;
  delete(id: string): Promise<void>;
}
```

## Verification Checklist

- [ ] Requirements gathered before design started
- [ ] At least 3 radically different designs generated
- [ ] Each design has interface signature, usage example, hidden complexity, and trade-offs
- [ ] User has compared designs and selected one
