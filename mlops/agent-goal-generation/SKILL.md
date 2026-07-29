---
name: agent-goal-generation
description: "Use when implementing goal generation for AI agents."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agent-goals, goal-generation, subgoal, decomposition, intrinsic-motivation]
    related_skills: [agent-planning-algorithms, hierarchical-planning-agents, agent-reasoning-patterns, agent-environment-interaction]
---

# Agent Goal Generation

Implementing goal generation for AI agents — from subgoal decomposition and intrinsic motivation through goal discovery, prioritization, and dynamic replanning.

## When to Use

- Agents that need to generate their own goals autonomously
- Hierarchical agents that decompose top-level goals into subgoals
- Implementing curiosity-driven or intrinsic motivation
- Building agents that can reprioritize goals dynamically

## Goal Generation Methods

```python
GOAL_GENERATION = {
    'task_decomposition': 'LLM-based or symbolic decomposition of high-level goal into subgoals',
    'intrinsic_motivation': 'Curiosity (novelty), competence (mastery), autonomy (choice)',
    'goal_discovery': 'Agent discovers goals from environment patterns or user behavior',
    'multi_agent_subgoal': 'Agents propose subgoals to each other, negotiate priority',
}

class GoalGenerator:
    """Generate and manage agent goals."""
    def __init__(self):
        self.goals = []
        self.completed = []
        self.priorities = {}
    
    def decompose_task(self, top_level: str, context: str) -> List[Dict]:
        """Decompose a top-level goal into subgoals."""
        subgoals = [
            {'description': f'Analyze {top_level}', 'status': 'pending', 'dependencies': []},
            {'description': f'Plan approach for {top_level}', 'status': 'pending', 'dependencies': [0]},
            {'description': f'Execute {top_level}', 'status': 'pending', 'dependencies': [1]},
            {'description': f'Verify {top_level} completion', 'status': 'pending', 'dependencies': [2]},
        ]
        for sg in subgoals:
            self.goals.append(sg)
        return subgoals
    
    def next_goal(self) -> Dict:
        for goal in self.goals:
            if goal['status'] == 'pending':
                deps = all(self.goals[d]['status'] == 'completed' for d in goal.get('dependencies', []))
                if deps: return goal
        return None
```

## Verification Checklist

- [ ] Goal decomposition produces meaningful subgoals
- [ ] Subgoal dependencies correctly tracked
- [ ] Intrinsic motivation (curiosity) balanced with extrinsic goals
- [ ] Dynamic reprioritization when environment changes
- [ ] Goal completion verified (not just assumed)
- [ ] Unreachable goals detected and re-assessed
