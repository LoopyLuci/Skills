---
name: agent-memory-systems
description: "Use when implementing memory for AI agents."
category: mlops
tags: [agents, memory, context, retrieval, vector-db]
---
# Agent Memory Systems

Implementing memory architectures for AI agents.

## Memory Types

| Type | Duration | Scope | Storage |
|------|----------|-------|---------|
| Working | One turn | Current context | Prompt window |
| Short-term | Conversation | Current session | Message list |
| Long-term | Persistent | Cross-session | Vector DB |
| Episodic | Persistent | Specific events | Time-series DB |
| Procedural | Permanent | Skills/knowledge | File system |

## Short-Term Memory (Conversation)

```python
class ConversationMemory:
    def __init__(self, max_tokens: int = 4000):
        self.messages = []
        self.max_tokens = max_tokens

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._trim()

    def _trim(self):
        total = sum(len(m["content"]) for m in self.messages)
        while total > self.max_tokens and len(self.messages) > 1:
            removed = self.messages.pop(0)
            total -= len(removed["content"])

    def get_context(self) -> list:
        return self.messages

    def summarize(self, llm) -> str:
        """Summarize old messages when context fills up."""
        old = self.messages[:-10]  # keep last 10
        if not old: return ""
        summary = llm.invoke(f"Summarize this conversation:\n{old}")
        self.messages = [{"role": "system", "content": f"Summary: {summary}"}] + self.messages[-10:]
        return summary
```

## Long-Term Memory (Vector DB)

```python
import chromadb
from chromadb.utils import embedding_functions

class LongTermMemory:
    def __init__(self, collection_name: str = "agent_memory"):
        self.client = chromadb.PersistentClient(path="./agent_memory")
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_functions.DefaultEmbeddingFunction(),
        )

    def remember(self, key: str, content: str, metadata: dict = None):
        """Store an episodic memory."""
        self.collection.add(
            documents=[content],
            metadatas=[metadata or {"key": key}],
            ids=[key],
        )

    def recall(self, query: str, n: int = 5) -> list[dict]:
        """Retrieve relevant memories."""
        results = self.collection.query(query_texts=[query], n_results=n)
        return [
            {"content": doc, "metadata": meta}
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])
        ]

    def forget(self, key: str):
        self.collection.delete(ids=[key])
```

## Episodic Memory

```python
import json
from datetime import datetime

class EpisodicMemory:
    def __init__(self, memory_file: str = "episodes.json"):
        self.memory_file = memory_file
        self.episodes = self._load()

    def record(self, event: str, result: str, success: bool):
        episode = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "result": result,
            "success": success,
        }
        self.episodes.append(episode)
        self._save()

    def recall_similar(self, event: str, n: int = 3) -> list:
        """Find past episodes with similar events."""
        query_words = set(event.lower().split())
        scored = []
        for ep in self.episodes:
            ep_words = set(ep["event"].lower().split())
            overlap = len(query_words & ep_words)
            if overlap > 0:
                scored.append((overlap, ep))
        scored.sort(key=lambda x: -x[0])
        return [ep for _, ep in scored[:n]]

    def success_rate(self, event_type: str) -> float:
        relevant = [ep for ep in self.episodes if event_type in ep["event"]]
        if not relevant: return 0.0
        return sum(1 for ep in relevant if ep["success"]) / len(relevant)
```

## Hybrid Memory Agent

```python
class MemoryAgent:
    def __init__(self, llm, long_term_memory: LongTermMemory):
        self.llm = llm
        self.conversation = ConversationMemory()
        self.ltm = long_term_memory
        self.episodic = EpisodicMemory()

    def run(self, task: str) -> str:
        # 1. Retrieve relevant long-term memories
        relevant = self.ltm.recall(task)

        # 2. Build enriched context
        context = "Relevant past knowledge:\n"
        for item in relevant:
            context += f"- {item['content']}\n"

        # 3. Add to conversation
        self.conversation.add("user", f"{context}\n\nTask: {task}")

        # 4. Generate response
        response = self.llm.invoke(self.conversation.get_context())
        self.conversation.add("assistant", response)

        return response
```

## Pitfalls

- Vector recall quality depends on embedding model — test on your domain
- Memory summarization loses detail — balance compression vs retention
- Episodic memory files grow over time — implement archiving
- Cross-session memory needs user identification for multi-user systems
- Working memory (context window) is the most expensive — optimize usage
