---
name: llm-evaluation
description: "Evaluate LLM outputs accuracy relevance and hallucination"
---

# LLM Evaluation

## Automated Checks
```python
# Relevance
def check_relevance(answer, context):
    return len([w for w in context.split() if w in answer]) / len(context.split())

# Hallucination: does answer contradict context?
def check_hallucination(answer, context):
    # Use NLI model or LLM judge
    pass
```

## Metrics
| Metric | What It Measures |
|--------|-----------------|
| BLEU | N-gram overlap |
| ROUGE | Recall of key phrases |
| BERTScore | Semantic similarity |
| LLM-as-judge | Overall quality |

## Evaluation Dataset
Split into correct/incorrect examples, score accuracy.
