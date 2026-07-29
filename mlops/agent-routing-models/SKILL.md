---
name: agent-routing-models
description: "Use when routing tasks between specialized agents."
category: mlops
tags: [agents, routing, classification, orchestration]
---
# Agent Routing Models

Routing tasks to the right agent based on task type, complexity, and agent capability.

## Routing Strategies

### Rule-Based Routing
```python
class RuleRouter:
    def route(self, task: str) -> str:
        task_lower = task.lower()

        if any(kw in task_lower for kw in ["docker", "container", "image", "volume"]):
            return "docker_agent"
        elif any(kw in task_lower for kw in ["c++", "rust", "compile", "build"]):
            return "build_agent"
        elif any(kw in task_lower for kw in ["python", "script", "data"]):
            return "python_agent"
        elif any(kw in task_lower for kw in ["wsl", "linux", "ubuntu"]):
            return "wsl_agent"
        else:
            return "general_agent"
```

### LLM-Based Router

```python
class LLMRouter:
    def __init__(self, router_llm, agents: dict):
        self.llm = router_llm
        self.agents = agents  # agent_name → {description, capabilities}

    def route(self, task: str) -> str:
        prompt = f"""Available agents:
{self._format_agents()}

User task: {task}

Which agent should handle this? Respond with just the agent name."""
        return self.llm.invoke(prompt).strip()

    def route_with_confidence(self, task: str) -> tuple[str, float]:
        prompt = f"""Available agents:
{self._format_agents()}

User task: {task}

Respond in JSON: {{"agent": "agent_name", "confidence": 0.95, "reason": "brief reason"}}"""
        import json
        result = json.loads(self.llm.invoke(prompt))
        return result["agent"], result["confidence"]

    def _format_agents(self) -> str:
        lines = []
        for name, info in self.agents.items():
            lines.append(f"- {name}: {info['description']} (capabilities: {', '.join(info['capabilities'])})")
        return "\n".join(lines)
```

### Embedding-Based Router

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class EmbeddingRouter:
    def __init__(self, agents: dict):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.agents = agents
        # Pre-encode agent descriptions
        self.agent_embeddings = {
            name: self.encoder.encode(info["description"])
            for name, info in agents.items()
        }

    def route(self, task: str) -> str:
        task_embedding = self.encoder.encode(task)
        scores = {
            name: cosine_similarity([task_embedding], [emb])[0][0]
            for name, emb in self.agent_embeddings.items()
        }
        best = max(scores, key=scores.get)
        return best
```

### Hybrid Router

```python
class HybridRouter:
    def __init__(self, rule_router: RuleRouter, llm_router: LLMRouter,
                 embedding_router: EmbeddingRouter):
        self.routers = [rule_router, llm_router, embedding_router]

    def route(self, task: str) -> str:
        votes = {}
        for router in self.routers:
            result = router.route(task)
            votes[result] = votes.get(result, 0) + 1
        return max(votes, key=votes.get)
```

## Task Classification Router

```python
class TaskClassifier:
    def __init__(self, llm):
        self.llm = llm

    def classify(self, task: str) -> dict:
        prompt = f"""Classify this task:
Task: {task}

Categories:
- type: question|instruction|debugging|analysis|creation
- domain: docker|wsl|windows|cpp|rust|python|general
- complexity: simple|medium|complex
- requires_admin: true|false
- estimated_steps: <number>

Respond in JSON format."""
        import json
        return json.loads(self.llm.invoke(prompt))
```

## Priority Routing

```python
class PriorityRouter(RuleRouter):
    def __init__(self, agents: dict, priority_map: dict = None):
        super().__init__()
        self.agents = agents
        self.priority_map = priority_map or {
            "error": 1,     # highest priority
            "blocking": 2,
            "feature": 3,
            "question": 4,
            "research": 5,
        }

    def route(self, task: str, urgency: str = "normal") -> tuple[str, int]:
        agent = super().route(task)
        priority = self.priority_map.get(urgency, 5)
        return agent, priority
```

## Pitfalls

- Rule-based: misses edge cases, needs constant updating
- LLM-based: adds latency and cost per routing decision
- Embedding-based: requires pre-encoded descriptions, domain-dependent
- No router handles 100% — always implement fallback agent
- Cold start: new agents need routing rules until sufficient routing data
