---
name: agent-tool-creation
description: "Use when designing and building tools for AI agents."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [tool-creation, agent-tools, function-calling, tool-schema, agent-integration]
    related_skills: [tool-augmented-agents, agent-framework-design, mcp-server-development, tool-augmented-models-training]
---

# Agent Tool Creation

Designing and building tools for AI agents to use — from tool schema definition and parameter design through documentation, error handling, and security.

## When to Use

- Creating custom tools for LLM agents
- Building MCP servers for agent integration
- Designing tool interfaces that agents can discover and use
- Implementing secure, robust tool execution
- Testing tools with various agent frameworks

## Tool Design Pattern

```python
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class Tool:
    """A single tool that an agent can call."""
    def __init__(self, name: str, description: str, 
                 parameters: Dict, handler: callable):
        self.name = name
        self.description = description
        self.parameters = parameters  # JSON schema
        self.handler = handler
    
    def to_openai_schema(self) -> Dict:
        """Convert to OpenAI function calling format."""
        return {
            'type': 'function',
            'function': {
                'name': self.name,
                'description': self.description[:1024],
                'parameters': self.parameters,
            }
        }

class SearchTool(Tool):
    """Example: web search tool for agents."""
    def __init__(self):
        super().__init__(
            name='web_search',
            description='Search the web for current information.',
            parameters={
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': 'The search query'
                    },
                    'limit': {
                        'type': 'integer',
                        'description': 'Max results (1-10)',
                        'default': 5,
                    },
                },
                'required': ['query'],
            },
            handler=self.search,
        )
    
    def search(self, query: str, limit: int = 5) -> str:
        # Actual search implementation
        return f"Results for '{query}'..."
```

## Common Pitfalls

1. **Poor descriptions** — agent doesn't understand when to use the tool; write clear descriptions
2. **Too many parameters** — 10+ parameters confuse agents; keep it simple (3-5 max)
3. **No error handling** — tool crashes without useful error message; return structured errors
4. **No idempotency** — tool run twice produces different results; document side effects
5. **Security holes** — agent can access unintended data via tool; validate permissions per tool

## Verification Checklist

- [ ] Tool name is clear and unique
- [ ] Description tells agent WHEN to use the tool
- [ ] Parameters minimal (3-5 max), with descriptions and defaults
- [ ] Error handling returns structured error (not exception)
- [ ] Side effects documented in parameter descriptions
- [ ] Idempotency for read operations
- [ ] Tool tested with multiple agent frameworks
- [ ] Rate limiting and quota per tool
- [ ] Tool registered with agent's tool registry
