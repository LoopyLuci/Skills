---
name: win32-gui-rendering
description: Build and verify hand-rolled Win32/GDI desktop UIs in Rust.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [windows, win32, gdi, rust, gui, rendering]
    related_skills: [windows-rust-android-build-env]
---

# Win32 GDI GUI in Rust

For desktop UIs built directly on GDI with no winit/egui/Tauri: laying out a
window, drawing text, and **proving it rendered**. The recurring failure is
silent — everything looks fine until you look at the pixels.

## When to Use

- Writing or debugging a window that draws itself via GDI in Rust
- Text renders nowhere, or only some labels appear
- A window renders pure white, or white boxes over the text
- A window's controls land off-screen or float in the wrong place
- A form's labels are missing even though the fields draw
- A window screenshots as solid black and you cannot tell whether it is broken
- Sibling windows share a title and you keep capturing the wrong one
- GUI unit tests hang, or pass against code you know is wrong
- A tray icon, context menu, or minimise-to-tray that compiles and reports
  success but does nothing when clicked
- Building a settings/agent/profile editor: what to model first, and the
  serialization rules that keep saved data readable (see
  [references/settings-editor-model.md](references/settings-editor-model.md))
- Deciding which settings to show, disable or label as unimplemented — the
  live / read-only-mirror / inert classification and the CI scan that keeps it
  honest (same reference)
- A list of "things not wired up yet" that you suspect is wrong
- Auditing whether a declared surface is consumed at all — settings keys, MCP
  tools, IPC commands — and turning the result into a CI gate
  (see [references/inert-surface-audits.md](references/inert-surface-audits.md))
- The UI stutters, or the loop misses its frame target and the average FPS hides
  it (see [references/render-loop-performance.md](references/render-loop-performance.md))
- Adding a command to the app's control surface, or a client needs to match
  replies to requests (see [references/local-control-api.md](references/local-control-api.md))

## Always-on rules

- **A window that renders but ignores every click and keystroke has no
  message pump.** A window proc is only ever invoked by the dispatcher, so if
  the main loop never calls `PeekMessage`/`DispatchMessage` (or `GetMessage`),
  the window receives no `WM_PAINT`, no `WM_KEYDOWN`/`WM_CHAR`, no
  `WM_LBUTTONDOWN` and no `WM_MOUSEWHEEL` — every control is dead no matter how
  correctly it is written. Grep the render loop for `PeekMessage`/`DispatchMessage`
  before diagnosing input handling: an app can have a working pump on one
  thread (an overlay) and none on the thread that owns the main window, which
  is what makes the window look alive while ignoring everything. Fix:
  `PeekMessageW(&mut msg, null_mut(), 0, 0, PM_REMOVE)` in a `while` loop at the
  top of the frame loop, `TranslateMessage` + `DispatchMessageW` each, and break
  on `WM_QUIT`. The tell-tale symptom in a probe: a colour count far too low for
  the layout (e.g. 23 where a full UI needs 150+).
- **`PrintWindow` flag 1 hangs when the window thread does not pump.**
  `PW_CLIENTONLY` (1) sends `WM_PRINTCLIENT` to the app thread, so it blocks
  forever on a window whose thread is not pumping; `PW_RENDERFULLCONTENT` (2)
  reads the DWM redirection surface instead, which returns *stale* content rather
  than hanging. A probe that captures successfully with flag 2 but hangs with
  flag 1 is evidence of a missing pump, not a probe bug. Use flag 1 once the pump
  exists — it also gives client-area coordinates directly.
- **Capture the CLIENT area, or every measured band is shifted by the frame.**
  `GetWindowRect` includes the title bar and border, so a band at y=60 in client
  coordinates lands on the title bar in a whole-window capture. Use
  `GetClientRect` for dimensions with `PrintWindow(hwnd, dc, 1)`, and measure
  bands from the client origin (0, 0).
- **`GetKeyState` misses injected, posted and `SendMessage`d input.** It reports
  only the *physical* key state of the calling thread, so a probe (or an
  automation tool) that posts Ctrl then F sees `GetKeyState(VK_CONTROL) >= 0` and
  the shortcut never fires — while real typing works, which makes it look like a
  probe-only problem. Track modifiers from the message stream instead:
  set a `ctrl_down`/`shift_down` flag on `WM_KEYDOWN` of the modifier and clear
  it on `WM_KEYUP`, then read the flag. This also makes the shortcut unit-testable
  without a window.
- **A before/after pixel diff beats an ink-vs-modal band when the change is
  low-contrast.** A search bar whose fill matches the surrounding background
  barely moves an ink count, so a band metric reports "no change" for a feature
  that plainly rendered. Capture before and after and count differing pixels
  directly (>200 is unambiguous); assert the reverse action restores the view
  (diff returns to ~0).
- **`CreateWindowExW` takes the OUTER size; layout constants are usually the
  CLIENT size.** Passing `WIN_WIDTH`/`WIN_HEIGHT` straight to `CreateWindowExW`
  when the layout is written against those constants leaves the client smaller by
  the frame (title bar + borders), so the bottom strip — typically the message
  input — lands below the visible edge and looks missing. Compute the outer size
  with `AdjustWindowRectEx(&mut RECT{right: WIN_WIDTH, bottom: WIN_HEIGHT},
  WS_OVERLAPPEDWINDOW, 0, 0)` and pass those dimensions. Tell-tale sign in a
  capture: the client area is smaller than the layout constants (e.g. 884x600
  where the code says 900x640).
