---
name: deep-reinforcement-learning
description: "Use when implementing deep RL algorithms and environments."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [reinforcement-learning, DRL, DQN, PPO, SAC, pytorch]
    related_skills: [reinforcement-learning, multi-agent-reinforcement-learning, custom-training-loops, agent-reasoning-patterns]
---

# Deep Reinforcement Learning (DRL)

Implementing deep reinforcement learning algorithms — from value-based (DQN) to policy-gradient (PPO) and actor-critic (SAC, TD3) methods, with practical implementation patterns, environment integration, and debugging.

## When to Use

- Solving sequential decision-making problems (games, robotics, control)
- Problems where supervised data is unavailable but reward signals exist
- Fine-tuning language models with human feedback (RLHF)
- Training agentic AI systems that interact with environments
- Optimizing long-horizon tasks with delayed rewards

## Algorithm Selection

| Algorithm | Type | Best For | Sample Efficiency | Stability |
|-----------|------|---------|-------------------|-----------|
| DQN | Value-based | Discrete actions, Atari | Low | Good |
| Double DQN | Value-based | Reducing Q-overestimation | Low | Better |
| Dueling DQN | Value-based | Large action spaces | Low | Good |
| REINFORCE | Policy-gradient | Simple continuous | Very Low | Poor |
| PPO | Policy-gradient | General purpose | Medium | Best |
| SAC | Actor-Critic | Continuous control | High | Good |
| TD3 | Actor-Critic | Continuous, deterministic | High | Best |
| DDPG | Actor-Critic | Continuous, deterministic | Medium | Fair |
| IMPALA | Off-policy | Distributed training | Medium | Good |

## Core Components

### Replay Buffer

```python
import random
import numpy as np
from collections import deque

class ReplayBuffer:
    """Experience replay for off-policy algorithms (DQN, SAC, TD3, DDPG)."""
    def __init__(self, capacity=1000000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size=256):
        batch = random.sample(self.buffer, min(batch_size, len(self.buffer)))
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            np.array(states), np.array(actions), np.array(rewards, dtype=np.float32),
            np.array(next_states), np.array(dones, dtype=np.float32)
        )
    
    def __len__(self):
        return len(self.buffer)
```

### DQN (Deep Q-Network)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    """Deep Q-Network for discrete action spaces."""
    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )
    
    def forward(self, x):
        return self.net(x)
    
    def act(self, state, epsilon=0.1):
        """Epsilon-greedy action selection."""
        if random.random() < epsilon:
            return random.randrange(self.net[-1].out_features)
        with torch.no_grad():
            q_values = self(torch.FloatTensor(state).unsqueeze(0))
            return q_values.argmax().item()
    

class DQNAgent:
    """DQN with target network, replay buffer, and double Q-learning."""
    def __init__(self, state_dim, action_dim, lr=1e-4, gamma=0.99, tau=0.005):
        self.q_network = DQN(state_dim, action_dim)
        self.target_network = DQN(state_dim, action_dim)
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.optimizer = torch.optim.Adam(self.q_network.parameters(), lr=lr)
        
        self.gamma = gamma
        self.tau = tau
        self.buffer = ReplayBuffer()
        self.action_dim = action_dim
    
    def update(self, batch_size=256):
        if len(self.buffer) < batch_size:
            return
        
        states, actions, rewards, next_states, dones = self.buffer.sample(batch_size)
        
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards).unsqueeze(1)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones).unsqueeze(1)
        
        # Double DQN: use online network to select action, target network to evaluate
        with torch.no_grad():
            next_actions = self.q_network(next_states).argmax(dim=1, keepdim=True)
            next_q = self.target_network(next_states).gather(1, next_actions)
            target_q = rewards + self.gamma * next_q * (1 - dones)
        
        current_q = self.q_network(states).gather(1, actions)
        loss = F.mse_loss(current_q, target_q)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Polyak update for target network
        for target_param, param in zip(self.target_network.parameters(), self.q_network.parameters()):
            target_param.data.copy_(self.tau * param.data + (1 - self.tau) * target_param.data)
        
        return loss.item()
```

### PPO (Proximal Policy Optimization)

```python
class PPONetwork(nn.Module):
    """Actor-Critic network for PPO."""
    def __init__(self, state_dim, action_dim, hidden_dim=256, continuous=True):
        super().__init__()
        self.continuous = continuous
        
        self.encoder = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
        )
        
        self.actor_mean = nn.Linear(hidden_dim, action_dim)
        if continuous:
            self.actor_log_std = nn.Parameter(torch.zeros(1, action_dim))
        self.critic = nn.Linear(hidden_dim, 1)
    
    def forward(self, x):
        features = self.encoder(x)
        action_mean = self.actor_mean(features)
        if self.continuous:
            action_std = self.actor_log_std.exp().expand_as(action_mean)
            return action_mean, action_std
        return action_mean
    
    def get_value(self, x):
        return self.critic(self.encoder(x))
    
    def act(self, state):
        if self.continuous:
            mean, std = self(state)
            dist = torch.distributions.Normal(mean, std)
            action = dist.sample()
            log_prob = dist.log_prob(action).sum(dim=-1)
            return action, log_prob
        else:
            logits = self(state)
            dist = torch.distributions.Categorical(logits=logits)
            action = dist.sample()
            log_prob = dist.log_prob(action)
            return action, log_prob


