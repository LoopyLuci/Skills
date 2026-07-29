---
name: rlhf-implementation-guide
description: "Use when implementing RLHF for training language models."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [RLHF, reinforcement-learning, LLM, training, human-feedback]
    related_skills: [reinforcement-learning, llm-fine-tuning-lora, deep-reinforcement-learning, agent-safety-alignment]
---

# RLHF (Reinforcement Learning from Human Feedback)

Implementing RLHF to align language models with human preferences — from reward model training to PPO-based fine-tuning, with practical patterns for stability, efficiency, and safety.

## When to Use

- Aligning LLMs with human preferences (helpfulness, harmlessness, honesty)
- Fine-tuning models to follow instructions more reliably
- Reducing harmful outputs without sacrificing capability
- Building models that reflect specific value systems
- Producing the final alignment stage after supervised fine-tuning

## RLHF Pipeline

```
SFT Model → Collect Preferences → Train Reward Model → PPO Fine-tune → Aligned Model
```

### Stage 1: Supervised Fine-Tuning (SFT)

```python
# Before RLHF, the model should be instruction-tuned via SFT
# This provides a good initialization for the RLHF process
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("base-model")
tokenizer = AutoTokenizer.from_pretrained("base-model")

# SFT on demonstration data
# (Standard language modeling on human-written responses)
```

### Stage 2: Collect Human Preferences

```python
"""
Preference data format:
{
    "prompt": "Explain quantum computing",
    "chosen": "Quantum computing uses qubits...",    # Preferred response
    "rejected": "It's like magic computers..."        # Dispreferred response
}

Typically 10K-100K preference pairs are needed.
Data can be collected via:
1. Human raters comparing model outputs
2. AI feedback (RLAIF) using a strong model as judge
3. User interaction logs (upvote/downvote)
"""
```

### Stage 3: Train Reward Model

```python
import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer

class RewardModel(nn.Module):
    """Reward model: scores how good a response is.
    Usually initialized from the SFT model with a value head."""
    
    def __init__(self, base_model_name="sft-model", dropout=0.1):
        super().__init__()
        self.base_model = AutoModel.from_pretrained(base_model_name)
        hidden_size = self.base_model.config.hidden_size
        
        # Value head: maps last hidden state to a scalar reward
        self.value_head = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(hidden_size, 1)
        )
    
    def forward(self, input_ids, attention_mask=None):
        outputs = self.base_model(input_ids, attention_mask=attention_mask)
        # Use the last token's hidden state as the pooled representation
        last_hidden = outputs.last_hidden_state
        # For causal LMs, take the last non-padding token
        if attention_mask is not None:
            last_token_indices = attention_mask.sum(dim=1) - 1
            batch_indices = torch.arange(last_hidden.shape[0], device=last_hidden.device)
            pooled = last_hidden[batch_indices, last_token_indices]
        else:
            pooled = last_hidden[:, -1, :]
        
        reward = self.value_head(pooled).squeeze(-1)
        return reward


def train_reward_model(model, dataloader, tokenizer, epochs=3, lr=1e-5):
    """Train reward model on preference pairs using Bradley-Terry loss.
    
    Loss: -log(σ(r_chosen - r_rejected))
    """
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    
    for epoch in range(epochs):
        total_loss = 0
        for batch in dataloader:
            # Tokenize chosen and rejected responses
            chosen_inputs = tokenizer(batch['chosen'], return_tensors='pt', padding=True)
            rejected_inputs = tokenizer(batch['rejected'], return_tensors='pt', padding=True)
            
            # Get rewards
            r_chosen = model(**chosen_inputs)
            r_rejected = model(**rejected_inputs)
            
            # Bradley-Terry loss
            loss = -torch.log(torch.sigmoid(r_chosen - r_rejected) + 1e-8).mean()
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        # Accuracy: how often does the RM prefer the chosen response?
        acc = (r_chosen > r_rejected).float().mean()
        print(f"Epoch {epoch}: loss={total_loss/len(dataloader):.4f}, acc={acc:.4f}")
    
    return model
```

### Stage 4: PPO Fine-Tuning

