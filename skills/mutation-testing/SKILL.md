---
name: mutation-testing
description: Run mutmut to measure test effectiveness by mutating code
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [mutation, testing]
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

## Trigger

Activate this skill when the user mentions:
- mutation, testing workflows or issues
- Building, fixing, or optimizing mutation testing


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
