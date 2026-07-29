---
name: reinforcement-learning-human-feedback
description: "Use when implementing RLHF or RLAIF for alignment."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [RLHF, reinforcement-learning, human-feedback, alignment, reward-modeling, PPO, DPO]
    related_skills: [rlhf-implementation-guide, advanced-reasoning-patterns, agent-ethics-alignment, custom-training-loops]
---

# Reinforcement Learning from Human Feedback

Implementing RLHF and alternatives (DPO, RLAIF) — from preference data collection through reward modeling and reinforcement learning optimization for LLM alignment.

## When to Use

- Aligning LLMs with human preferences and values
- Fine-tuning models to follow instructions
- Reducing harmful or biased model outputs
- Improving model helpfulness and honesty

## Methods Compared

```python
ALIGNMENT_METHODS = {
    'rlhf_ppo': 'Four-stage: SFT → reward model → PPO optimization → evaluation',
    'dpo': 'Direct Preference Optimization — closed-form, no separate reward model',
    'rrlhf': 'Rejection sampling + PPO — simpler than full RLHF',
    'rlaif': 'AI-generated preferences instead of human labels — scalable',
    'constitutional_ai': 'Self-critique and revision based on constitution — no human feedback needed',
}

def dpo_loss(policy_logps, ref_logps, wins, losses):
    """Direct Preference Optimization loss."""
    import torch.nn.functional as F
    win_logps = policy_logps[wins] - ref_logps[wins]
    lose_logps = policy_logps[losses] - ref_logps[losses]
    log_odds = win_logps - lose_logps
    beta = 0.1  # KL penalty coefficient
    return -F.logsigmoid(beta * log_odds).mean()
```

## Verification Checklist

- [ ] Alignment method chosen (PPO-RLHF, DPO, RLAIF)
- [ ] Preference data collected/generated with quality controls
- [ ] Reward model trained and validated (if using RLHF)
- [ ] KL penalty prevents reward hacking (if using PPO)
- [ ] Alignment evaluation: helpfulness, harmlessness, honesty
- [ ] Compared against SFT baseline
- [ ] Safety evaluations before deployment
