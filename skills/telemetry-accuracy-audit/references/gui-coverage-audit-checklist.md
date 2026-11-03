## GUI Feature / Settings Coverage Audit Checklist

Use when verifying that a desktop GUI exposes every declared feature and setting.
Classify each declared surface into one of three states:

- **Live** — written by the app and read by the UI / runtime.
- **Read-only** — written by the app, rendered by the UI, but changing the UI
  control has no effect on the running system.
- **Inert** — nothing reads it at runtime (dead control, stale settings).

### Checklist

1. **Sensor surface.** Every declared sensor ID/type must be discoverable AND
   represented in the UI by at least one live control (table, gauge, chart,
   trend). Note which sensors have no UI representation.
2. **Fan surface.** Every `Fan` field (mode, speed, RPM, min/max speed,
   PWM/RPM input, voltage, current) must be readable AND editable by the UI.
   Check min/max and bound fields against the model, not the UI.
3. **Curve surface.** Every `FanCurve` field (points, interpolation, source
   sensor, fan IDs, min/max temp/speed, enabled) must be settable by the user.
   Verify each bound field is actually wired in the editor.
4. **Settings surface.** Every config key (polling intervals, safety bounds,
   server/MCP toggles, server port) must be editable by the user AND take effect
   on the running workers — not just written to the config file. Read the live
   config inside the worker loop at runtime; confirm the workers honor a changed
   value.
5. **Profiles.** Every profile operation (save/load/import/export) must have a
   live consumer in the UI.
6. **Diagnostics.** Telemetry/event history must be readable and exported
   through the UI.
7. **Coverage gate.** For every declared field, confirm a UI control exists
   that reads it. For every UI control, confirm a runtime read that honours it.
   If a control writes a value the runtime never reads, it is inert — wire a
   consumer, do not exempt it.

### Enumeration gotchas
- A UI toggle is both a writer and a reader: check whether the UI reads the
  setting to render its state before concluding it has no consumer.
- `grep` for a setting name near a `.set(` is not evidence it is written —
  trace the actual call sites.
- A settings panel that disables its controls (e.g. "backend settings API
  unavailable in desktop mode") makes every control there inert — which is a
  real gap to record, not a false positive to ignore.
