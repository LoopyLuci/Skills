---
name: android-instrumented-testing
description: Use when Android instrumented tests fail or hang on devices.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [android, instrumented, testing]
---

# Android Instrumented Test Execution & Debugging

Use when running `connectedAndroidTest` on an emulator, a physical phone, or a CI
matrix (debug + release variants) and the suite fails, hangs, or crashes before or
during test execution. Covers the full ladder of device-level blockers: install
timeouts, screen sleep, OEM ROM background-activity policing, runtime-permission
dialogs, and Hilt lifecycle crashes.

Related: `android-toolchain-provisioning` (build + verifier infrastructure),
`android-audio-device-control` / `android-audio-dsp-equalizer` (SonicCore app
domain). All three are user-owned in this profile — if they are stale, run
`hermes curator adopt` on them in a foreground session.

## The failure ladder (check in this order)

### 1. Build the test APKs first (`verify.sh` pattern)

```bash
./gradlew :app:assembleFullDebugAndroidTest --no-daemon   # or your variant
# If verify.sh exists, run it: it builds both flavors + test APKs in one go
bash verify.sh
```

Confirm the artifacts exist before blaming the device:
`app/build/outputs/apk/androidTest/{flavor}/{buildType}/*-androidTest.apk`

### 2. Confirm the device is ready (`check-device.sh` pattern)

Compose UI tests need a VISIBLE, UNLOCKED window. A locked/dozing device makes the
Activity launch and pause immediately, and every test fails with the misleading
`No compose hierarchies found in the app` (looks like a setContent bug; it is not).

```bash
adb devices -l
adb shell getprop sys.boot_completed        # must be 1
adb shell dumpsys power | grep mWakefulness  # must be Awake
adb shell dumpsys window | grep isKeyguardShowing  # must be false
adb shell input keyevent KEYCODE_WAKEUP
adb shell wm dismiss-keyguard
adb shell svc power stayon true              # keep screen on for the whole run
adb shell settings put system screen_off_timeout 1800000  # 30 min
```

### 3. Pre-grant runtime permissions OUT OF BAND

On a freshly wiped device (`-wipe-data` on the AVD) or a new phone, no runtime
permissions are pre-granted, so the system injects `GrantPermissionsActivity` over
MainActivity at launch. The activity is paused + destroyed before Compose registers
its hierarchy → every test fails with `No compose hierarchies found in the app`.

```bash
# Install FIRST, then grant (grant against an uninstalled package fails with
# "package not found").
adb install -r app/build/outputs/apk/full/debug/app-full-debug.apk
adb shell pm grant com.soniccore.debug android.permission.RECORD_AUDIO
adb shell pm grant com.soniccore.debug android.permission.POST_NOTIFICATIONS
adb shell pm grant com.soniccore.debug android.permission.BLUETOOTH_CONNECT
# GRANT BOTH packages: debug builds carry an applicationIdSuffix (e.g. .debug);
# release runs use the plain id (e.g. com.soniccore).
adb shell pm grant com.soniccore android.permission.RECORD_AUDIO
```

Don't add a `GrantPermissionRule` to the test class: granting a permission that is
not already held RESTARTS the app process, destroying the Activity the
ComposeTestRule is waiting on → "No compose hierarchies found in the app" again.
Normal permissions (MODIFY_AUDIO_SETTINGS) are not grantable (`not a changeable
permission type`) — that error is expected and harmless.

### 4. UTP install hang: `ShellCommandUnresponsiveException` / "Starting 0 tests"

UTP installs APKs with `pm install-create/write/commit` and the shell command can
time out on slow devices. The suite "runs" 0 tests and the XML shows
`Failed to install split APK(s) ... ShellCommandUnresponsiveException`. Fix:
lengthen the ADB timeout.

```bash
./gradlew :app:connectedFullDebugAndroidTest \
  -Pandroid.adbOptions.timeOutInMs=120000 --no-daemon
```

Restart adb first if the device was disconnected/reconnected: `adb kill-server`
then `adb start-server`. Kill stale Gradle daemons between killed runs:
`powershell -Command "Get-Process java | Stop-Process -Force"` on Windows.

### 5. MIUI/HyperOS blocks the activity start

Xiaomi phones log `Abort background activity starts from <uid>` and broadcast starts
refuse with `process is not permitted to auto start`. The Compose activity never
reaches the foreground (launcher keeps `mCurrentFocus`) and the suite hangs at the
first UI test for minutes. Workaround ladder:

1. Keep the screen awake (step 2) and force-stop stale packages first:
   `adb shell am force-stop com.soniccore.debug com.soniccore.debug.test`
