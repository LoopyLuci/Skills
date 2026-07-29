---
name: code-refactoring-strategies
description: "Use when systematically refactoring code."
category: software-development
tags: [refactoring, code-quality, cleanup, technical-debt]
---
# Code Refactoring Strategies

Systematic approaches to refactoring code safely.

## The Refactoring Workflow

```
1. Identify the target (smell, debt, pattern)
2. Ensure tests exist (write them first if not)
3. Make ONE change at a time
4. Run tests after each change
5. Commit each micro-step
```

## Common Code Smells & Fixes

```python
# 1. Long function → Extract method
# BEFORE
def process_order(order):
    # 50 lines of validation
    # 30 lines of pricing
    # 20 lines of shipping
    pass

# AFTER
def process_order(order):
    validate_order(order)
    calculate_pricing(order)
    arrange_shipping(order)

# 2. Duplicate code → Extract common
# BEFORE
def calc_tax_usd(price): return price * 0.08
def calc_tax_eur(price): return price * 0.19

# AFTER
def calc_tax(price, rate): return price * rate

# 3. Large class → Split into focused classes
class OrderProcessor:  # too many responsibilities
class OrderValidator:  # validation only
class OrderPricer:     # pricing only
class OrderShipper:    # shipping only
```

## Safe Refactoring (The Mikado Method)

```python
# 1. Mark target
# REFACTOR: Replace if/elif chain with strategy pattern

# 2. Make ONE change, run tests
# If tests fail, note the dependency, revert, fix dependency, retry

# 3. Graph of dependencies
# Target: strategy pattern
# ├── Need: create Strategy base class
# ├── Need: extract each branch into its own class
# ├── Need: add factory method
# └── Test: all branches produce same output
```

## Large-Scale Refactoring

```python
# Strangler Fig pattern
# ┌── Old API ──┐     ┌── Old ──┐
# │              │ ──→ │          │
# │              │     │  New      │
# └── New API ──┘     └──────────┘

# 1. Add new API alongside old
# 2. Route some traffic to new
# 3. Monitor and compare
# 4. Route all traffic to new
# 5. Remove old API
```

## Pitfalls

- Never refactor and add features in the same change
- Large refactors without tests = disaster
- Rename tools (IDE rename refactoring) are safer than find/replace
- Refactoring public APIs breaks consumers — deprecate first
- Performance regression can sneak in — benchmark before and after
