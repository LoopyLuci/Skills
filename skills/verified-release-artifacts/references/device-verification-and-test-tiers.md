# Device verification and test tiers

Shipping an artifact means installing it where it will actually run. A green unit
suite proves nothing about a UI that crashes on first tap.

## Why the cheap tier misses whole bug classes

| Defect class | Tier that can catch it |
|---|---|
| Plain logic, parsing, data transforms | Unit / JVM tests |
| Concurrency, resource lifetime, native crashes | Stress runs at high thread counts, then CI |
| UI composition, layout, lifecycle, rendering | Instrumented tests on device/emulator |
| Install, upgrade-over-existing, permissions | Real install on a real device |

When everything is green and the app still breaks on hardware, the gap is the
tier, not the tests. Add the missing tier to CI.

## Driving a real Android device

```bash
export PATH="$PATH:$HOME/AppData/Local/Android/Sdk/platform-tools"
adb devices -l
adb -s <serial> shell getprop ro.build.version.sdk     # check against minSdk
adb -s <serial> install -r app-release.apk
adb -s <serial> shell am start -n <pkg>/.MainActivity
```

Check the installed artifact's identity, not just that install returned 0:

```bash
adb -s <serial> shell dumpsys package <pkg> | grep -E "versionCode|versionName"
```

### Read the crash log — do not trust "no crash" too early

Checking for a crash immediately after launch is a race: a tap that kills the app
may not have happened yet. Clear the log, drive the UI, wait, *then* read:

```bash
adb -s <serial> logcat -c
adb -s <serial> shell input tap <x> <y>
sleep 5
adb -s <serial> shell "ps -A | grep <pkg>"     # still running?
adb -s <serial> logcat -d -v brief | grep -c "FATAL EXCEPTION"
```

A `Force finishing activity` line means the process died even if the log excerpt
you grepped looked clean.

### Tap real coordinates, not guessed ones

Tapping near the bottom of the screen can hit the gesture bar and send the user to
the launcher instead of switching tabs. Get real bounds:

```bash
adb -s <serial> shell uiautomator dump /sdcard/ui.xml
adb -s <serial> shell cat /sdcard/ui.xml > ui.xml
# parse text="..." bounds="[l,t][r,b]" and tap the centre
```

### Isolate which screen is at fault

Force-stop, relaunch, tap one target, wait, then check liveness and crash count.
Repeat per screen. That turns "the app crashes" into "this one control does",
which is the difference between a fixable report and a mystery.

### Read what actually rendered

`uiautomator dump` gives the semantic tree:

```bash
adb -s <serial> shell cat /sdcard/ui.xml | grep -o 'text="[^"]*"' | sort -u
```

This catches both the crash case and the "renders blank / shows an error state"
case, and unlike a screenshot it needs no vision step.

## Instrumentation in CI

Emulator job, with KVM enabled or the emulator falls back to software and times
out:

```yaml
- name: Enable KVM
  run: |
    echo 'KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"' \
      | sudo tee /etc/udev/rules.d/99-kvm4all.rules
    sudo udevadm control --reload-rules
    sudo udevadm trigger --name-match=kvm

- name: Instrumented tests
  uses: reactivecircus/android-emulator-runner@v2
  with:
    api-level: 30
    arch: x86_64
    profile: pixel_2
    disable-animations: true
    script: cd ScreenBuddy-Android && ./gradlew connectedDebugAndroidTest
```

The `script:` runs from the **repository root**, ignoring the job's
`defaults.run.working-directory` — put the directory in the script itself or it
fails with `./gradlew: not found`.

## Prove the new test catches the bug

Instrumented tests are expensive to write and easy to write wrong. Reintroduce the
defect, confirm the test goes red with the same signature, restore the fix:

```
reintroduce bug -> test FAILS with ArrayIndexOutOfBoundsException: length=0; index=-5
restore fix   -> test passes
```

Matching the *original* exception is the evidence that you reproduced the real
defect rather than some nearby failure.

Test the real subject, not a copy. Make the production composable/function
`internal` so the test drives it directly — a test that re-declares the thing it
is testing drifts from the original and keeps passing while shipped code stays
broken.

## Composition-specific hazards

- **Early `return` from a composable** swaps the child subtree out from under the
  composer as a state flag flips, corrupting the slot table
  (`ArrayIndexOutOfBoundsException` in `SlotTableKt.key`). Branch on the flag
  instead of returning early, keeping the group structure stable across
  recompositions.
- **Duplicate keys** in a lazy list (`items(list, key = { it.id })`) throw the same
  way. Check the id source for duplicates — including ids assembled from a
  database overlay.
- Build a **debug** APK for stack traces when a release build yields only
  framework frames; R8 strips your app's frames entirely.
