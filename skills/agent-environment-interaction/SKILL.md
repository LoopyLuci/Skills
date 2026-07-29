---
name: agent-environment-interaction
description: "Use when designing agent interaction with environments."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agent-environment, perception, action, observation, world-model, state]
    related_skills: [deep-reinforcement-learning, agent-framework-design, tool-augmented-agents, agent-planning-algorithms]
---

# Agent-Environment Interaction

Designing how agents perceive and interact with environments — from observation spaces and action spaces through world modeling, feedback loops, and multi-agent environments.

## When to Use

- Building agents that interact with real or simulated environments
- Defining observation and action spaces
- Implementing feedback and reward mechanisms
- Creating multi-agent environments
- Integrating agents with external tools and APIs

## Environment Types

```python
ENV_TYPES = {
    'simulated': 'Game engines, RL environments, virtual worlds (Gymnasium, Unity ML-Agents)',
    'API_based': 'Web APIs, databases, file systems, cloud services',
    'human': 'Chat interfaces, collaborative tools, feedback forms',
    'information': 'Web search, document retrieval, knowledge bases',
}

class EnvironmentInteraction:
    """Define agent-environment interaction protocol."""
    
    OBSERVATION_TYPES = {
        'state': 'Full environment state (simulation)',
        'partial': 'Partial observation (real world, information asymmetry)',
        'exogenous': 'External observations (market data, weather, news)',
    }
    
    ACTION_TYPES = {
        'discrete': 'Finite set of actions (up/down/left/right)',
        'continuous': 'Continuous action space (angle, force, amount)',
        'composite': 'Structured action with parameters (tool call with args)',
    }
    
    def __init__(self):
        self.observations = []
        self.actions_taken = []
    
    def observe(self) -> Dict:
        """Get current observation from environment."""
        observation = self._sense_environment()
        self.observations.append(observation)
        return observation
    
    def act(self, action: Dict) -> Dict:
        """Execute action in environment and get result."""
        result = self._execute_action(action)
        self.actions_taken.append({'action': action, 'result': result})
        return result
```

## Common Pitfalls

1. **Observation masking** — agent can't see critical state changes; define comprehensive obs space
2. **Action space too large** — too many action choices paralyze learning; group or abstract
3. **No feedback delay** — consequences of actions may be delayed; handle temporal credit assignment
4. **Non-stationary environment** — environment changes outside agent's control; model explicitly
5. **Information asymmetry** — different agents see different parts; design for cooperative info sharing

## Verification Checklist

- [ ] Observation space defined (what agent sees at each step)
- [ ] Action space defined (what agent can do)
- [ ] State transitions deterministic or stochastic
- [ ] Feedback/reward defined (dense vs sparse, delayed)
- [ ] Episode boundaries defined (success, failure, timeout)
- [ ] Multi-agent considerations (shared/private observations, agent count)
- [ ] Reset mechanism for reproducible episodes
