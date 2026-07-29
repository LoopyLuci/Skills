---
name: multi-agent-collaboration-patterns
description: "Use when designing multi-agent collaboration and delegation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [multi-agent, collaboration, delegation, negotiation, teamwork, coordination]
    related_skills: [agent-swarm-architectures, hierarchical-swarm-architectures, swarm-communication-protocols, agent-ensembles-voting]
---

# Multi-Agent Collaboration Patterns

Designing collaboration patterns for multi-agent systems — from task delegation and joint problem-solving through negotiation, consensus, and team formation.

## When to Use

- Multiple agents need to work together on a shared task
- Agents with different specializations need to coordinate
- Complex tasks that no single agent can handle alone
- Building agent teams that can dynamically reorganize
- Implementing market-based or auction-style task allocation

## Collaboration Patterns

```python
COLLABORATION_PATTERNS = {
    'delegation': 'Manager delegates subtasks to worker agents, collects results',
    'peer_collaboration': 'Peer agents share context and work jointly on shared task',
    'auction_bidding': 'Tasks are auctioned, agents bid based on capability/availability',
    'blackboard': 'Agents read/write to shared workspace, coordinate via artifacts',
    'debate': 'Agents argue different positions, converge through structured debate',
    'voting': 'Each agent contributes a vote or score, results are aggregated',
}

class TaskDelegation:
    """Manager-worker delegation pattern."""
    def __init__(self, manager, workers):
        self.manager = manager
        self.workers = workers
    
    def execute(self, complex_task: str) -> Dict:
        # Manager decomposes task
        subtasks = self.manager.decompose(complex_task)
        results = {}
        
        # Delegate to workers
        for subtask in subtasks:
            best_worker = self._select_worker(subtask)
            results[subtask['id']] = best_worker.execute(subtask)
        
        # Manager synthesizes results
        return self.manager.synthesize(results)
```

## Common Pitfalls

1. **Over-communication** — agents broadcasting everything creates noise; use targeted messages
2. **Responsibility ambiguity** — unclear who handles what causes duplication or gaps
3. **Deadlock** — agents waiting for each other indefinitely; use timeouts
4. **Free-riding** — some agents don't contribute; track contribution metrics
5. **Groupthink** — agents converge too quickly on wrong solution; encourage diversity

## Verification Checklist

- [ ] Collaboration pattern matches task structure
- [ ] Each agent has defined role and responsibilities
- [ ] Communication protocol defined (what, when, how)
- [ ] Conflict resolution mechanism in place
- [ ] Task decomposition and result synthesis logic tested
- [ ] Agent failures handled gracefully (re-assignment, escalation)
