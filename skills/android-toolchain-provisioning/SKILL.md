---
name: android-toolchain-provisioning
description: Build Android APKs with no JDK/SDK/Studio installed.
---

# Android Toolchain Provisioning (headless, no Android Studio)

Use when `java`, `gradle`, `sdkmanager`, or `$ANDROID_HOME` are missing but you must
produce a real compiled APK. Everything installs user-local — no admin rights, no
system PATH changes.

## 0. Verify what's missing

```bash
java -version; gradle -version; echo "$JAVA_HOME $ANDROID_HOME"
ls "$LOCALAPPDATA/Android/Sdk" 2>/dev/null   # Windows default SDK location
```

## 1. Portable JDK 21 (Temurin)

Resolve the current zip link from the Adoptium API rather than hardcoding a version:

```bash
ROOT="$HOME/android-toolchain"; mkdir -p "$ROOT"; cd "$ROOT"
LINK=$(curl -s "https://api.adoptium.net/v3/assets/latest/21/hotspot?architecture=x64&image_type=jdk&os=windows" \
  | tr ',' '\n' | grep -o 'https://[^"]*OpenJDK21U-jdk_x64_windows_hotspot[^"]*\.zip' | head -1)
curl -sSL -o jdk.zip "$LINK" && unzip -q jdk.zip     # -> jdk-21.x.y+z/
```

Use `os=linux` + `.tar.gz` on Linux. JDK **21** is the right target for AGP 8.5–8.7;
JDK 17 also works, JDK 23+ breaks older Gradle.

## 2. Android SDK command-line tools

```bash
curl -sSL -o cmdline-tools.zip https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip
unzip -q cmdline-tools.zip -d tmp
mkdir -p sdk/cmdline-tools && mv tmp/cmdline-tools sdk/cmdline-tools/latest
```
The `sdk/cmdline-tools/latest/` nesting is **mandatory** — sdkmanager refuses to run
from a flat directory.

## 3. Licenses + packages — call the Java class directly

**PITFALL:** `sdkmanager.bat` through git-bash `cmd.exe /c` fails with
`'sdk' is not recognized` / `'"C:\..."' is not recognized` no matter how you quote it,
and a `.bat` wrapper invoked as `cmd.exe //c foo.bat` can silently return only the
Windows banner. Skip the wrapper entirely and invoke the CLI class:

```bash
export JAVA_HOME="$ROOT/jdk-21.0.12+8"
CT="$ROOT/sdk/cmdline-tools/latest"; SDK="$ROOT/sdk"

# licenses (yes-pipe works here)
yes 2>/dev/null | "$JAVA_HOME/bin/java" -Dcom.android.sdklib.toolsdir="$CT" \
  -classpath "$CT/lib/*" com.android.sdklib.tool.sdkmanager.SdkManagerCli \
  --sdk_root="$SDK" --licenses

# packages
"$JAVA_HOME/bin/java" -Dcom.android.sdklib.toolsdir="$CT" -classpath "$CT/lib/*" \
  com.android.sdklib.tool.sdkmanager.SdkManagerCli --sdk_root="$SDK" \
  "platform-tools" "platforms;android-35" "build-tools;35.0.0"
```

Use forward-slash native paths (`C:/Users/x/...`) — MSYS path translation is disabled
for native binaries, so `/c/Users/...` args fail.

## 4. Gradle — never install it, use the wrapper

Do **not** download Gradle separately. Write `gradle/wrapper/gradle-wrapper.properties`
by hand and let the wrapper self-provision:

```properties
distributionUrl=https\://services.gradle.org/distributions/gradle-8.9-bin.zip
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
```

You need `gradlew`, `gradlew.bat`, and `gradle/wrapper/gradle-wrapper.jar`. If the jar
is absent, fetch it from the Gradle GitHub tag matching your version:
`https://raw.githubusercontent.com/gradle/gradle/v8.9.0/gradle/wrapper/gradle-wrapper.jar`

