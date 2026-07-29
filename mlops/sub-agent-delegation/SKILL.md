---
name: sub-agent-delegation
description: "Use when delegating subtasks to sub-agents."
category: mlops
tags: [agents, delegation, sub-agents, sub-tasks, hierarchy]
---
# Sub-Agent Delegation

Delegating tasks to sub-agents with context, constraints, and result verification.

## Delegation Contract

```
Parent Agent
├── Defines: goal, context, constraints, output format
├── Delegates to: Sub-Agent
│   ├── Receives: isolated context + task
│   ├── Executes: independently (tools, research, code)
│   └── Returns: result + metadata (confidence, steps taken)
└── Verifies: result meets constraints before accepting
```

## Delegation Implementation

```python
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class DelegationRequest:
    task: str
    context: str
    constraints: list[str]
    output_format: str
    max_steps: int = 20
    parent_notify_url: Optional[str] = None

@dataclass
class DelegationResult:
    success: bool
    output: Any
    steps_taken: int
    confidence: float  # 0-1
    error: Optional[str] = None

class DelegationAgent:
    def __init__(self, name: str, llm, tools: dict, max_concurrent: int = 3):
        self.name = name
        self.llm = llm
        self.tools = tools
        self.max_concurrent = max_concurrent
        self.active_children = {}

    def delegate(self, sub_agent: 'DelegationAgent', request: DelegationRequest) -> DelegationResult:
        """Delegate a task to a sub-agent and wait for result."""
        if len(self.active_children) >= self.max_concurrent:
            return DelegationResult(False, None, 0, 0.0, "Max concurrent delegations reached")

        task_id = f"{self.name}_delegates_to_{sub_agent.name}_{id(request)}"
        self.active_children[task_id] = request

        try:
            result = sub_agent.execute_with_context(request)
            self.active_children.pop(task_id)
            return result
        except Exception as e:
            self.active_children.pop(task_id)
            return DelegationResult(False, None, 0, 0.0, str(e))

    def execute_with_context(self, request: DelegationRequest) -> DelegationResult:
        """Execute a task with provided context."""
        system_prompt = f"""You are {self.name}. You have been delegated a task.

Context: {request.context}

Task: {request.task}

Constraints:
{chr(10).join(f'- {c}' for c in request.constraints)}

Output format: {request.output_format}

Max steps: {request.max_steps}"""
        return self._execute_internal(system_prompt, request)

    def verify_result(self, result: DelegationResult, constraints: list[str]) -> bool:
        """Verify sub-agent result meets constraints."""
        if not result.success:
            return False
        verification_prompt = f"""Verify this result meets ALL constraints:
Result: {result.output}
Constraints: {constraints}
Respond: PASS or FAIL (explain why if FAIL)"""
        verdict = self.llm.invoke(verification_prompt)
        return verdict.startswith("PASS")
```

## Hierarchical Delegation

```python
class HierarchicalDelegator:
    """Manages a tree of agent delegations."""
    def __init__(self, root_agent: 'DelegationAgent', llm):
        self.root = root_agent
        self.llm = llm

    def decompose_and_delegate(self, complex_task: str, agent_pool: dict) -> dict:
        """Break task into subtasks and delegate each to appropriate agents."""
        # 1. Decompose
        subtasks = self.llm.invoke(
            f"Decompose this task into independent subtasks:\n{complex_task}"
        )

        # 2. Match subtasks to agents
        results = {}
        for subtask in subtasks.split("\n"):
            subtask = subtask.strip()
            if not subtask: continue

            # Find best agent
            best_agent = max(
                agent_pool.values(),
                key=lambda a: self._match_score(subtask, a.name)
            )

            # Delegate
            request = DelegationRequest(
                task=subtask,
                context=f"Part of larger task: {complex_task}",
                constraints=[],
                output_format="text",
            )
            result = self.root.delegate(best_agent, request)
            results[subtask] = result

        return results

    def _match_score(self, task: str, agent_name: str) -> int:
        task_words = set(task.lower().split())
        agent_words = set(agent_name.lower().replace('-', ' ').split())
        return len(task_words & agent_words)
```

## Pitfalls

- Sub-agent context must include ALL necessary info — can't ask parent questions
- Deadlock: agent A waits for B, B waits for A — set timeouts
- Result verification is critical — sub-agents can hallucinate
- Delegation overhead (context transfer) eats token budget
- Recursive delegation (agent delegates to agent that delegates back) needs depth limits
