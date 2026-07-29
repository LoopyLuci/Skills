---
name: agent-framework-design
description: "Use when building custom AI agent frameworks."
category: mlops
tags: [agents, framework, design, ai, llm, tool-use]
---
# Agent Framework Design

Designing and building custom AI agent frameworks.

## Core Agent Loop

```python
class Agent:
    def __init__(self, llm, tools: dict):
        self.llm = llm
        self.tools = tools          # name → callable
        self.messages = []
        self.max_steps = 10

    def run(self, task: str) -> str:
        self.messages.append({"role": "user", "content": task})

        for step in range(self.max_steps):
            response = self.llm.invoke(self.messages)

            if response.get("type") == "final":
                return response["content"]

            tool_name = response["tool"]
            tool_args = response["args"]
            result = self.tools[tool_name](**tool_args)

            self.messages.append({
                "role": "tool",
                "tool": tool_name,
                "content": str(result)
            })

        return "Max steps reached"
```

## Tool Definition

```python
from pydantic import BaseModel
from typing import Any, Callable

class Tool(BaseModel):
    name: str
    description: str
    parameters: dict          # JSON Schema
    function: Callable
    requires_admin: bool = False

    def to_llm_format(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }

# Example tools
tools = {
    "read_file": Tool(
        name="read_file",
        description="Read a file from disk",
        parameters={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to file"}
            },
            "required": ["path"]
        },
        function=lambda path: open(path).read(),
    ),
    "run_command": Tool(
        name="run_command",
        description="Execute a shell command",
        parameters={
            "type": "object",
            "properties": {
                "command": {"type": "string"},
                "timeout": {"type": "integer", "default": 30}
            },
            "required": ["command"]
        },
        function=lambda command, timeout=30: ...,
        requires_admin=True,
    ),
}
```

## System Prompt Template

```python
SYSTEM_PROMPT = """You are an AI assistant with access to the following tools:
{tool_descriptions}

You must decide which tool to use or provide a final answer.
For tool calls, respond with:
  TOOL: tool_name
  ARGS: {{"arg1": "value1"}}

For final answers, respond with:
  FINAL: your answer here

Rules:
1. Only use tools that exist in the list above
2. Pass all required parameters
3. If a tool fails, try an alternative approach
4. Be concise in observations
5. Max {max_steps} steps"""
```

## Agent with Planning

```python
class PlanningAgent(Agent):
    def run(self, task: str) -> str:
        # Step 1: Create plan
        plan_prompt = f"Create a step-by-step plan to: {task}"
        plan = self.llm.invoke(plan_prompt)

        # Step 2: Execute each step
        for step in plan.split("\n"):
            if step.strip():
                result = super().run(step.strip())

        # Step 3: Summarize
        summary = self.llm.invoke(f"Summarize the results: {result}")
        return summary
```

## Pitfalls

- Tool descriptions must be precise — vague descriptions cause wrong tool selection
- Max steps prevents infinite loops but may truncate complex tasks
- Error handling per tool prevents one failure from crashing the agent
- Rate limiting: agents can hit API limits quickly — add delays
- Context window fills with tool results — summarize intermediate steps
