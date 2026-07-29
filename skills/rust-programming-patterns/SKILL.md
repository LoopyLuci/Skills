---
name: rust-programming-patterns
description: "Use when writing production Rust: ownership, traits, error-handling."
category: software-development
tags: [rust, programming, ownership, traits, error-handling]
---
# Rust Programming Patterns

Production Rust patterns: ownership, borrowing, traits, error handling, async.

## Error Handling

```rust
use anyhow::{Context, Result};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Network error: {0}")]
    Network(String),
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("Not found: {0}")]
    NotFound(String),
}

pub fn read_config(path: &str) -> Result<String> {
    std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read config at {path}"))
}
```

## Builder Pattern

```rust
#[derive(Debug, Default)]
pub struct ModelConfig {
    name: Option<String>,
    hidden_size: Option<usize>,
    num_layers: Option<usize>,
    dropout: Option<f64>,
}

impl ModelConfig {
    pub fn new() -> Self { Self::default() }
    pub fn name(mut self, name: &str) -> Self {
        self.name = Some(name.to_string()); self
    }
    pub fn hidden_size(mut self, size: usize) -> Self {
        self.hidden_size = Some(size); self
    }
    pub fn build(self) -> Result<Config, &'static str> {
        Ok(Config {
            name: self.name.ok_or("name required")?,
            hidden_size: self.hidden_size.unwrap_or(768),
            num_layers: self.num_layers.unwrap_or(12),
            dropout: self.dropout.unwrap_or(0.1),
        })
    }
}
```

## Type State Pattern

```rust
struct Uninitialized;
struct Initialized;

struct Pipeline<S> {
    steps: Vec<String>,
    _state: std::marker::PhantomData<S>,
}

impl Pipeline<Uninitialized> {
    pub fn new() -> Self {
        Pipeline { steps: vec![], _state: PhantomData }
    }
    pub fn add_step(mut self, step: &str) -> Self {
        self.steps.push(step.to_string()); self
    }
    pub fn initialize(self) -> Pipeline<Initialized> {
        Pipeline { steps: self.steps, _state: PhantomData }
    }
}

impl Pipeline<Initialized> {
    pub fn run(&self) {
        for step in &self.steps { println!("Running {step}"); }
    }
}
```

## Borrow Patterns

```rust
// Interior mutability
use std::cell::RefCell;
use std::rc::Rc;

struct SharedState {
    counter: RefCell<u32>,
}

let state = Rc::new(SharedState { counter: RefCell::new(0) });
*state.counter.borrow_mut() += 1;
```

## Pitfalls

- Lifetimes can be elided in most function signatures
- `Rc` is single-threaded; use `Arc` for threads
- `RefCell` runtime borrow checks — panic if already borrowed
- `async` traits need `#[async_trait]` or `trait_variant::make`
- `?` operator only works in functions returning `Result` or `Option`
