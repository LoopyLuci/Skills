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

## Clippy Warning Fix Patterns (Deep Audit Lessons)

### Workspace Dependency Resolution
When a workspace member depends on another workspace member via `workspace = true` in its Cargo.toml, the root Cargo.toml MUST have that dependency listed under `[workspace.dependencies]` with an explicit `path = "..."`. Without the path, `cargo check` fails with:
```
dependency (browzeit-core) specified without providing a local path, Git repository, version, or workspace dependency to use
```
The fix is to add `path = "crates/<crate-name>"` for each internal dependency in the root workspace.dependencies section.

### Systematic Clippy Warning Reduction
1. **Auto-fixable warnings**: Run `cargo clippy --fix --lib -p <crate> --allow-no-vcs --` for each crate
2. **Non-auto-fixable warnings**: Use a Python script with targeted `str.replace()` for patterns:
   - `dead_code` — add `#[allow(dead_code)]` at struct/enum/function level
   - `unused_variables` / `unused_mut` — prefix with `_` or remove `mut`
   - `too_many_arguments` — add `#[allow(clippy::too_many_arguments)]` on the function
   - `unnecessary_operation` — add `#[allow(clippy::unnecessary_operation)]` on the expression
   - `if_same_then_else` — collapse redundant if/else branches or add allow attribute
   - `let_unit_value` — remove unnecessary `let` bindings to unit
   - `manual_let_else` — use `let else` pattern where applicable
   - `unused_imports` — remove the import
   - `needless_return` / `unneeded_return` — remove explicit `return` at end of block
   - `push_str` for single char — use `push(c)` instead
   - `static_mut_refs` — add `#[allow(static_mut_refs)]` on the unsafe block
3. **Add `Default` derive/implementation** for types that need it (e.g., `BrowserWindow`, `ModelPicker`, `ContainerComponent`, `DriverAgentOrchestrator`, `CustodeAgent`)
4. **Always re-run** `cargo clippy --workspace --all-targets` after fixes to verify reduction

### Python Script Approach for Systematic Fixes
When many files need similar clippy fixes, write a Python script that:
- Reads each target file
- Applies targeted string replacements for known warning patterns
- Writes the file back
This is faster and more reliable than manual patching for repetitive changes.

### CRLF Line Endings
The Browzeit repo uses CRLF line endings. Always run `sed -i 's/\r$//' <file>` before using the `patch` tool, or use `write_file` which handles line endings correctly. The patch tool silently fails on CRLF files.

### Clippy Warning Categories Encountered and Fixed
- `dead_code` — unused structs, enums, fields, methods, functions → add `#[allow(dead_code)]` or prefix with `_`
- `unused_variables` / `unused_mut` — prefix with `_` or remove `mut`
- `too_many_arguments` — add `#[allow(clippy::too_many_arguments)]` on the function
- `unnecessary_operation` — add `#[allow(clippy::unnecessary_operation)]` on the expression
- `if_same_then_else` — collapse redundant if/else branches or add allow attribute
- `let_unit_value` — remove unnecessary `let` bindings to unit
- `manual_let_else` — use `let else` pattern where applicable
- `unused_imports` — remove the import
- `needless_return` / `unneeded_return` — remove explicit `return` at end of block
- `push_str` for single char — use `push(c)` instead
- `static_mut_refs` — add `#[allow(static_mut_refs)]` on the unsafe block
