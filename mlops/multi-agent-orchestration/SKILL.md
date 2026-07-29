---
name: multi-agent-orchestration
description: "Use when orchestrating multiple AI agents working together."
category: mlops
tags: [agents, orchestration, multi-agent, swarms, coordinator]
---
# Multi-Agent Orchestration

Orchestrating multiple AI agents for complex tasks.

## Orchestration Patterns

### Manager-Worker
```
Manager Agent
├── Worker Agent 1 (research)
├── Worker Agent 2 (code)
└── Worker Agent 3 (review)
```

### Pipeline
```
Agent A (parse) → Agent B (analyze) → Agent C (generate) → Agent D (verify)
```

### Debate
```
Agent A (pro) ↔ Agent B (con) → Judge Agent (synthesis)
```

### Ensemble
```
Agent A → answer
Agent B → answer  → Consensus Agent
Agent C → answer
```

## Manager-Worker Implementation

```python
class WorkerAgent:
    def __init__(self, name: str, role: str, llm, tools: dict):
        self.name = name
        self.role = role
        self.llm = llm
        self.tools = tools
        self.system_prompt = f"You are {name}, a {role}. Be concise."

    def execute(self, task: str) -> str:
        return self.llm.invoke(f"{self.system_prompt}\nTask: {task}")

class ManagerAgent:
    def __init__(self, llm, workers: list[WorkerAgent]):
        self.llm = llm
        self.workers = {w.name: w for w in workers}

    def run(self, task: str) -> dict:
        # 1. Decompose task
        plan = self.llm.invoke(
            f"Decompose this task into subtasks for available workers.\n"
            f"Workers: {list(self.workers.keys())}\nTask: {task}\n"
            f"Format: worker_name: subtask"
        )

        # 2. Dispatch to workers
        results = {}
        for line in plan.strip().split("\n"):
            if ":" in line:
                worker_name, subtask = line.split(":", 1)
                worker_name = worker_name.strip()
                if worker_name in self.workers:
                    results[worker_name] = self.workers[worker_name].execute(subtask.strip())

        # 3. Synthesize
        summary = self.llm.invoke(
            f"Synthesize these results:\n{results}\nOriginal task: {task}"
        )
        return {"plan": plan, "results": results, "summary": summary}
```

## Pipeline Orchestration

```python
class PipelineAgent:
    def __init__(self, stages: list[dict]):
        self.stages = stages  # [{"name": str, "agent": Agent, "input_key": str, "output_key": str}]

    def run(self, initial_input: dict) -> dict:
        context = initial_input
        for stage in self.stages:
            input_data = context.get(stage["input_key"], "")
            result = stage["agent"].execute(input_data)
            context[stage["output_key"]] = result
            print(f"[{stage['name']}] → {stage['output_key']}")
        return context
```

## Consensus / Debate

```python
class DebateAgent:
    def __init__(self, pro_agent, con_agent, judge_agent, rounds=3):
        self.pro = pro_agent
        self.con = con_agent
        self.judge = judge_agent
        self.rounds = rounds

    def run(self, proposition: str) -> str:
        pro_args = []
        con_args = []

        for r in range(self.rounds):
            pro_arg = self.pro.execute(
                f"Round {r+1}. Argue FOR: {proposition}.\n"
                f"Counter previous con points: {con_args[-1] if con_args else 'None'}"
            )
            pro_args.append(pro_arg)

            con_arg = self.con.execute(
                f"Round {r+1}. Argue AGAINST: {proposition}.\n"
                f"Counter previous pro points: {pro_args[-1]}"
            )
            con_args.append(con_arg)

        verdict = self.judge.execute(
            f"After {self.rounds} rounds of debate:\n"
            f"Pro arguments: {pro_args}\nCon arguments: {con_args}\n"
            f"Provide a balanced synthesis and verdict on: {proposition}"
        )
        return verdict
```

## Error Handling in Swarms

```python
class ResilientOrchestrator:
    def __init__(self, workers: list, retries=2, fallback=None):
        self.workers = workers
        self.retries = retries
        self.fallback = fallback

    def dispatch(self, task: str, preferred_worker: str = None) -> str:
        workers = [w for w in self.workers if w.name == preferred_worker] or self.workers

        for worker in workers:
            for attempt in range(self.retries):
                try:
                    return worker.execute(task)
                except Exception as e:
                    if attempt == self.retries - 1:
                        print(f"Worker {worker.name} failed: {e}")
                        break
                    continue

        if self.fallback:
            return self.fallback.execute(task)
        return "All workers failed"
```

## Pitfalls

- Manager becomes bottleneck — distribute decision-making
- Worker context isolation prevents interference
- Token costs multiply per agent — budget carefully
- Synchronous pipelines block on slow agents — use async
- Agent output quality varies — implement validation gates
