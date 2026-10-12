# The local control API of a desktop app

For the socket/queue surface a desktop app exposes to scripts, agents and other
processes. The recurring failures are all about *compatibility* and *resource
bounds*, not about the command handlers themselves.

## Additive wire changes must not change the shape clients already see

A client that does not send the new field must receive byte-identical output to
before, or every existing client breaks on a cosmetic release.

Add an optional field to the **serialised object**, not to every variant of the
response enum:

```rust
let bytes = match request_id {
    Some(id) => match serde_json::to_value(value) {
        Ok(serde_json::Value::Object(mut map)) => {
            map.insert("id".into(), serde_json::Value::from(id));
            serde_json::to_vec(&serde_json::Value::Object(map)).unwrap_or_else(|_| fallback())
        }
        _ => serde_json::to_vec(value).unwrap_or_else(|_| fallback()),
    },
    None => serde_json::to_vec(value).unwrap_or_else(|_| fallback()),
};
```

Pin the compatibility with a test asserting the **exact** serialised string for
the no-field case (`{"status":"pong"}`), not merely that it parses.

## Correlation ids

A client that pipelines commands cannot match replies to requests without one.
Echo an optional id when the request carried one.

A missing, non-numeric or malformed id must be `None`, **never a parse error**:
an unknown field must not turn a valid command into a failure.

```rust
fn request_id_of(payload: &[u8]) -> Option<u64> {
    serde_json::from_slice::<serde_json::Value>(payload).ok()?.get("id")?.as_u64()
}
```

## Bound the connection count

An accept loop that spawns a task per connection with no cap can be driven to
exhaust file descriptors by anything that can reach the port.

- One semaphore permit per in-flight client, **held for the connection
  lifetime**, not just the handshake — otherwise the cap covers only the part of
  the connection that costs least.
- Acquire with `try_acquire_owned` so the accept loop never blocks on the cap.
- Refuse past the cap by **closing the stream without writing**: a response
  costs the very resource the cap protects.

## Deferred persistence for a store written from the loop

A store serialised and written on every mutation is O(n) per change.

- **Keep the immediate write as the default** and let the loop opt in, so
  existing callers and tests are unchanged.
- **Turning the mode off must flush anything pending**, or a mode switch silently
  drops the last change.
- **Write to a sibling file then rename.** A whole-store write interrupted
  mid-way leaves a truncated file and loses everything.
- Flush once on clean shutdown.
- Benchmark the worst case the caps allow before restructuring; the test doubles
  as the regression guard. Assert a generous bound so it cannot flake.

## Observability: install the subscriber

A crate full of `tracing::info!` calls with no `tracing_subscriber` init discards
every line, and a user reporting a problem has nothing to send.

- Install a subscriber at startup writing to **both** the console and a log file
  under the app data directory. The file is what a support request needs.
- **A bad level must fall back to `info`, never `off`.** Falling back to off
  silently discards the log the request needs.
- `EnvFilter` lives behind the `env-filter` feature on `tracing-subscriber`.
- A file writer can be a small `MakeWriter` over an `Arc<Mutex<File>>`; a rolling
  appender is unnecessary for one process writing one file per run.

## Verify over the real socket

A unit test that calls the handler directly proves the handler, not the framing,
the correlation echo or the cap. Send the command over a real TCP connection,
read the length-prefixed reply, and assert on the field.

For the connection cap specifically: hold the permits with real connections,
then assert the next client is refused (the read returns 0 bytes or resets)
rather than answered.
