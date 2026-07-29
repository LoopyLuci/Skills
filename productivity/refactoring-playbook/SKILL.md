---
name: refactoring-playbook
description: "Use for refactoring. Smell detection, patterns, metrics."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [programming, refactoring, technical-debt, code-quality, clean-code]
    related_skills: [code-review-checklist, debugging-workflow, performance-profiling]
---

# Refactoring Playbook

## Overview

A structured methodology for identifying technical debt, applying proven refactoring patterns, and measuring before/after code quality. Covers code smell detection (long methods, god classes, shotgun surgery, duplication), refactoring patterns (extract method, replace conditional with polymorphism, strategy pattern), testing strategies during refactoring, and quantitative metrics.

## When to Use

- A function or class has become too large or complex
- Adding a new feature requires understanding tangled code
- The same logic appears in multiple places (copy-paste debt)
- Test coverage is low and the codebase is fragile
- Bug fixes keep surfacing in the same module
- Onboarding new team members to a legacy module
- Before implementing a performance optimization

## Workflow

### Phase 1: Code Smell Detection

Run automated scans to locate hot spots before manual review:

```bash
# Python — complexity analysis
pip install radon xenon 2>/dev/null

# McCabe cyclomatic complexity — find complex functions
radon cc . -s -n C --exclude 'venv,node_modules,.git,__pycache__' | head -30

# Maintainability index (lower = harder to maintain)
radon mi . -s --exclude 'venv,node_modules,.git,__pycache__' | head -30

# Raw metrics (LOC, comments, blank)
radon raw . --exclude 'venv,node_modules,.git,__pycache__' -s | sort -t: -k2 -rn | head -20

# JavaScript/TypeScript — complexity
npx complexity-report --limit 10 src/ 2>/dev/null || npm install -g complexity-report

# Find long functions (> 50 lines)
find . -name '*.py' -not -path '*/venv/*' -not -path '*/.git/*' \
  -exec awk '/^def |^async def /{if(func) print func, lines; func=$0; lines=0} \
    func && /^[^#]/{lines++} END{if(func) print func, lines}' {} \; \
  | sort -t' ' -k2 -rn | head -20
```

**Smell catalog (with detection commands):**

```python
# 1. Long Method (> 30 lines)
# Detection: radon cc, or line count by function

# 2. God Class (> 200 lines, > 10 methods)
# Detection: find . -name '*.py' | xargs awk '/^class /{if(ml>200) print cname, ml; cname=$0; ml=0; mc=0} /^    def /{mc++} {ml++} END{if(ml>200) print cname, ml}'

# 3. Shotgun Surgery (a change requires editing many files)
# Detection: git log --oneline --name-only | sort | uniq -c | sort -rn | head -20
# Then: check which files frequently change together

# 4. Duplicate Code
# Detection: pip install flake8 flake8-copy
flake8 --select=CPY --exclude=venv,.git,node_modules
# Or with jscpd:
npx jscpd . --min-lines 5 --min-tokens 50

# 5. Long Parameter List (> 3 params)
grep -rn --include='*.py' -E 'def [^(]+\([^)]*(, [^,)]+){4,}' . | head -20

# 6. Feature Envy (method uses more of another class than its own)
# Manual: grep for self. vs other_class. usage in method body
# Look for grep -c 'self\.' vs grep -c 'other\.'

# 7. Primitive Obsession (overuse of strings/ints instead of types)
grep -rn --include='*.py' "phone\|email\|zip\|ssn\|address" . | head -20

# 8. Switch Statements / Type-Checking Conditionals
grep -rn --include='*.py' -E '(elif.*type\(|isinstance|if.*==.*"|match.*:)'. | head -20
```

### Phase 2: Refactoring Patterns

