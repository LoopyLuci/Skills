---
name: multi-agent-reinforcement-learning
description: "Use when designing multi-agent RL systems and environments."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [reinforcement-learning, multi-agent, MARL, cooperation, competition]
    related_skills: [reinforcement-learning, deep-reinforcement-learning, hierarchical-swarm-architectures, swarm-communication-protocols]
---

# Multi-Agent Reinforcement Learning (MARL)

Designing and implementing multi-agent reinforcement learning systems — cooperative, competitive, and mixed-motive environments with multiple learning agents interacting simultaneously.

## When to Use

- Training multiple AI agents that interact in a shared environment
- Cooperative scenarios (robots moving boxes together, traffic light coordination)
- Competitive scenarios (game-playing, bidding, negotiation)
- Mixed-motive scenarios (resource sharing with individual incentives)
- Swarm intelligence systems that learn rather than being programmed

## MARL Taxonomy

```
MARL
├── Cooperative (common reward)
├── Competitive (opposing rewards)
└── Mixed (individual + shared rewards)
    ├── Fully Decentralized
    ├── Centralized Training, Decentralized Execution (CTDE)
    └── Fully Centralized
```

## Algorithm Families

| Algorithm | Type | Centralization | Best For |
|-----------|------|----------------|----------|
| IQL | Value-based | Decentralized | Simple tasks |
| VDN | Value-based | CTDE (value decomposition) | Cooperative |
| QMIX | Value-based | CTDE (mixing network) | Cooperative |
| MADDPG | Actor-Critic | CTDE | Mixed/Competitive |
| MAPPO | Policy-gradient | CTDE | Cooperative |
| COMA | Actor-Critic | CTDE | Cooperative |
| IPPO | Policy-gradient | Decentralized | Simple (surprisingly good) |

## CTDE Architecture (Centralized Training, Decentralized Execution)

```python
class CTDEMADDPG:
    """Multi-Agent DDPG with Centralized Training, Decentralized Execution."""
    
    class Critic(nn.Module):
        """Centralized critic: observes all agents' states and actions."""
        def __init__(self, num_agents, state_dims, action_dims, hidden=256):
            super().__init__()
            total_state = sum(state_dims)
            total_action = sum(action_dims)
            self.net = nn.Sequential(
                nn.Linear(total_state + total_action, hidden),
                nn.ReLU(),
                nn.Linear(hidden, hidden),
                nn.ReLU(),
                nn.Linear(hidden, 1)
            )
        
        def forward(self, all_states, all_actions):
            x = torch.cat([*all_states, *all_actions], dim=-1)
            return self.net(x)
    
    class Actor(nn.Module):
        """Decentralized actor: observes only local state."""
        def __init__(self, state_dim, action_dim, hidden=256):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(state_dim, hidden),
                nn.ReLU(),
                nn.Linear(hidden, hidden),
                nn.ReLU(),
                nn.Linear(hidden, action_dim),
                nn.Tanh()  # Bounded actions
            )
        
        def forward(self, state):
            return self.net(state)
    
    def __init__(self, num_agents, state_dims, action_dims, lr=1e-4):
        self.num_agents = num_agents
        self.actors = [self.Actor(s, a) for s, a in zip(state_dims, action_dims)]
        self.critics = [self.Critic(num_agents, state_dims, action_dims) for _ in range(num_agents)]
        
        # One critic per agent (or shared critic for cooperative)
        self.target_actors = [self.Actor(s, a) for s, a in zip(state_dims, action_dims)]
        self.target_critics = [self.Critic(num_agents, state_dims, action_dims) for _ in range(num_agents)]
        
        for ta, a in zip(self.target_actors, self.actors):
            ta.load_state_dict(a.state_dict())
        for tc, c in zip(self.target_critics, self.critics):
            tc.load_state_dict(c.state_dict())
        
        self.actor_opts = [torch.optim.Adam(a.parameters(), lr=lr) for a in self.actors]
        self.critic_opts = [torch.optim.Adam(c.parameters(), lr=lr) for c in self.critics]
    
    def update(self, experiences, gamma=0.95, tau=0.01):
        """Update all agents from a batch of joint experiences."""
        states = [exp['states'] for exp in experiences]
        actions = [exp['actions'] for exp in experiences]
        rewards = torch.stack([exp['rewards'] for exp in experiences])  # (num_agents, batch)
        next_states = [exp['next_states'] for exp in experiences]
        dones = torch.stack([exp['dones'] for exp in experiences])
        
        for i in range(self.num_agents):
            # Critic update (centralized)
            with torch.no_grad():
                next_actions = [ta(ns) for ta, ns in zip(self.target_actors, next_states)]
                target_q = self.target_critics[i](next_states, next_actions).squeeze()
                target_value = rewards[i] + gamma * (1 - dones[i]) * target_q
            
            current_q = self.critics[i](states, actions).squeeze()
            critic_loss = F.mse_loss(current_q, target_value)
            
            self.critic_opts[i].zero_grad()
            critic_loss.backward()
            self.critic_opts[i].step()
            
            # Actor update (decentralized — looks only at own critic)
            new_actions = [a(s) if j == i else a(s).detach() 
                          for j, (a, s) in enumerate(zip(self.actors, states))]
            actor_loss = -self.critics[i](states, new_actions).mean()
            
            self.actor_opts[i].zero_grad()
            actor_loss.backward()
            self.actor_opts[i].step()
        
        # Soft update targets
        for i in range(self.num_agents):
            for tp, p in zip(self.target_actors[i].parameters(), self.actors[i].parameters()):
                tp.data.copy_(tau * p + (1 - tau) * tp)
            for tp, p in zip(self.target_critics[i].parameters(), self.critics[i].parameters()):
                tp.data.copy_(tau * p + (1 - tau) * tp)
```