- **Do not use Escape to reset a probe's state.** If the app maps Escape to
  "close search, else hide the window", a probe that sends Escape first hides the
  window, captures nothing, and reports a render failure that is really a
  harness bug. Assert an idempotent pair instead: toggle twice and check that
  each transition moves pixels and the third capture matches the first.
- **Measure a suspected hot path before restructuring it.** An audit note that
  "the store saves on every message" is a hypothesis, not a finding. Time the
  worst case the caps allow (the test doubles as the regression guard) and let
  the number decide: here the write was 8.8ms against a 16.7ms frame budget, so
  it was worth batching, but a 0.3ms write would have been left alone. Assert a
  generous bound rather than an exact time so the test does not flake.
- **A snapshot derived by assignment clobbers keys another writer inserted.**
  Publishing a store into a shared read-back map with `snapshot = store.clone()`
  wipes every key a *different* writer put there — control handlers, caches,
  computed fields. The other writer's work silently disappears on the next
  publish, and a correct change reads back as missing. Merge per key
  (`for (k, v) in store.snapshot() { map.insert(k, ...) }`) so store values
  refresh while foreign keys survive. This is distinct from staleness: the
  data was there and the publish deleted it.
- **Do not recreate GDI objects per frame.** A DIBSection, bitmap or brush that is
  deleted and recreated on every present is a full allocation plus a
  whole-buffer copy each frame for an object that almost never changes. Create
  once, keep the DC's original bitmap, and reallocate only when the size
  actually changes. A bitmap selected into a DC must not be freed — restore the
  DC's original bitmap with `SelectObject` before `DeleteObject`, or GDI leaks
  and eventually fails.
- **Sharing a store behind `Arc<Mutex<>>` when a consumer holds a raw pointer
  is safe only if the allocation never moves.** A `*mut SettingsUI` stored in a
  window struct is a borrowed pointer into the store; wrapping the store in
  `Arc<Mutex<>>` for cross-thread sharing keeps the heap allocation stable for
  the Arc's lifetime, so the raw pointer stays valid. Moving the store (e.g. into
  a `Vec` that reallocates, or returning it by value from a function) invalidates
  every raw pointer into it. This is the standard pattern for a Win32 GDI app
  where the render loop owns state and a window holds a borrowed pointer to it.
- **A custom-drawn window has no OS tooltip, so each hit target needs one.** A hand-rolled GDI window cannot fall back on the OS tooltip: a button whose meaning is not obvious from its label is a dead end. Add a `tooltip: String` field to the hit target and fill it from the action in a constructor (`HitTarget::new(rect, action)`), so a new control cannot ship without one — the compiler enforces it. Store the tooltip text lookup (`fn tooltip_for(&UiAction) -> String`) next to the action enum so all strings are in one place. In the paint loop, read the hovered index and draw a small box near the cursor. The tooltip is drawn from `win.draw_dc` (the off-screen DC published for the frame), not from a local `dc` — `draw_ui` does not receive the DC directly.
- **A modal file dialog blocks forever in a test.** `GetSaveFileNameW` and
  `GetOpenFileNameW` are modal and wait for user input; calling them from a unit
  test hangs the suite indefinitely. Make the path prompt injectable: add a
  `path_prompt: Option<fn(bool) -> Option<String>>` field to the view, default
  to `None` (use the real dialog), and let tests supply a closure that returns
  a fixed path. The same applies to any blocking OS dialog (colour picker,
  folder browser, print dialog).
- **Batch a whole-store write; do not do it per change.** A store that
  serialises and writes everything on each mutation is O(n) per message. Mark it
  dirty and flush at most once a second from the loop, plus once on shutdown.
  Keep the immediate path as the default so existing tests and callers are
  unchanged, and make turning the mode off flush anything pending so a switch
  cannot drop a change. Write to a sibling file and rename, or a crash mid-write
  leaves a truncated store and loses everything.
- **A theme is not wired until something reads the setting.** A
  `set_theme()` that exists and is never called leaves the window permanently on
  the default, and the setting screen still shows the control working. Grep for
  the setter's call site: if the only hit is its definition, the feature is
  inert. Wire it by reading the setting each frame and applying on change, and
  apply the saved value before the first frame so a restart honours it.
- **Hardcoded colour constants defeat a theme.** Replacing them in the panels
  but not the message bubbles, sidebar and input leaves a theme switch that
  changes most of the window, which reads as a bug. Grep the draw code for the
  old constants after introducing a theme; the fill helpers taking a stride
  makes this easy to miss because the call sites changed shape at the same time.
- **`WM_LBUTTONDBLCLK` never arrives without `CS_DBLCLKS` on the window class.**
  Registering with only `CS_HREDRAW | CS_VREDRAW` means Windows never
  synthesises the double-click message, so a double-click feature silently does
  nothing however correct its handler is. Add `CS_DBLCLKS` to `WNDCLASSEXW.style`
  whenever a control responds to a double-click.
- **Escape is a shared key: a mode must consume it before the window does.** If
  Escape both leaves an edit mode and hides the window, pressing it while editing
  must cancel the edit and return, not fall through to hide — otherwise a user
  correcting a typo loses the window. Give the active mode the first look at the
  key and delegate only when no mode is active.
