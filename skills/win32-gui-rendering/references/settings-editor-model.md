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

## Audit that the surface is consumed, before claiming it works

A config screen that saves is not a feature. The most expensive defect in this
area is a surface that looks complete, persists correctly, and is read by
nothing — every value inert, every control a no-op. Before reporting such work
done, prove the consumer exists:

```bash
# For each setting/profile field, is it ever READ?
for f in volume_master fps_target rag_enabled; do
  echo "$f: $(grep -rn "\"$f\"" --text crates/app/src/ | grep -v settings_window | wc -l)"
done
```

A field with zero readers outside its own definition and the window that edits
it is dead, however well it renders. The same check applies to a profile type:
grep for the accessor that turns it into runtime config (`to_agent_config`,
`composed_system_prompt`). If nothing calls it, the model is a data dump.

Two shapes this audit finds, both worth checking by name:

- **The runtime holds config by value, fixed at construction.** A runtime built
  as `new(ai)` with `config: AgentConfig::default()` can never be influenced by
  a profile. Make it swappable and prove it.
- **The window owns a duplicate of the type it edits.** A settings window with
  its own `SettingValue` enum and its own `HashMap`, never connected to the real
  store, passes its own tests and displays nothing. A window must hold a
  *reference* to the live store (see below), never a copy of the data.

## Config a runtime holds must be swappable, and observable

Put the config behind `Arc<RwLock<_>>`, expose `apply_profile()` / `set_config()`
plus an `active_config()` readback, and snapshot it **once per request**. One
snapshot per run matters twice: a profile applied mid-request cannot then change
the iteration budget halfway through, and no read guard is ever held across an
`.await`.

Expose the live settings through the app's status/query surface, so "the profile
took effect" is checkable rather than assumed:

```rust
snapshot.active_agent = agent.active_agent();
snapshot.active_agent_settings = serde_json::to_value(agent.active_config())?;
```

Then verify by round trip, not by inspection: save a profile with a distinctive
marker, activate it, read it back from the live surface, and confirm the marker
is in the **prompt the model receives**. Confirm persistence separately by
quitting, relaunching, and checking the app logs that it restored the choice —
an in-memory activation that is lost on restart makes the feature pointless.

Prefer `RwLock::read()` over `Mutex` for config, and keep the apply method
symmetric with the readback so the two cannot drift.

## Selection by capability must include an explicit override

If a runtime picks a model by *tier* (`select_model(tier)`), then a profile
naming a specific model can never be honoured — the field parses, validates,
serialises, and does nothing. Add an explicit override that wins over the
tier-based choice, and make an unresolvable name an **error listing what is
available**, never a silent fallback to a different model: a fallback is
indistinguishable from success until it produces the wrong answer.

## Label what is not wired up, instead of shipping it as working

When some fields genuinely have no consumer, do not render them as if they do.
Keep an explicit list, grey them out, mark them in the UI, and make them
unclickable:

```rust
pub const INERT_SETTINGS: &[&str] = &["ai_provider", "multi_gpu", /* ... */];
pub fn setting_is_live(name: &str) -> bool { !INERT_SETTINGS.contains(&name) }
```

A test must assert the list matches reality **in both directions**: every listed
name is a real setting (no stale entries), and every real setting is classified
consistently. Otherwise the list silently rots into mislabelling a working
control as dead. A refusal path that explains itself ("not wired up yet") also
doubles as the assertion that the guard is reachable.

The same honesty rule applies to overflowing categories: when rows overflow the
window, say "more settings below" rather than silently dropping them.

## Tests must assert the container is populated

A suite that exercises an empty collection passes regardless of whether the code
is correct. Five tests on a window backed by an empty `HashMap` prove only that
assignment works. Before asserting behaviour, assert the shape the behaviour
depends on:

- every tab/category has at least one row (an empty tab is a dead tab)
- the count of clickable controls equals the count of *enabled* rows
- an inert row has no hit target at all

Also give tests a store that cannot touch real user files (`in_memory()` with an
empty path, and skip persisting when the path is empty) — otherwise a test run
rewrites the user's actual configuration.

## Mutating a store must include its persistence

A `reset()` that clears the map but does not `save()` is undone on the next
launch, so the user sees the reset silently revert. Every mutating path —
`set`, `reset`, delete — persists. There is deliberately no save button: the
user will not remember it, and a setting that only lives in memory is
indistinguishable from one that does not work.

On load, accept only keys the current build defines, so a stale or hand-edited
file cannot inject settings the app would then honour, and treat an unparseable
file as "use the defaults" rather than a fatal error.

## A tagged enum with numeric variants needs a shared reader

If one variant holds a number (`Bool(f64)`, where `1.0` means on), every caller
that wants "the magnitude" ends up repeating a match. Add one accessor
(`number()`) that unwraps all numeric variants, and use it everywhere; a tagged
enum plus a `Default` impl in the same module is a common source of `Result`
vs `Option` mismatches worth checking once.

## Persist beside, not over, existing user data

Give the store its own file next to the session store rather than extending it, so
a corrupt or unknown-format agent file cannot take chat history with it. On load,
re-merge code-defined presets instead of trusting the file: a profile written by an
older build still loads, and a newer build's new presets appear.