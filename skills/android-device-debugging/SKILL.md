---
name: android-device-debugging
description: MIUI/HyperOS Android device debugging and workarounds.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [android, device, debugging]
---

# Android Device Debugging (OEM-specific, real devices)

Use when a debug/install/test workflow behaves differently on a physical device than on
stock Android or an AVD. The lessons below are durable cross-OEM patterns, not
one-off hacks.

## 0. Distinguish three layers before debugging

1. **AOSP behavior** — what stock Android 11–15 does.
2. **OEM modification** — MIUI SmartPower, Samsung Knox, OnePlus GameMode, etc.
3. **App-side code** — your routing, permissions, manifest, tests.

Most "the app is broken on my phone" reports are actually layer 2. Verify layer 1
first (AVD or another stock device) before changing app code.

## 1. MIUI / HyperOS: the SmartPower trap

**Symptom:** instrumented test suite hangs for minutes then fails with
`Process crashed` / `Abort background activity starts from <uid>`.
A single Compose `NavigationTest` method consumes the entire 11+ minute timeout.

**Root cause:** MIUI SmartPower kills the UTP test-harness process before it can
launch the app's Activity. This happens BEFORE any `@Before` hook runs, so
`Assume.assumeFalse(isMIUI)` cannot help — the process is dead before JUnit
starts.

**What does NOT fix it:**
- `appops set pkg SYSTEM_ALERT_WINDOW allow` — SmartPower ignores the AOSP overlay
  exemption entirely.
- `settings put global background_activity_starts_enabled 1/0`
- `dumpsys deviceidle whitelist +pkg`
- `pm grant` for `START_ACTIVITIES_FROM_BACKGROUND` / `RUN_ANY_IN_BACKGROUND`

**What does fix it (user-side only):**
- Developer options -> Turn off MIUI optimization (requires reboot).
- Or: whitelist the test runner package in MIUI SmartPower / Battery settings.

**App-side pragmatic answer:** remove or skip the offending test class on MIUI.
A class-level skip is cleaner than per-test skips because SmartPower aborts
before any `@Before` runs.

## 2. MIUI / HyperOS: the install gate

**Symptom:** `adb install` / `adb install -r` returns
`INSTALL_FAILED_USER_RESTRICTED: Install canceled by user` and the package never
appears on the device.

**Root cause:** MIUI requires on-device confirmation for sideloaded APKs.

**What does NOT bypass it:**
- Staged install (`pm install-create` + `install-write` + `install-commit`) — same
  PackageManagerService code path, same rejection.
- `install_via_adb_enabled=1` alone — this only relaxes USB debugging installs; it
  does not override the user-confirmation gate.
- `adb_install_need_confirm=0` — same limitation.

**What works:**
- Tap Allow / 允许 on the MIUI confirmation dialog when it appears.
- Developer options -> Install via USB (if available on that MIUI version).
- Once the user has approved one install, `adb install -r` updates succeed without
  re-prompting.

**Pitfall:** `com.soniccore.debug` and `com.soniccore` are treated as separate
packages. The debug flavor may trigger its own confirmation even after the release
flavor was approved.

## 3. MIUI / HyperOS: appops reset on UTP reinstall

**Symptom:** after a successful `adb install`, `appops get pkg` shows
`SYSTEM_ALERT_WINDOW: allow`, but once the instrumented test run starts and UTP
pushes the test APK, MIUI resets it to `SYSTEM_ALERT_WINDOW: ignore`.

**Root cause:** MIUI resets appops on every UTP reinstall cycle.

**Lesson:** never assume `appops set ... allow` survives an instrumented test run
on MIUI. Re-apply after every install if you need the grant for the test itself.

## 4. MIUI / HyperOS: GrantPermissionsActivity blocks foreground

**Symptom:** after `am start`, `dumpsys window` shows
`GrantPermissionsActivity` as the focused window, not your app. `waitForIdle()`
throws "No compose hierarchies found."

**Fix:** dismiss the system dialog with `adb shell input keyevent KEYCODE_ESCAPE`
before launching the activity. Do not tap permission dialogs via ADB.

## 5. Wireless ADB reliability on Xiaomi / HyperOS

**Symptom:** a long-running operation (install + test suite) drops mid-flight with
`adb.exe: device offline` or `cannot connect to <ip>:<port>`.

**Root cause:** HyperOS aggressively manages the wireless debugging transport.
Long operations can exceed the keepalive window. The device may also enter a
low-power state while the screen is off.

**Mitigation:**
- `svc power stayon true` and increase screen timeout before long operations.
- For installs: keep the screen on and watch for the MIUI confirmation dialog.
- If the link drops, reconnect from the host side
  (`adb kill-server && adb start-server && adb connect <ip>:<port>`).
- Have the user fall back to USB if TCP repeatedly fails.

## 6. A2DP Bluetooth routing on pre-31 devices (MIUI / HyperOS)

**Symptom:** JBL Go 3 and other A2DP speakers show in the system audio routes but
the app's Devices screen says "No output device detected" or audio plays through
the phone speaker instead.

**Root cause:** calling `startBluetoothSco()` for every Bluetooth device opens a
voice-call SCO channel, not an A2DP media path. On MIUI this actively kills A2DP
media routing, so the speaker never receives audio.

**Fix:** remove SCO-based routing from the legacy pre-31 path entirely. Let the
platform handle A2DP natively. The A2DP proxy (`BluetoothA2dp` via
`getProfileProxy`) can stay for codec/battery introspection — it does not
interfere with routing.

**Verification:**
```bash
adb shell dumpsys audio | grep "Active communication"
# should show: Active communication device: bt_a2dp name=JBL Go 3
```

