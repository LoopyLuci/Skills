---
name: agent-ensembles-voting
description: "Use when implementing multi-agent ensemble voting systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents, ensemble, voting, consensus, multi-agent, debate]
    related_skills: [agent-swarm-architectures, swarm-communication-protocols, agent-reasoning-patterns, agent-evaluation-metrics]
---

# Agent Ensembles and Voting

Techniques for combining outputs from multiple agents through voting, ensemble weighting, debate, and consensus mechanisms to improve reliability and accuracy.

## When to Use

- Improving answer reliability by sampling multiple independent agents
- Reducing single-agent hallucination risk through cross-validation
- Aggregating diverse expert agent opinions (e.g., multiple domain specialists)
- Building debate/reflection systems where agents critique each other
- Implementing self-consistency checks for critical decisions

## Voting Strategies

### Simple Majority

Each agent votes, majority wins:

```python
def majority_vote(agent_responses, num_agents):
    """Classic majority voting. Best for classification tasks."""
    from collections import Counter
    vote_counts = Counter(agent_responses)
    winner, count = vote_counts.most_common(1)[0]
    confidence = count / num_agents
    return winner, confidence
```

### Weighted Voting

Agents have weights based on past accuracy:

```python
def weighted_vote(agent_responses, agent_weights):
    """Each agent's vote weighted by historical performance."""
    score = {}
    for response, weight in zip(agent_responses, agent_weights):
        score[response] = score.get(response, 0) + weight
    winner = max(score, key=score.get)
    total_weight = sum(agent_weights)
    return winner, score[winner] / total_weight
```

### Confidence-Weighted Voting

Agents report confidence alongside their answer:

```python
def confidence_weighted_vote(agent_responses_with_confidence):
    """Weight votes by each agent's self-reported confidence."""
    score = {}
    for response, confidence in agent_responses_with_confidence:
        score[response] = score.get(response, 0) + confidence
    winner = max(score, key=score.get)
    return winner
```

### Borda Count

Rated voting where each agent ranks options:

```python
def borda_count(agent_rankings, num_options):
    """Each agent ranks options; Borda points assigned by rank."""
    scores = {}
    for ranking in agent_rankings:  # ranking = [best, 2nd, 3rd, ...]
        for i, option in enumerate(ranking):
            points = num_options - i
            scores[option] = scores.get(option, 0) + points
    return max(scores, key=scores.get)
```

## Ensemble Architectures

### Parallel Ensemble (Independent)

```
[Agent 1]  [Agent 2]  [Agent 3]  [Agent N]
     \          |          |        /
      └─────────VOTER──────────────┘
              (Result)
```

Best for: Independent expert agents, diverse perspectives, speed.

**Implementation**:
```python
from hermes_tools import delegate_task

# Launch N agents in parallel
tasks = [
    {"goal": f"Answer: {question}", "context": f"Role: domain expert {i}"}
    for i in range(num_agents)
]
results = delegate_task(tasks=tasks)

# Vote on responses
winner, confidence = majority_vote([r.summary for r in results], len(results))
```

### Sequential Refinement (Pipeline)

```
[Agent 1] → [Agent 2] → [Agent 3] → Result
   (draft)    (review)    (finalize)
```

Best for: Writing, code generation, planning — tasks that benefit from iteration.

**Implementation**:
```python
# Sequential: each agent refines previous output
draft = delegate_task(goal="Write initial solution for: " + problem)
review = delegate_task(goal="Review and critique this solution", context=draft)
final = delegate_task(goal="Fix issues from review. Produce final answer.", context=review)
```

### Debate Ensemble

```
[Agent A] ← → [Agent B]
    ↓     ↑     ↓
[Agent C] ← → [Agent D]
    ↓     ↑
  [JUDGE]
```

Two or more agents debate, each round exposes flaws in the other's reasoning:

```python
def debate_round(question, agents, rounds=3):
    """Multi-agent debate with iterative refinement."""
    positions = [agent.initial_answer(question) for agent in agents]
    
    for round in range(rounds):
        for i, agent in enumerate(agents):
            critiques = []
            for j, other_pos in enumerate(positions):
                if i != j:
                    critiques.append(other_pos)
            positions[i] = agent.refine(question, positions[i], critiques)
    
    # Judge evaluates final positions
    judge = LLMJudge()
    return judge.evaluate(question, positions)
```

