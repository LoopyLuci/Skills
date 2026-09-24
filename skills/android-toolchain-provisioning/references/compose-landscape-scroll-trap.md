# Compose instrumented tests on landscape / short-viewport devices

## The false-failure pattern

On a device in landscape (or any configuration where the viewport height is shorter
than the content), a `LazyColumn`/`LazyRow` item that is scrolled below the visible
area has **no active semantics node**. `composeRule.onNodeWithText("Foo")` throws
`AssertionError: Node with text 'Foo' not found` or `waitUntil` times out at 10s,
even though the content exists in the tree and the app renders correctly.

The same failure class appears as:
- `component is not displayed`
- `No compose hierarchies found` (when the first test's root assertion targets below-fold content)
- `waitUntil` timeout at the default 10s

## Hard evidence from a real session

Device: Nokia 7.2 (Android 11, stock), when accidentally left in landscape (viewport
height 1080px).

Failing assertions (all on content that was genuinely rendered):
- EQ "Presets" at semantic `t=1755px` while viewport is `0..1080px` → below fold
- Parametric "Bands" at `t=1244px` → below fold
- Volume stream sliders ("Media") → below fold
- Devices list "Built-in" section → scroll maxValue=100, item below fold

EQ dump proved the app is correct: all presets present ("Acoustic", "Flat", "23 available").
Rotating to portrait (`user_rotation=0`, `accelerometer_rotation=0`) made all four
assertions pass immediately.

## Fix checklist for instrumented Compose tests

1. **Lock portrait before running:** do this once per device session, not in every test.
   ```bash
   adb shell settings put system user_rotation 0
   adb shell settings put system accelerometer_rotation 0
   ```
   Re-lock after every physical rotation and after every AVD reboot.

2. **For scrollable content, assert a visible anchor** (a header, a count label) that
   is always in the viewport, rather than an item that may be scrolled off:
   ```kotlin
   // Weak — fails when the item is below fold
   composeRule.onNodeWithText("Presets").assertIsDisplayed()

   // Strong — header is at the top of the list, always visible
   composeRule.onNodeWithText("EQ Presets").assertIsDisplayed()
   ```

3. **Scroll into view before asserting:**
   ```kotlin
   composeRule.onNodeWithText("Presets")
       .assertIsDisplayed()  // only after scroll
   composeRule.onNode(
       hasScrollToIndexAction()
   ).performScrollToIndex(0)
   ```

4. **For automation/background tests:** avoid depending on Compose content
   being in the foreground; use `ComponentResolutionTest` (services, receivers,
   tiles, widget) for the on-device signal that survives SmartPower/MIUI.

## Do NOT do this

- Do NOT add "fix working production code to satisfy the assertion" by hardcoding
  content to the top of the list. The user can scroll; the test should mirror real use.
- Do NOT chase this in app code (`LazyColumn` always positions items at 0, etc.) —
  that is not how Compose lists work and it breaks the production layout.
- Do NOT disable rotation lock in the test and rely on `setRequestedOrientation` —
  MIUI and some OEMs ignore it for the test runner.
