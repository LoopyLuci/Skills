# Settings editors: the data model behind the window

The window is the easy half. These notes cover the profile/settings model a GUI
editor needs *before* any pixel is drawn, because the defects here are silent —
the editor renders fine while the data it saves is wrong.

## Ship the model, its persistence and its presets before the UI

An editor is unbuildable in pieces: the window needs a type to edit, a store to
persist to, and a default set of profiles to populate a fresh install. Building
the model first also surfaces the questions the UI must answer (what happens when
a referenced character is deleted?) while they are still cheap to answer.

## Make the catalogue shared, not duplicated

Anything the picker offers must live in the same module the runtime reads, or the
two drift and the GUI offers options that cannot be displayed. Moving a hardcoded
`Vec` of tuples out of `main.rs` into a `catalogue()` function in the core crate
costs one refactor and buys a single source of truth for names, defaults and
descriptions.

## Serialization is a public contract

Two spellings for one value means data written by one path cannot be read by
another. Verify with a test that asserts the serialized form equals the string
your `as_str()`/`from_str()` pair uses:

```rust
for provider in Provider::ALL {
    let json = serde_json::to_value(provider).unwrap();
    assert_eq!(json, serde_json::Value::String(provider.as_str().into()));
    assert_eq!(serde_json::from_value::<Provider>(json).unwrap(), provider);
}
```

`#[serde(rename_all = "snake_case")]` derives names mechanically and will
disagree with a hand-written parser for any acronym or underscore-bearing variant
(`OpenAi` → `"open_ai"`, not `"openai"`). Spell each variant's rename out
explicitly, or keep the derive and derive your parser from it — never both by hand.

## Accept partial input

A settings payload from an agent, an IPC client or a hand-edited file will omit
fields. `#[serde(default)]` on the struct plus per-variant `#[serde(rename)]` makes
`{"id": "x", "name": "X", "persona": "wry"}` valid and fills the rest. Without it,
the natural minimal payload is rejected outright and the failure surfaces as a
confusing parse error rather than "you left out provider".

`#[default]` on an enum variant requires `Default` in the `derive` list; a
hand-written `impl Default` is what clippy then flags as derivable.

## Clamp on the way in, not on the way out

Validate at the store boundary (`sanitised()`), so every write path — GUI, IPC,
MCP — is covered once. Clamp iterations, timeouts and temperature into a usable
range and path-sanitise any id used as a filename or lookup key. A hostile or
merely careless payload then cannot produce a profile that hangs or never answers.

## Derive intent; never infer it from a value

Deciding "did the user choose this?" by comparing against a default breaks as soon
as two options share that default — the editor can no longer distinguish a
deliberate choice from a default and starts overriding the user. Track the intent
explicitly:

```rust
// Set true when the user picks movement directly; cleared when a preset or
// character supplies it.
movement_is_ours: bool,
```

## Sort explicitly when the ordering is a product decision

`sort_by(|a, b| a.builtin.cmp(&b.builtin))` puts user rows *first*, because
`false < true`. When built-ins must lead, sort descending on the flag. Assert the
ordering in a test — the compiler has no opinion and neither does the author at
the time.

## Presets are code, and read-only in the UI

Define built-ins as code rather than seed data so a fresh install has them and they
cannot be lost. Mark them, refuse their deletion in the store, and have the UI
offer "Duplicate" (with a collision-free id) instead of in-place edit. Removing the
last agent must be impossible.

## Persist beside, not over, existing user data

Give the store its own file next to the session store rather than extending it, so
a corrupt or unknown-format agent file cannot take chat history with it. On load,
re-merge code-defined presets instead of trusting the file: a profile written by an
older build still loads, and a newer build's new presets appear.