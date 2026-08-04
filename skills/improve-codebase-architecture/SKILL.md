---
name: improve-codebase-architecture
description: Use when improving codebase architecture, reducing coupling, or increasing cohesion
tags: [architecture, refactoring, coupling, cohesion, analysis]
related_skills: [codebase-design, request-refactor-plan, code-review]
---

# Improve Codebase Architecture

Analyze and improve codebase architecture by identifying opportunities for deeper modules, better seams, and reduced coupling.

## Process

### 1. Map the current architecture
- Identify modules (packages, directories, classes)
- Document entry points and dependencies
- Measure module depth (interface vs implementation ratio)

### 2. Identify problems
- Shallow modules (interface nearly as complex as implementation)
- Tight coupling between unrelated concerns
- God modules that do too much
- Missing seams (should be separable but aren't)

### 3. Report with an HTML report
Generate a structured report with the current architecture, identified issues, and specific recommendations. Present both a quick summary inline and a detailed HTML report.

### 4. Prioritize improvements
Rank by impact: which changes give the most leverage for the least risk?

## Common Pitfalls

- **Analyzing without a clear baseline**: Run the analysis tools before making any changes to establish the baseline metrics.
- **Focusing only on structure, not behavior**: Architecture is about both. A structurally clean module that is hard to use or test is not an improvement.
- **Refactoring without tests**: Architecture improvements without test coverage are risky. Ensure the critical paths are tested before restructuring.

## Verification Checklist

- [ ] Baseline architecture metrics gathered
- [ ] Deepening opportunities identified
- [ ] Coupling points documented
- [ ] Specific recommendations provided
- [ ] Changes tested and verified