```python
# ==========================================
# PATTERN 1: Extract Method
# ==========================================
# BEFORE: Long method doing too much
def process_order(order, user, inventory, payment_gateway):
    total = 0
    for item in order['items']:
        if item['sku'] not in inventory:
            raise ValueError(f"Item {item['sku']} out of stock")
        total += item['quantity'] * item['price']

    if user['balance'] < total:
        raise ValueError("Insufficient funds")

    charge = payment_gateway.charge(user['id'], total)
    if not charge['success']:
        raise RuntimeError(f"Payment failed: {charge['error']}")

    for item in order['items']:
        inventory[item['sku']]['stock'] -= item['quantity']
        if inventory[item['sku']]['stock'] < 0:
            raise ValueError(f"Inventory underflow for {item['sku']}")

    return {'order_id': order['id'], 'total': total, 'charge_id': charge['id']}

# AFTER: Extracted methods with single responsibility
def calculate_order_total(order, inventory):
    for item in order['items']:
        if item['sku'] not in inventory:
            raise ValueError(f"Item {item['sku']} out of stock")
    return sum(item['quantity'] * item['price'] for item in order['items'])

def verify_balance(user, required):
    if user['balance'] < required:
        raise ValueError("Insufficient funds")

def process_payment(gateway, user_id, amount):
    charge = gateway.charge(user_id, amount)
    if not charge['success']:
        raise RuntimeError(f"Payment failed: {charge['error']}")
    return charge

def update_inventory(order, inventory):
    for item in order['items']:
        inventory[item['sku']]['stock'] -= item['quantity']
        if inventory[item['sku']]['stock'] < 0:
            raise ValueError(f"Inventory underflow for {item['sku']}")

def process_order(order, user, inventory, payment_gateway):
    total = calculate_order_total(order, inventory)
    verify_balance(user, total)
    charge = process_payment(payment_gateway, user['id'], total)
    update_inventory(order, inventory)
    return {'order_id': order['id'], 'total': total, 'charge_id': charge['id']}

# ==========================================
# PATTERN 2: Replace Conditional with Polymorphism
# ==========================================
# BEFORE: Switch on type
def calculate_shipping(order):
    if order['type'] == 'standard':
        return order['weight'] * 0.5 if order['weight'] < 10 else order['weight'] * 0.3
    elif order['type'] == 'express':
        return order['weight'] * 1.5 + 5
    elif order['type'] == 'overnight':
        return order['weight'] * 3.0 + 10
    elif order['type'] == 'international':
        return order['weight'] * 2.0 + 15 + order['weight'] * 0.1
    raise ValueError(f"Unknown shipping type: {order['type']}")

# AFTER: Strategy pattern
from abc import ABC, abstractmethod

class ShippingStrategy(ABC):
    @abstractmethod
    def calculate(self, weight: float) -> float:
        pass

class StandardShipping(ShippingStrategy):
    def calculate(self, weight: float) -> float:
        return weight * (0.5 if weight < 10 else 0.3)

class ExpressShipping(ShippingStrategy):
    def calculate(self, weight: float) -> float:
        return weight * 1.5 + 5

class OvernightShipping(ShippingStrategy):
    def calculate(self, weight: float) -> float:
        return weight * 3.0 + 10

class InternationalShipping(ShippingStrategy):
    def calculate(self, weight: float) -> float:
        return weight * 2.0 + 15 + weight * 0.1

STRATEGIES = {
    'standard': StandardShipping(),
    'express': ExpressShipping(),
    'overnight': OvernightShipping(),
    'international': InternationalShipping(),
}

def calculate_shipping(order):
    strategy = STRATEGIES.get(order['type'])
    if not strategy:
        raise ValueError(f"Unknown shipping type: {order['type']}")
    return strategy.calculate(order['weight'])

# ==========================================
# PATTERN 3: Extract Class (God Class decomposition)
# ==========================================
# BEFORE: God class
class OrderProcessor:
    def validate_order(self, order): ...
    def calculate_taxes(self, order): ...
    def process_payment(self, order, gateway): ...
    def update_inventory(self, order, inventory): ...
    def send_confirmation(self, order, user): ...
    def generate_invoice(self, order): ...
    def apply_discount(self, order, coupon): ...

# AFTER: Decomposed classes
class OrderValidator:
    def validate(self, order): ...
class TaxCalculator:
    def calculate(self, order): ...
class PaymentProcessor:
    def __init__(self, gateway): ...
    def process(self, order): ...
class InventoryManager:
    def update(self, order): ...
class NotificationService:
    def send_confirmation(self, order, user): ...
class InvoiceGenerator:
    def generate(self, order): ...
class DiscountEngine:
    def apply(self, order, coupon): ...

class OrderService:
    def __init__(self, validator, tax, payment, inventory,
                 notification, invoice, discount):
        self.validator = validator
        self.tax = tax
        self.payment = payment
        self.inventory = inventory
        self.notification = notification
        self.invoice = invoice
        self.discount = discount

    def process_order(self, order, coupon=None):
        self.validator.validate(order)
        if coupon:
            self.discount.apply(order, coupon)
        order['tax'] = self.tax.calculate(order)
        self.payment.process(order)
        self.inventory.update(order)
        self.notification.send_confirmation(order)
        self.invoice.generate(order)

# ==========================================
# PATTERN 4: Introduce Parameter Object
# ==========================================
# BEFORE: Long parameter list
def search_users(age_min, age_max, city, country, is_active, sort_by, limit, offset):
    ...

# AFTER: Parameter object
from dataclasses import dataclass
from typing import Optional

@dataclass
class UserSearchCriteria:
    age_range: tuple[Optional[int], Optional[int]] = (None, None)
    city: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = None
    sort_by: str = "created_at"
    limit: int = 20
    offset: int = 0

def search_users(criteria: UserSearchCriteria):
    ...
```

