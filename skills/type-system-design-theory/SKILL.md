---
name: type-system-design-theory
description: "Use when designing programming language type systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [type-systems, type-theory, programming-languages, PLT, compiler]
    related_skills: [compiler-interpreter-basics, formal-verification-methods, functional-programming-concepts]
---

# Type System Design

Designing type systems for programming languages — from simple type checkers through generics, traits, dependent types, and type-level computation.

## When to Use

- Designing a new programming language or DSL
- Adding a type system to an existing dynamic language
- Implementing type inference, generics, or advanced type features
- Understanding type theory concepts (soundness, completeness, decidability)
- Building static analysis tools that reason about types

## Type System Spectrum

| System | Expressiveness | Inference | Complexity | Examples |
|--------|---------------|-----------|------------|----------|
| Untyped | None | N/A | Trivial | Assembly, B |
| Simple types | Basic safety | Full | Low | C (basic) |
| Hindley-Milner | Parametric polymorphism | Full (HM) | Medium | ML, Haskell |
| Gradual | Dynamic + static opt-in | Partial | Medium | TypeScript, Python |
| System F | Higher-rank types | Undecidable | High | GHC Haskell |
| Dependent | Values as types | Partial | Very high | Idris, Coq |
| Linear/Substructural | Resource tracking | Limited | High | Rust |

## Type Checker Implementation

### Base Type System

```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Set

class Type:
    """Base type class."""
    pass

@dataclass
class IntType(Type):
    pass

@dataclass
class BoolType(Type):
    pass

@dataclass
class FunctionType(Type):
    param_type: Type
    return_type: Type

@dataclass
class TypeVariable(Type):
    name: str

@dataclass
class GenericType(Type):
    name: str
    params: List[Type]


class TypeChecker:
    """Simple type checker for a lambda calculus with let-polymorphism."""
    
    def __init__(self):
        self.env = {}  # name -> Type
        self.constraints = []
    
    def check(self, expr, env=None):
        """Infer/check type of expression."""
        if env is None:
            env = self.env
        
        # Literals
        if isinstance(expr, int):
            return IntType()
        if isinstance(expr, bool):
            return BoolType()
        
        # Variables
        if isinstance(expr, str):
            if expr in env:
                return env[expr]
            raise TypeError(f"Unbound variable: {expr}")
        
        # Lambda: λx: T. e
        if expr[0] == 'lambda':
            _, param, param_type, body = expr
            body_type = self.check(body, {**env, param: param_type})
            return FunctionType(param_type, body_type)
        
        # Application: e1 e2
        if isinstance(expr, tuple) and len(exp) == 2:
            fn_type = self.check(exp[0], env)
            arg_type = self.check(exp[1], env)
            
            if isinstance(fn_type, FunctionType):
                if fn_type.param_type != arg_type:
                    raise TypeError(f"Type mismatch: expected {fn_type.param_type}, got {arg_type}")
                return fn_type.return_type
            
            raise TypeError(f"Expected function, got {fn_type}")
        
        raise ValueError(f"Unknown expression: {expr}")
```

### Hindley-Milner Type Inference

```python
class HindleyMilner:
    """Hindley-Milner type inference with unification."""
    
    def __init__(self):
        self.var_counter = 0
        self.substitutions = {}
    
    def fresh_var(self):
        name = f"t{self.var_counter}"
        self.var_counter += 1
        return TypeVariable(name)
    
    def unify(self, t1: Type, t2: Type):
        """Unify two types, updating substitutions."""
        t1 = self.apply(t1)
        t2 = self.apply(t2)
        
        if t1 == t2:
            return
        
        if isinstance(t1, TypeVariable):
            if self.occurs_check(t1, t2):
                raise TypeError(f"Occurs check: {t1} in {t2}")
            self.substitutions[t1.name] = t2
            return
        
        if isinstance(t2, TypeVariable):
            if self.occurs_check(t2, t1):
                raise TypeError(f"Occurs check: {t2} in {t1}")
            self.substitutions[t2.name] = t1
            return
        
        if isinstance(t1, FunctionType) and isinstance(t2, FunctionType):
            self.unify(t1.param_type, t2.param_type)
            self.unify(t1.return_type, t2.return_type)
            return
        
        raise TypeError(f"Cannot unify {t1} with {t2}")
    
    def infer(self, expr, env=None):
        """Infer the type of an expression."""
        if env is None:
            env = {}
        
        if isinstance(expr, int):
            return IntType()
        if isinstance(expr, bool):
            return BoolType()
        
        if isinstance(expr, str):
            if expr not in env:
                raise TypeError(f"Unbound: {expr}")
            return self.apply(env[expr])
        
        if expr[0] == 'let':
            _, var, value, body = expr
            # Polymorphic let: generalize then instantiate
            var_type = self.infer(value, env)
            # Generalize (simplified)
            generalized = self.generalize(var_type, env)
            env[var] = generalized
            return self.infer(body, env)
        
        if expr[0] == 'lambda':
            _, param, body = expr
            param_type = self.fresh_var()
            body_type = self.infer(body, {**env, param: param_type})
            return FunctionType(param_type, body_type)
        
        if isinstance(expr, tuple) and len(expr) == 2:
            fn_type = self.infer(expr[0], env)
            arg_type = self.infer(expr[1], env)
            result_type = self.fresh_var()
            self.unify(fn_type, FunctionType(arg_type, result_type))
            return result_type
```

