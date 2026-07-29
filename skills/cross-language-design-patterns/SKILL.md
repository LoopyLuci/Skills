---
name: cross-language-design-patterns
description: "Use when implementing cross-language design patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [design-patterns, gof, python, rust, typescript, architecture]
    related_skills: [software-design-patterns, api-design-rest-graphql, functional-programming-concepts]
---

# Cross-Language Design Patterns

Implementing classic GoF and modern design patterns across multiple languages — Python, Rust, TypeScript — with language-specific idioms and trade-offs.

## When to Use

- Implementing design patterns in a language you're less familiar with
- Translating patterns between languages
- Choosing the right pattern for your language's paradigm
- Teaching or learning design patterns across language boundaries
- Building multi-language systems with consistent architecture

## Pattern Selection by Language

| Pattern | Python | Rust | TypeScript |
|---------|--------|------|------------|
| Singleton | Module-level | No (use DI) | Module export |
| Factory | __init_subclass__ | Enum dispatch | Class + switch |
| Builder | Dataclass + builder | Typestate builder | Fluent API |
| Observer | __call__ / signal | Channel | EventEmitter |
| Strategy | Function passing | Trait + dyn | Interface + class |
| State | Enum + methods | State machine | State pattern |
| Command | Callable | Trait + Vec | Command class |
| Visitor | @singledispatch | Pattern matching | Visitor interface |
| Iterator | __iter__ / yield | IntoIterator | Symbol.iterator |
| Decorator | @decorator | Middleware | @decorator + HOF |

## Creational Patterns

### Singleton (Language-Specific)

```python
# Python: module-level is naturally singleton
# _singleton_store.py
_instance = None

def get_instance():
    global _instance
    if _instance is None:
        _instance = ExpensiveObject()
    return _instance


# Python alternative: metaclass
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
```

```rust
// Rust: no singleton pattern needed — use DI or lazy_static!
use std::sync::OnceLock;

fn global_config() -> &'static Config {
    static CONFIG: OnceLock<Config> = OnceLock::new();
    CONFIG.get_or_init(|| Config::load())
}
```

```typescript
// TypeScript: module export is naturally singleton
// config.ts
export const config = new Config();
// or simple object literal
export const settings = {
    apiUrl: 'https://api.example.com',
    timeout: 5000,
};
```

### Builder Pattern

```python
# Python: dataclass builder pattern
from dataclasses import dataclass, field

@dataclass
class QueryBuilder:
    select_clause: str = "*"
    from_clause: str = ""
    where_clause: str = ""
    order_by_clause: str = ""
    limit_value: int = 0
    
    def select(self, columns: str) -> 'QueryBuilder':
        self.select_clause = columns
        return self
    
    def from_table(self, table: str) -> 'QueryBuilder':
        self.from_clause = table
        return self
    
    def where(self, condition: str) -> 'QueryBuilder':
        self.where_clause = f"WHERE {condition}"
        return self
    
    def build(self) -> str:
        query = f"SELECT {self.select_clause} FROM {self.from_clause}"
        if self.where_clause:
            query += f" {self.where_clause}"
        return query

# Usage: QueryBuilder().select("*").from_table("users").where("active=1").build()
```

```rust
// Rust: typestate builder pattern (compile-time safety!)
struct QueryBuilder<Select, From, Where> {
    select: Select,
    from: From,
    where_clause: Where,
}

// Empty state types
struct NoSelect;
struct SelectClause(String);
struct NoFrom;
struct FromClause(String);
struct NoWhere;
struct WhereClause(String);

impl QueryBuilder<NoSelect, NoFrom, NoWhere> {
    fn new() -> Self {
        QueryBuilder { select: NoSelect, from: NoFrom, where_clause: NoWhere }
    }
    
    fn select(self, cols: &str) -> QueryBuilder<SelectClause, NoFrom, NoWhere> {
        QueryBuilder {
            select: SelectClause(cols.to_string()),
            from: NoFrom,
            where_clause: NoWhere,
        }
    }
}

impl QueryBuilder<SelectClause, NoFrom, NoWhere> {
    fn from_table(self, table: &str) -> QueryBuilder<SelectClause, FromClause, NoWhere> {
        QueryBuilder {
            select: self.select,
            from: FromClause(table.to_string()),
            where_clause: NoWhere,
        }
    }
}

impl QueryBuilder<SelectClause, FromClause, NoWhere> {
    fn r#where(self, cond: &str) -> QueryBuilder<SelectClause, FromClause, WhereClause> {
        QueryBuilder {
            select: self.select,
            from: self.from,
            where_clause: WhereClause(cond.to_string()),
        }
    }
}

impl QueryBuilder<SelectClause, FromClause, WhereClause> {
    fn build(&self) -> String {
        format!("SELECT {} FROM {} WHERE {}",
                self.select.0, self.from.0, self.where_clause.0)
    }
}
```

```typescript
// TypeScript: fluent builder
class HttpRequestBuilder {
    private method: string = 'GET';
    private url: string = '';
    private headers: Record<string, string> = {};
    private body?: string;
    
    get(url: string): this {
        this.method = 'GET';
        this.url = url;
        return this;
    }
    
    post(url: string): this {
        this.method = 'POST';
        this.url = url;
        return this;
    }
    
    withHeader(key: string, value: string): this {
        this.headers[key] = value;
        return this;
    }
    
    withJsonBody(data: unknown): this {
        this.body = JSON.stringify(data);
        this.headers['Content-Type'] = 'application/json';
        return this;
    }
    
    async send(): Promise<Response> {
        return fetch(this.url, {
            method: this.method,
            headers: this.headers,
            body: this.body,
        });
    }
}
```

## Structural Patterns

### Adapter Pattern

