---
name: prompt-optimization-automation
description: "Use when optimizing and automating prompt engineering."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [prompt-engineering, optimization, dspy, auto-prompt, LLM, evaluation]
    related_skills: [prompt-engineering-patterns, advanced-reasoning-patterns, agent-framework-design, llm-fine-tuning-lora]
---

# Prompt Optimization and Automation

Optimizing prompts systematically — from manual iteration through DSPy-style programmable prompts, automated optimization, and prompt evaluation.

## When to Use

- Improving LLM response quality and consistency
- Automating prompt testing and iteration
- Building prompt pipelines with DSPy or similar
- Evaluating prompts across metrics (accuracy, safety, cost)
- Scaling prompt management across many use cases

## Optimization Methods

```python
OPTIMIZATION_STRATEGIES = {
    'manual_iteration': 'Human A/B tests prompt variants, measures output quality',
    'dspy_optimization': 'Programmatic: define signature, modules, teleprompter optimizes',
    'meta_prompting': 'LLM generates and evaluates its own prompt improvements',
    'few_shot_selection': 'Dynamically selects best examples for few-shot prompts',
    'prompt_chaining': 'Decompose complex tasks into optimized sub-prompts',
}

class PromptOptimizer:
    """Simple A/B prompt testing framework."""
    
    def __init__(self, llm_callable):
        self.llm = llm_callable
        self.results = {}
    
    def test_variant(self, prompt: str, test_cases: List[Dict], 
                     evaluator: Callable) -> float:
        """Test a prompt variant against test cases and return avg score."""
        scores = []
        for case in test_cases:
            response = self.llm(prompt.format(**case))
            score = evaluator(case['expected'], response)
            scores.append(score)
        return sum(scores) / len(scores)
    
    def optimize(self, base_prompt: str, variants: List[str], 
                 test_cases: List[Dict], evaluator: Callable) -> str:
        """Find best prompt variant."""
        best_score = 0
        best_prompt = base_prompt
        for v in [base_prompt] + variants:
            score = self.test_variant(v, test_cases, evaluator)
            if score > best_score:
                best_score, best_prompt = score, v
        return best_prompt
```

## Common Pitfalls

1. **Overfitting to test set** — prompt optimized for 10 cases may fail on real data; use held-out eval
2. **LLM variance** — same prompt produces different outputs; test with multiple runs
3. **Cost of evaluation** — automated optimization can be expensive; budget wisely
4. **Ignoring prompt length** — longer prompts cost more and may exceed context; optimize for brevity
5. **No structured output** — unstructured llm responses are hard to evaluate consistently

## Verification Checklist

- [ ] Baseline prompt established for comparison
- [ ] Evaluation criteria defined (accuracy,format, safety)
- [ ] Test set diverse (edge cases, normal cases)
- [ ] Optimization method chosen (manual, DSPy, meta)
- [ ] Results tracked per prompt version
- [ ] Cost per inference measured
- [ ] Final prompt validated on held-out set