```python
class PPOTrainer:
    """PPO for RLHF. Key components:
    - Policy (the model being trained)
    - Reference model (frozen, for KL penalty)
    - Reward model (frozen, for scoring)
    - Value model (usually same as policy with a value head)
    """
    
    def __init__(self, policy_model, ref_model, reward_model, 
                 tokenizer, lr=1e-6, kl_coef=0.1, clip_epsilon=0.2):
        self.policy = policy_model
        self.ref_model = ref_model
        self.ref_model.eval()
        for p in self.ref_model.parameters():
            p.requires_grad = False
        
        self.reward_model = reward_model
        self.reward_model.eval()
        for p in self.reward_model.parameters():
            p.requires_grad = False
        
        self.tokenizer = tokenizer
        self.optimizer = torch.optim.AdamW(self.policy.parameters(), lr=lr)
        self.kl_coef = kl_coef
        self.clip_epsilon = clip_epsilon
    
    def compute_kl_penalty(self, policy_logprobs, ref_logprobs):
        """KL divergence between policy and reference model.
        Acts as a trust region to prevent policy from diverging too far."""
        ratio = torch.exp(policy_logprobs - ref_logprobs)
        kl = (ratio - 1 - (policy_logprobs - ref_logprobs)).mean()
        return kl
    
    def compute_advantages(self, rewards, values, gamma=1.0, lam=0.95):
        """GAE (Generalized Advantage Estimation) for the reward signals."""
        advantages = []
        gae = 0
        
        for t in reversed(range(len(rewards))):
            if t == len(rewards) - 1:
                next_value = 0
            else:
                next_value = values[t + 1]
            
            delta = rewards[t] + gamma * next_value - values[t]
            gae = delta + gamma * lam * gae
            advantages.insert(0, gae)
        
        returns = [adv + val for adv, val in zip(advantages, values)]
        return advantages, returns
    
    def generate_experience(self, prompts, max_length=512):
        """Generate responses using current policy for PPO training."""
        experiences = []
        
        for prompt in prompts:
            # Tokenize
            inputs = self.tokenizer(prompt, return_tensors='pt')
            input_ids = inputs['input_ids']
            attention_mask = inputs['attention_mask']
            
            # Generate response from policy
            with torch.no_grad():
                # Greedy or sample-based generation
                response_ids = self.policy.generate(
                    input_ids,
                    max_length=max_length,
                    do_sample=True,
                    temperature=0.7,
                    pad_token_id=self.tokenizer.eos_token_id
                )
                
                # Get logprobs for the generated tokens
                outputs = self.policy(response_ids, attention_mask=attention_mask)
                policy_logprobs = torch.log_softmax(outputs.logits, dim=-1)
                
                # Get reference logprobs
                ref_outputs = self.ref_model(response_ids, attention_mask=attention_mask)
                ref_logprobs = torch.log_softmax(ref_outputs.logits, dim=-1)
                
                # Get reward
                reward = self.reward_model(response_ids, attention_mask=attention_mask)
            
            experiences.append({
                'input_ids': response_ids,
                'attention_mask': attention_mask,
                'policy_logprobs': policy_logprobs,
                'ref_logprobs': ref_logprobs,
                'reward': reward.item()
            })
        
        return experiences
    
    def train_step(self, experiences):
        """Single PPO update step."""
        for exp in experiences:
            input_ids = exp['input_ids']
            attention_mask = exp['attention_mask']
            
            # Current policy logprobs
            outputs = self.policy(input_ids, attention_mask=attention_mask)
            logprobs = torch.log_softmax(outputs.logits, dim=-1)
            
            # Ratio for PPO clipping
            ratio = torch.exp(logprobs - exp['policy_logprobs'])
            
            # KL penalty
            kl = self.compute_kl_penalty(logprobs, exp['ref_logprobs'])
            
            # PPO clipped objective
            reward = exp['reward'] - self.kl_coef * kl
            advantages = reward  # Simplified (no GAE for single-token rewards)
            
            pg_loss = -torch.min(
                ratio * advantages,
                torch.clamp(ratio, 1 - self.clip_epsilon, 1 + self.clip_epsilon) * advantages
            ).mean()
            
            self.optimizer.zero_grad()
            pg_loss.backward()
            torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 1.0)
            self.optimizer.step()
        
        return pg_loss.item()
```

## Reward Shaping

```python
def composite_reward(reward_model_score, safety_score=None, length_penalty=0.0):
    """Combine multiple reward signals."""
    reward = reward_model_score
    
    if safety_score is not None:
        # Penalize unsafe responses
        reward -= safety_score_coef * max(0, safety_threshold - safety_score)
    
    if length_penalty != 0:
        # Optional length penalty (shorter responses often preferred)
        pass
    
    return reward

def reward_normalize(rewards):
    """Normalize rewards to have zero mean and unit variance.
    Crucial for PPO stability."""
    rewards = torch.tensor(rewards)
    return (rewards - rewards.mean()) / (rewards.std() + 1e-8)
```

## Efficiency Optimizations

```python
# LoRA for RLHF: only train LoRA adapters instead of full model
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05
)
policy_model = get_peft_model(policy_model, lora_config)

# Reward model can also be LoRA-tuned
# This dramatically reduces memory requirements
```

## Common Pitfalls

1. **Reward hacking** — model exploits reward signal in unintended ways; use KL penalty and diverse reward signals
2. **KL collapse** — too strong KL penalty prevents learning; too weak allows mode collapse; tune carefully
3. **Catastrophic forgetting** — model loses language capabilities; mix in SFT loss during PPO (10-20% weight)
4. **Reward model over-optimization** — RM scores improve but actual quality degrades; use held-out RM and human eval
5. **Mode collapse** — policy produces low-diversity outputs; increase entropy bonus or use diverse prompts
6. **Memory explosion** — policy + reference + reward model + value model = 4x memory; use LoRA or offloading

## Verification Checklist

- [ ] Reward model achieves >70% accuracy on held-out preference pairs
- [ ] PPO training increases average reward without increasing KL beyond threshold
- [ ] Human evaluation shows improvement over SFT baseline
- [ ] No reward hacking detected (qualitative review of high-reward outputs)
- [ ] Model retains language capabilities (standard benchmark score drop < 5%)
- [ ] Output diversity maintained (distinct-N, perplexity metrics)
- [ ] Safety benchmarks don't regress

## See Also

- reinforcement-learning — foundational RL concepts
- llm-fine-tuning-lora — efficient fine-tuning for RLHF
- deep-reinforcement-learning — PPO implementation details
- agent-safety-alignment — safety evaluation for aligned models
