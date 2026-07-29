---
name: agent-communication-languages
description: "Use when designing agent communication languages."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agent-communication, ACL, FIPA, speech-acts, agent-protocols]
    related_skills: [swarm-communication-protocols, multi-agent-collaboration-patterns, tool-augmented-agents, agent-framework-design]
---

# Agent Communication Languages

Designing agent communication languages and protocols — from FIPA ACL through structured messaging, ontologies, and protocol negotiation.

## When to Use

- Designing how agents communicate in multi-agent systems
- Defining message schemas and interaction protocols
- Implementing agent conversation policies
- Creating agent negotiation protocols

## Communication Framework

```python
class AgentMessage:
    """FIPA ACL-style agent message."""
    def __init__(self, sender: str, receiver: str, performative: str,
                 content: dict, ontology: str = ''):
        self.sender = sender
        self.receiver = receiver
        self.performative = performative
        self.content = content
        self.conversation_id = str(uuid.uuid4())
        self.timestamp = datetime.now().isoformat()

PERFORMATIVES = ['inform', 'query', 'request', 'propose', 'accept', 'reject', 'cfp']
```

## Common Pitfalls

1. **Over-complex schemas** — 50-field messages obscure intent; keep it simple
2. **No ontology** — agents using different terms for the same concept
3. **Synchronous only** — design async by default; don't block on responses
4. **No conversation state** — multi-turn interactions need context tracking

## Verification Checklist

- [ ] Message schema defined (sender, receiver, performative, content)
- [ ] Core performatives defined
- [ ] Conversation IDs for multi-turn interactions
- [ ] Async communication support
- [ ] Ontology documented (shared vocabulary)
- [ ] Timeout handling for unanswered messages
