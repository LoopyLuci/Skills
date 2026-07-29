---
name: multi-agent-routing-optimization
description: "Use when optimizing routing between specialized AI agents."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents, routing, optimization, orchestration, load-balancing]
    related_skills: [agent-routing-models, agent-swarm-architectures, hierarchical-swarm-architectures, multi-agent-orchestration, agent-task-decomposition]
---

# Multi-Agent Routing Optimization

Techniques for intelligently routing tasks, queries, and messages between specialized agents to minimize latency, maximize throughput, and balance load across the swarm.

## When to Use

- Your swarm has 5+ specialized agents and tasks need matching to the right agent
- Agents have overlapping capabilities and you need optimal assignment
- You observe hot-spotting (some agents overloaded while others idle)
- Tasks have different priority levels that should influence routing
- You need to minimize end-to-end latency across multi-step agent pipelines

## Routing Strategies

### Content-Based Routing

Route based on task content/type:

```python
class ContentRouter:
    def __init__(self):
        self.routes = {
            "code": ["code-writer", "code-reviewer"],
            "research": ["web-researcher", "paper-analyzer"],
            "creative": ["writer", "designer"],
            "data": ["data-analyst", "visualizer"],
            "default": ["general-assistant"]
        }
    
    def route(self, task_description):
        """Classify task and route to appropriate agent pool."""
        task_type = self.classify(task_description)
        candidates = self.routes.get(task_type, self.routes["default"])
        return self.pick_best(candidates, task_description)
    
    def classify(self, text):
        """Simple keyword or ML-based classification."""
        keywords = {
            "code": ["write code", "implement", "function", "bug", "refactor"],
            "research": ["find", "research", "paper", "literature", "study"],
            "creative": ["write", "design", "create", "compose", "draft"],
            "data": ["analyze", "visualize", "statistics", "dataset", "plot"]
        }
        text_lower = text.lower()
        scores = {}
        for category, kws in keywords.items():
            scores[category] = sum(1 for kw in kws if kw in text_lower)
        return max(scores, key=scores.get) if max(scores.values()) > 0 else "default"
    
    def pick_best(self, candidates, task):
        """Load-balance among candidate agents."""
        loads = [get_agent_load(a) for a in candidates]
        return candidates[loads.index(min(loads))]
```

### Semantic Routing

Use embeddings to match task intent to agent capability:

```python
import numpy as np

class SemanticRouter:
    def __init__(self, agent_profiles, embedding_fn):
        """
        agent_profiles: dict of {agent_id: {"capability_desc": str, "embedding": None}}
        embedding_fn: function that returns embedding vector for text
        """
        self.agent_ids = list(agent_profiles.keys())
        # Pre-compute capability embeddings
        self.cap_embeddings = np.array([
            embedding_fn(agent_profiles[a]["capability_desc"])
            for a in self.agent_ids
        ])
        self.embedding_fn = embedding_fn
    
    def route(self, task_text, top_k=1):
        """Route task to agent with most similar capability description."""
        task_emb = self.embedding_fn(task_text)
        similarities = np.dot(self.cap_embeddings, task_emb) / (
            np.linalg.norm(self.cap_embeddings, axis=1) * np.linalg.norm(task_emb)
        )
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [self.agent_ids[i] for i in top_indices]
```

### Priority-Based Routing

Higher priority tasks preempt lower priority ones:

```python
class PriorityRouter:
    def __init__(self):
        self.queues = {
            "critical": [],  # Processed immediately
            "high": [],      # After critical
            "normal": [],    # Default
            "low": []        # Background
        }
        self.current_task = None
    
    def enqueue(self, task, priority="normal"):
        self.queues[priority].append(task)
    
    def dequeue(self):
        """Get highest priority waiting task."""
        for priority in ["critical", "high", "normal", "low"]:
            if self.queues[priority]:
                return self.queues[priority].pop(0)
        return None
    
    def preempt(self, new_task):
        """Preempt current task if new task is higher priority."""
        if self.current_task and new_task.priority > self.current_task.priority:
            self.enqueue(self.current_task, self.current_task.priority)
            self.current_task.pending = True  # Mark as interrupted
            return True
        return False
```

## Load Balancing

### Least-Connections

Route to agent with fewest current tasks:

```python
def least_connections(agents):
    """Pick agent with minimum active task count."""
    return min(agents, key=lambda a: a.active_tasks)
```

### Weighted Distribution

Account for agent capability differences:

