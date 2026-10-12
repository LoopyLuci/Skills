# Render-loop performance in a hand-rolled desktop app

For a loop that draws its own window on a frame budget and is missing it. The
recurring shape: the average FPS looks acceptable, the app still feels sluggish,
and nothing points at a cause.

## 1. Measure with percentiles, never an average

An average cannot show stutter, and stutter is what a user notices. A run can
average 60fps and still hitch every few seconds.

Keep a bounded ring buffer of frame times (600 samples is ~10s at 60fps) and
report the distribution:

- **Nearest-rank percentiles** p50 / p95 / p99, plus mean.
- **`worst` must not be evicted with the window.** A single 250ms hitch is the
  thing a user complains about, so it has to survive the sample aging out of the
  ring. Keep it as a separate running maximum.
- **Ignore non-finite and negative samples.** One `NaN` poisons every percentile
  computed from the window.
- **Return `0`, not `NaN`, for an empty window** so the summary serialises
  cleanly for a caller that polls before any frames have run.
- `fps = 1000 / ms`, guarding `ms <= 0`.

Assert the percentile arithmetic directly with a known sequence (`1..=100` gives
p50=50, p95=95, p99=99) rather than through the live loop.

## 2. Expose it as its own command

Give the metrics their own control-surface command instead of widening the main
status snapshot. A profiling loop wants only these numbers, and the full
snapshot is large enough that cloning it is itself a cost worth avoiding.

Return the derived FPS values alongside the millisecond percentiles so a caller
is not left redoing the arithmetic.

## 3. The per-frame clone audit — do this before anything clever

Grep the frame loop for `.to_vec()`, `.clone()`, `.snapshot()`, `.list()`,
`.messages()`. The standard bug is cloning the whole world every frame merely to
decide whether anything changed:

- the AI/chat transcript cloned **twice** per frame to compare against a copy
- the session list and current transcript cloned per frame to re-render a view
- a status snapshot cloned per frame — transcript, entity map and every setting
  — for a poller that reads a few times a second

Each is invisible in a unit test and dominates the frame budget. Three fixes:

**A. Cheap change signature.** Keep the last length or version and clone only on
change.

```rust
let len = bridge.overlay().lock().map(|o| o.messages().len()).unwrap_or(0);
if len != last_overlay_len {
    let messages = bridge.overlay().lock().unwrap().messages().to_vec();
    // ... sync ...
    last_overlay_len = len;
}
```

**B. Throttle the publisher.** A snapshot whose only consumer polls is
indistinguishable at 4Hz from per-frame. Gate on elapsed time.

```rust
if last_publish.elapsed() >= Duration::from_millis(250) {
    publish_status(...);
    last_publish = Instant::now();
}
```

**C. Re-read a store only when it changed.** A tuple of cheap counts is enough:

```rust
let sig = (store.list().len(), store.current_id().len(),
           store.current().map(|s| s.messages.len()).unwrap_or(0));
if sig != last_sig { view.refresh_from(&store); last_sig = sig; }
```

Report the before and after numbers, not just "optimised".

## 4. Verify, and be honest about what is left

Poll the metrics command before and after a change and compare p50/p95/p99.

A fix that removes a real regression may still leave the loop above its target —
say so, with the number, rather than implying it now hits the target. `p50
40.5ms -> 30.5ms against a 13ms target` is a true and useful statement; "fixed"
is not.

## Pitfall: the sleep granularity floor

`std::thread::sleep` on Windows has ~15ms granularity, so any target below that
is unreachable by sleeping alone. Sleep for `target_ms - 2`, then busy-wait with
`std::hint::spin_loop()` until the target elapses. If the measured p50 sits near
a multiple of ~15.6ms, the pacing is sleep-bound rather than work-bound — check
that before optimising code.
