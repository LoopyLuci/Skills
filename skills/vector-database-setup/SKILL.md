---
name: vector-database-setup
description: "Set up Chroma Qdrant pgvector for semantic search"
---

# Vector Database Setup

## Chroma (Local)
```python
import chromadb
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.create_or_get_collection("my_docs")
```

## Qdrant (Docker)
```yaml
services:
  qdrant:
    image: qdrant/qdrant
    ports: ["6333:6333"]
    volumes: ["./qdrant_data:/qdrant/storage"]
```

## pgvector (PostgreSQL)
```sql
CREATE EXTENSION vector;
CREATE TABLE docs (id SERIAL, content TEXT, embedding VECTOR(384));
CREATE INDEX ON docs USING ivfflat (embedding vector_cosine_ops);
```
