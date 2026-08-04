---
name: agent-task-decomposition
description: "Use when decomposing tasks for multi-agent execution."
category: mlops
tags: [agents, task-decomposition, planning, sub-tasks]
---
# Agent Task Decomposition

Breaking complex tasks into manageable subtasks for agent execution.

## Decomposition Strategies

### Top-Down (Hierarchical)
```
Task: "Set up a production Docker environment"
├── Install Docker Engine
│   ├── Select OS
│   ├── Install via package manager
│   └── Configure daemon.json
├── Configure networking
│   ├── Create bridge network
│   ├── Set up reverse proxy
│   └── Configure TLS
├── Deploy services
│   ├── Database container
│   ├── Application container
│   └── Monitoring stack
└── Verify and test
    ├── Health checks
    ├── Logging
    └── Backup strategy
```

### Bottom-Up (Data Flow)
```
Input: "github.com/user/repo"
├── Clone and analyze
├── Identify Docker components
├── Check for docker-compose.yml
├── Identify service dependencies
├── Generate docker-compose.yml
└── Output: deployment-ready config
```

### Dependency Graph
```
Task A ──┐
         ├──→ Task C ──→ Task D
Task B ──┘
         └──→ Task E (parallel with C)
```

## Decomposition Agent

```python
class TaskDecomposer:
    def __init__(self, llm):
        self.llm = llm

    def decompose(self, task: str, max_depth: int = 3) -> list:
        prompt = f"""Decompose this task into subtasks:
Task: {task}

Rules:
- Each subtask must be independently executable
- Subtasks should be sequential unless marked [PARALLEL]
- Max depth: {max_depth}
- Use format: level: subtask_description [dependency]

Example:
1: Install Docker [none]
2: Configure daemon.json [1]
3: Create network [1]
4 [PARALLEL]: Start database [3]
5 [PARALLEL]: Start application [3]"""
        return self.llm.invoke(prompt)

    def estimate_effort(self, subtasks: list) -> dict:
        prompt = f"""Estimate effort for each subtask:
{subtasks}
Format: subtask: (easy|medium|hard) - estimated_steps"""
        return self.llm.invoke(prompt)
```

## Assigning to Workers

```python
def assign_subtasks(subtasks: list, workers: dict) -> list:
    """Assign subtasks to available workers based on expertise."""
    assignments = []

    for subtask in subtasks:
        best_worker = None
        best_score = -1

        for worker_name, worker_info in workers.items():
            # Simple overlap scoring
            score = len(set(subtask.lower().split()) & set(worker_info["keywords"]))
            if score > best_score:
                best_score = score
                best_worker = worker_name

        assignments.append({
            "subtask": subtask,
            "worker": best_worker,
            "score": best_score,
        })

    return assignments
```

## Dependency Resolution

```python
class DependencyResolver:
    def __init__(self):
        self.completed = set()
        self.dependencies = {}  # subtask → [dependencies]

    def add_subtask(self, subtask: str, deps: list[str]):
        self.dependencies[subtask] = deps

    def get_ready(self) -> list[str]:
        """Get subtasks whose dependencies are all met."""
        return [
            s for s, deps in self.dependencies.items()
            if s not in self.completed and all(d in self.completed for d in deps)
        ]

    def mark_complete(self, subtask: str):
        self.completed.add(subtask)

    def is_dag(self) -> bool:
        """Check if dependency graph has cycles."""
        visited = set()
        path = set()

        def dfs(node):
            if node in path: return False
            if node in visited: return True
            path.add(node)
            for dep in self.dependencies.get(node, []):
                if not dfs(dep): return False
            path.remove(node)
            visited.add(node)
            return True

        return all(dfs(n) for n in self.dependencies)
```

## Parallel Execution Planner

```python
class ParallelPlanner:
    def __init__(self, max_parallel: int = 3):
        self.max_parallel = max_parallel

    def plan_batches(self, subtasks: list) -> list[list]:
        """Group subtasks into parallel-executable batches."""
        resolver = DependencyResolver()

        for item in subtasks:
            resolver.add_subtask(item["name"], item.get("dependencies", []))

        batches = []
        remaining = {item["name"] for item in subtasks}

        while remaining:
            ready = [s for s in remaining if s in resolver.get_ready()]
            if not ready:
                raise ValueError("Deadlock in dependency graph")

            batch = ready[:self.max_parallel]
            batches.append(batch)
            for s in batch:
                remaining.remove(s)
                resolver.mark_complete(s)

        return batches
```

## Pitfalls

- Over-decomposition creates coordination overhead
- Under-decomposition creates complex, unmanageable subtasks
- Circular dependencies must be detected before execution
- Parallel execution needs idempotent subtasks (no shared mutable state)
- Depth limits prevent runaway recursion but may miss granular work