2. Whitelist via appops — named ops like AUTO_START fail with "Unknown operation
   string" on MIUI; use the numeric codes:
   ```bash
   adb shell appops set <pkg> RUN_ANY_IN_BACKGROUND allow
   adb shell appops set <pkg> 10021 allow  # START_ACTIVITIES_FROM_BACKGROUND
   adb shell appops set <pkg> 10022 allow  # START_FOREGROUND_SERVICES_FROM_BACKGROUND
   adb shell appops set <pkg> 10026 allow
   ```
3. Disable AOSP's background-activity gate:
   `adb shell settings put global background_activity_starts_enabled 1`
   (verify with `dumpsys activity settings`).
4. Add to the device-idle whitelist:
   `adb shell dumpsys deviceidle whitelist +<pkg>`

If the phone still blocks, fall back to the provisioned AVD — CI always boots a
fresh emulator (`-wipe-data`) and never hits this.

### 6. Hilt receiver crash: "The component was not created"

If the process dies during install with
`Unable to start receiver ... IllegalStateException: The component was not created.
Check that you have added the HiltAndroidRule`, the app's `@AndroidEntryPoint`
receivers are the culprit. The generated `Hilt_<Name>Receiver.onReceive()` calls
`inject()` unconditionally on ANY broadcast — including real system broadcasts
(`MY_PACKAGE_REPLACED` fired when the test run reinstalls the APK over a previous
session, or `BOOT_COMPLETED`) — and throws when no component exists yet. Under
`HiltTestApplication` the component is created lazily per-test by `HiltAndroidRule`,
so such a broadcast takes down the whole instrumentation before a single test runs
(0 tests in the XML, "Process crashed").

Fix (production-grade, not a test hack): drop `@AndroidEntryPoint` from receivers and
resolve dependencies lazily via an `@EntryPoint` interface:

```kotlin
@EntryPoint
@InstallIn(SingletonComponent::class)
interface ReceiverEntryPoint {
    fun automationEngine(): AutomationEngine
}

private fun resolveEngine(context: Context): AutomationEngine? = runCatching {
    EntryPointAccessors.fromApplication(
        context.applicationContext, ReceiverEntryPoint::class.java,
    ).automationEngine()
}.getOrNull()

class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action != Intent.ACTION_BOOT_COMPLETED
            && intent.action != Intent.ACTION_MY_PACKAGE_REPLACED) return
        val engine = resolveEngine(context) ?: return  // no-op until DI exists
        // ... start service / dispatch to engine ...
    }
}
```

Receivers degrade to no-ops until DI exists — correct production behaviour for
direct-boot / process-restored-for-broadcast edge cases too. The receiver tests keep
working; they call `onReceive()` directly with arbitrary intents and must not crash.

### 7. Minified release variant

The CI matrix runs debug AND release: `:app:connectedFullReleaseAndroidTest`. The
task name only exists when the property is set (default is debug):

```bash
./gradlew :app:connectedFullReleaseAndroidTest \
  -PtestBuildType=release -Pandroid.adbOptions.timeOutInMs=120000
```

Without `-PtestBuildType=release` you get `task 'connectedFullReleaseAndroidTest'
not found` even though the debug task exists. Discover valid task names with
`./gradlew :app:tasks --all | grep -i connected`. Grants must be re-run for the
release package (no `.debug` suffix) on a wiped device.

## Reading the truth from reports

- XML results live in `app/build/outputs/androidTest-results/connected/{buildType}/flavors/{flavor}/*.xml`
- `tests=0` + "Tool failures" in the HTML report = install/UTP failure, not a test failure
- `No compose hierarchies found in the app` = activity never reached RESUMED with
  Compose content — permission dialog, screen sleep, or MIUI background block
- `Process crashed` with Hilt stack = receiver/service/tile injected before component existed
- Dump the live semantics tree for on-device debugging (survives uninstall):
  `adb shell uiautomator dump /sdcard/ui.xml` then read the XML — it shows the real
  window stack and any dialog covering the activity.

## Pitfalls

- An emulator AND a phone both attached makes AGP shard across every device; an empty
  shard reports "Starting 0 tests" and fails the build. Disconnect extras with
  `adb disconnect <serial>` before running.
- Wiped AVD cold boots take ~80s (API 35 google_apis); poll `sys.boot_completed` with
  a loop, never a blind sleep.
- `grep` on binary dex/XML: `grep -c` on no match exits 1 (use `tr -c '[:print:]' '\n'`
  or count via python) so the pipeline exit code is not a false failure.
- The Gradle tail -45 pipeline masks the real exit code — `head`/`tail` exit 0 even
  when the build failed. Capture the full log and grep the XML reports for truth.
