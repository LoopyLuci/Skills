---
name: clean-code-principles
description: "Use when applying clean code and software craftsmanship."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [clean-code, craftsmanship, naming, refactoring, SOLID, readability]
    related_skills: [code-refactoring-strategies, software-design-patterns, test-driven-development, code-review-checklist]
---

# Clean Code Principles

Writing clean, maintainable, and readable code — from naming conventions and function design through SOLID principles, comments, and code organization.

## When to Use

- Writing new code that will be maintained by others
- Reviewing code for readability and maintainability
- Refactoring legacy code to be more understandable
- Onboarding new developers to code standards
- Improving code quality across a team

## Core Principles

```python
# Principle 1: Meaningful Names
# BAD:
def fn(a, b):
    x = a + b
    return x * 0.1

# GOOD:
def calculate_tax(income: float, tax_rate: float) -> float:
    taxable_income = income
    tax_amount = taxable_income * tax_rate
    return tax_amount

# Principle 2: Small Functions (do one thing)
# BAD:
def process_order(order):
    validate(order)
    total = sum(item['price'] for item in order['items'])
    if total > 100: total *= 0.9  # Discount logic mixed in
    charge_payment(order['customer'], total)
    send_email(order['customer']['email'], f"Order confirmed for ${total}")
    update_inventory(order['items'])

# GOOD:
def process_order(order):
    validate_order(order)
    total = calculate_order_total(order)
    charge_customer(order['customer'], total)
    send_confirmation(order['customer'], total)
    update_inventory(order['items'])
```

## Verification Checklist

- [ ] Names reveal intent (not `data`, `info`, `temp`, `x`)
- [ ] Functions do one thing (3-5 lines ideal)
- [ ] No side effects (functions only do what they say)
- [ ] Comments explain WHY not WHAT
- [ ] Error handling is separate from business logic
- [ ] Tests exist before or alongside code