- **A keyboard-only user needs focus regions, not just a text box.** Tab between
  the panes, arrows within a list, Enter activates whatever holds focus — so
  Enter's meaning must be region-dependent (send in the input, open in the
  sidebar), and text entry must be gated on the focused region or keystrokes
  silently edit a draft the user is not looking at. Draw a focus indicator: a
  keyboard user cannot otherwise tell what Enter would activate.
- **An undo stack must be written by the reversal, not by the recording setter.**
  Calling the normal setter from `undo()` records the undo itself as a new change,
  so the history grows on every reversal and redo becomes unreachable. Write the
  value directly in `undo`/`redo` and move the entry between the two stacks. A
  bulk reset must clear the history rather than leave a stack that no longer
  describes the state.
- **A snapshot mirrored only on write goes stale the moment anything changes the
  store by another path.** Publishing state into a shared read-back struct inside
  the writer leaves every other mutator — undo, a loader, a reset — reporting the
  old value, so a correct change looks like it did not take. Derive the snapshot
  from the store on a timer instead, and throttle it: cloning it per frame is
  wasted work when the only consumer polls.
- **Case-insensitive search must take its offsets from the original text.**
  `to_lowercase()` can change byte length (some characters expand), so an offset
  taken from the lowered string can land mid-character in the original and panic
  on the slice that follows. Match against the original, and snap any snippet
  window to `is_char_boundary` before slicing.
- **The frame loop must not clone the world every frame.** Cloning the whole
  transcript, session list or status snapshot just to ask "is anything new?" is
  the standard way a loop that should hit 75fps lands at 25fps. Grep the loop for
  `.to_vec()` / `.clone()` / `.list()` / `.messages()`; gate each on a cheap
  length or version signature, and throttle any publisher whose only consumer
  polls. Measure before and after rather than assuming — see
  [references/render-loop-performance.md](references/render-loop-performance.md).
- **Additive changes to a wire format must not change the shape existing clients
  see.** Insert the new optional field into the serialised object rather than
  adding it to every variant of the response enum, then pin the no-field case with
  a test asserting the exact serialised bytes. Details, plus the connection cap and
  deferred-persistence patterns a local control surface needs, in
  [references/local-control-api.md](references/local-control-api.md).
- **Text and fills must share one surface.** `DrawTextW`/`TextOutW` write to a GDI
  device context; filling a `Vec<u32>` writes to your buffer. Different surfaces
  means every glyph lands somewhere the app never blits from.
- **`SetBkMode(dc, TRANSPARENT)` before every text draw.** GDI's default fills an
  opaque rectangle behind each string using the current background brush, so a dark
  UI gets a white box painted over every label and field — legible only where the
  box happens to match. It is per-DC state that resets between DCs, so set it in
  the same helper that selects the font, not at each call site.
- **`WM_PAINT` must call `BeginPaint`/`EndPaint`.** Without them the DC is invalid
  and GDI **silently discards every drawing call** — no error, no entry in the
  debug output, just an untouched window. This looks identical to a bug in your
  draw code.
- **Lay out against `GetClientRect`, never a height constant.** The created window
  size includes the frame, so the client area is smaller; adding a guessed frame
  constant (`WIN_HEIGHT + 80`) is worse still, because the guess is wrong on every
  DPI setting and theme. Panels and footers anchored to a constant end up cropped
  or floating mid-window.
- **Paint panels back-to-front, and never draw content at an x a later panel
  covers.** A sidebar painted *after* the body erases any body content drawn at the
  sidebar's x range, which reads as "the labels never rendered" rather than as an
  ordering mistake. Same for a title and a tab strip sharing an origin.
- **Never conclude a window is broken from a black screenshot.** `GetWindowDC` +
  `GetDIBits` returns all-black for a window rendering perfectly. Use
  `PrintWindow(hwnd, mem_dc, 2)`.
- **Identify windows by class, not title.** Sibling windows in one app routinely
  share a title, so title matching screenshots the wrong one.
- **Prove behaviour with assertions, not eyeballs.** Colour count shows *something*
  drew; only looking at it shows the *right* thing drew. Do both.
- **Test UI states that are mutually exclusive separately.** When a render path
  is `if state_a { draw_x() } else if state_b { draw_y() }`, the two controls
  never appear together. A test that sets both states and asserts both tooltips
  fails on the second one. Split into two tests, each setting only the state that
  makes its control appear. The tell-tale failure is `left: None, right:
  Some("...")` for the second assertion — the control was never rendered, not
  rendered without a tooltip.
