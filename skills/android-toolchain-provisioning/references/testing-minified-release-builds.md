# Testing a MINIFIED release build on a device

Everything you verify in `debug` says nothing about the binary users install. R8
shrinks, optimizes and obfuscates, and the failures it introduces appear **only at
runtime, only in release**. This is the checklist for closing that gap.

## Why it matters

A debug suite can be 100% green while the release APK is broken, because R8 removes
code that is only reached reflectively or from *another* APK. Symptoms are always
`NoClassDefFoundError`, `ClassNotFoundException`, `NoSuchMethodException`,
`NoSuchFieldError` or `ClassCastException` — never a compile error.

## Setup

```kotlin
// app/build.gradle.kts
android {
    // -PtestBuildType=release runs connectedAndroidTest against the minified APK
    testBuildType = (project.findProperty("testBuildType") as String?) ?: "debug"

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            testProguardFiles("proguard-test-rules.pro")   // rules for the TEST apk
        }
    }
}
```

```bash
./gradlew :app:connectedAndroidTest -PtestBuildType=release
```

## The core insight

**An instrumented test APK runs inside the app's process and links against the app's
dex.** So the app's R8 config must preserve everything the *test* APK references —
even code the app itself never calls. `-keepnames` is NOT enough: it preserves names
but still lets R8 **shrink** unused classes, so each fix just surfaces the next
missing class. Keep the whole package.

## Keep rules the release build actually needed

Found empirically, each one from a real crash on a Nokia 7.2 / Android 11:

```proguard
# 1. androidx.tracing.Trace — resolved reflectively by androidx.test + profileinstaller
-keep class androidx.tracing.** { *; }
-keep class androidx.profileinstaller.** { *; }
-keep class androidx.startup.** { *; }

# 2. Kotlin stdlib + coroutines. androidx.test / compose-ui-test are Kotlin code and
#    reference kotlin.LazyKt, kotlinx.coroutines.JobKt,
#    kotlinx.coroutines.DelayWithTimeoutDiagnostics ... which the app never calls.
-keep class kotlin.** { *; }
-keep class kotlinx.coroutines.** { *; }

# 3. Compose runtime/platform/semantics. compose-ui-test needs
#    InfiniteAnimationPolicy, MonotonicFrameClock$DefaultImpls, and the INSTANCE
#    singletons of SemanticsProperties (hasText/onNodeWithText read them):
#      NoSuchFieldError: No field INSTANCE of type Ll0/t;
-keep class androidx.compose.ui.platform.** { *; }
-keep class androidx.compose.runtime.** { *; }
-keep class androidx.compose.ui.semantics.** { *; }
-keepclassmembers class androidx.compose.** { public static ** INSTANCE; }

# 4. Lifecycle/activity — ViewTreeLifecycleOwner et al.
-keep class androidx.lifecycle.** { *; }
-keep class androidx.activity.** { *; }
-keep class androidx.savedstate.** { *; }

# 5. Dagger internals + GENERATED code. The test dex has its own generated component
#    that instantiates the app's factories by name:
#      ClassNotFoundException: com.x.di.AudioModule_ProvideContextFactory
-keep class dagger.** { *; }
-keep class dagger.internal.** { *; }
-keep class hilt_aggregated_deps.** { *; }
-keep class com.yourapp.**_Factory { *; }
-keep class com.yourapp.**_MembersInjector { *; }
-keep class com.yourapp.**Module_* { *; }

# 6. Hilt generated component INTERFACES. Under @HiltAndroidTest the component is
#    DaggerDefault_HiltComponents_* and is cast to *_HiltComponents:
#      ClassCastException: ...SingletonC$ActivityCImpl cannot be cast to com.x.a
-keep class com.yourapp.*_HiltComponents* { *; }
-keep class **.Hilt_* { *; }
-keep class dagger.hilt.android.internal.testing.** { *; }

# 7. ViewModels are constructed reflectively; R8 drops the @Inject constructor:
#      NoSuchMethodException: com.x.feature.dashboard.G.<init> []
-keep class * extends androidx.lifecycle.ViewModel { <init>(...); *; }
-keepclasseswithmembers class * { @javax.inject.Inject <init>(...); }
```

And in `proguard-test-rules.pro`:

```proguard
-keep class org.junit.** { *; }
-keep class androidx.test.** { *; }
-keep class com.yourapp.**Test { *; }
-keepclassmembers class com.yourapp.** { @org.junit.Test *; @org.junit.Rule *; }
-keep class dagger.hilt.android.testing.** { *; }
# Compile-only annotations that never exist at runtime; R8 hard-errors without these:
-dontwarn com.google.auto.value.**
-dontwarn javax.lang.model.**
-dontwarn com.google.errorprone.annotations.**
```

## Debugging loop that actually converges

1. Run the instrumentation **directly**, not through Gradle — you get the real
   exception instead of "Starting 0 tests":
   ```bash
   adb install -r -t app/build/outputs/apk/release/app-release.apk
   adb install -r -t app/build/outputs/apk/androidTest/release/app-release-androidTest.apk
   adb shell am instrument -w com.yourapp.test/com.yourapp.TestRunner
   ```
2. Read the FIRST `Caused by:` line. That names the exact missing class.
3. Check whether it is present in the dex before writing a rule:
   ```python
   import zipfile
   z = zipfile.ZipFile(apk)
   blob = b"".join(z.read(n) for n in z.namelist() if n.endswith(".dex"))
   print(b"Lkotlin/LazyKt;" in blob)
   ```
   Present in the test dex but absent from the app dex == a keep-rule gap.
