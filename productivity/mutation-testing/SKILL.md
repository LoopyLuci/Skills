---
name: mutation-testing
description: "Run mutmut to measure test effectiveness by mutating code"
---

# Mutation Testing

## Install
```bash
pip install mutmut
```

## Run
```bash
mutmut run --paths-to-mutate src/
mutmut results
```

## Interpreting Results
- Killed: test caught the mutation (good)
- Survived: test missed it (bad)
- Timeout: mutation caused infinite loop

## Aim For
- >80% mutation score
- Focus on survived mutants first
- Add tests for untested branches
