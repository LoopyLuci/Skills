---
name: agent-evaluation-metrics
description: "Use when evaluating AI agent performance."
category: mlops
tags: [agents, evaluation, metrics, benchmarking, performance]
---
# Agent Evaluation Metrics

Measuring and evaluating AI agent performance systematically.

## Core Metrics

```
Task Success:
  - Success Rate: fraction of tasks completed successfully
  - Partial Success: fraction of subtasks completed
  - Goal Satisfaction: user rates output quality (1-5)

Efficiency:
  - Steps to Completion: fewer = better planning
  - Time to Complete: wall-clock time
  - Token Cost: total tokens consumed

Quality:
  - Output Accuracy: factual correctness
  - Tool Selection Accuracy: choosing the right tool for the job
  - Hallucination Rate: claiming things not supported by context

Safety:
  - Error Rate: operations that failed
  - Damage Rate: operations that caused irreversible harm
  - Constraint Violations: ignoring user-specified limits
```

## Evaluation Framework

```python
from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime

@dataclass
class AgentEvaluation:
    task: str
    success: bool
    steps: int
    tokens_used: int
    tools_called: list[dict]
    errors: list[str]
    partial_score: float = 0.0  # 0.0 to 1.0
    user_rating: Optional[int] = None

class AgentEvaluator:
    def __init__(self):
        self.results = []

    def evaluate_task(self, agent, task: str, expected_output: Any = None) -> AgentEvaluation:
        start = datetime.now()
        errors = []
        tools_called = []
        steps = 0

        try:
            result = agent.run(task)
            steps = len(agent.steps)
            tools_called = [s.get("tool") for s in agent.steps if "tool" in s]
        except Exception as e:
            errors.append(str(e))
            result = None

        success = self._check_success(result, expected_output)
        partial = self._compute_partial(result, expected_output)
        tokens = sum(s.get("tokens", 0) for s in getattr(agent, "steps", []))

        eval_result = AgentEvaluation(
            task=task, success=success, steps=steps,
            tokens_used=tokens, tools_called=tools_called,
            errors=errors, partial_score=partial,
        )
        self.results.append(eval_result)
        return eval_result

    def summary(self) -> dict:
        if not self.results:
            return {"error": "No evaluations"}
        n = len(self.results)
        return {
            "tasks": n,
            "success_rate": sum(1 for r in self.results if r.success) / n,
            "avg_steps": sum(r.steps for r in self.results) / n,
            "avg_tokens": sum(r.tokens_used for r in self.results) / n,
            "total_errors": sum(len(r.errors) for r in self.results),
            "avg_partial_score": sum(r.partial_score for r in self.results) / n,
        }
```

## Agent Benchmark Suites

```
Tool-Use Benchmarks:
  - ToolBench: 16 real-world APIs
  - API-Bank: 300+ API tools
  - SWE-Bench: GitHub issue resolution

Reasoning Benchmarks:
  - GSM8K: math word problems
  - HotpotQA: multi-hop QA
  - AgentBench: OS/tasks

Safety Benchmarks:
  - AdvBench: harmful request detection
  - TruthfulQA: factual accuracy
```

## Cost Analysis

```python
@dataclass
class AgentCost:
    prompt_tokens: int
    completion_tokens: int
    tool_call_count: int
    model: str

    def estimate_cost(self, rates: dict = None) -> float:
        if rates is None:
            rates = {
                "gpt-4": {"prompt": 0.03, "completion": 0.06},
                "gpt-3.5": {"prompt": 0.001, "completion": 0.002},
            }
        r = rates.get(self.model, {"prompt": 0.01, "completion": 0.02})
        prompt_cost = (self.prompt_tokens / 1000) * r["prompt"]
        completion_cost = (self.completion_tokens / 1000) * r["completion"]
        return prompt_cost + completion_cost
```

## Pitfalls

- Success rate alone doesn't capture partial progress
- Token cost varies hugely by model (GPT-4 vs 3.5 vs local)
- Evaluation tasks must match real usage distribution
- Multiple runs needed per task (non-deterministic outputs)
- User ratings are subjective — combine with automated metrics
