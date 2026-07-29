---
name: hierarchical-swarm-architectures
description: "Use when designing hierarchical multi-agent swarm systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents, swarm, hierarchy, architecture, orchestration]
    related_skills: [agent-swarm-architectures, multi-agent-orchestration, sub-agent-delegation, agent-routing-models, agent-task-decomposition]
---

# Hierarchical Swarm Architectures

Designing multi-level agent swarm systems where agents are organized into hierarchical tiers, each with distinct responsibilities, communication patterns, and decision-making authority.

## When to Use

- Building agent systems with 10+ agents that need structure beyond flat swarms
- Designing systems where different agents operate at different abstraction levels
- Implementing command-and-control or tree-based agent organizations
- Scaling agent systems where flat swarms create coordination overhead
- Building enterprise-grade multi-agent systems with clear responsibility boundaries

## Hierarchy Levels

### Level 1: Executive Layer (Strategists)

One or a few agents that set goals, decompose tasks, and evaluate outcomes.

```
Responsibilities:
- Receive human/mission goals
- Decompose into strategic objectives
- Assign work packages to managers
- Evaluate final results
- Handle exceptions not resolvable below
```

**Key attributes**: Large context window, strong reasoning, tool access for evaluation.

### Level 2: Management Layer (Orchestrators)

Agents that plan, coordinate, and monitor execution across multiple workers.

```
Responsibilities:
- Receive strategic objectives from executives
- Create execution plans with milestones
- Assign tasks to specialist workers
- Monitor progress and detect bottlenecks
- Consolidate results upward
- Resolve inter-worker conflicts
```

**Key attributes**: Planning capability, monitoring tools, coordination protocols.

### Level 3: Worker Layer (Specialists)

Agents that execute concrete tasks with domain-specific knowledge.

```
Responsibilities:
- Execute assigned tasks using domain expertise
- Report progress and results upward
- Request clarification when specifications are ambiguous
- Flag blockers and dependencies
```

**Key attributes**: Deep domain knowledge, task-specific tools, efficient execution.

## Communication Patterns

### Top-Down (Command)
```
Executive → Manager → Workers
- Goals flow downward
- Each level adds specificity
- Workers receive well-scoped tasks
```

### Bottom-Up (Report)
```
Workers → Manager → Executive
- Results flow upward
- Each level summarizes/aggregates
- Executives see condensed progress
```

### Lateral (Peer Coordination)
```
Worker A ↔ Worker B (same manager)
- Direct coordination on shared tasks
- Manager only notified on conflict
- Reduces upward communication load
```

## Architecture Topologies

### Tree Hierarchy
```
         [Executive]
        /     |     \
  [Mgr-A]  [Mgr-B]  [Mgr-C]
   /  \     /  \     /  \
  W1  W2   W3  W4   W5  W6
```
Best for: Clear domains, independent workstreams, strict accountability.

### Matrix Hierarchy
```
         [Executive]
        /          \
  [Mgr-Function]  [Mgr-Product]
      |         /       |       \
    W1—W2—W3        W4—W5—W6
```
Best for: Complex projects where workers report to both functional and product managers.

### Recursive Hierarchy
```
[Supervisor]
    └── [Supervisor]
           └── [Supervisor]
                  └── [Worker]
```
Best for: Deep reasoning tasks where each level refines the problem further.

## Implementation Patterns

### Pattern 1: Two-Level Delegation

```python
# Executive delegates to manager, manager to workers
from hermes_tools import delegate_task

# Executive phase
task_breakdown = delegate_task(
    goal="Decompose this mission into work packages",
    context=f"Mission: {mission}"
)

# Manager phase (one per work package)
for wp in task_breakdown.work_packages:
    result = delegate_task(
        goal=f"Execute work package: {wp.description}",
        context=f"Sub-tasks: {wp.sub_tasks}"
    )
```

### Pattern 2: Hierarchical Context Passing

Each level passes context both directions:

```python
# Executive provides strategic context
strategic_context = {
    "mission": "Build adblock engine",
    "constraints": ["must use Rust", "cross-platform"],
    "success_criteria": ["10M rules", "< 5ms lookup"]
}

# Manager adds operational context
operational_context = {
    **strategic_context,
    "team": ["packet-capture", "rule-parser", "lookup-engine"],
    "deadlines": {"phase1": "2 weeks", "phase2": "4 weeks"}
}

# Worker gets focused execution context
worker_context = {
    "task": "Implement rule parser",
    "interface": operational_context["specs"][1],
    "depends_on": "packet-capture module"
}
```

### Pattern 3: Escalation Protocol

```python
class EscalationProtocol:
    def __init__(self):
        self.levels = [
            ("worker", "manager"),
            ("manager", "executive"),
            ("executive", "human")
        ]
    
    def handle_issue(self, issue, current_level):
        if current_level.can_resolve(issue):
            return current_level.resolve(issue)
        else:
            next_level = self.escalate(current_level)
            return next_level.handle_issue(issue, next_level)
```

## Scaling Considerations

| Swarm Size | Recommended Architecture | Pattern |
|-----------|------------------------|---------|
| 2–5 agents | Flat or single-manager | Star |
| 5–20 agents | Two-level hierarchy | Tree |
| 20–100 agents | Three-level hierarchy | Tree + Matrix |
| 100+ agents | Multi-level with routing | Recursive + Matrix |

## Common Pitfalls

1. **Manager bottleneck** — too many workers per manager (span of control > 7)
2. **Context dilution** — information lost as it passes through layers; use structured summaries
3. **Over-escalation** — workers escalate too readily; train workers to resolve common issues
4. **Latency accumulation** — each level adds round-trip delay; use async patterns for deep hierarchies
5. **Rigid hierarchies** — fixed trees break when workload shifts; design for dynamic reassignment
6. **Duplicated work** — sibling workers unaware of each other's progress; implement lateral communication

## Verification Checklist

- [ ] Each agent has clear role, authority, and success criteria
- [ ] Span of control ≤ 7 per manager
- [ ] Escalation path defined for every issue type
- [ ] Context passed both directions (top-down for instructions, bottom-up for results)
- [ ] Lateral coordination mechanism in place between sibling agents
- [ ] Maximum hierarchy depth documented and justified
- [ ] Fallback when a manager/executive agent fails

## See Also

- agent-swarm-architectures — flat swarm topology and communication
- multi-agent-orchestration — orchestrating multiple agents
- sub-agent-delegation — delegating subtasks
- agent-task-decomposition — breaking down tasks for agents