## 7. AudioDeviceRegistry: MIUI early-empty device enumeration

**Symptom:** system `dumpsys audio` shows `bt_a2dp` active, but the app's UI shows
"No output device detected."

**Root cause:** `AudioManager.getDevices()` often returns an empty array on MIUI
when called immediately after the Bluetooth stack initializes. The platform
publishes the callback before the stack settles.

**Fix:** re-enumerate once after a short delay inside `observeDevices()`.
```kotlin
CoroutineScope(coroutineContext).launch {
    delay(1500L)
    trySend(runCatching { enumeratePlatform() }.getOrDefault(emptyList()))
}
```
1.5s covers the worst-case MIUI delay without perceptible UI lag.

## 8. Compose UI tests on short-viewport / landscape devices

**Symptom:** "component is not displayed" / timeout for items scrolled below the
fold in `LazyColumn` / `LazyRow`. Happens on Nokia 7.2 in landscape, on any
device with viewport height < 1080px.

**Root cause:** off-screen Compose items have NO semantics node. `onNodeWithText`
fails for content that exists in the database but is scrolled out of view.

**Fix:** lock test devices to portrait before the run:
```bash
adb shell settings put system user_rotation 0
adb shell settings put system accelerometer_rotation 0
```
Do not "fix" production scrolling behavior to satisfy a test assertion.

## 9. ComponentResolutionTest as a MIUI sanity check

`ComponentResolutionTest` (25 tests: services, receivers, tiles, widget, Cast
provider) passes cleanly on MIUI API 30 (Redmi Note 12 Pro 5G). Use it as a
quick "the manifest is intact on this OEM" check after any manifest refactor.

See `references/android-kotlin-pitfalls.md` for Kotlin compilation pitfalls that surface
during `assembleDebug` (@Inject vs module-provided, @Contextual IR crash, Size aliasing
with CameraX, viewModelScope.launch scope, val reassignment, Icons.AlertCircle) and cost
1-3 build cycles each.

## Pitfalls

- **MIUI SmartPower ignores `@Before` hooks.** Any assume/skip logic inside JUnit
  lifecycle methods is unreachable. Remove the test class entirely if it cannot
  pass on MIUI.
- **`adb disconnect` detaches USB devices too.** When both a phone and an AVD are
  attached, `adb disconnect <serial>` removes the phone from the device list so
  AGP does not shard across both. Do not assume `disconnect` is TCP-only.
- **`adb logcat -d` truncates long lines.** Route structured debug output to a
  file on `/sdcard/Download/` instead; that directory survives package uninstall.
- **Compress test loops on Windows PTY.** `process(write)` sends `\n` which is not
  delivered as a line terminator to Windows PTY children. Use
  `process(submit)` for prompts; it sends `\r\n`.
- **CameraX + ML Kit QR scanning on Nokia 7.2.** PDAF defocus errors from the
  camera driver (`sensor_pdaf_cal_defocus: pdaf defocus calculation fail`,
  `isp_port_process_upstream_event: failed`) are NORMAL on Nokia 7.2 and do NOT
  indicate an app crash. Check `pidof com.your.package` — if the app process is
  still alive, the camera is working.
- **CameraX `Size` import conflict.** `android.util.Size` (used by
  `ImageAnalysis.Builder.setTargetResolution()`) collides with
  `androidx.compose.ui.geometry.Size`. Alias-import:
  `import android.util.Size as AndroidSize`.
- **Material Icons does not include `AlertCircle`.** Using
  `Icons.Default.AlertCircle` fails with "Unresolved reference: AlertCircle".
  Use `Icons.Default.Warning` instead.
- **MSYS path translation is disabled for native binaries.** `adb push
  /c/Users/x/file.apk /data/...` fails. Use `C:/Users/x/file.apk` with
  forward slashes for all native tool paths.
- **Xiaomi can surface model codes / raw identifiers as device names.** On MIUI,
  `AudioDeviceInfo.productName`, `BluetoothDevice.name`, and mDNS service names
  may be blank, equal to a MAC/IP, or equal to a model code such as `22101316G`.
  Sanitize display names at the mapping layer; never expose raw identifiers in the
  UI.
- **Transient error messages may auto-dismiss before inspection.** On MIUI,
  snackbar/system notifications can disappear automatically. Capture the UI with
  `uiautomator dump` immediately after the action, and capture logs to
  `/sdcard/Download/logcat.txt` if live `logcat -d` is unreliable.
- **Verify build artifacts on Xiaomi before install.** After routing/logging
  changes, rebuild with `--no-build-cache`, then verify the exact diagnostic
  string exists in the APK DEX before installing. Example: confirm
  `"invalid device type"` appears in `classes*.dex` inside the APK.
- **Verify build artifacts on Xiaomi before install.** After routing/logging
  changes, rebuild with `--no-build-cache`, then verify the exact diagnostic
  string exists in the APK DEX before installing. Example: confirm
  `"invalid device type"` appears in `classes*.dex` inside the APK.
- **Windows repo hygiene:** remove stray `nul` and Gradle/log artifacts before
  `git add -A`; otherwise `git add` fails with `invalid path 'nul'`.
- **Subagent buildout of multi-stream code:** When spawning parallel
  `delegate_task` agents for independent code streams (e.g., networking,
  hypervisors, containers), run import checks on ALL packages after all complete.
  Missing type aliases (`VMDisplayType = DisplayType`) and empty `__init__.py`
  files are common failure modes where `write_file` refuses to overwrite an
  existing file without first reading it. Search for empty `__init__.py` files
  and missing cross-package imports in the fix step.