## 5. local.properties + a build script

`local.properties` (never commit it):
```properties
sdk.dir=C:/Users/<user>/android-toolchain/sdk
```

Always build through a small script that exports the env, so every invocation is
identical:
```bash
#!/usr/bin/env bash
export JAVA_HOME="$HOME/android-toolchain/jdk-21.0.12+8"
export ANDROID_HOME="$HOME/android-toolchain/sdk"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
export PATH="$JAVA_HOME/bin:$PATH"
exec ./gradlew "$@"
```

## 6. Build

First build downloads Gradle + all dependencies — run it in the background:
`terminal(background=true, notify_on_complete=true)`, 15–25 min cold. Never pipe the
build through `tail`: it masks the real exit code.

```bash
./build.sh :app:assembleDebug --no-daemon --stacktrace
```

Verify the artifact instead of trusting the log:
```bash
ls -la app/build/outputs/apk/debug/*.apk
"$ANDROID_HOME/build-tools/35.0.0/aapt2.exe" dump badging app/.../app-debug.apk | head
```

### Prefer ONE verification pass over per-module checks

**PITFALL:** compiling module-by-module (`:core:audio:compileDebugKotlin`, then
`:feature:x:compileDebugKotlin`, …) to catch errors early generates a separate
background-job notification per run. Every intermediate failure you already fixed
gets replayed later as an alarming-looking `BUILD FAILED`, and you waste turns
re-verifying fixes that already landed.

`:app:assembleDebug` **transitively compiles every module the app depends on**, so a
single task covers the whole graph. Write a `verify.sh` that does everything at once
and prints one consolidated report:

```bash
./gradlew :app:assembleDebug test --no-daemon
# then, in the same script:
#   - aggregate tests="N" failures="N" from **/test-results/**/*.xml
#   - assert the APK file exists (exit 1 if gradle "succeeded" with no artifact)
#   - aapt2 dump badging   -> package name, minSdk, launchable activity
#   - apksigner verify     -> signature present
#   - aapt2 dump xmltree   -> count registered components
```

Use per-module compiles only when actively iterating on one module's errors, and
prefer a foreground call with a short timeout so no notification is queued.

## 7. Robolectric: Compose UI tests without an emulator

Compose UI tests normally need a device. Robolectric runs them on the JVM so they
execute inside plain `./gradlew test`:

```kotlin
// module build.gradle.kts
android { testOptions { unitTests { isIncludeAndroidResources = true } } }

testImplementation(libs.robolectric)
testImplementation(libs.androidx.junit)
testImplementation(platform(libs.androidx.compose.bom))
testImplementation(libs.androidx.compose.ui.test.junit4)
testImplementation(libs.androidx.compose.ui.test.manifest)   // NOT debugImplementation
debugImplementation(libs.androidx.compose.ui.test.manifest)
```

```kotlin
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [34])
class MyTest {
    @get:Rule val composeRule = createComposeRule()
}
```

**PITFALL:** putting `ui-test-manifest` on `debugImplementation` only makes
`testDebugUnitTest` pass while `testReleaseUnitTest` fails every Compose test with
`RuntimeException: Unable to resolve activity for Intent { ... ComponentActivity }`.
`./gradlew test` runs *both* variants. Add it to `testImplementation` as well.

Set `@Config(sdk = [34])`; Robolectric 4.13 has no SDK 35 jar yet.

## 8. Release signing + App Bundle

Keep credentials out of the build file, and let a fresh clone still build:

