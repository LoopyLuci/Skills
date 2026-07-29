---
name: tool-augmented-agents
description: "Use when building tools for LLM agents to use."
category: mlops
tags: [agents, tools, tool-use, function-calling, llm]
---
# Tool-Augmented Agents

Building and integrating tools for LLM agents to use.

## Tool Contract

Every tool needs:
1. **Name** — unique, descriptive
2. **Description** — when to use, what it does
3. **Parameters** — JSON Schema definition
4. **Implementation** — callable function
5. **Error handling** — graceful failure

## Defining Tools (Python)

```python
from typing import Any, Callable, Optional
import subprocess
import json

class AgentTool:
    def __init__(self, name: str, description: str, parameters: dict,
                 function: Callable, error_message: str = "Tool execution failed"):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.function = function
        self.error_message = error_message

    def execute(self, **kwargs) -> str:
        try:
            result = self.function(**kwargs)
            return str(result) if result is not None else "Done (no output)"
        except Exception as e:
            return f"{self.error_message}: {e}"

    def to_openai_format(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }
```

## Tool Examples

```python
# Filesystem tools
tools = {
    "read_file": AgentTool(
        name="read_file",
        description="Read the contents of a file. Returns the full text.",
        parameters={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Absolute path to the file"}
            },
            "required": ["path"]
        },
        function=lambda path: open(path, 'r').read(),
    ),

    "write_file": AgentTool(
        name="write_file",
        description="Write content to a file. Overwrites if exists.",
        parameters={
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"]
        },
        function=lambda path, content: (open(path, 'w').write(content), "Written")[1],
    ),

    "run_command": AgentTool(
        name="run_command",
        description="Run a shell command and get output.",
        parameters={
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Shell command to execute"},
                "timeout": {"type": "integer", "default": 30}
            },
            "required": ["command"]
        },
        function=lambda command, timeout=30: subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=timeout
        ).stdout,
        error_message="Command execution failed"
    ),
}
```

## Tool Selection Strategies

```python
# Strategy 1: LLM decides (function calling)
response = client.chat.completions.create(
    model="gpt-4",
    messages=...,
    tools=[tool.to_openai_format() for tool in tools.values()],
    tool_choice="auto",           # LLM chooses
)

# Strategy 2: Force specific tool
response = client.chat.completions.create(
    ...,
    tool_choice={"type": "function", "function": {"name": "read_file"}},
)

# Strategy 3: Rule-based routing
def route_to_tool(query: str) -> str:
    if query.startswith("read "): return "read_file"
    if any(cmd in query for cmd in ["run ", "execute ", "bash"]):
        return "run_command"
    return "llm_direct"
```

## Tool Safety

```python
class SafeToolExecutor:
    def __init__(self):
        self.allowed_commands = ["docker ps", "docker images", "docker version"]
        self.blocked_patterns = ["rm -rf", "> /dev/sda", "dd if="]

    def execute_command(self, command: str) -> str:
        # Whitelist check
        if not any(command.startswith(cmd) for cmd in self.allowed_commands):
            return f"Command not allowed. Allowed: {self.allowed_commands}"

        # Blacklist check
        for pattern in self.blocked_patterns:
            if pattern in command:
                return f"Command rejected: contains blocked pattern '{pattern}'"

        return run_shell(command)
```

## Pitfalls

- Tool descriptions must be precise—vague = wrong tool selection
- Large tool lists confuse LLMs — group related tools
- Async tools need special handling (await in tool execution)
- Secret parameters (API keys) should not be exposed to LLM
- Tool timeouts prevent hanging — always set reasonable timeouts
