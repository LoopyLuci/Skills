---
name: codebase-design
description: Use when designing module interfaces, finding deepening opportunities, or making code testable
tags: [design, architecture, modules, depth, interfaces]
related_skills: [design-an-interface, improve-codebase-architecture, domain-driven-design-tactical]
---

# Codebase Design

Design deep modules: a lot of behavior behind a small interface, placed at a clean seam, testable through that interface.

## Glossary
Use these terms exactly - consistent language is the point.

- **Module** - anything with an interface and an implementation. Deliberately scale-agnostic: a function, class, package, or tier-spanning slice.
- **Interface** - everything a caller must know to use the module correctly: type signature, invariants, ordering constraints, error modes, configuration, and performance characteristics.
- **Implementation** - what is inside a module, its body of code.
- **Depth** - leverage at the interface: the amount of behavior a caller can exercise per unit of interface they have to learn.
- **Seam** (Michael Feathers) - a place where you can alter behavior without editing in that place.

## Principles
- Deep over shallow: prefer a small interface that hides lots of behavior
- Test through the interface: if the seam is clean, the test is simple
- Caller leverage: every line of interface should unlock multiple lines of behavior

## Common Pitfalls

- **Inconsistent terminology**: Do not substitute 'component', 'service', 'API', or 'boundary' for the defined terms. Consistent language is the whole point.
- **Depth over everything**: Depth is a goal, but not the only one. Performance requirements, operational constraints, and team familiarity also matter.
- **Seams placed at the wrong level**: A seam should match a natural boundary in the domain, not an architectural fashion. Forcing seams where they do not belong creates accidental complexity.

## Code Examples

```typescript
// Deep module example: small interface, complex implementation

interface PaymentProcessor {
  charge(amount: Money, source: PaymentSource): Result<Payment>;
  refund(paymentId: string): Result<Payment>;
}

// Implementation handles: retries, idempotency, webhook verification,
// currency conversion, fee calculation, receipt email,
// fraud detection, dispute handling, logging
// But caller only sees charge() and refund()
class StripePaymentProcessor implements PaymentProcessor {
  // ... complex internals hidden behind a simple interface
}
```

## Verification Checklist

- [ ] Module terminology used consistently throughout
- [ ] Interface signatures are clear and minimal
- [ ] Depth evaluated: behavior per unit of interface
- [ ] Seam boundaries identified and justified
- [ ] Design principles documented