```kotlin
val keystorePropertiesFile = rootProject.file("keystore.properties")
val keystoreProperties = Properties().apply {
    if (keystorePropertiesFile.exists()) { keystorePropertiesFile.inputStream().use { load(it) } }
}
val hasSigningConfig = keystoreProperties.containsKey("storeFile")

signingConfigs {
    if (hasSigningConfig) {
        create("release") {
            storeFile = rootProject.file(keystoreProperties.getProperty("storeFile"))
            storePassword = keystoreProperties.getProperty("storePassword")
            keyAlias = keystoreProperties.getProperty("keyAlias")
            keyPassword = keystoreProperties.getProperty("keyPassword")
            enableV1Signing = true; enableV2Signing = true
            enableV3Signing = true; enableV4Signing = true
        }
    }
}
```

Generate the key with the portable JDK's keytool, and gitignore `*.jks`,
`keystore/`, and `keystore.properties`:

```bash
"$JAVA_HOME/bin/keytool" -genkeypair -v -keystore keystore/release.jks \
  -alias myalias -keyalg RSA -keysize 4096 -validity 10950 \
  -storepass ... -keypass ... -dname "CN=App, O=Org, C=US"
```

Verify the **bundle's** signer (apksigner does not read .aab):
```bash
"$JAVA_HOME/bin/keytool" -printcert -jarfile app/build/outputs/bundle/release/app-release.aab
```
## 9. Emulator provisioning (headless, no Android Studio)

Check virtualization first — without it the emulator is unusably slow:
```bash
powershell.exe -NoProfile -Command "(Get-CimInstance Win32_ComputerSystem).HypervisorPresent"
```

Install and create the AVD. **PITFALL:** `AvdManagerCli` uses a DIFFERENT system
property than `SdkManagerCli` — `com.android.sdkmanager.toolsdir`, not
`com.android.sdklib.toolsdir`. The wrong one fails with "The tools directory
property is not set".

```bash
CT="$ANDROID_HOME/cmdline-tools/latest"
# sdkmanager:
java -Dcom.android.sdklib.toolsdir="$CT" -classpath "$CT/lib/*" \
  com.android.sdklib.tool.sdkmanager.SdkManagerCli --sdk_root="$ANDROID_HOME" \
  "emulator" "system-images;android-35;google_apis;x86_64"
# avdmanager (note the different property):
echo "no" | java -Dcom.android.sdkmanager.toolsdir="$CT" -classpath "$CT/lib/*" \
  com.android.sdklib.tool.AvdManagerCli create avd -n test_avd \
  -k "system-images;android-35;google_apis;x86_64" -d pixel_6 --force
```

Boot headless (background process; first cold boot takes minutes):
```bash
"$ANDROID_HOME/emulator/emulator.exe" -avd test_avd -no-window -no-audio \
  -no-boot-anim -no-snapshot -gpu swiftshader_indirect -memory 3072 -wipe-data
```
Readiness is `adb shell getprop sys.boot_completed` returning `1` — never a blind sleep.

## 10. Instrumented tests: three traps that cost real time

**TRAP 1 — "Starting 0 tests" then BUILD FAILED.** AGP's default Kotlin source roots
cover `main` and unit tests but NOT `androidTest`. With sources in
`src/androidTest/kotlin/`, the suite compiles to nothing. Verify with
`find app/build -path "*androidTest*" -name "*.class" | wc -l` — zero means the source
set is unregistered. Fix once in the convention plugin:
```kotlin
sourceSets.configureEach { java.srcDir("src/$name/kotlin") }
```

**TRAP 2 — an emulator AND a phone both attached.** AGP shards across every connected
device; a device that receives an empty shard reports "Starting 0 tests" and fails the
whole build even when the other device passes 10/10. Kill one (`adb emu kill`) or
target explicitly.

**TRAP 3 — `HiltTestApplication` replaces your `@HiltAndroidApp` class.** Anything done
in `Application.onCreate` (DB seeding, notification channels) does NOT run under
`@HiltAndroidTest`. Seed defensively from the ViewModel/repository instead, and use
`composeRule.waitUntil { ... }` rather than bare assertions, since seeding is async.

## 11. Getting the truth out of a device UI

