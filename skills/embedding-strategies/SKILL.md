---
name: embedding-strategies
description: "Choose chunking overlap model selection for embeddings"
---

# Embedding Strategies

## Chunking
| Strategy | Chunk Size | Overlap | Use Case |
|----------|-----------|---------|----------|
| Fixed | 512 tokens | 50 | General |
| Sentence | By sentence | 1 sent | Q&A |
| Paragraph | By paragraph | 0 | Documents |
| Recursive | 1000 tokens | 200 | Code |

## Models
| Model | Dimensions | When to Use |
|-------|-----------|-------------|
| all-MiniLM-L6-v2 | 384 | Fast, general |
| text-embedding-3-small | 512 | OpenAI quality |
| BGE-base-en-v1.5 | 768 | Reranking |
