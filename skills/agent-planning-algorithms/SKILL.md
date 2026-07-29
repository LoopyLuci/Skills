---
name: agent-planning-algorithms
description: "Use when implementing planning algorithms for AI agents."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [planning, STRIPS, PDDL, HTN, task-planning, agent-reasoning]
    related_skills: [agent-task-decomposition, agent-reasoning-patterns, advanced-reasoning-patterns, agent-framework-design]
---

# Agent Planning Algorithms

Implementing classical and modern planning algorithms for AI agents — from STRIPS and PDDL through hierarchical task networks (HTN) to learned planning with neural networks.

## When to Use

- Building agents that need to plan before acting (not just react)
- Decomposing complex tasks into ordered sub-steps
- Generating multi-step plans with dependencies and constraints
- Implementing task and motion planning for robotics
- Reasoning about action sequences and their effects

## Planning Approaches

| Approach | Expressiveness | Computational Cost | When to Use |
|----------|---------------|-------------------|-------------|
| STRIPS | Low | Low | Simple deterministic domains |
| PDDL | High | High | Complex domains with constraints |
| HTN | Medium | Medium | Hierarchical, repetitive tasks |
| GraphPlan | Medium | Medium | Parallel plan discovery |
| FF/FFS | Medium | Medium | Fast heuristic search |
| Neural Planning | Variable | Variable | Learned in complex domains |

## STRIPS Planner

```python
from typing import List, Tuple, Set, Dict
from dataclasses import dataclass

@dataclass
class Action:
    name: str
    preconditions: Set[str]
    add_effects: Set[str]
    delete_effects: Set[str]

class STRIPSPlanner:
    """Classical STRIPS forward (progression) planner."""
    
    def __init__(self, actions: List[Action]):
        self.actions = actions
    
    def plan(self, initial_state: Set[str], goal_state: Set[str], max_depth=50):
        """Forward search from initial to goal state."""
        from collections import deque
        
        # BFS through state space
        queue = deque()
        queue.append((initial_state, []))  # (current_state, plan_so_far)
        visited = set()
        
        while queue:
            state, plan = queue.popleft()
            state_tuple = frozenset(state)
            
            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            
            # Check if goal achieved
            if goal_state.issubset(state):
                return plan
            
            if len(plan) >= max_depth:
                continue
            
            # Try each applicable action
            for action in self.actions:
                if action.preconditions.issubset(state):
                    new_state = (state - action.delete_effects) | action.add_effects
                    queue.append((new_state, plan + [action.name]))
        
        return None  # No plan found

# Example usage:
# actions = [
#     Action("pick_up", {"at_robot", "at_item"}, {"holding"}, {"at_item"}),
#     Action("move_to", {"at_robot", "connected"}, {"at_target"}, {"at_robot"}),
# ]
# planner = STRIPSPlanner(actions)
# plan = planner.plan({"at_robot", "at_item", "connected"}, {"holding"})
```

## PDDL Parser and Grounder

```python
class PDDLPlanner:
    """Simplified PDDL-style planning with fluent tracking."""
    
    def __init__(self, domain_file=None):
        self.predicates = {}  # name -> arity
        self.actions = []
        self.objects = set()
    
    def add_action(self, name, parameters, precondition, effect):
        """Add a parameterized action."""
        self.actions.append({
            'name': name,
            'params': parameters,
            'precondition': precondition,  # lambda params -> set of fluents
            'effect': effect,  # lambda params -> (add, delete)
        })
    
    def ground(self, objects):
        """Ground all actions with all possible parameter bindings."""
        grounded = []
        import itertools
        
        for action in self.actions:
            param_combos = itertools.product(objects, repeat=len(action['params']))
            for binding in param_combos:
                ground_action = {
                    'name': f"{action['name']}({', '.join(binding)})",
                    'precondition': action['precondition'](binding),
                    'effect': action['effect'](binding),
                }
                grounded.append(ground_action)
        
        return grounded
```

## Hierarchical Task Network (HTN) Planning

```python
class HTNPlanner:
    """Hierarchical Task Network planning.
    
    HTN decomposes high-level tasks into primitive actions
    using methods (recipes for how to accomplish a task)."""
    
    def __init__(self):
        self.methods = {}  # task_name -> [(conditions, subtasks)]
        self.primitive_actions = set()
    
    def add_method(self, task, conditions, subtasks):
        """Define a method to decompose a task."""
        if task not in self.methods:
            self.methods[task] = []
        self.methods[task].append((conditions, subtasks))
    
    def add_primitive(self, action):
        """Mark an action as primitive (directly executable)."""
        self.primitive_actions.add(action)
    
    def plan(self, tasks, state, max_depth=100):
        """Decompose tasks into a plan.
        
        tasks: list of high-level tasks to accomplish
        state: current world state (set of facts)
        """
        if not tasks:
            return []  # All done
        
        current_task = tasks[0]
        remaining = tasks[1:]
        
        # If primitive, just do it
        if current_task in self.primitive_actions:
            subplan = [current_task]
            # Apply effects
            new_state = self._apply(current_task, state)
            rest = self.plan(remaining, new_state)
            if rest is not None:
                return subplan + rest
            return None
        
        # Find applicable method
        if current_task in self.methods:
            for conditions, subtasks in self.methods[current_task]:
                if conditions.issubset(state):
                    # Decompose: replace current task with its subtasks
                    new_tasks = subtasks + remaining
                    plan = self.plan(new_tasks, state)
                    if plan is not None:
                        return plan
        
        return None  # No decomposition found
```

## Planning Domain Definition (Cooking Example)

```python
# Define a simple cooking domain

# State: set of facts
state = {"has_ingredients", "clean_hands", "oven_off", "pantry_open"}

# Actions
actions = [
    Action("chop_vegetables", {"has_ingredients", "knife"}, 
           {"vegetables_chopped"}, {"pantry_open"}),
    Action("preheat_oven", {"oven_off", "oven_clean"}, 
           {"oven_hot"}, {"oven_off"}),
    Action("bake", {"vegetables_chopped", "oven_hot", "baking_dish"}, 
           {"meal_ready"}, {"vegetables_chopped"}),
]

# Planner
planner = STRIPSPlanner(actions)
plan = planner.plan(state, {"meal_ready"})
# Result: ["chop_vegetables", "preheat_oven", "bake"]
```

## Common Pitfalls

1. **Frame problem** — STRIPS assumes unchanged facts persist; handle domain-specific exceptions
2. **State explosion** — BFS over state space explodes exponentially; use heuristic search (A*)
3. **Conjunctive goals** — achieving one goal may undo another; plan for goal interactions
4. **Sensing uncertainty** — classical planning assumes perfect knowledge; use conformant or contingent planning
5. **Continuous time** — STRIPS can't handle durative actions; use temporal planners for time
6. **Resource constraints** — classical planning ignores resource limits; use numeric fluents

## Verification Checklist

- [ ] Planner finds a valid plan for simple test domains (blocks world, logistics)
- [ ] Plan achieves all goal conditions
- [ ] Plan contains only executable actions given initial state
- [ ] No redundant actions in plan
- [ ] HTN methods decompose correctly into primitives
- [ ] Planner handles at least 10-state medium complexity

## See Also

- agent-task-decomposition — breaking down tasks for planning
- agent-reasoning-patterns — using planning in reasoning
- advanced-reasoning-patterns — CoT integration with planning
- agent-framework-design — integrating planners in agents