## QMIX (Value Decomposition)

```python
class QMIX:
    """QMIX: monotonic value decomposition for cooperative MARL."""
    
    class AgentNetwork(nn.Module):
        """Per-agent Q-network (receives own observation + action)."""
        def __init__(self, obs_dim, n_actions, hidden=64):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(obs_dim, hidden),
                nn.ReLU(),
                nn.Linear(hidden, hidden),
                nn.ReLU(),
                nn.Linear(hidden, n_actions)
            )
        
        def forward(self, obs):
            return self.net(obs)
    
    class MixingNetwork(nn.Module):
        """Mixing net: combines agent Q-values into joint Q-value.
        Enforces monotonicity (positive weights) for CTDE consistency."""
        def __init__(self, num_agents, state_dim, hidden=32):
            super().__init__()
            self.hyper_w1 = nn.Linear(state_dim, hidden * num_agents)
            self.hyper_b1 = nn.Linear(state_dim, hidden)
            self.hyper_w2 = nn.Linear(state_dim, hidden)
            self.hyper_b2 = nn.Sequential(
                nn.Linear(state_dim, hidden),
                nn.ReLU(),
                nn.Linear(hidden, 1)
            )
        
        def forward(self, agent_qs, states):
            """agent_qs: (batch, num_agents), states: (batch, state_dim)"""
            batch = agent_qs.shape[0]
            
            w1 = torch.abs(self.hyper_w1(states)).view(batch, -1, self.num_agents)
            b1 = self.hyper_b1(states).view(batch, -1, 1)
            hidden = torch.bmm(w1, agent_qs.unsqueeze(-1)) + b1
            hidden = F.elu(hidden)
            
            w2 = torch.abs(self.hyper_w2(states)).view(batch, 1, -1)
            b2 = self.hyper_b2(states).view(batch, 1, 1)
            q_total = torch.bmm(w2, hidden) + b2
            
            return q_total.squeeze()
```

## Environment Design for MARL

