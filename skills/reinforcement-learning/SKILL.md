---
name: reinforcement-learning
description: "Use when implementing reinforcement learning algorithms."
category: mlops
tags: [reinforcement-learning, rl, dqn, ppo, policy-gradient]
---
# Reinforcement Learning

Implementing core RL algorithms: value-based, policy-based, and actor-critic.

## Core Concepts

```
State (s)  →  Agent  →  Action (a)
                ↓
            Environment
                ↓
         Reward (r) + Next State (s')
```

## DQN (Deep Q-Network)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import deque
import random

class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, 128), nn.ReLU(),
            nn.Linear(128, 128), nn.ReLU(),
            nn.Linear(128, action_dim),
        )

    def forward(self, x):
        return self.net(x)

class ReplayBuffer:
    def __init__(self, capacity=100000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        return map(torch.stack, zip(*batch))

# DQN training loop
def train_dqn(env, agent, target, buffer, optimizer, batch_size=64):
    states, actions, rewards, next_states, dones = buffer.sample(batch_size)
    with torch.no_grad():
        target_q = target(next_states).max(1)[0]
        target_q = rewards + (0.99 * target_q * ~dones)
    current_q = agent(states).gather(1, actions.unsqueeze(1)).squeeze()
    loss = F.mse_loss(current_q, target_q)
    optimizer.zero_grad(); loss.backward(); optimizer.step()
```

## PPO (Proximal Policy Optimization)

```python
class PPO(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.actor = nn.Sequential(
            nn.Linear(state_dim, 128), nn.Tanh(),
            nn.Linear(128, 128), nn.Tanh(),
            nn.Linear(128, action_dim),  # mean for Gaussian policy
        )
        self.critic = nn.Sequential(
            nn.Linear(state_dim, 128), nn.Tanh(),
            nn.Linear(128, 128), nn.Tanh(),
            nn.Linear(128, 1),
        )

    def get_action(self, state):
        mean = self.actor(state)
        dist = torch.distributions.Normal(mean, 1.0)
        action = dist.sample()
        return action, dist.log_prob(action).sum(-1)

    def get_value(self, state):
        return self.critic(state)

# PPO loss
def ppo_loss(advantages, old_log_probs, new_log_probs, epsilon=0.2):
    ratio = (new_log_probs - old_log_probs).exp()
    clipped = torch.clamp(ratio, 1 - epsilon, 1 + epsilon)
    return -torch.min(ratio * advantages, clipped * advantages).mean()
```

## Reward Shaping for Agent Systems

```python
# Reward signals for AI agents
rewards = {
    "task_completion": +100,    # successful task done
    "correct_tool_use": +10,    # selected the right tool
    "efficient_steps": +5,      # completed in minimal steps
    "loop_detected": -20,       # repeating same action
    "wrong_tool": -10,          # selected wrong tool
    "step_cost": -1,            # per-step penalty (encourage efficiency)
    "hallucination": -50,       # claiming success without evidence
}
```

## Pitfalls

- DQN overestimates Q-values — use Double DQN for correction
- PPO is sensitive to hyperparameters (clip range, learning rate, entropy bonus)
- Sparse rewards (only +1 at end) make learning very hard — use reward shaping
- Environment interaction is usually the bottleneck — parallelize environments
- Deterministic environments need exploration noise (epsilon-greedy, entropy)
