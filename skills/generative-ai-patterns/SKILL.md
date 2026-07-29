---
name: generative-ai-patterns
description: "Use when implementing generative AI applications."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [generative-ai, LLM, diffusion, RAG, agent-patterns, GenAI, vector-databases]
    related_skills: [rag-system-design, large-language-model-optimization, advanced-reasoning-patterns, few-shot-prompting-advanced]
---

# Generative AI Patterns

Implementing generative AI applications — from LLM-based patterns (RAG, agents, chains) through diffusion models, structured generation, and evaluation frameworks.

## When to Use

- Building LLM-powered applications
- Implementing RAG (Retrieval-Augmented Generation)
- Building AI agents with tools and memory
- Generating images, code, or structured data
- Evaluating and monitoring GenAI outputs

## GenAI Application Patterns

```python
GENAI_PATTERNS = {
    'rag': 'Retrieval-Augmented Generation — ground LLM in external knowledge',
    'agent': 'Tool-using LLM that plans, acts, and observes',
    'chain': 'Composed LLM calls — sequential or parallel with intermediate outputs',
    'structured': 'LLM outputs structured data (JSON, schema) from natural language',
    'multi_modal': 'Generate or understand across text, image, audio, video',
    'evaluation': 'LLM-as-judge, assertion-based, or human evaluation',
}

class GenAIApplication:
    """Pattern-based generative AI application builder."""
    
    def rag_chain(self, vector_store, llm, query: str) -> str:
        docs = vector_store.similarity_search(query, k=3)
        context = '\n'.join(d.page_content for d in docs)
        prompt = f"Answer using context:\n{context}\n\nQuestion: {query}"
        return llm.invoke(prompt)
    
    def structured_output(self, llm, text: str, schema: Dict) -> Dict:
        prompt = f"Extract {schema} from: {text}. Return as valid JSON."
        result = llm.invoke(prompt)
        return json.loads(result)
```

## Verification Checklist

- [ ] Application pattern chosen (RAG, agent, chain, structured, multi-modal)
- [ ] LLM provider and model selected
- [ ] Vector store configured (if RAG)
- [ ] Prompt engineering optimized for the pattern
- [ ] Evaluation framework in place (LLM-as-judge, assertions)
- [ ] Cost and latency measured per inference
- [ ] Guardrails for safety, accuracy, and bias