```python
class MARLEnvironment:
    """Template for multi-agent environments."""
    def __init__(self, num_agents=4):
        self.num_agents = num_agents
        self.agents = [f'agent_{i}' for i in range(num_agents)]
    
    def reset(self):
        """Return initial observations for all agents."""
        self.step_count = 0
        return {agent: self._get_obs(agent) for agent in self.agents}
    
    def step(self, actions):
        """actions: dict {agent_id: action}. Returns obs, rewards, done, info."""
        self.step_count += 1
        
        # Apply actions, update state
        rewards = {}
        dones = {}
        
        for agent in self.agents:
            self._apply_action(agent, actions[agent])
        
        # Compute rewards (can be shared or per-agent)
        if self.cooperative_mode:
            team_reward = self._compute_team_reward()
            rewards = {a: team_reward for a in self.agents}
        else:
            rewards = {a: self._compute_individual_reward(a) for a in self.agents}
        
        dones = {a: self._check_done(a) for a in self.agents}
        dones['__all__'] = all(dones.values()) or self.step_count >= self.max_steps
        
        return {a: self._get_obs(a) for a in self.agents}, rewards, dones, {}
```

## Training Patterns

### Centralized Training Loop

```python
def train_mappo(env, num_episodes=1000):
    """MAPPO: CTDE policy gradient for cooperative MARL."""
    agents = [PPOAgent(obs_dim, action_dim) for _ in range(env.num_agents)]
    
    for episode in range(num_episodes):
        obs = env.reset()
        done = False
        
        while not done:
            actions = {}
            log_probs = {}
            values = {}
            
            for i, agent in enumerate(agents):
                action, log_prob = agent.network.act(torch.FloatTensor(obs[f'agent_{i}']))
                value = agent.network.get_value(torch.FloatTensor(obs[f'agent_{i}']))
                actions[f'agent_{i}'] = action
                log_probs[f'agent_{i}'] = log_prob
                values[f'agent_{i}'] = value
            
            next_obs, rewards, dones, _ = env.step(actions)
            
            # Store trajectory (shared reward for cooperative)
            for i, agent in enumerate(agents):
                agent.store_transition(obs[f'agent_{i}'], actions[f'agent_{i}'], 
                                      rewards[f'agent_{i}'], next_obs[f'agent_{i}'],
                                      dones[f'agent_{i}'], log_probs[f'agent_{i}'], values[f'agent_{i}'])
            
            obs = next_obs
            done = dones['__all__']
        
        # Update all agents
        for agent in agents:
            if len(agent.buffer) >= agent.batch_size:
                agent.update()
```

## Common Pitfalls

1. **Non-stationarity** — other agents' policies change, making the environment non-stationary from any one agent's view; CTDE helps
2. **Credit assignment** — in cooperative settings, which agent caused the reward? VDN/QMIX decomposes the joint Q
3. **Scalability** — joint action space grows exponentially with agents; use parameter sharing or mean-field approximations
4. **Relative overgeneralization** — agents converge to suboptimal cooperative behavior; use population-based training
5. **Communication overhead** — agents sharing full observations defeats decentralization; limit communication bandwidth
6. **Symmetric agents** — identical agents shouldn't learn different policies; use parameter sharing for homogeneous teams

## Verification Checklist

- [ ] Environment correctly implements MARL interface (per-agent obs, actions, rewards)
- [ ] Training converges in simple cooperative task (e.g., spread, push)
- [ ] Agents learn to cooperate (joint reward increases) OR compete (individual reward gaps widen)
- [ ] CTDE implementation has correct gradient flow (centralized critic, decentralized actor)
- [ ] Communication protocols (if any) have bandwidth limits verified
- [ ] Homogeneous agents share parameters correctly
- [ ] Evaluation: trained agents vs heuristic baselines

## See Also

- deep-reinforcement-learning — single-agent deep RL
- hierarchical-swarm-architectures — combining MARL with hierarchy
- swarm-communication-protocols — agent communication in MARL
