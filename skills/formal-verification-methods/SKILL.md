---
name: formal-verification-methods
description: "Use when implementing formal verification for software."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [formal-verification, model-checking, theorem-proving, correctness]
    related_skills: [compiler-interpreter-basics, type-system-design-theory, systematic-debugging, test-driven-development]
---

# Formal Verification Methods

Applying formal verification to software systems — model checking, theorem proving, symbolic execution, and static analysis for proving correctness properties.

## When to Use

- Safety-critical systems (medical devices, avionics, autonomous vehicles)
- Smart contract auditing (DeFi, blockchain)
- Cryptographic protocol verification
- Operating system or hypervisor correctness
- Proving absence of entire classes of bugs (buffer overflows, race conditions)
- Regulatory compliance requiring formal methods (DO-178C, ISO 26262)

## Verification Approaches

| Method | What it Proves | Automation | Scalability |
|--------|---------------|------------|-------------|
| Model Checking | Temporal properties | Fully auto | Medium |
| Theorem Proving | Arbitrary properties | Interactive | Low |
| Symbolic Execution | Path-specific bugs | Automated | Low |
| Abstract Interpretation | Absence of errors | Auto | High |
| SAT/SMT Solving | Constraint satisfaction | Auto | High |
| Type Systems | Type safety | Auto | Very High |

### Model Checking

```python
class ModelChecker:
    """Simple model checker for finite-state systems.
    Checks CTL/LTL properties via state space exploration."""
    
    def __init__(self, initial_state, transition_fn, properties):
        self.initial = initial_state
        self.transition = transition_fn  # state -> list of next states
        self.properties = properties      # list of property check functions
        self.visited = set()
        self.counterexamples = []
    
    def verify(self):
        """Verify all properties via explicit-state model checking."""
        results = {}
        for prop_name, prop_fn in self.properties.items():
            self.visited.clear()
            sat = self._check_property(self.initial, prop_fn, set())
            results[prop_name] = sat
            if not sat:
                print(f"Property '{prop_name}' VIOLATED")
            else:
                print(f"Property '{prop_name}' satisfied")
        return results
    
    def _check_property(self, state, prop_fn, path):
        """DFS-based property checking on state space."""
        if state in self.visited:
            return True  # Already checked
        self.visited.add(state)
        
        if not prop_fn(state):
            self.counterexamples.append(list(path) + [state])
            return False
        
        for next_state in self.transition(state):
            if not self._check_property(next_state, prop_fn, path + [state]):
                return False
        return True
```

### SMT-Based Verification

```python
# Using Z3 SMT solver for symbolic verification
from z3 import *

def verify_contract(balance_pre: int, amount: int):
    """
    Verify: withdraw(balance, amount) ensures balance >= 0
    """
    balance = Int('balance')
    withdraw_amount = Int('amount')
    
    # Pre-conditions
    pre = And(balance >= 0, withdraw_amount > 0, withdraw_amount <= balance)
    
    # Post-conditions
    post = (balance - withdraw_amount >= 0)
    
    # Verify: if pre holds, post must hold after execution
    verify = Implies(pre, post)
    
    s = Solver()
    s.add(Not(verify))
    
    if s.check() == unsat:
        print("✅ Contract verified: withdrawal maintains non-negative balance")
    else:
        print("❌ Counterexample found!")
        print(s.model())
```

### Abstract Interpretation

```python
class AbstractDomain:
    """Abstract domain for sign analysis (+, -, 0, ⊥, ⊤)."""
    
    SIGN_BOT = 0   # Bottom (unreachable)
    SIGN_NEG = 1   # Negative
    SIGN_ZERO = 2  # Zero
    SIGN_POS = 3   # Positive
    SIGN_TOP = 4   # Top (anything)
    
    # Abstract operations
    def abstract_add(s1, s2):
        if s1 == SIGN_BOT or s2 == SIGN_BOT:
            return SIGN_BOT
        if s1 == SIGN_TOP or s2 == SIGN_TOP:
            return SIGN_TOP
        
        results = set()
        concrete = {
            SIGN_NEG: {-1}, SIGN_ZERO: {0}, SIGN_POS: {1}
        }
        for v1 in concrete.get(s1, {}):
            for v2 in concrete.get(s2, {}):
                r = v1 + v2
                if r < 0: results.add(SIGN_NEG)
                elif r == 0: results.add(SIGN_ZERO)
                else: results.add(SIGN_POS)
        return AbstractDomain._join(results)
    
    def abstract_mul(s1, s2):
        # Similar to abstract_add
        pass
    
    def abstract_gt(s1, s2):
        """s1 > s2 in abstract domain."""
        # If pos > anything or anything > neg, result may be true
        pass

# Apply to a simple program
def analyze_loop():
    """Prove i >= 0 after loop: for (i = N; i > 0; i--)"""
    # Without knowing N, we can prove i is non-negative at loop exit
    pass
```

## Common Pitfalls

1. **State explosion** — explicit model checking doesn't scale past 10^6 states; use symbolic techniques
2. **Environment modeling** — formal verification is only as good as the model of the environment
3. **Specification correctness** — verifying the wrong property gives false confidence; review specs independently
4. **Tool fragmentation** — different tools for different properties; integrate into CI pipeline
5. **False positives from abstraction** — over-approximation reports bugs that aren't real; refine the abstraction
6. **Proof maintenance** — verified software becomes unverified after changes; use continuous verification

## Verification Checklist

- [ ] Properties formally specified (safety, liveness, invariance)
- [ ] Model/environment accurately represents the system
- [ ] Verification terminates without timeout
- [ ] Counterexamples reviewed (not just discarded)
- [ ] Proof artifacts versioned alongside code
- [ ] CI pipeline runs verification on every change

## See Also

- compiler-interpreter-basics — verified compilers
- type-system-design-theory — type-based verification
- systematic-debugging — debugging when verification fails
- test-driven-development — testing complements verification
