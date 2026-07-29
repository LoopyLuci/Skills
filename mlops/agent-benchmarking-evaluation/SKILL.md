---
name: agent-benchmarking-evaluation
description: "Use when benchmarking and evaluating AI agent performance."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agent-evaluation, benchmarking, metrics, success-rate, cost, latency]
    related_skills: [agent-evaluation-metrics, agent-framework-design, model-evaluation-metrics, research-workflow]
---

# Agent Benchmarking and Evaluation

Systematically evaluating AI agent performance — from task completion metrics through cost analysis, latency measurement, and benchmarking against baselines.

## When to Use

- Comparing different agent architectures or models
- Measuring if an agent improvement actually helps
- Evaluating agent performance before production deployment
- Tracking agent performance regression over time
- Publishing agent benchmark results

## Evaluation Framework

```python
AGENT_EVAL_FRAMEWORK = {
    'task_success': '% of tasks completed successfully',
    'cost_per_task': 'Average cost (tokens + API calls) per task',
    'latency_p50_p95': 'Median and P95 completion time',
    'error_rate': 'Rate of errors, hallucinations, or unsafe outputs',
    'tool_accuracy': 'Correct tool selection and parameter usage rate',
}

class AgentBenchmark:
    """Benchmark agent performance across tasks."""
    
    def __init__(self, test_suite: List[Dict]):
        self.tests = test_suite  # [{task, expected, tools_allowed}, ...]
    
    def evaluate(self, agent) -> Dict:
        results = {'success': [], 'latency': [], 'cost': [], 'errors': []}
        
        for test in self.tests:
            start = time.time()
            try:
                response = agent.run(test['task'])
                latency = time.time() - start
                
                success = self._check_success(response, test['expected'])
                results['success'].append(success)
                results['latency'].append(latency)
                results['cost'].append(agent.get_last_run_cost())
            except Exception as e:
                results['errors'].append(str(e))
                results['success'].append(False)
        
        return {
            'success_rate': round(sum(results['success']) / len(self.tests) * 100, 1),
            'avg_latency': round(np.mean(results['latency']), 2),
            'p95_latency': round(np.percentile(results['latency'], 95), 2),
            'avg_cost': round(np.mean(results['cost']), 4),
            'error_rate': round(len(results['errors']) / len(self.tests) * 100, 1),
        }
```

## Common Pitfalls

1. **Task leakage** — evaluation tasks seen during development overstate performance
2. **Cost not tracked** — an agent that works but costs $100/task isn't useful
3. **Only success rate** — latency and cost matter just as much; track all three
4. **No baseline** — agent evaluation without a baseline (random, simple prompt) is meaningless
5. **Overspecified tasks** — tests too close to training data don't measure true capability

## Verification Checklist

- [ ] Test suite represents real-world tasks (not toy examples)
- [ ] Baseline established (human performance or simple prompt)
- [ ] Metrics cover success, latency, cost, and safety
- [ ] Multiple runs per task to account for nondeterminism
- [ ] Test set versioned and not used in development
- [ ] Results reported with confidence intervals
