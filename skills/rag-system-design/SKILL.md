---
name: rag-system-design
description: "Use when building retrieval-augmented generation systems."
category: mlops
tags: [rag, retrieval, llm, embeddings, vector-db]
---
# RAG System Design

Designing retrieval-augmented generation systems for LLMs.

## Architecture

```
User Query
    │
    ▼
[ Embedding Model ] → query vector
    │
    ▼
[ Vector Database ] → relevant chunks (ANN search)
    │
    ▼
[ Context Assembly ] → system prompt + retrieved chunks + user query
    │
    ▼
[ LLM ] → generated answer
```

## Indexing Pipeline

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Load documents
from langchain_community.document_loaders import DirectoryLoader
loader = DirectoryLoader("./docs", glob="**/*.md")
documents = loader.load()

# 2. Chunk documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " "],
)
chunks = text_splitter.split_documents(documents)

# 3. Embed and store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
```

## Retrieval

```python
# 1. Semantic search
query = "How do I remove Docker from Windows?"
results = vectorstore.similarity_search_with_score(query, k=5)

# 2. Hybrid (dense + sparse)
from langchain.retrievers import BM25Retriever, EnsembleRetriever
bm25_retriever = BM25Retriever.from_documents(chunks)
semantic_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
ensemble = EnsembleRetriever(retrievers=[bm25_retriever, semantic_retriever], weights=[0.3, 0.7])
results = ensemble.get_relevant_documents(query)

# 3. MMR (maximum marginal relevance) for diversity
results = vectorstore.max_marginal_relevance_search(query, k=5, fetch_k=20)
```

## Context Assembly

```python
def build_prompt(query: str, chunks: list) -> str:
    context = "\n\n".join([
        f"Source [{i+1}]: {chunk.page_content}"
        for i, chunk in enumerate(chunks)
    ])
    return f"""Use the following context to answer the question.
If the context doesn't contain the answer, say "I don't have enough information."

Context:
{context}

Question: {query}

Answer:"""
```

## Full RAG Pipeline

```python
class RAGPipeline:
    def __init__(self, vectorstore_path: str, llm):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Chroma(persist_directory=vectorstore_path, embedding_function=self.embeddings)
        self.llm = llm

    def query(self, user_query: str, k: int = 5) -> str:
        chunks = self.vectorstore.similarity_search(user_query, k=k)
        prompt = build_prompt(user_query, chunks)
        return self.llm.invoke(prompt)

    def query_with_sources(self, user_query: str) -> dict:
        chunks = self.vectorstore.similarity_search(user_query, k=5)
        prompt = build_prompt(user_query, chunks)
        answer = self.llm.invoke(prompt)
        return {"answer": answer, "sources": [c.metadata for c in chunks]}
```

## Pitfalls

- Chunk size affects retrieval quality — too small misses context, too large includes noise
- Overlap prevents cutting sentences mid-way
- Embedding model must match the domain (code docs → code embedding)
- Metadata filtering (date, source) improves relevance
- Re-ranking (cross-encoder) after initial retrieval boosts accuracy significantly
