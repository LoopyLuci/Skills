# Rust Workspace Pitfalls for Browzeit

## Module Path Resolution Across Crates

**Problem**: Sibling crates in the workspace use different crate names than their directory names.

- `crates/types/` → crate name `types` (not `browzeit_types`)
- `crates/core/` → crate name `browzeit_core`
- `crates/engine/` → crate name `browzeit_engine`
- `crates/driver/` → crate name `browzeit_driver`
- `crates/api/` → crate name `browzeit_api`
- `crates/traits/` → crate name `browzeit_traits`

**Fix**: Always use the actual crate name from `Cargo.toml`, not the directory name.

```toml
# In crates/types/Cargo.toml
name = "types"

# In dependent crate:
use types::agent::Task;  # NOT browzeit_types::agent::Task
```

## Public Structs Need Debug/Clone Derives

**Problem**: Structs used across crate boundaries (in public APIs) must implement `Debug` and `Clone` for ergonomic use.

**Fix**: Add `#[derive(Debug, Clone)]` to all public structs in public APIs:

```rust
// In router.rs, verifier.rs, perceptor.rs, registry.rs
#[derive(Debug, Clone)]
pub struct RouterDecision { ... }

#[derive(Debug, Clone)]
pub struct Verdict { ... }

#[derive(Debug, Clone, PartialEq)]
pub struct Observation { ... }

#[derive(Debug, Clone)]
pub struct CustodeToolRegistry { ... }
```

## Missing Imports from Sibling Crates

**Problem**: Types from sibling crates must be explicitly imported.

- `Observation` from `crate::perceptor` needed in `verifier.rs`
- `RouterDecision` from `crate::router` needed in `agent.rs`
- `HashSet` from `std::collections` needed wherever used

**Fix**: Add explicit `use` statements at top of file:

```rust
use crate::perceptor::Observation;
use crate::router::{RuleRouter, RouterRequest, RouterResponse, RouterDecision};
use std::collections::HashSet;
```

## Duplicate Derive Attributes

**Problem**: Accidentally adding duplicate `#[derive(...)]` attributes.

```rust
// BAD
#[derive(Debug, Clone, PartialEq)]
#[derive(Debug, Clone)]
pub struct Observation { ... }

// GOOD
#[derive(Debug, Clone, PartialEq)]
pub struct Observation { ... }
```

## Prefilter API Signature

**Problem**: The `CustodeToolRegistry::prefilter` method takes two `HashSet<&str>` parameters (capabilities, member_permissions).

```rust
fn prefilter(&self, capabilities: &HashSet<&str>, member_permissions: &HashSet<&str>) -> Vec<ToolSpec>
```

**Fix**: Call with proper HashSet construction:

```rust
use std::collections::HashSet;

let prefiltered = registry.prefilter(
    &["read"].into_iter().map(|s| s as &str).collect::<HashSet<_>>(),
    &HashSet::new()  // empty member_permissions
);
```

## Crate-Specific: custode-browzeit

The `custode-browzeit` crate implements the Custode agent for Browzeit. It depends on:
- `browzeit_traits` (trait contracts)
- `types` (DOM, render tree, agent types)
- `regex` (for tool name validation)
- `serde`, `serde_json` (for ToolSpec serialization)

**Key files**:
- `src/agent.rs` — Main agent loop implementing `browzeit_traits::Agent`
- `src/router.rs` — Rule-based router (interim until learned router)
- `src/perceptor.rs` — Observation extraction from DOM
- `src/verifier.rs` — Rule-based verification (no model weights)
- `src/registry.rs` — Tool registry with Custode ToolSpec
- `src/bridge.rs` — JSON-RPC bridge client (stubbed)
- `src/lib.rs` — Public exports

**Verification**: `cargo check -p custode-browzeit` must pass with 0 errors.