When a Compose assertion fails on-device, dump the real semantics tree instead of
guessing:
```kotlin
val tree = composeRule.onRoot().printToString(maxDepth = 100)
File("/sdcard/Download/dump.txt").writeText(tree)   // survives package uninstall
```
Then `adb pull /sdcard/Download/dump.txt`. Do NOT route long dumps through logcat —
it truncates lines and rotates, silently losing most of the output. The app's
`getExternalFilesDir()` is wiped when the test APK is uninstalled after the run;
`/sdcard/Download` is not.

The most common false failure: items in a `LazyColumn`/`LazyRow` that are scrolled
off screen have NO semantics node. `onNodeWithText("Music")` fails even though the row
exists in the database. Assert on a visible header/count, or scroll the item into view
first — do not "fix" working production code to satisfy the assertion. On landscape or
short-viewport devices this is especially severe because the visible viewport is small;
see `references/compose-landscape-scroll-trap.md` for the full diagnosis recipe and
the `user_rotation 0` lock that makes it go away.

## 12. Read the model before writing tests against it

Writing a test suite from memory of a data class costs more time than reading it.
Four separate compile failures in one session came from assumed API surface:
`DeviceKind.SMART_SPEAKER` (real value: `SPEAKER`), package `model.session` (real:
`model.mixer`), `SpatialSettings` (real: `SpatialAudioSettings`), and
`DeviceTransport.displayName` (plain enum, no such property).

Cheap reconnaissance before writing any test file:
```bash
# exact fields of a data class
sed -n '/^data class AppSettings/,/^)/p' path/To/File.kt
# enum members
sed -n '/enum class DeviceKind/,/^}/p' path/To/File.kt | grep -oE "^    [A-Z_]+"
# ViewModel constructor deps + public API, all modules at once
grep -A20 "class .*ViewModel @Inject constructor" **/*ViewModel.kt
```
Add shared test dependencies in the **convention plugin**, not per module — one edit
to `AndroidFeatureConventionPlugin` gave all 9 feature modules Robolectric.

## 13. Testing the MINIFIED release build

A green debug suite says nothing about the binary users install. R8 breaks
reflection-based code paths at runtime only, in release only.

```bash
./gradlew :app:connectedAndroidTest -PtestBuildType=release
```

The task name is NOT `connectedFullReleaseAndroidTest` unless the module reads
`-PtestBuildType=release` via `testBuildType = findProperty("testBuildType")` —
without the property the only task that exists is `connectedFullDebugAndroidTest`.
Pass the property or `./gradlew :app:tasks` shows nothing matching.

The key insight: an instrumented test APK runs **inside the app's process and links
against the app's dex**, so the app's keep rules must preserve everything the test APK
references — including code the app never calls. `-keepnames` is insufficient (it still
allows shrinking).

Know where to stop: keep rules are right for YOUR reflective code (services, tiles,
receivers, Hilt factories, ViewModel `@Inject` constructors), but chasing
`compose-ui-test`'s reach into Compose internals never converges. Minify what you ship;
run Compose UI assertions unminified.

### Local-device traps that cost real time

**TRAP A — MIUI/HyperOS blocks instrumented activity launches AND ignores overlay permission as an exemption.** Xiaomi phones refuse "background activity starts" for test-installed apps: logcat shows `Abort background activity starts from <uid>` and every Compose test hangs in `waitForIdle()` with the launcher focused, because the app's Activity was never given the foreground. Attempted fixes that do NOT hold: `appops set ... allow` for `START_ACTIVITIES_FROM_BACKGROUND` (10021) / `RUN_ANY_IN_BACKGROUND`, `settings put global background_activity_starts_enabled 1/0`, `dumpsys deviceidle whitelist +pkg`, and — critically — `SYSTEM_ALERT_WINDOW: allow`. MIUI SmartPower ignores the AOSP overlay exemption entirely; it does not consult `SYSTEM_ALERT_WINDOW` when deciding whether to abort. The pragmatic answer is to run instrumented tests on an AVD instead of a MIUI phone — and detach the phone first, or AGP shards across both and the phone's empty shard fails the build. `adb disconnect <serial>` works even for USB devices.

