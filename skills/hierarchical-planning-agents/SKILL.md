---
name: hierarchical-planning-agents
description: "Use when implementing hierarchical planning for agents."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hierarchical-planning, HTN, task-decomposition, STRIPS, PDDL, subgoals]
    related_skills: [agent-planning-algorithms, agent-task-decomposition, multi-agent-collaboration-patterns, advanced-reasoning-patterns]
---

# Hierarchical Planning for Agents

Implementing hierarchical planning for agents — from Hierarchical Task Networks (HTN) through goal decomposition, plan refinement, and execution monitoring.

## When to Use

- Complex tasks that decompose into subtask hierarchies
- Agents that need to plan at multiple abstraction levels
- Environments with recurring task patterns
- Long-horizon planning problems
- Coordinating multiple agents with shared goals

## HTN Planning

```python
class HTNPlanner:
    """Hierarchical Task Network planner."""
    def __init__(self):
        self.methods = {}  # task -> [{(subtasks, preconditions)}]
        self.operators = {}  # -> {(preconditions, effects)}
        self.domain = {}
    
    def add_method(self, task: str, subtasks: List[str], 
                   preconditions: List[str] = None):
        """Decompose a task into subtasks."""
        self.methods.setdefault(task, []).append({
            'subtasks': subtasks,
            'preconditions': preconditions or [],
        })
    
    def add_operator(self, action: str, preconditions: List[str],
                     effects: List[str]):
        """Define primitive action with preconditions and effects."""
        self.operators[action] = {
            'preconditions': preconditions,
            'effects': effects,
        }
    
    def plan(self, task: str, state: Dict) -> List[str]:
        """Decompose task into plan of primitive actions."""
        if task in self.operators:
            if self._check_preconditions(task, state):
                state.update(self.operators[task]['effects'])
                return [task]
            return None
        
        if task in self.methods:
            for method in self.methods[task]:
                if self._check_preconditions(method, state):
                    plan = []
                    for subtask in method['subtasks']:
                        subplan = self.plan(subtask, state)
                        if subplan is None:
                            return None
                        plan.extend(subplan)
                    return plan
        
        return None  # Cannot decompose
```

## Common Pitfalls

1. **Flat decomposition** — not using hierarchy effectively; design 3+ levels (strategic → tactical → operational)
2. **Non-optimal plans** — hierarchy constrains the search space, may miss optimal plans
3. **Brittle preconditions** — missing edge cases in preconditions causes plan failures
4. **No execution monitoring** — plan generated but not monitored during execution; add re-planning
5. **Knowledge engineering burden** — HTNs require significant domain expertise; consider learning methods

## Verification Checklist

- [ ] Task hierarchy defined (3+ levels: goal → tasks → actions)
- [ ] Decomposition methods for each compound task
- [ ] Primitive operators with preconditions and effects
- [ ] Planning state representation defined
- [ ] Re-planning triggers (plan failure, unexpected state)
- [ ] Performance: plan generation time within acceptable bounds
- [ ] Execution monitoring (is plan being followed? producing expected effects?)
