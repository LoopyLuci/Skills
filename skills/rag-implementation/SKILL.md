---
name: rag-implementation
description: "Build retrieval augmented generation with embeddings and vector DB"
---

# RAG Implementation

## Pipeline
1. Chunk documents
2. Generate embeddings
3. Store in vector DB
4. Query: embed question + search + context + LLM

## Minimal RAG
```python
from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.create_collection("docs")

# Index
collection.add(documents=["doc1 text", "doc2 text"], ids=["1", "2"])

# Query
results = collection.query(query_texts=["user question"], n_results=3)
context = "
".join(results["documents"][0])
prompt = f"Context: {context}
Question: ..."
```