### Gradual Typing (TypeScript-style)

```python
class GradualTypeChecker:
    """Gradual typing: static + dynamic types with consistency."""
    
    DYNAMIC = TypeVariable("any")  # Dynamic type
    
    def consistent(self, t1, t2):
        """Consistency relation: like equality but 'any' matches anything."""
        if t1 == self.DYNAMIC or t2 == self.DYNAMIC:
            return True
        if isinstance(t1, FunctionType) and isinstance(t2, FunctionType):
            return self.consistent(t1.param_type, t2.param_type) and \
                   self.consistent(t1.return_type, t2.return_type)
        return t1 == t2
    
    def check_annotation(self, annotated_type, inferred_type):
        """Check annotated type against inferred type with consistency."""
        if not self.consistent(annotated_type, inferred_type):
            raise TypeError(
                f"Type annotation mismatch: declared {annotated_type}, "
                f"inferred {inferred_type}"
            )
```

## Subtyping

```python
class SubtypeChecker:
    """Structural subtyping (like TypeScript's type compatibility)."""
    
    def is_subtype(self, t1, t2):
        """Is t1 a subtype of t2 (t1 <= t2)?"""
        if t1 == t2:
            return True
        
        # Top type
        if isinstance(t2, Top):
            return True
        
        # Bottom type
        if isinstance(t1, Bot):
            return True
        
        if isinstance(t1, RecordType) and isinstance(t2, RecordType):
            # Width subtyping: t1 has all fields of t2 (and possibly more)
            for field, field_type in t2.fields.items():
                if field not in t1.fields:
                    return False
                if not self.is_subtype(t1.fields[field], field_type):
                    return False
            return True
        
        # Function types (contravariant parameter, covariant return)
        if isinstance(t1, FunctionType) and isinstance(t2, FunctionType):
            return self.is_subtype(t2.param_type, t1.param_type) and \
                   self.is_subtype(t1.return_type, t2.return_type)
        
        return False
```

## Common Pitfalls

1. **Undecidable inference** — full type inference for System F is undecidable; restrict to Hindley-Milner or require annotations
2. **Subtyping + generics** — variance matters; get covariance/contravariance/invariance wrong and the type system is unsound
3. **Gradual typing performance** — runtime type checks for gradual types add overhead; optimize hot paths
4. **Error messages** — type errors in complex generic code are cryptic; invest in good error reporting
5. **Soundness vs. completeness** — sound type systems reject some valid programs; trade off for safety
6. **Recursive types** — without equi-recursive or iso-recursive handling, infinite types crash the checker

## Verification Checklist

- [ ] Type checker passes standard test suite (PLT redex, etc.)
- [ ] Soundness: well-typed programs don't have type errors at runtime (progress + preservation)
- [ ] Inference terminates on all inputs (no infinite loops)
- [ ] Error messages include source location and expected/actual types
- [ ] Subtyping is transitive (A <: B, B <: C => A <: C)
- [ ] Generic instantiation is correct (no unsound escapes)
- [ ] Gradual types degrade gracefully to dynamic checking

## See Also

- compiler-interpreter-basics — implementing type checkers in compilers
- formal-verification-methods — type-based verification
- functional-programming-concepts — type systems in FP
