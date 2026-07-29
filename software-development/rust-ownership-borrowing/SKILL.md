---
name: rust-ownership-borrowing
description: "Use when understanding Rust ownership and borrowing."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [rust, ownership, borrowing, lifetimes, references, memory-safety]
    related_skills: [rust-programming-patterns, go-concurrency-patterns, type-system-design-theory]
---

# Rust Ownership and Borrowing

Understanding Rust's ownership and borrowing system — from owners and references through lifetimes, borrowing rules, and common patterns.

## When to Use

- Learning Rust's ownership model
- Writing safe Rust without fighting the borrow checker
- Managing lifetimes in complex data structures
- Implementing safe abstractions

## Ownership Patterns

```rust
// Ownership transfer
fn take_ownership(s: String) -> usize { s.len() }

// Borrowing
fn borrow(s: &String) -> usize { s.len() }

// Mutable borrow
fn append(s: &mut String, text: &str) { s.push_str(text); }

// Lifetime annotations
struct Config<'a> {
    name: &'a str,
    version: &'a str,
}

impl<'a> Config<'a> {
    fn new(name: &'a str, version: &'a str) -> Self {
        Config { name, version }
    }
}

// Lifetime elision rules
fn first_word(s: &str) -> &str {
    s.split_whitespace().next().unwrap_or(s)
}
```

## Verification Checklist

- [ ] Each value has exactly one owner
- [ ] References never outlive borrowed data
- [ ] Mutable references are exclusive (no aliasing)
- [ ] Lifetime annotations only where needed (elision rules)
- [ ] Interior mutability (RefCell, Mutex) for shared mutation
- [ ] Clone vs Copy semantics understood
