# CLI command exposure recipe

A Rust CLI that exposes every feature and setting to a terminal uses a `config`-style command family.

## Steps

1. Read the settings schema (`settings_schema`) — the single source of truth for every setting, its category, type, default and locked flag.
2. Write one function per subcommand, e.g. `cmd_config_show(args, project)`.
3. Add `split_project(args)` to parse `--project DIR` before dispatch.
4. Wire the dispatch: `"config" => cmd_config(rest)`, and inside `cmd_config` match the subcommand key to the command functions.
5. Update `usage()` so every command appears in `nlp-cli help`.
6. Add tests: one per command, plus a regression test that the schema lists every setting.

## Verify before behaviour testing

- `cargo check --workspace` (EXIT=0, no warnings)
- `cargo clippy --all-targets -- -D warnings` (0 errors, 0 warnings) — includes the CLI family
- `cargo test -p nlpcli-core -p nlpcli-service -p nlp-cli` (all pass)

Record per-crate test counts (core 106, service 39, cli 10 in this project) — aggregate only.

## Pitfalls

- `config::BTreeMap` / `config::BTreeSet` are private inside config.rs. Use `std::collections::BTreeMap` / `BTreeSet` in CLI code.
- `serde_json` was not imported at all in the initially-committed CLI. Add `use serde_json::{self, Value, Map};` before using `serde_json::...` paths.
- A moved value (e.g. `value` after `Value::String(value)`) must be cloned.
- Prefix an unused parameter with `_` to silence the unused-variable warning (`let _spec`).