class PPOAgent:
    """PPO with clipping, GAE, and minibatch updates."""
    def __init__(self, state_dim, action_dim, lr=3e-4, gamma=0.99, 
                 gae_lambda=0.95, clip_epsilon=0.2, value_coef=0.5,
                 entropy_coef=0.01, epochs=10, continuous=True):
        self.network = PPONetwork(state_dim, action_dim, continuous=continuous)
        self.optimizer = torch.optim.Adam(self.network.parameters(), lr=lr)
        
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.clip_epsilon = clip_epsilon
        self.value_coef = value_coef
        self.entropy_coef = entropy_coef
        self.epochs = epochs
    
    def compute_gae(self, rewards, values, dones):
        """Generalized Advantage Estimation."""
        advantages = []
        gae = 0
        values = values.squeeze()
        for t in reversed(range(len(rewards))):
            if t == len(rewards) - 1:
                next_value = 0
            else:
                next_value = values[t + 1]
            delta = rewards[t] + self.gamma * next_value * (1 - dones[t]) - values[t]
            gae = delta + self.gamma * self.gae_lambda * (1 - dones[t]) * gae
            advantages.insert(0, gae)
        returns = [adv + val for adv, val in zip(advantages, values)]
        return torch.FloatTensor(advantages), torch.FloatTensor(returns)
    
    def update(self, trajectories):
        """PPO update over collected trajectories."""
        states = torch.FloatTensor(trajectories['states'])
        actions = torch.FloatTensor(trajectories['actions']) if self.network.continuous \
                  else torch.LongTensor(trajectories['actions'])
        old_log_probs = torch.FloatTensor(trajectories['log_probs'])
        advantages, returns = self.compute_gae(
            trajectories['rewards'], 
            self.network.get_value(states).detach(),
            trajectories['dones']
        )
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        for _ in range(self.epochs):
            if self.network.continuous:
                mean, std = self.network(states)
                dist = torch.distributions.Normal(mean, std)
                new_log_probs = dist.log_prob(actions).sum(dim=-1)
                entropy = dist.entropy().sum(dim=-1).mean()
            else:
                logits = self.network(states)
                dist = torch.distributions.Categorical(logits=logits)
                new_log_probs = dist.log_prob(actions)
                entropy = dist.entropy().mean()
            
            # PPO clipping objective
            ratio = torch.exp(new_log_probs - old_log_probs)
            clipped_ratio = torch.clamp(ratio, 1 - self.clip_epsilon, 1 + self.clip_epsilon)
            policy_loss = -torch.min(ratio * advantages, clipped_ratio * advantages).mean()
            
            # Value loss
            values = self.network.get_value(states).squeeze()
            value_loss = F.mse_loss(values, returns)
            
            # Total loss
            loss = policy_loss + self.value_coef * value_loss - self.entropy_coef * entropy
            
            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.network.parameters(), 0.5)
            self.optimizer.step()
        
        return loss.item()