4. `mapping/release/usage.txt` lists what R8 REMOVED; `seeds.txt` lists what it KEPT.
   Grep both before guessing.

## Verify the components, not just the screens

The highest-value release test is not a UI test — it is checking that every manifest
component still resolves, because the framework instantiates them **by name string**:

```kotlin
val info = pm.getServiceInfo(ComponentName(context, MyService::class.java), 0)
assertEquals("android.permission.BIND_QUICK_SETTINGS_TILE", info.permission)
cls.getDeclaredConstructor().newInstance()   // proves it survived obfuscation
```

This suite (services, tiles, receivers, widget, Cast OptionsProvider meta-data)
passed 15/15 under R8 and is what actually proves the shipped binary is wired up.

## Known unresolved boundary

*(RESOLVED — see "Check the device before you bisect the code" below.)*

## Where to STOP adding keep rules

Two different problems hide behind the same-looking errors, and only one is worth
solving with keep rules:

**1. YOUR code + reflective framework entry points — fix with keep rules.** Services,
tiles, receivers, widgets, Hilt factories, ViewModel `@Inject` constructors, the Cast
`OptionsProvider`. These are finite, and a `ComponentResolutionTest` proves them under
full R8. All the rules above belong here.

**2. `compose-ui-test` reaching into Compose internals — do NOT chase.** It calls
`SemanticsNode.getParentInfo()`, reads `SemanticsProperties.INSTANCE`, needs
`MonotonicFrameClock$DefaultImpls`. R8's **optimizer** rewrites these even when
`-keep` preserves the class, so every fix surfaces the next `NoSuchMethodError`. It
does not converge, and loosening the shipping config (e.g. `-optimizations
!method/removal/*`) to satisfy a test harness is the wrong trade.

The right split — minify what you ship, don't minify what you point the UI suite at:

```kotlin
release {
    val testingRelease = project.findProperty("testBuildType") == "release"
    isMinifyEnabled = !testingRelease
    isShrinkResources = !testingRelease
    proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
    testProguardFiles("proguard-test-rules.pro")
}
```

Coverage then comes from three angles, each doing what it is good at:

| What | How | Proves |
|---|---|---|
| App's reflective wiring under R8 | `ComponentResolutionTest`, release variant | 13/13 manifest components resolve + instantiate obfuscated |
| The shipped binary actually runs | install the real minified APK, launch it | 0 NoClassDef/NoSuchMethod/NoSuchField at runtime |
| UI behaviour | Compose tests, unminified | screens, navigation, state |

Verify the shipped artifact really is minified (do not assume):

```python
lines = [l for l in open("mapping/release/mapping.txt") if "->" in l and not l.startswith(" ")]
short = [l for l in lines if len(l.split("->")[1].strip().rstrip(":")) <= 4]
print("MINIFIED:", len(short) > 500)   # 2875/11228 on this project
```

```bash
adb install -r app/build/outputs/apk/release/app-release.apk
adb shell am start -W -n pkg/.MainActivity
adb shell dumpsys activity top | grep -c ComposeView          # non-zero
adb logcat -d | grep -icE "FATAL|NoClassDef|NoSuchMethod|NoSuchField"   # must be 0
```

## Check the device BEFORE you bisect the code

`IllegalStateException: No compose hierarchies found in the app` is usually **not** an
app bug. Compose instrumented tests need a **visible, unlocked** window. On a dozing or
locked device the Activity reaches RESUMED and is paused by the keyguard ~50 ms later,
and every Compose assertion fails — while service/receiver/component tests keep passing
because they need no window.

The tell is the split: if *only* the Compose tests fail and non-UI instrumented tests
pass, suspect the device, not the source.

```bash
adb shell dumpsys power  | grep -oE "mWakefulness=[A-Za-z]+"      # want Awake, not Dozing
adb shell dumpsys window | grep -oE "isKeyguardShowing=(true|false)"  # want false
adb shell getprop sys.boot_completed                              # want 1
adb shell input keyevent KEYCODE_WAKEUP
adb shell svc power stayon true                                   # keep it awake
```

A PIN/pattern keyguard cannot be cleared over adb — it needs a manual unlock. Verify
the app itself is fine with:

```bash
adb shell am start -n pkg/.MainActivity
adb shell dumpsys activity top | grep -c ComposeView    # non-zero == hierarchy exists
```

**Write this as a precondition script** and run it before any instrumented suite.
I burned roughly an hour bisecting source — reverting two correct production fixes
along the way — because I never checked whether the phone screen was on. The check
takes one second.

## Other traps

- **Do NOT add `GrantPermissionRule` alongside a Compose rule.** Granting a permission
  the app does not already hold restarts the process, destroying the Activity the
  Compose rule awaits — every test then reports "No compose hierarchies found".
- **Request runtime permissions AFTER `setContent`.** Before it, the dialog appears
  while the window is still forming; the Activity goes RESUMED -> PAUSED in ~50 ms.
- **Debug and release `applicationId`s must not collide on device.** Installing the
  release APK over a debug install (or vice versa) leaves a package/test-package
  mismatch and `Unable to find instrumentation info`. `adb uninstall` both first.
- **Orphaned UTP processes lock the results directory.** After a killed run, Gradle
  fails with `Unable to delete directory ... androidTest-results`. Find it with
  `jps -l` (look for `com.google.testing.platform.launcher.Launcher`) and kill it.
- **A foreground service must create its notification channel itself.** Under
  `HiltTestApplication` the real Application never runs, and a missing channel makes
  `startForeground` throw `RemoteServiceException: Bad notification for
  startForeground`, killing the process on a real device.
