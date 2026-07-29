---
name: continuous-integration-advanced
description: "Use when implementing advanced CI/CD pipelines."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [CI-CD, continuous-integration, GitHub-Actions, pipelines, automation, testing]
    related_skills: [ci-cd-pipeline-setup, mlops-pipeline-ci-cd, testing-pyramid-practice, performance-budgeting-web]
---

# Advanced CI/CD Pipelines

Implementing advanced CI/CD pipelines — from build caching and parallel jobs through matrix testing, deployment strategies, and pipeline optimization.

## When to Use

- Optimizing CI/CD pipeline speed and reliability
- Implementing parallel job execution and build caching
- Matrix testing across platforms and versions
- Blue/green or canary deployment strategies
- Building self-service CI/CD for multiple teams

## CI/CD Optimization

```python
CI_OPTIMIZATIONS = {
    'caching': 'Cache node_modules, pip, docker layers, Gradle/Maven — restore in seconds',
    'parallelism': 'Split tests across N parallel runners (matrix strategy)',
    'selective_execution': 'Run only affected tests (Nx/Turborepo), skip unchanged code paths',
    'pre_built_images': 'Use pre-built docker images with common deps, not installing from scratch',
}

CI_MATRIX_CONFIG = """
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node: [18, 20, 22]
    include:
      - os: ubuntu-latest
        node: 20
        coverage: true
"""

def estimate_pipeline_speed(tests: int, parallel_runners: int = 4, 
                            cache_hit: bool = True) -> Dict:
    setup_time = 60 if not cache_hit else 15  # seconds
    test_time_per_runner = (tests * 2) / parallel_runners  # 2 seconds per test
    total = setup_time + test_time_per_runner
    return {'setup_seconds': setup_time, 'test_seconds': round(test_time_per_runner), 'total_seconds': round(total)}
```

## Verification Checklist

- [ ] Build caching configured (package manager + docker layer)
- [ ] Parallel job execution across runners
- [ ] Matrix testing across required platforms/versions
- [ ] Selective execution (only changed modules tested)
- [ ] Pipeline completes under 10 minutes
- [ ] Deployment strategy (blue/green or canary) implemented
- [ ] Failure notifications and rollback automation
