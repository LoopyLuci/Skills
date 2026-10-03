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

## Always-on rules

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
- **A handler that returns `Ok(())` proves only that it ran.** Every OS
  registration — tray icon, hotkey, hook, clipboard listener — must be checked by
  the OS's own acknowledgement, and `start()` must propagate that rather than
  assuming success. See [System tray](#system-tray-lifecycle).
- **A `break` inside a `match` inside a `for` leaves only the match.** Loops
  driven by event handlers need a flag set in the arm and tested after the loop.

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

- `RECT`, `SIZE`, `HDC`, `HFONT`, `HBRUSH` and `HBITMAP` are all in
  `shared::windef`. `shared::minwindef` holds only the scalar typedefs (`UINT`,
  `DWORD`, …), so an `HDC`/`HFONT` import from `minwindef` does not resolve — this
  costs a build cycle each time, so write `windef` for handles outright.
- `GetModuleHandleW` is in `um::libloaderapi`, not `um::winuser`.
- `WNDCLASSW.hbrBackground` is `HBRUSH`; the `(COLOR_WINDOW + 1) as usize as HBRUSH`
  idiom avoids importing `GetStockObject` at all.
- `GET_X_LPARAM` / `GET_Y_LPARAM` live behind the `windowsx` cargo feature. Do not
  add a feature flag for two shifts and masks — `let p = lparam as u32;`
  then `(p & 0xFFFF)` / `(p >> 16)` is clearer and dependency-free.
- Colour constants need no `as u32` in recent winapi. Many pet/overlay windows in
  one app means the *class name* is the only reliable selector — match
  `"AppMain"` rather than the window title, which siblings share.