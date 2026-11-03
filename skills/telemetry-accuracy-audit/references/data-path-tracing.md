## Data-Path Tracing Recipe

Use when verifying that a sensor/telemetry value reaches a UI consumer correctly.
Follow ONE value end-to-end and assert both its data and its shaping at each hop.

1. **Read the source.** Call the provider directly (or run the headless driver that
   exercises it) and record the raw `SensorReading`/`Fan` object fields.
2. **Find the serialization.** Identify the `to_dict()` / `serialize_*` / route
   response envelope. Note every field it emits and every field it drops.
3. **Find the delivery point.** Event bus emit → websocket message type → HTTP
   response body → Tauri IPC call. Record the channel and the shape.
4. **Follow the consumer.** Find the single UI line that renders that field.
   Confirm it reads the field the API emitted (not a different field name).
5. **Assert real behavior.** Run the driver / TestClient / live process and print
   the actual rendered value. Compare against the source, not against the code's
   expectation. A value sitting in the UI is the only proof of the whole path.

### Common drift points
- A model field dropped by `to_dict()` never reaches the UI.
- A websocket message shape (`sensor.update` vs `sensors.readings`) mismatched
  with the handler that decodes it.
- A Tauri IPC command that writes a setting but the UI reads a different key.
- A closure capturing a loop variable by reference (all handlers see the last
  iteration's value).