- **A handler that returns `Ok(())` proves only that it ran.** Every OS
  registration — tray icon, hotkey, hook, clipboard listener — must be checked by
  the OS's own acknowledgement, and `start()` must propagate that rather than
  assuming success. The same applies to any command queued for another thread:
  `{"queued": true}` is the *normal* response for an accepted control request, so
  it distinguishes nothing. Poll for the observable effect it was supposed to
  cause — the value in the snapshot, the row in the list, the line in the log —
  and treat the ack as merely proof the request was received.
  See [System tray](#system-tray-lifecycle).
- **A `break` inside a `match` inside a `for` leaves only the match.** Loops
  driven by event handlers need a flag set in the arm and tested after the loop.
- **A config screen that saves is not a feature.** Before reporting one done,
  grep each field for a reader outside its own definition and the window that
  edits it; zero readers means every control is a no-op however well it renders.
  Check the two usual shapes by name: a runtime whose config is fixed at
  construction (`new()` + `AgentConfig::default()`), and a window holding a
  *copy* of the data instead of a reference to the live store. Details and the
  swappable-runtime recipe in
  [references/settings-editor-model.md](references/settings-editor-model.md).
- **Settings must be loaded before being read.** A `SettingsUI::new()` creates
  an empty settings object; calling `load()` before any read is required to
  populate it from disk. Without this, saved settings are never applied at
  startup — the default value is always used. This is the most common cause of
  "my setting saved but didn't take effect" bugs.
- **Window procs have no `self`.** An `unsafe extern "system" fn` window proc
  cannot use `self`. Get the state pointer from `GetWindowLongPtrW(hwnd,
  GWLP_USERDATA) as *mut YourState`, null-check it, then use `(*ptr).field`
  for every access. Using `self` in a window proc is a compile error (E0424).
  See [references/window-proc-state-access.md](references/window-proc-state-access.md)
  for the full pattern with code examples and common compile errors.
- **Adding a new message handler (WM_MOUSEMOVE, WM_LBUTTONDOWN, etc.) to a
  window proc follows a strict pattern:** get the state pointer from
  `GetWindowLongPtrW`, null-check, use `(*ptr).field` for every access, and
  call `InvalidateRect(hwnd, ptr::null_mut(), 0)` to trigger a repaint.
  Any deviation — using `self`, forgetting the null check, or not calling
  `InvalidateRect` — causes a compile error or a silent no-op. When adding
  a hover state, add a `btn_hover: bool` field to the struct, initialize it
  in `new()`, update it in `WM_MOUSEMOVE`, and change the render color
  based on it.
- **A feature that compiles is not a feature that works.** After adding a new
  field, function, or message handler, grep for its call site in the render
  path. If the only reference is the definition, the feature is inert — it
  exists in the binary but never runs. This is the most common failure mode
  in a large GUI overhaul: the struct gets the field, the proc gets the match
  arm, but nothing calls either. Before reporting a feature done, trace from
  the paint loop to the new code and confirm the path is reachable.
- **The "field exists but render ignores it" gap is the most common.** A field
  is added to the state struct, a setter is written, but the render function
  never reads the field — it still uses hardcoded values. Examples: a
  `search_query` field that `paint_rows()` never filters on, a `typing` bool
  that `render_chat_window()` never checks, a `stats_overlay` string that is
  set but never drawn. Before reporting a feature done, grep the render
  function for the field name and confirm it is actually used in a draw call.
- **Handle `WM_ERASEBKGND` by returning `1`.** Without this, the window
  flickers on resize and repaint. Add `WM_ERASEBKGND => 1` to every window proc's
  match block — it is a one-liner that prevents visible flicker.
- **Hybrid sleep for precise frame pacing.** `std::thread::sleep` on Windows has
  ~15ms granularity. For sub-2ms precision, sleep for `target_ms - 2` ms, then
  busy-wait with `std::hint::spin_loop()` until the target duration elapses.
  **Measure the deadline from the START of the frame, not from after the
  sleep.** Measuring from after the sleep adds the whole target again, so every
  frame costs about twice its budget (a 13ms target produces ~30ms frames).
  Call `timeBeginPeriod(1)` at startup and `timeEndPeriod(1)` at exit so the
  sleep honours the requested duration rather than rounding up to ~15.6ms.
  This is essential for consistent frame timing in a render loop.
- **Register for `TaskbarCreated` to recover from Explorer restarts.** Call
  `RegisterWindowMessageW("TaskbarCreated")` at startup, then handle the
  returned message ID in the tray window proc to re-add the icon via
  `Shell_NotifyIconW(NIM_ADD, ...)`. Without this, the tray icon disappears
  permanently after an Explorer crash or restart.
- **Balloon notifications use `NIM_MODIFY` with `NIF_INFO`.** Call
  `Shell_NotifyIconW(NIM_MODIFY, ...)` with `uFlags = NIF_INFO` and the
  `szInfoTitle`/`szInfo` fields populated. The `NIF_INFO` flag must also be set
  on the initial `NIM_ADD` for balloons to work.
- **Dynamic context menus need `CreatePopupMenu`/`AppendMenuW`/`TrackPopupMenu`.**
  Build the menu each time it is shown based on current state. Use `MF_STRING`
  for items, `MF_SEPARATOR` for dividers, and `MFT_CHECKED` for toggle state.
  `TrackPopupMenu` returns the chosen item ID — assign it to a variable, don't
  discard it.
- **Multiple GUI processes block all input.** When two instances of a Win32 GUI
  app run simultaneously, neither responds to mouse or keyboard — the user sees
  windows but clicks do nothing. Before diagnosing input handling, check
  `tasklist` for duplicate PIDs and kill all but one. This is the first thing to
  verify when the user reports "I cannot interact with any GUI elements"
  despite windows being visible.
- **When three defects in a row share a shape, audit for that shape before
  implementing anything else.** The signal that a surface is inert — renders,
  persists, reports success, and is read by nothing — is easy to miss once and
  impossible to miss twice. On the third occurrence, stop implementing and
  *measure* the whole class (scan every declared item for readers and writers,
  turn the result into a CI gate). Listing your findings as "not wired up yet"
  is a claim about code you have not checked, and it is often wrong: check for
  written-but-never-read settings before calling anything inert.
- **An audit built by parsing source can report PASS while being broken.** A
  clean audit result is only evidence if the audit found what it claims to look
  for, so make the parser prove itself and print the picture it derived. Two
  specific traps: slicing a Rust enum up to the *next* `pub enum` swallows
  everything between them (so the real variants vanish and a neighbouring enum's
  appear instead), and a serde `rename_all = "snake_case"` wire name never string-
  equals the PascalCase variant (`nine_router_status` != `NineRouterStatus`), so
  every item reads as unknown. Both produced a total false PASS here. Have the
  audit print counts and the full name lists per category, and sanity-check them
  against something you already know is true before believing a clean run.
- **Verify the far end, not the near end.** Rendering correctly, persisting
  without error, and returning `Ok(())`/`{"queued": true}` are all evidence about
  the code you just wrote, not about the feature. For anything that crosses a
  boundary — window to store, store to runtime, request to handler — assert on
  an observable at the destination (a value in a live readback, a log line, a
  pixel), and if the boundary is a queue, poll for the effect rather than
  trusting the ack.
- **Write the destination probe before reporting the source done.** Asking "what
  are the optimal next steps?" right after a feature lands will surface whether
  anything consumes it, and it is cheaper to find out before the user does. The
  probe is also the only thing that survives as a regression test for the
  wiring, which unit tests of the producer never are. If a cross-boundary
  feature cannot be probed, say so explicitly rather than describing the
  boundary as if it were verified.
- **"What is next?" asked twice is a command, not a question.** Answering it with
  a re-ranked list the second time reads as stalling, and it burns the turn the
  user spent to find out whether the work is real. When the same question comes
  back after you already answered it, pick the highest-value item yourself and
  build it; report what changed afterwards. Reserve the list for the first ask.
  The same applies to "proceed", "properly proceed with all" and "optimally":
  they mean act on the whole scope now, not plan it again.
- **When adding `use` imports to files with `//!` doc comments, place them
  after all `//!` lines and after any `#![cfg(windows)]` inner attributes.**
  The order is: `//!` docs → `#![...]` attrs → `use` statements. A `use` line
  inserted between `//!` lines or before `#![cfg(windows)]` causes an E0753
  ("expected outer doc comment") or E0753 ("inner attribute is not permitted")
  that costs a build cycle to diagnose. When bulk-adding an import to many
  files, check each file's first 5 lines before moving on.
- **Deleting a dead module requires cleaning up its exclusive dependencies.** A
  module that is never constructed often pulls in dependencies nothing else
  uses (e.g. `wgpu`, `winit`, `raw-window-handle`, `pollster`). After deleting
  the module, grep the remaining code for each dependency — if zero references,
  remove it from `Cargo.toml`. But first verify no other code references them:
  a dependency used only by the dead module is safe to remove, one used
  elsewhere (e.g. `hardware.rs` using `wgpu` for GPU enumeration) must stay.
  The tell-tale sign is a build error naming the removed crate.
- **Test-only hooks must not be `#[cfg(test)]` in a library used by another
  crate's tests.** The attribute applies only within its own crate, so the
  consuming test binary sees nothing. Use `#[doc(hidden)] pub` and document it
  as not part of the user-facing API, or gate the *callers* instead.
- **`#[cfg(windows)]` on an implementation does not gate its tests or its
  imports.** Tests calling a cfg-gated helper still compile on every target, so
  `cargo test --lib` fails on Linux/macOS while a Windows build stays green; and
  `use x::{self, ...}` names `self` on every platform, so a `-D warnings` build
  off Windows fails on an import only the Windows path uses. Gate the tests with
  the same attribute as the code they exercise rather than deleting them, and
  split the import. A Windows-only dev loop cannot see either failure, so a
  green local suite is evidence about Windows only.

## Layout

1. `BeginPaint` for the DC you will blit to.
2. Paint into a `CreateDIBSection` (top-down: negative `biHeight`).
3. `SelectObject` the DIB into a memory DC.
4. Publish that DC on your window state, *then* run the layout code.
5. `BitBlt` to the paint DC once — drawing direct to the window flickers.
6. `EndPaint`.

Read the surface size from `GetClientRect` and pass it down; full-height fills
guarantee no unpainted band, and it is what makes the footer land on the real
bottom edge.

```rust
let buf: &mut [u32] = std::slice::from_raw_parts_mut(raw as *mut u32, total);
win.draw_dc = Some(mem_dc);   // text must land here
draw_ui(win, buf);
win.draw_dc = None;
```

Layout code reads `win.draw_dc`. Do **not** open a scratch DC per text call: that
is both wasteful and how the two-surface bug gets introduced.

## winapi 0.3.9 signature traps

Grep the bindings rather than guessing — each of these cost real debugging time:

```bash
grep -n "pub fn CreateFontW" -A 16 ~/.cargo/registry/src/*/winapi-0.3.*/src/um/wingdi.rs
```

- `SelectObject` / `DeleteObject` take `*mut c_void`. Wrap in one helper rather
  than casting at each call site — and check the helper doesn't call itself.
- `CreateDIBSection`'s 4th parameter (`ppvBits`) is `*mut *mut c_void`, not
  `&mut *mut c_void`. Passing `&mut raw` where `raw: *mut c_void` gives a
  mismatched-types error. Use `&raw as *const _ as *mut _` — the compiler
  infers the target type from the function signature. This applies to every
  `CreateDIBSection` call site; grep for them all when one fails.
- `CreateFontW`'s `fwWeight` is `i32`; `DEFAULT_CHARSET as u32` trips clippy as a
  no-op cast.
- `GetBitmapDimensionEx(hbit: HBITMAP, lpsize: *mut SIZE)`; see the type-name
  section below for which module each handle lives in.
- `CreateCompatibleBitmap` gave a surface reporting 0x0 dimensions on this host,
  and `DrawTextW` clips to the surface — so text silently vanished. Use
  `CreateDIBSection` for any DC you draw text into. Do not assert on
  `GetBitmapDimensionEx` as a size check.
- `#[allow(dead_code)]` silences unused *methods* on the **`impl` block**, not on
  the struct.
- `NOTIFYICONDATAW` fields are all `u32` — `cbSize`, `uID`, `uFlags`,
  `uCallbackMessage` included. A `uID: ICON_ID as usize` is a compile error; the
  shell rejects nothing here, it just fails to build. The struct is `repr(packed)`
  on x86, so bind it `mut` and pass `&mut data as *mut _` — `Shell_NotifyIconW`
  takes a pointer, not a reference.
- `NIF_ICON | NIF_MESSAGE | NIF_TIP` is already `u32`; `as u32` is a no-op cast
  that clippy rejects.
- `GetFileType(...) == FILE_TYPE_CHAR` (not `!=`) decides whether stdin is a real
  terminal. Getting this backwards inverts every prompt-suppression check; it
  needs `std::os::windows::io::AsRawHandle`.

## Making a window property a real setting

A style or alpha value hardcoded at `CreateWindowExW` makes its setting a no-op:
there is no path from the toggle to the existing window. Three rules when a
setting must reach a live window.

- **Read the setting where the window is created**, not once at startup, and pass
  the resulting style in as a parameter. Reading it once and threading it as a
  parameter is what makes the call site honest about its dependency.
- **One window kind is not another.** `replace_all` over a duplicated creation
  block also rewrites the chat/main window, which legitimately keeps its own
  topmost. Patch by unique surrounding context, or scope the edit to the
  function, or you will make the *other* window wrong while fixing this one.
- **Cache the last applied value and act only on change.** Applying
  `SetLayeredWindowAttributes` or `SetWindowPos` every frame fights the window
  manager and costs needless work; the app also stutters. Compare against a
  tracked `applied` value.

Properties and their calls:

| Setting | Creation | Live change |
|---|---|---|
| always-on-top | omit `WS_EX_TOPMOST` from `ex_style` | `SetWindowPos` with `HWND_TOPMOST`/`HWND_NOTOPMOST` + `SWP_NOMOVE\|SWP_NOSIZE\|SWP_NOACTIVATE` |
| transparency | window must be `WS_EX_LAYERED` | `SetLayeredWindowAttributes(hwnd, 0, alpha, LWA_ALPHA)` |

Give transparency a **floor** (clamp to something like `0.05`): a settings store
that accepts `0` must not be able to make a window the user cannot see.

Handle types for these two calls are a common build-cycle sink: `SetWindowPos`
and `SetLayeredWindowAttributes` want `*mut HWND__`, which `DECLARE_HANDLE!` puts
in `shared::windef`, while `winuser::HWND` is a *private* alias. A `*mut c_void`
handle needs `as *mut winapi::shared::windef::HWND__`, and there is no
dereference — `*hwnd as *mut ...`, not `*hwnd as *mut ...` of a deref.
`WS_EX_TOPMOST` is `DWORD` from `shared::minwindef`, and `COLORREF` is a type
alias, so `0 as COLORREF` rather than a tuple-struct call.

## Building an editor window

Three tabs beats one long form: a single scrolling list of twenty fields is how
settings screens become unusable. Click-to-cycle suits enum choices; `-`/`+`
steppers suit bounded numbers; reserve real text entry for name/model fields.
Show the selected option's description so the choice is informed.

Wire every control the layout draws. A panel that renders but registers no hit
target is the classic dead-control bug, so assert that every tab produces at
least one target, that Save is absent while the form is invalid, and that a
read-only record offers Duplicate but not Delete. Show unsaved state persistently
(a marker plus an enabled Revert) rather than only in a confirm-on-close dialog.

Expose the editor's events to the app rather than letting it mutate state itself:
saves and deletes go through the app's store so the same data is visible over IPC
and MCP afterwards, and there is one implementation of id-uniqueness and
validation.

## Asserting on pixels

GDI writes **BGRA**; `SetTextColor` takes `0x00BBGGRR`. Comparing the DIB's `u32`
values to your own `0x00BBGGRR` constants looks correct and is wrong except for
symmetric colours (`0xE8E8EC` reads back as `0xECE8E8`).

Antialiasing also yields many near-miss values, so match channel-wise with a
tolerance rather than by equality:

```rust
let near = |target: u32| {
    let d = |shift: u32| (((pixel >> shift) & 0xFF) as i32
                       - ((target >> shift) & 0xFF) as i32).abs();
    d(0) <= 90 && d(8) <= 90 && d(16) <= 90
};
```

Quick health check on a capture:

| Distinct colours | Meaning |
|---|---|
| 1 | nothing rendered |
| 150+ | backgrounds, borders, antialiased glyphs all present |

A distinct-colour count is a *floor*, not a pass. “41 distinct colours” is
consistent with a correct window and also with white boxes stamped over every
label. Assert on **regions**: for each panel you care about, count pixels
differing from that region's modal (background) colour. A label column reading 0%
inked means nothing was drawn there no matter how colourful the window is overall.

### A capture that cannot be read proves nothing

Validate the capture file before drawing conclusions from it. A BMP header packed
via a `ctypes` struct gets padded to 8 bytes, so the offsets silently do not line
up; the resulting "screenshot" decodes to nonsense dimensions and a 100%-white
histogram, which reads exactly like a blank window. Write the headers with
`struct.pack` and assert the decoded width/height match what you asked for. Also
verify the dominant colours are the palette you specified — if you chose
`#141212` for the background and the histogram says `#FFFFFF`, the window did not
paint, whatever the colour count says.

### Let vision, but do not depend on it

Reading a screenshot with a vision model is the best check available, and it gets
rate-limited (HTTP 429) on shared keys. Have a pixel-level fallback ready so
verification degrades instead of stopping: region ink coverage, dominant-colour
comparison, and size assertions. Report which you used, and when vision was
unavailable say the visual assessment is unverified rather than implying you saw it.

## Verifying a change that adds a command or setting

A probe that launches the built binary and drives the new control path is worth
more than any unit test, because it proves the wiring between socket, queue and
handler. Two failure modes make such a probe lie to you:

- **A stale binary reports the feature as missing.** Preferring a fixed path
  (`target/release/app.exe`) runs yesterday's build, so a newly added handler looks
  like it never runs. Select the **newest** binary by mtime:
  `max([p for p in candidates if p.exists()], key=lambda p: p.stat().st_mtime)`.
- **Reading state back through a shared snapshot picks up the previous step's
  value.** Poll for the value you expect to be written (match on its id), not
  merely for "something non-empty", or the assertions silently pass against
  whatever landed earlier.

Make the probe clean up after itself. Agents and settings created by a probe
persist to the user's real store and make the *next* run fail on collisions, which
reads as a product bug. Delete created ids on the way out, and sweep leftovers
from prior runs at the start.

Prefer reading the app's own stdout when a probe fails. `[Agents] Saved 'x' over
IPC` distinguishes "the handler never ran" from "the handler ran and the readback
path is wrong" — a distinction that unit tests cannot make.

## Unit-testing a GUI with no window

Have the test path use the same surface the window does, and return **both** the
filled slice and the DIB surface — they hold different things, so asserting on
the wrong one gives a false pass or a false failure.

Two tests that earn their place:
- glyph pixels reach the DIB surface (catches the two-surface bug)
- layout fill colours reach the slice

Then test **event semantics**, where GUI bugs actually live: Enter sends and
clears the field, blank input sends nothing, whitespace is trimmed, Backspace on
empty is harmless, `WM_CHAR` control characters are not inserted as text, the
topmost hit target wins over the one beneath it, scroll clamps at both ends.

If a GUI test suite hangs, grep for a helper that calls its own name before
suspecting GDI — self-recursion from a refactor looks exactly like a hang.

## System tray lifecycle

A tray implementation that compiles can still be entirely inert, and the failure
is invisible until someone clicks. Four separate things must all be true; any one
missing makes every menu item a no-op while the code reads as complete.

1. **The icon must actually be registered.** Creating a hidden message window is
   not a tray. Call `Shell_NotifyIconW(NIM_ADD, ...)`; without it there is no icon
   at all, yet `start()` still returns `Ok`. Record the result in an
   `is_installed()` flag, remove the icon on shutdown, and implement `Drop` so a
   crash-free exit still leaves no ghost icon.
2. **The menu selection must not be discarded.** `TrackPopupMenu` with
   `TPM_RETURNCMD` *returns* the chosen id. Assigning it to `_cmd` and moving on
   makes every item dead. Map id → typed event through one function, and add a
   test asserting **every** id maps — an unmapped id is a silently dead item.
3. **There must be a path from the tray thread to the loop that acts on it.** The
   tray window has its own thread. A process-wide queue written by the handler and
   drained by the render loop is the simple shape; a channel is fine if the
   receiver is public.
4. **Drain the queue completely, every frame.** Taking one event per iteration
   drops the rest of a burst. Collect the whole queue, then handle it.

```rust
// In the render loop — drain everything, then act.
let events: Vec<_> = take_pending_events().into_iter()
    .chain(std::iter::from_fn(|| tray.poll_event()))
    .collect();
let mut should_quit = false;          // not `break` inside the match
for event in events { /* ... */ if quit { should_quit = true; } }
if should_quit { break; }
```

Minimize-to-tray must be gated on `is_installed()`. Hiding the window when no
icon registered is a one-way trip with no way back. Intercept `SC_MINIMIZE` in
`WM_SYSCOMMAND` to hide rather than minimise to the taskbar, and make close hide
too — a companion that vanishes when its window is closed looks like a crash.
Add/remove `WS_EX_TOOLWINDOW` alongside hide/show so the app rests only in the
tray and no orphaned taskbar button is left behind. Offer the hide action inside
the app's own header too, not only via the title bar.

### Verifying a tray without a screenshot

The notification area's toolbar is a private shell structure; `TB_GETBUTTONCOUNT`
and `TB_GETBUTTONTEXT` return stale or empty data, so do not build a check on it.
Instead drive the behaviour the way the shell does, and read the window state back
— the round trip is the evidence:

```python
WM_TRAY_CALLBACK = 0x8000 + 1
user32.PostMessageW(tray_hwnd, WM_TRAY_CALLBACK, 1, 0x0202)  # WM_LBUTTONUP
```

Find windows by class with `EnumWindows` + `GetClassNameW`, and assert the
sequence: visible → hide → **not** visible → click → visible, twice. Report the
icon's *appearance* (overflow placement, dark mode) as unverified when you have
not looked at a screen.

## Capturing a window from Python (ctypes)

```python
user32.GetClassNameW(hwnd, cls, 256)     # match on class
user32.GetWindowRect(hwnd, ctypes.byref(r))
hdc = user32.GetWindowDC(hwnd)
mdc = gdi32.CreateCompatibleDC(hdc)
bmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
gdi32.SelectObject(mdc, bmp)
user32.PrintWindow(hwnd, mdc, 2)         # PW_RENDERFULLCONTENT
# then GetDIBits + PIL "raw","BGRA",0,1
```

Set `user32.SetProcessDPIAware()` first or the capture comes back scaled.

## Rust/winapi type-name checks

Grep the bindings when a call will not typecheck; each of the following cost a
build cycle, and none is guessable from the signature.

- `RECT`, `SIZE`, `HDC`, `HFONT`, `HBRUSH` and `HBITMAP` are all in
  `shared::windef`. `shared::minwindef` holds only the scalar typedefs (`UINT`,
  `DWORD`, …), so an `HDC`/`HFONT` import from `minwindef` does not resolve — this
  costs a build cycle each time, so write `windef` for handles outright.
- `HWND` is a **private** alias, and `winuser::HWND__` does not exist:
  `DECLARE_HANDLE!{HWND, HWND__}` puts the struct in `shared::windef`. Functions
  taking `*mut HWND__` (as `SetWindowPos` and `SetLayeredWindowAttributes` do) need
  `x as *mut winapi::shared::windef::HWND__` from a `*mut c_void`. There is no
  dereference: `*h as *mut T`, not `*h as *mut *mut T`.
- `WINDOW_EX_STYLE` is not a name in winapi 0.3.9; an extended style is
  `shared::minwindef::DWORD`, and `WS_EX_TOPMOST` is declared as one.
- `COLORREF` is a **type alias**, not a tuple struct, so `COLORREF(0)` does not
  compile — write `0 as winapi::shared::windef::COLORREF`. `wingdi` re-exports it
  privately, so importing from there fails too.
- `GetModuleHandleW` is in `um::libloaderapi`, not `um::winuser`.
- `WNDCLASSW.hbrBackground` is `HBRUSH`; the `(COLOR_WINDOW + 1) as usize as HBRUSH`
  idiom avoids importing `GetStockObject` at all.
- `GET_X_LPARAM` / `GET_Y_LPARAM` live behind the `windowsx` cargo feature. Do not
  add a feature flag for two shifts and masks — `let p = lparam as u32;`
  then `(p & 0xFFFF)` / `(p >> 16)` is clearer and dependency-free.
- `GetSaveFileNameW`/`GetOpenFileNameW` live in `um::commdlg` behind the
  `commdlg` feature (not `comdlg32` — that feature does not exist and cargo
  fails with a version-resolution error). `OFN_OVERWRITEPROMPT` and
  `OFN_PATHMUSTEXIST` are the flags to combine. The dialog is modal, so the
  calling thread blocks until the user acts — fine for a window, fatal in a test.
- `EnumDisplayDevicesW` lives in `um::winuser`, not `um::wingdi`. The
  `DISPLAY_DEVICEW` struct is in `um::wingdi` and has no `Default` impl — use
  `mem::zeroed()` and set `cb` manually. `DEVICE_STATE_ACTIVE` is `0x1`.
- `std::ffi::c_void` and `winapi::ctypes::c_void` are **distinct types**.
  All winapi GDI function signatures use `winapi::ctypes::c_void`; passing a
  `*mut std::ffi::c_void` where `*mut winapi::ctypes::c_void` is expected
  fails with a mismatched-types error that names both types. Import
  `use winapi::ctypes;` and use `winapi::ctypes::c_void` in every GDI helper
  signature. A bulk find-and-replace of `core::ffi::c_void` → `winapi::ctypes::c_void`
  across all `.rs` files is safe (it is a type-name replacement, not a structural
  change), but always verify each file's first 5 lines afterwards for doc-comment
  ordering.
- Colour constants need no `as u32` in recent winapi. Many pet/overlay windows in
  one app means the *class name* is the only reliable selector — match
  `"AppMain"` rather than the window title, which siblings share.

## Per-category audio needs a sink per sound

A single shared `rodio::Sink` carries **one** volume, so `master * sfx` for every
sound makes a music bus structurally unreachable — the setting reads back, saves,
and changes nothing. Give each playback its own child sink of the mixer, compute
`master * category_bus * sound_own_level` at play time, then `detach()` so it
survives the local scope.

rodio 0.17 specifics, each a compile error otherwise: there is no
`Sink::new(&sink)` and no `Sink::mixer()` — build from a stream handle with
`rodio::Sink::try_new(&handle)`, and get the handle from
`rodio::OutputStream::try_default()` which returns `(OutputStream,
OutputStreamHandle)`. **Store the handle on the struct**: sinks attach to it, so
dropping it silences playback, and opening an output device per sound is slow
and fails on a busy device. Gate the whole thing behind a cached `Option<...>`.

Test the bus arithmetic as a pure function of `(config, category)` rather than
through playback, and see
[references/audio-bus-and-runtime-property-settings.md](references/audio-bus-and-runtime-property-settings.md)
for the rodio 0.17 API and the general "single application point" shape.