```python
def weighted_distribution(agents, agent_weights):
    """Distribute tasks proportionally to weights."""
    total_weight = sum(agent_weights.values())
    current_loads = {a: a.active_tasks for a in agents}
    
    # Normalize: actual_load / capacity
    normalized = {
        a: current_loads[a] / agent_weights.get(a, 1)
        for a in agents
    }
    return min(normalized, key=normalized.get)
```

### Adaptive Routing

Learn from past routing outcomes:

```python
class AdaptiveRouter:
    def __init__(self, decay=0.95):
        self.success_rates = {}  # agent_id -> rolling success rate
        self.latency_history = {}  # agent_id -> [latency samples]
        self.decay = decay
    
    def record_outcome(self, agent_id, success, latency):
        """Update agent stats after task completion."""
        # Success rate (exponential moving average)
        prev = self.success_rates.get(agent_id, 0.5)
        self.success_rates[agent_id] = prev * self.decay + (1 - self.decay) * int(success)
        
        # Latency
        self.latency_history.setdefault(agent_id, []).append(latency)
        if len(self.latency_history[agent_id]) > 100:
            self.latency_history[agent_id].pop(0)
    
    def score_agent(self, agent_id):
        """Composite score for routing decisions."""
        success = self.success_rates.get(agent_id, 0.5)
        latencies = self.latency_history.get(agent_id, [100])
        avg_latency = sum(latencies) / len(latencies)
        # Higher success rate + lower latency = better score
        return success * (1 / (1 + avg_latency))
    
    def route(self, agents):
        """Route to highest-scored available agent."""
        scores = {a: self.score_agent(a) for a in agents}
        return max(scores, key=scores.get)
```

## Pipeline Routing

For multi-step tasks that pass through multiple agents in sequence:

```python
class PipelineRouter:
    def __init__(self, pipeline_def):
        """
        pipeline_def: list of (stage_name, router_for_stage) tuples
        """
        self.stages = pipeline_def
    
    def execute(self, initial_input):
        current_input = initial_input
        for stage_name, router in self.stages:
            agent = router.route(current_input)
            current_input = agent.process(current_input)
        return current_input
```

## Circuit Breaker Pattern

Prevent routing to failing agents:

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failures = {}
        self.threshold = failure_threshold
        self.timeout = reset_timeout
        self.state = {}  # agent_id -> "closed" | "open" | "half-open"
        self.last_failure_time = {}
    
    def record_success(self, agent_id):
        self.failures[agent_id] = 0
        self.state[agent_id] = "closed"
    
    def record_failure(self, agent_id):
        self.failures[agent_id] = self.failures.get(agent_id, 0) + 1
        if self.failures[agent_id] >= self.threshold:
            self.state[agent_id] = "open"
            self.last_failure_time[agent_id] = time.time()
    
    def is_available(self, agent_id):
        if self.state.get(agent_id) != "open":
            return True
        # Check if timeout elapsed
        if time.time() - self.last_failure_time.get(agent_id, 0) > self.timeout:
            self.state[agent_id] = "half-open"  # Try one request
            return True
        return False
```

## Metrics for Routing Quality

```python
# Track these metrics to evaluate routing performance
routing_metrics = {
    "avg_latency_ms": 0,        # End-to-end task latency
    "throughput_tps": 0,        # Tasks per second
    "agent_utilization_pct": {},  # Per-agent busy time %
    "queue_depth": 0,           # Waiting tasks count
    "routing_accuracy_pct": 0,  # Right-agent-for-task rate
    "circuit_breaker_trips": 0, # How often breakers open
}
```

## Common Pitfalls

1. **Sticky sessions** — routing similar tasks to the same agent creates cache benefits but imbalance; use bounded stickiness
2. **Router bottleneck** — the router itself becomes a bottleneck; consider distributed hashing for large swarms
3. **Cold start** — new agents have no history; use default weights and warm up with low-priority tasks
4. **Stale capability profiles** — agents' skills evolve; periodically re-embed or update profiles
5. **Priority inversion** — low-priority tasks blocking higher-priority ones; implement preemption
6. **Oscillation** — router ping-pongs tasks between agents due to load metric noise; add damping

## Verification Checklist

- [ ] Routing strategy matches task diversity and agent specialization
- [ ] Load balancing prevents hot-spotting under peak load
- [ ] Circuit breakers configured for each agent
- [ ] Priority queues defined with preemption support
- [ ] Routing quality metrics collected and monitorable
- [ ] Cold-start strategy for new agents
- [ ] Pipeline routing has fallback at each stage

## See Also

- agent-routing-models — base routing model patterns
- agent-swarm-architectures — swarm topology
- hierarchical-swarm-architectures — multi-level hierarchies
- agent-task-decomposition — task breakdown for routing
