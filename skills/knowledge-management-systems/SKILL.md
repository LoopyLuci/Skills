---
name: knowledge-management-systems
description: "Use when designing knowledge bases for AI systems."
category: mlops
tags: [knowledge-management, knowledge-base, wiki, documentation]
---
# Knowledge Management Systems

Designing knowledge bases for AI systems and human teams.

## Knowledge Types

| Type | Examples | Storage | Update Frequency |
|------|----------|---------|-----------------|
| Explicit | Docs, APIs, configs | Files, Wiki | Manual |
| Implicit | Patterns, best practices | Skills, Code | After iteration |
| Tacit | Expertise, intuition | Person | Not captured |
| Episodic | Past incidents | Logs, DB | Continuous |
| Structural | Org charts, workflows | Graph DB | Periodic |

## Knowledge Base Architecture

```
User Query
    │
    ▼
[Query Router] ──→ Simple Q: FAQ match
    │
    ├──→ Technical: Vector DB (docs + code)
    │
    ├──→ Complex: RAG pipeline (retrieve + synthesize)
    │
    └──→ Unknown: Escalate to expert
```

## Building a Knowledge Base

```python
from pathlib import Path
import yaml
from typing import List, Dict, Optional

class KnowledgeEntry:
    def __init__(self, title: str, content: str, tags: List[str],
                 domain: str, source: str, version: str = "1.0"):
        self.title = title
        self.content = content
        self.tags = tags
        self.domain = domain
        self.source = source
        self.version = version

class KnowledgeBase:
    def __init__(self, base_path: str = "./knowledge"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def add_entry(self, entry: KnowledgeEntry):
        """Add a knowledge entry from a skill or document."""
        path = self.base_path / entry.domain / f"{entry.title.lower().replace(' ', '_')}.md"
        path.parent.mkdir(parents=True, exist_ok=True)

        content = f"""---
title: {entry.title}
tags: [{', '.join(entry.tags)}]
domain: {entry.domain}
source: {entry.source}
version: {entry.version}
---

{entry.content}
"""
        path.write_text(content)

    def search(self, query: str, domain: str = None, tags: List[str] = None) -> List[Path]:
        """Simple keyword search (for vector search, use RAG pipeline)."""
        results = []
        search_dir = self.base_path / domain if domain else self.base_path

        for path in search_dir.rglob("*.md"):
            content = path.read_text()
            if query.lower() in content.lower():
                if tags and not all(tag in content for tag in tags):
                    continue
                results.append(path)

        return results
```

## Knowledge from Skills

Skills ARE knowledge entries — they capture procedural knowledge. Convert skills to knowledge base entries:

```python
def skill_to_knowledge(skill_name: str, skill_content: str) -> KnowledgeEntry:
    """Convert a Hermes skill to a KnowledgeBase entry."""
    frontmatter = {}
    content = skill_content

    if skill_content.startswith("---"):
        parts = skill_content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            content = parts[2]

    return KnowledgeEntry(
        title=frontmatter.get("name", skill_name),
        content=content,
        tags=frontmatter.get("tags", []),
        domain=frontmatter.get("category", "general"),
        source="hermes-skill",
        version="1.0",
    )
```

## Knowledge Lifecycle

```
Discovery → Capture → Organize → Store → Retrieve → Update → Archive
```

## Pitfalls

- Knowledge decays — documents about v1 tools are dangerous for v2
- Categorization drift — tags that made sense 6 months ago may not now
- Single source of truth — don't duplicate knowledge across systems
- Discovery is the hardest part — most knowledge is never captured
- Query understanding determines retrieval quality — invest in query parsing
