---
name: few-shot-prompting-advanced
description: "Use when implementing advanced few-shot prompting."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [few-shot, prompting, in-context-learning, example-selection, dynamic-prompting]
    related_skills: [prompt-optimization-automation, advanced-reasoning-patterns, llm-fine-tuning-lora, large-language-model-optimization]
---

# Advanced Few-Shot Prompting

Implementing advanced few-shot prompting techniques — from dynamic example selection through chain-of-thought, structured outputs, and multi-turn example management.

## When to Use

- Improving LLM output quality with minimal examples
- Dynamic example selection based on query similarity
- Few-shot chain-of-thought for reasoning tasks
- Managing context window with example compression

## Few-Shot Methods

```python
FEW_SHOT_METHODS = {
    'static': 'Fixed examples in every prompt — simple, but may not match query',
    'dynamic_knn': 'Retrieve examples from database via embedding similarity — best match',
    'auto_generated': 'LLM generates its own examples for the task — no labeled data needed',
    'clustered': 'Select diverse examples covering different task types/classes',
    'compressed': 'Summarize examples to fit more in context — trade detail for quantity',
}

class DynamicFewShot:
    """Dynamic example selection using embedding similarity."""
    def __init__(self, examples: List[Dict], encoder):
        self.examples = examples
        self.encoder = encoder
        self.example_embeddings = encoder.encode([e['query'] for e in examples])
    
    def select_examples(self, query: str, k: int = 3) -> List[Dict]:
        from sklearn.metrics.pairwise import cosine_similarity
        query_emb = self.encoder.encode([query])
        similarities = cosine_similarity(query_emb, self.example_embeddings)[0]
        top_k = similarities.argsort()[-k:][::-1]
        return [self.examples[i] for i in top_k]
```

## Verification Checklist

- [ ] Few-shot method chosen (static, dynamic, auto-generated)
- [ ] Examples representative of expected queries
- [ ] Dynamic selection performance (embedding similarity latency)
- [ ] Context window budgeted (examples + instructions + query fit in context)
- [ ] Example diversity maintained (not all similar examples)
- [ ] Accuracy compared with zero-shot baseline