### Mixture of Agents (MoA)

Layered ensemble where each layer's agents feed into the next:

```python
def mixture_of_agents(question, layers, num_agents_per_layer=4):
    """Each agent in layer N sees outputs from layer N-1 agents."""
    layer_outputs = []
    
    for layer_idx, agents in enumerate(layers):
        current_outputs = []
        tasks = []
        for agent in agents:
            context = f"Previous layer outputs: {layer_outputs}" if layer_outputs else ""
            tasks.append({
                "goal": f"Answer: {question}",
                "context": context
            })
        layer_outputs = delegate_task(tasks=tasks)
    
    return layer_outputs  # Final layer outputs
```

## Self-Consistency

Ask the same agent the same question multiple times with different temperatures:

```python
def self_consistency(question, agent, num_samples=5, temperature=0.7):
    """Sample multiple reasoning paths from same agent."""
    responses = []
    for i in range(num_samples):
        response = agent.answer(question, temperature=temperature + i*0.1)
        responses.append(response)
    
    # Majority vote on final answers
    winner, confidence = majority_vote(responses, num_samples)
    return winner, confidence, responses
```

## Confidence Scoring

```python
def compute_ensemble_confidence(votes, method="entropy"):
    """Compute ensemble confidence using entropy or agreement."""
    from collections import Counter
    import math
    
    counts = Counter(votes)
    total = len(votes)
    probs = [c/total for c in counts.values()]
    
    if method == "entropy":
        # Lower entropy = higher confidence
        entropy = -sum(p * math.log(p) for p in probs)
        max_entropy = math.log(len(counts))
        confidence = 1 - (entropy / max_entropy) if max_entropy > 0 else 1.0
    elif method == "agreement":
        # Highest vote share
        confidence = max(probs)
    
    return confidence
```

## When to Use Each Strategy

| Strategy | Best For | Num Agents | Trade-off |
|----------|---------|------------|-----------|
| Simple Majority | Classification | 3–11 | Fast, but ignores confidence |
| Weighted Voting | Known agent strengths | 3–20 | Needs historical data |
| Confidence-Weighted | Varied confidence | 3–10 | Requires calibrated confidence |
| Borda Count | Ranking tasks | 3–10 | Handles ties well |
| Parallel Ensemble | Speed-critical | 3–∞ | Resource heavy for many agents |
| Sequential Refinement | Quality-critical | 2–5 | Slow, but best quality |
| Debate | Reasoning tasks | 2–6 | Expensive, but catches flaws |
| MoA | Complex reasoning | 8–20 | State of the art quality |
| Self-Consistency | Single agent | 1 × N runs | No multi-agent overhead |

## Common Pitfalls

1. **False consensus** — all agents make the same mistake (training data bias); diversify agent roles
2. **Weight staleness** — agent weights from months ago don't reflect current accuracy
3. **Cost explosion** — N agents × M debate rounds is expensive; set budget limits
4. **Voter fatigue** — agents optimized for consensus rather than truth; penalize groupthink
5. **Judge bias** — the judge agent may favor certain agent types; use multiple judges
6. **Sequential bottleneck** — pipeline mode is only as fast as the slowest agent

## Verification Checklist

- [ ] Voting strategy chosen based on task type (classification/ranking/generation)
- [ ] Agent diversity verified (different context, role, or sampling parameters)
- [ ] Confidence threshold set for when to fall back to human review
- [ ] Cost budget defined (max agents × max rounds)
- [ ] Judge agent (if used) is neutral and distinct from debaters
- [ ] Self-consistency temperature range appropriate for task
- [ ] Experimental validation: ensemble outperforms best single agent

## See Also

- agent-reasoning-patterns — individual agent reasoning strategies
- agent-swarm-architectures — swarm topology design
- swarm-communication-protocols — agent messaging patterns
- agent-evaluation-metrics — measuring agent performance