**TRAP A2 — MIUI resets appops on every UTP reinstall, including `SYSTEM_ALERT_WINDOW`.** After a successful `adb install`, `appops get pkg` shows `SYSTEM_ALERT_WINDOW: allow`, but once the test harness cycle kicks off and UTP pushes the test APK, MIUI immediately resets it to `SYSTEM_ALERT_WINDOW: ignore` with `rejectTime=+<N>ms ago`. Setting it before the run (`appops set pkg SYSTEM_ALERT_WINDOW allow`) does not help — the reset happens before the first `startActivity` from the test runner. Any future "appops survive reinstall" assumption is wrong on MIUI.

**TRAP A3 — MIUI's USB install gate requires on-device confirmation.** `INSTALL_FAILED_USER_RESTRICTED: Install canceled by user` blocks `adb install` entirely. The on-device unlock is either: (a) tap the prompt when it appears, or (b) Developer options → "Install via USB" (some MIUI versions also expose `settings put global install_via_adb_enabled 1`, but this alone does NOT override the user-confirmation gate). Once the user has approved one install, subsequent `adb install -r` updates succeed without re-prompting. The `com.soniccore.debug` flavor is treated as a separate package and may trigger the confirmation independently of the release flavor.

**TRAP B — a fresh AVD boots with NO permissions granted.** The app requests
permissions itself; the GrantPermissionsActivity dialog lands on top of MainActivity,
pauses it, and the first `waitForIdle()` throws "No compose hierarchies found in the
app" for every test that touches Compose — every Compose test fails identically even
though the non-UI tests pass. Pre-grant before the run (the test suite deliberately
has no GrantPermissionRule because granting mid-run restarts the process):

```bash
adb shell pm install -r app/build/outputs/apk/<flavor>/debug/app-<flavor>-debug.apk
adb shell pm grant com.soniccore.debug android.permission.RECORD_AUDIO
# also POST_NOTIFICATIONS, BLUETOOTH_CONNECT, BLUETOOTH_SCAN as the app requests them
```
(The `MODIFY_AUDIO_SETTINGS` grant FAILS with SecurityException — that's normal, it is
not a runtime-grantable permission.)
Note the DEBUG appId carries the `.debug` suffix (`com.soniccore.debug`); the release
build is `com.soniccore` — grant BOTH or the other variant's Compose tests all fail.

**TRAP C — `@AndroidEntryPoint` receivers crash the whole process on real broadcasts.**
The generated `Hilt_*Receiver.inject()` runs before `onReceive` and throws "The
component was not created. Check that you have added the HiltAndroidRule" whenever the
DI component doesn't exist yet. Under instrumented tests the component is created
per-test by `HiltAndroidRule`, so a genuine `MY_PACKAGE_REPLACED`/`BOOT_COMPLETED`
broadcast delivered when UTP installs the APK over a previous session kills the entire
run with `Instrumentation run failed due to Process crashed` before a single test
executes. Fix in production code, not tests: drop `@AndroidEntryPoint` from receivers
and resolve dependencies lazily:

```kotlin
@EntryPoint
@InstallIn(SingletonComponent::class)
interface ReceiverEntryPoint {
    fun automationEngine(): AutomationEngine
}

private fun resolveEngine(context: Context): AutomationEngine? = runCatching {
    EntryPointAccessors.fromApplication(context.applicationContext, ReceiverEntryPoint::class.java)
        .automationEngine()
}.getOrNull()
```
A receiver then degrades to a no-op until DI exists — also correct for direct boot and
process-restored-for-a-broadcast edge cases.

**TRAP D — UTP install can time out.** `ShellCommandUnresponsiveException` during
split-APK install (test APK) produces `tests=0` with a `Tool failures` entry in the
HTML report and `BUILD FAILED` after ~5 min. Use `-Pandroid.adbOptions.timeOutInMs=120000`.

