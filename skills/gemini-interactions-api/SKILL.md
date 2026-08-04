---
name: gemini-interactions-api
description: Use when running multi-turn conversations with the Gemini Interactions API on Agent Platform.
tags: [gemini, interactions, api, conversations, streaming, function-calling]
related_skills: [gemini-api, gemini-agents-api, google-cloud-recipe-auth]
---

# Gemini Interactions API

The modern way to execute Generative AI agent conversations, background research tasks, multi-turn chats, and structured workflows on Gemini Enterprise Agent Platform.

## Client Initialization

```bash
export GOOGLE_GENAI_USE_ENTERPRISE=true
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="global"
```

```python
from google import genai
client = genai.Client()
```

## Code Example: Single-Turn

```python
interaction = client.interactions.create(
    agent="your-agent-id",
    input="Explain serverless computing in one sentence."
)
print(interaction.output_text)
```

## Code Example: Multi-Turn Stateful Conversation

```python
# Turn 1
turn1 = client.interactions.create(
    agent="your-agent-id",
    input="Hi! My name is John.",
    store=True
)
print(f"Turn 1: {turn1.output_text}")

# Turn 2 (references previous interaction)
turn2 = client.interactions.create(
    agent="your-agent-id",
    input="What is my name?",
    previous_interaction_id=turn1.id
)
print(f"Turn 2: {turn2.output_text}")
```

## Code Example: Streaming

```python
for event in client.interactions.create(
    agent="your-agent-id",
    input="Write a poem about debugging.",
    stream=True
):
    if event.event_type == "step.delta" and event.delta.type == "text":
        print(event.delta.text, end="", flush=True)
```

## Code Example: Structured Output

```python
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    year_published: int

interaction = client.interactions.create(
    agent="your-agent-id",
    input="Recommend a sci-fi book.",
    response_format=Book
)
print(interaction.output_text)
```

## Common Pitfalls

- **GEAP requires provisioned agent**: Use `agent="..."` not `model="..."` on Agent Platform
- **Legacy SDKs unsupported**: `google-cloud-aiplatform` and `google-generativeai` are not compatible
- **Turn-scoped parameters**: Tools, system_instruction, and generation_config must be passed with each request
- **SDK version**: Use `google-genai >= 2.3.0` for Interactions API support

## Verification Checklist

- [ ] Client initializes without errors
- [ ] Single-turn interaction returns response
- [ ] Multi-turn conversation maintains state
- [ ] Streaming yields typed events
- [ ] Structured output returns valid JSON