```

### SAC (Soft Actor-Critic)

```python
class SACAgent:
    """Soft Actor-Critic for maximum entropy reinforcement learning."""
    def __init__(self, state_dim, action_dim, hidden_dim=256, 
                 lr=3e-4, gamma=0.99, tau=0.005, alpha=0.2, 
                 target_entropy=None):
        
        self.actor = self._build_actor(state_dim, action_dim, hidden_dim)
        self.critic1 = self._build_critic(state_dim, action_dim, hidden_dim)
        self.critic2 = self._build_critic(state_dim, action_dim, hidden_dim)
        self.target_critic1 = self._build_critic(state_dim, action_dim, hidden_dim)
        self.target_critic2 = self._build_critic(state_dim, action_dim, hidden_dim)
        
        self.target_critic1.load_state_dict(self.critic1.state_dict())
        self.target_critic2.load_state_dict(self.critic2.state_dict())
        
        self.actor_optim = torch.optim.Adam(self.actor.parameters(), lr=lr)
        self.critic_optim = torch.optim.Adam(
            list(self.critic1.parameters()) + list(self.critic2.parameters()), lr=lr)
        
        self.gamma = gamma
        self.tau = tau
        
        # Automatic entropy tuning
        self.log_alpha = torch.tensor(np.log(alpha), requires_grad=True)
        self.alpha_optim = torch.optim.Adam([self.log_alpha], lr=lr)
        self.target_entropy = target_entropy or -action_dim
    
    def update(self, batch):
        states, actions, rewards, next_states, dones = batch
        
        with torch.no_grad():
            next_actions, next_log_probs = self.actor.sample(next_states)
            target_q1 = self.target_critic1(next_states, next_actions)
            target_q2 = self.target_critic2(next_states, next_actions)
            target_q = torch.min(target_q1, target_q2) - self.alpha.detach() * next_log_probs
            target_value = rewards + self.gamma * (1 - dones) * target_q
        
        # Critic update (clipped double Q)
        current_q1 = self.critic1(states, actions)
        current_q2 = self.critic2(states, actions)
        critic_loss = F.mse_loss(current_q1, target_value) + F.mse_loss(current_q2, target_value)
        
        self.critic_optim.zero_grad()
        critic_loss.backward()
        self.critic_optim.step()
        
        # Actor update
        new_actions, log_probs = self.actor.sample(states)
        q1 = self.critic1(states, new_actions)
        q2 = self.critic2(states, new_actions)
        q = torch.min(q1, q2)
        actor_loss = (self.alpha.detach() * log_probs - q).mean()
        
        self.actor_optim.zero_grad()
        actor_loss.backward()
        self.actor_optim.step()
        
        # Alpha update (automatic entropy tuning)
        alpha_loss = -(self.log_alpha * (log_probs + self.target_entropy).detach()).mean()
        self.alpha_optim.zero_grad()
        alpha_loss.backward()
        self.alpha_optim.step()
        self.alpha = self.log_alpha.exp()
        
        # Target network update
        for target, source in zip(
            [self.target_critic1, self.target_critic2],
            [self.critic1, self.critic2]
        ):
            for tp, sp in zip(target.parameters(), source.parameters()):
                tp.data.copy_(self.tau * sp.data + (1 - self.tau) * tp.data)
```

## Environment Wrapper

```python
import gymnasium as gym

def make_env(env_id, seed=0):
    """Create a standardized Gymnasium environment."""
    env = gym.make(env_id)
    env = gym.wrappers.RecordEpisodeStatistics(env)
    env = gym.wrappers.ClipAction(env)
    env = gym.wrappers.NormalizeObservation(env)
    env = gym.wrappers.TransformObservation(env, lambda obs: np.clip(obs, -10, 10))
    env = gym.wrappers.NormalizeReward(env)
    env = gym.wrappers.TransformReward(env, lambda r: np.clip(r, -10, 10))
    env.action_space.seed(seed)
    env.observation_space.seed(seed)
    return env
```

## Training Loop

```python
def train_ppo(env_name="HalfCheetah-v4", total_timesteps=1_000_000):
    env = make_env(env_name)
    agent = PPOAgent(
        state_dim=env.observation_space.shape[0],
        action_dim=env.action_space.shape[0],
        continuous=True
    )
    
    state, _ = env.reset()
    episode_reward = 0
    trajectories = {'states': [], 'actions': [], 'rewards': [], 
                    'next_states': [], 'dones': [], 'log_probs': []}
    
    for step in range(total_timesteps):
        action, log_prob = agent.network.act(torch.FloatTensor(state))
        next_state, reward, terminated, truncated, _ = env.step(action.numpy())
        done = terminated or truncated
        
        trajectories['states'].append(state)
        trajectories['actions'].append(action)
        trajectories['rewards'].append(reward)
        trajectories['dones'].append(done)
        trajectories['log_probs'].append(log_prob)
        
        episode_reward += reward
        state = next_state
        
        if done or step % 2048 == 0:  # Update every 2048 steps
            if len(trajectories['states']) > 0:
                loss = agent.update(trajectories)
                trajectories = {k: [] for k in trajectories}
            
            if done:
                print(f"Step {step}, Episode Reward: {episode_reward:.1f}")
                episode_reward = 0
                state, _ = env.reset()
```

## Common Pitfalls

1. **Reward scaling** — unscaled rewards cause gradient explosion; normalize returns (z-score per batch)
2. **NaNs from gradients** — clip gradients (max_norm=0.5 for PPO, 1.0 for SAC)
3. **Hyperparameter sensitivity** — DRL is more sensitive than supervised learning; use established defaults first
4. **Stochasticity vs determinism** — high entropy in early training helps exploration; anneal over time
5. **Training instability** — if loss spikes, reduce learning rate or increase batch size
6. **Evaluation vs training** — always evaluate with deterministic policy (no noise, greedy actions)

## Verification Checklist

- [ ] Algorithm converges on simple environment (CartPole, Pendulum)
- [ ] Training reward increases monotonically over training
- [ ] Evaluation reward stabilizes (not oscillating wildly)
- [ ] Gradient norms in healthy range (10⁻³ to 10²)
- [ ] No NaN/Inf in gradients or parameters
- [ ] Replay buffer diversity (samples cover state space)
- [ ] Exploration vs exploitation balance verified

## See Also

- reinforcement-learning — foundational RL concepts
- multi-agent-reinforcement-learning — MARL extensions
- custom-training-loops — customizing the training loop
- agent-reasoning-patterns — using DRL for agent reasoning