### Phase 3: Testing Strategy During Refactoring

```python
"""Characterization tests — capture current behavior before refactoring."""
def test_process_order_snapshot(snapshot):
    order = make_test_order()
    inventory = make_test_inventory()
    user = make_test_user()
    gateway = FakePaymentGateway()
    result = process_order(order, user, inventory, gateway)
    snapshot.assert_match(repr(result), "process_order_output.txt")
```

```bash
# Property-based testing for invariants
pip install hypothesis 2>/dev/null

# Safe refactoring workflow:
# 1. Ensure complete test coverage of the target code
pytest --cov=path/to/module --cov-fail-under=80

# 2. Commit the starting state
git add -A && git commit -m "chore: snapshot before refactoring [ci skip]"

# 3. Create a feature branch
git checkout -b refactor/extract-method-order-processing

# 4. Apply ONE refactoring pattern at a time
# 5. Run tests after each step
pytest && echo "GREEN" || echo "RED - revert and retry"

# 6. Commit after each successful pattern
git add -p && git commit -m "refactor: extract calculate_order_total method"

# 7. When all patterns applied, rebase for clean history
git rebase -i main

# 8. Run full test suite + lint
pytest && flake8 && mypy . && echo "ALL PASS"

# 9. Merge
git checkout main && git merge --squash refactor/extract-method-order-processing
```

### Phase 4: Before/After Metrics

```bash
# === BEFORE ===
radon cc path/to/module -s --exclude 'venv'
radon mi path/to/module -s --exclude 'venv'
npx jscpd path/to/module --min-lines 5 --min-tokens 50

# === DO THE REFACTORING ===

# === AFTER ===
radon cc path/to/module -s --exclude 'venv'
radon mi path/to/module -s --exclude 'venv'
npx jscpd path/to/module --min-lines 5 --min-tokens 50

# Generate diff report
echo "=== REFACTORING METRICS ==="
echo "Complexity (Max): $(radon cc path/to/module -s | grep -c 'F\|C' || echo 'check')"
echo "Maintainability Index: $(radon mi path/to/module -s)"
echo "Total LOC: $(find path/to/module -name '*.py' | xargs wc -l | tail -1)"
echo "Test Coverage: $(pytest --cov=path/to/module --cov-report=term 2>/dev/null | grep 'TOTAL')"
```

## Common Pitfalls

- **Refactoring without tests**: Never refactor code without good test coverage. Write characterization tests first.
- **Big bang refactoring**: Apply one pattern at a time. Frequent small commits catch regressions early.
- **Mixing refactoring with feature work**: Never add features and refactor in the same commit. Different risk profiles.
- **Changing interfaces**: Public API changes break callers. Keep old interfaces as wrappers, deprecate don't remove.
- **Premature optimization**: Refactor for readability first. Optimize only when profiling shows a bottleneck.
- **Over-engineering**: A simple if/elif chain is fine for 3 cases. Use polymorphism when variants grow.
- **Ignoring performance regressions**: Refactoring can introduce perf issues. Run benchmarks before and after.
- **Not agreeing on quality bars**: Get team consensus on what "clean" means. Different projects have different standards.

## Verification Checklist

- [ ] All code smells in the target module identified (long methods, god classes, duplication, etc.)
- [ ] Characterization/snapshot tests written for areas without test coverage
- [ ] Test coverage meets team threshold (≥80%) before refactoring begins
- [ ] Starting state committed to git with clear message
- [ ] Each refactoring pattern applied and tested in its own commit
- [ ] Refactoring branch squashed to clean history on merge
- [ ] Before/after metrics collected (complexity, LOC, duplication %, coverage)
- [ ] All existing tests pass after refactoring
- [ ] No public API interfaces broken (backward compatible)
- [ ] Code review conducted focusing on: readability, test quality, no hidden logic changes
- [ ] Performance benchmarks show no regression (or regression is acceptable/planned)
- [ ] Updated documentation (docstrings, README, type annotations) for changed code
