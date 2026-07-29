---
name: ab-testing-experimentation
description: "Use when designing and analyzing A/B testing experiments."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ab-testing, experimentation, statistics, hypothesis-testing, optimization]
    related_skills: [conversion-rate-optimization, marketing-funnel-design, website-analytics-tracking, digital-marketing-strategy]
---

# A/B Testing and Experimentation

Designing, running, and analyzing A/B tests with statistical rigor — from hypothesis formulation and sample size calculation through test execution and result interpretation.

## When to Use

- Testing changes to landing pages, CTAs, or pricing
- Optimizing email subject lines, content, or send times
- Comparing feature variants or product changes
- Making data-driven decisions with statistical confidence
- Building a culture of experimentation

## Test Design

```python
from typing import Dict, List, Optional
import math
from scipy import stats

class ABTestDesigner:
    """Design statistically rigorous A/B tests."""
    
    @staticmethod
    def calculate_sample_size(baseline_rate: float, min_detectable_effect: float,
                              alpha: float = 0.05, beta: float = 0.20) -> int:
        """Calculate required sample size per variant.
        
        Uses the standard formula for two-proportion z-test.
        baseline_rate: current conversion rate (e.g., 0.05 for 5%)
        min_detectable_effect: minimum lift to detect (e.g., 0.20 for 20%)
        alpha: significance level (default 5%)
        beta: power (default 80%)
        """
        z_alpha = stats.norm.ppf(1 - alpha / 2)
        z_beta = stats.norm.ppf(1 - beta)
        
        effect = min_detectable_effect * baseline_rate
        p = baseline_rate + effect / 2
        q = 1 - p
        
        n = (2 * q * (z_alpha + z_beta) ** 2) / (effect ** 2)
        return math.ceil(n)
    
    @staticmethod
    def estimate_test_duration(sample_size: int, traffic_per_day: int, 
                                variants: int = 2) -> Dict:
        """Estimate how long the test needs to run."""
        days_needed = math.ceil(sample_size * variants / max(traffic_per_day, 1))
        return {
            'sample_size_per_variant': sample_size,
            'total_needed': sample_size * variants,
            'expected_days': days_needed,
            'recommendation': f'Run for at least {days_needed} days ({max(days_needed, 7)} days minimum)',
        }
```

## Test Analyzer

```python
class TestAnalyzer:
    """Analyze A/B test results with statistical methods."""
    
    @staticmethod
    def analyze(results: Dict) -> Dict:
        """Analyze A/B test results.
        
        results = {
            'control': {'visitors': 10000, 'conversions': 500},
            'variant': {'visitors': 10000, 'conversions': 550},
        }
        """
        control = results['control']
        variant = results['variant']
        
        # Calculate metrics
        c_rate = control['conversions'] / control['visitors']
        v_rate = variant['conversions'] / variant['visitors']
        lift = (v_rate - c_rate) / c_rate
        
        # Z-test for proportions
        z_stat, p_value = ABTestAnalyzer._two_proportion_z_test(
            control['conversions'], control['visitors'],
            variant['conversions'], variant['visitors']
        )
        
        # Confidence interval
        ci = ABTestAnalyzer._confidence_interval(c_rate, v_rate, 
                                                  control['visitors'], variant['visitors'])
        
        return {
            'control_rate': round(c_rate * 100, 2),
            'variant_rate': round(v_rate * 100, 2),
            'absolute_lift': round((v_rate - c_rate) * 100, 2),
            'relative_lift': round(lift * 100, 2),
            'p_value': round(p_value, 4),
            'significant': p_value < 0.05,
            'confidence_interval': ci,
            'recommendation': 'Implement variant' if p_value < 0.05 and lift > 0 else (
                'Keep control' if p_value < 0.05 else 'Continue test (not enough data)'
            ),
        }
    
    @staticmethod
    def _two_proportion_z_test(c1, n1, c2, n2):
        p1 = c1 / n1
        p2 = c2 / n2
        p_pool = (c1 + c2) / (n1 + n2)
        se = math.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
        z = (p2 - p1) / se
        p = 2 * (1 - stats.norm.cdf(abs(z)))
        return z, p
    
    @staticmethod
    def _confidence_interval(p1, p2, n1, n2, confidence=0.95):
        import numpy as np
        se = math.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
        z = stats.norm.ppf(1 - (1 - confidence) / 2)
        return {
            'lower': round((p2 - p1 - z * se) * 100, 2),
            'upper': round((p2 - p1 + z * se) * 100, 2),
            'confidence_level': confidence,
        }
```

## Test Plan Template

```python
class TestPlan:
    """Document an A/B test plan."""
    
    @staticmethod
    def create(name: str, hypothesis: str, element: str,
               control_desc: str, variant_desc: str,
               primary_metric: str, secondary_metrics: List[str]) -> Dict:
        return {
            'test_name': name,
            'hypothesis': hypothesis,
            'element_changed': element,
            'control': control_desc,
            'variant': variant_desc,
            'primary_metric': primary_metric,
            'secondary_metrics': secondary_metrics,
            'status': 'draft',
            'sample_size': None,
            'duration_days': None,
            'results': None,
            'learnings': None,
        }
```

## Common Pitfalls

1. **Peeking at results** — checking for significance daily inflates false positives; set duration upfront
2. **Stopping early** — stopping at "significant" often reverses with more data; wait for required sample
3. **Multiple comparisons** — testing 10 metrics, one may be significant by chance; correct for multiplicity
4. **Novelty effect** — new experience gets more attention initially; run minimum 7-14 days
5. **Segment dilution** — overall "no significant effect" may hide big lift in a segment; analyze segments
6. **Not documenting** — can't learn from tests without recording results; document everything

## Verification Checklist

- [ ] Hypothesis clearly stated (we believe X change will cause Y result)
- [ ] Sample size calculated before test starts
- [ ] Test duration estimated (minimum 7 days)
- [ ] Primary metric defined and measurable
- [ ] Statistical significance threshold set (α=0.05)
- [ ] Test runs to completion (no early stopping)
- [ ] Results analyzed with proper statistical test
- [ ] Segments analyzed (device, source, new vs returning)
- [ ] Learnings documented regardless of outcome

## See Also

- conversion-rate-optimization — applying test results
- marketing-funnel-design — testing funnel stages
- website-analytics-tracking — tracking test metrics
- digital-marketing-strategy — experimentation strategy