See `references/testing-minified-release-builds.md` for the complete rule set, the
converging debug loop, and the traps around GrantPermissionRule, permission timing vs
`setContent`, colliding applicationIds, and orphaned UTP file locks.

## 14. Releasing to GitHub and F-Droid

F-Droid forbids non-free dependencies (Cast, Firebase, Play Billing, Maps, ML Kit). Solve
it with product flavors, not a fork: `foss` binds a no-op behind an interface, `full` binds
the real SDK, and the dependency is declared `"fullImplementation"(...)`.

Two traps that silently defeat the whole exercise:

- `missingDimensionStrategy(..., "full", ...)` pins flavorless modules to the
  Play-Services variant. Declare the flavor dimension in the **library convention plugin**
  so every module follows the app instead.
- SDK `meta-data` in the main manifest points at a class the FOSS build lacks. Move it to
  `app/src/full/AndroidManifest.xml`.

Verify purity from the compiled dex in CI, never from the config:
`unzip -p app-foss.apk classes.dex | grep -c 'com/google/android/gms'` must be 0.

Also: audit permissions from the manifest rather than memory, and confirm
`assembleFossRelease` succeeds with `keystore.properties` absent (F-Droid builds unsigned).

Full recipe: `references/fdroid-and-github-release.md`

A green debug suite says nothing about the binary users install. R8 breaks
reflection-based code paths at runtime only, in release only.

```bash
./gradlew :app:connectedAndroidTest -PtestBuildType=release
```

The key insight: an instrumented test APK runs **inside the app's process and links
against the app's dex**, so the app's keep rules must preserve everything the test APK
references — including code the app never calls. `-keepnames` is insufficient (it
still allows shrinking).

See `references/testing-minified-release-builds.md` for the complete set of keep rules
this required (androidx.tracing, Kotlin stdlib + coroutines, Compose
runtime/semantics INSTANCE fields, Dagger generated factories, Hilt component
interfaces, ViewModel `@Inject` constructors), the converging debug loop, and the
traps around GrantPermissionRule, permission timing vs `setContent`, colliding
applicationIds, and orphaned UTP file locks.


## 15. Retrofitting i18n onto a finished Compose app

Hundreds of near-identical edits, so script it — but a naive regex silently corrupts copy.

The trap that matters: Compose wraps long strings as `"part one " + "part two"`. Replacing
only the first literal leaves `stringResource(R.string.key) + "part two"` — a **broken
sentence that still compiles**. Detect with
`stringResource\(R\.string\.(\w+)\)\s*\+\s*\n?\s*"` and loop until zero remain.

Also: exclude `$` from the match pattern (interpolated strings need format args), escape
apostrophes and bare `%` for aapt2, use plurals for counts (never `"$n item(s)"`), and
remember `stringResource` is `@Composable` — Services/tiles/widgets need `getString`.

Prove it with `aapt2 dump resources | grep -A3 'string/<key>'` plus an on-device test using
`createConfigurationContext`, which needs no UI and so runs behind a keyguard.

Full recipe: `references/extracting-strings-to-resources.md`

## Pitfalls

- **Compile-only is enough for verification** — no emulator/device needed; `assembleDebug`
  proves the whole codebase compiles and links.
- Add `org.gradle.jvmargs=-Xmx4g` to `gradle.properties`; Kotlin+KSP OOMs at the 512m default.
- Kotlin 2.x requires the `compose-compiler` Gradle plugin (`org.jetbrains.kotlin.plugin.compose`);
  the old `composeOptions { kotlinCompilerExtensionVersion }` block is gone.
- `--no-daemon` avoids stale daemons holding file locks on Windows between runs.
- If the wrapper jar download is blocked, `gradle-wrapper.jar` can be extracted from any
  Gradle distribution zip under `lib/plugins/`.