```python
# Python
class EuropeanSocket:
    def voltage(self) -> int:
        return 230

class USASocket:
    def voltage(self) -> int:
        return 120

class Adapter:
    def __init__(self, socket):
        self.socket = socket
    
    def voltage(self) -> int:
        return self.socket.voltage() / 2  # Step down from 230 to 115
```

```typescript
// TypeScript
interface Logger {
    log(message: string): void;
}

class ConsoleLogger implements Logger {
    log(message: string): void {
        console.log(message);
    }
}

// External library with different interface
class ExternalLogger {
    writeMessage(msg: string, level: string): void {
        console.log(`[${level}] ${msg}`);
    }
}

// Adapter
class ExternalLoggerAdapter implements Logger {
    constructor(private external: ExternalLogger) {}
    
    log(message: string): void {
        this.external.writeMessage(message, 'INFO');
    }
}
```

## Behavioral Patterns

### Strategy Pattern

```python
# Python: functions are strategies naturally
def quick_sort(data):
    if len(data) <= 1:
        return data
    pivot = data[0]
    lesser = [x for x in data[1:] if x <= pivot]
    greater = [x for x in data[1:] if x > pivot]
    return quick_sort(lesser) + [pivot] + quick_sort(greater)

def merge_sort(data):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])
    return list(merge(left, right))

class Sorter:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def sort(self, data):
        return self.strategy(data)

# Usage: Sorter(strategy=quick_sort).sort([3, 1, 4, 1, 5])
```

```rust
// Rust: trait-based strategy pattern
trait SortStrategy {
    fn sort(&self, data: &mut [i32]);
}

struct QuickSort;
impl SortStrategy for QuickSort {
    fn sort(&self, data: &mut [i32]) {
        data.sort();  // Simplified; actual quicksort omitted
    }
}

struct MergeSort;
impl SortStrategy for MergeSort {
    fn sort(&self, data: &mut [i32]) {
        data.sort();  // Simplified
    }
}

struct Sorter {
    strategy: Box<dyn SortStrategy>,
}

impl Sorter {
    fn new(strategy: Box<dyn SortStrategy>) -> Self {
        Sorter { strategy }
    }
    
    fn sort(&self, data: &mut [i32]) {
        self.strategy.sort(data);
    }
}
```

### Observer Pattern

```python
# Python: __call__ makes any function an observer
class Observable:
    def __init__(self):
        self._observers = []
    
    def subscribe(self, callback):
        self._observers.append(callback)
    
    def unsubscribe(self, callback):
        self._observers.remove(callback)
    
    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer(*args, **kwargs)

# Usage
def on_data_received(data):
    print(f"Got: {data}")

source = Observable()
source.subscribe(on_data_received)
source.notify("hello")
```

```rust
// Rust: channel-based observer pattern
use std::sync::mpsc;

struct EventBus {
    sender: mpsc::Sender<String>,
    receiver: mpsc::Receiver<String>,
}

impl EventBus {
    fn new() -> Self {
        let (tx, rx) = mpsc::channel();
        EventBus { sender: tx, receiver: rx }
    }
    
    fn publish(&self, event: String) {
        self.sender.send(event).unwrap();
    }
    
    fn subscribe(&self) -> mpsc::Receiver<String> {
        self.receiver.clone()
    }
}
```

## Language-Specific Idioms

### Python: Protocol Classes (Structural Typing)

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def draw(self) -> str:
        return "Circle"
    
def render(shape: Drawable):
    print(shape.draw())

render(Circle())  # Works — structural subtyping
```

### Rust: Pattern Matching (Visitor Alternative)

```rust
enum Expr {
    Number(i32),
    Add(Box<Expr>, Box<Expr>),
    Mul(Box<Expr>, Box<Expr>),
}

fn evaluate(expr: &Expr) -> i32 {
    match expr {
        Expr::Number(n) => *n,
        Expr::Add(l, r) => evaluate(l) + evaluate(r),
        Expr::Mul(l, r) => evaluate(l) * evaluate(r),
    }
}
```

### TypeScript: Discriminated Unions

```typescript
type Shape = 
    | { kind: 'circle'; radius: number }
    | { kind: 'rectangle'; width: number; height: number }
    | { kind: 'triangle'; base: number; height: number };

function area(shape: Shape): number {
    switch (shape.kind) {
        case 'circle': return Math.PI * shape.radius ** 2;
        case 'rectangle': return shape.width * shape.height;
        case 'triangle': return 0.5 * shape.base * shape.height;
    }
}
```

## Common Pitfalls

1. **Pattern overuse** — patterns aren't goals; use them to solve specific problems, not because they're "correct"
2. **Rust ownership with patterns** — Observer pattern fights Rust's ownership model; use channels
3. **Python duck typing vs. patterns** — many patterns are simpler with duck typing; don't Java-ify Python
4. **TypeScript class overhead** — prefer functions and interfaces over classes for simple patterns
5. **Pattern translation ≠ pattern matching** — a pattern in one language may be anti-pattern in another
6. **Premature abstraction** — adding Strategy pattern for a single algorithm is over-engineering

## Verification Checklist

- [ ] Pattern solves the actual problem (not applied hypothetically)
- [ ] Implementation uses language-native idioms, not transliterated Java/C++
- [ ] No unnecessary object/class overhead where functions suffice
- [ ] Pattern is testable in isolation
- [ ] Pattern doesn't fight language's type system or ownership model
- [ ] Team is familiar with the pattern in the target language

## See Also

- software-design-patterns — detailed GoF pattern reference
- api-design-rest-graphql — API-level architecture patterns
- functional-programming-concepts — FP alternatives to OOP patterns
- rust-programming-patterns — Rust-specific patterns
