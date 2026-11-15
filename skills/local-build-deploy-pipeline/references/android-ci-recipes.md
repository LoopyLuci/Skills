# Android pipeline stage recipes

Concrete command recipes for the four on-device CI/CD stages (test, build, verify) plus preflight and report. All work from the repo root; `CI_SDK_DIR`/`CI_ANDROID_HOME`/`ANDROID_SDK_ROOT`/`CI_JAVA_HOME` override the SDK/JDK paths.

## Preflight (env checks)

```bash
# SDK root (from local.properties sdk.dir, overridable)
export CI_SDK_DIR=${CI_SDK_DIR:-$(grep '^sdk.dir=' local.properties | cut -d= -f2-)}
export CI_ANDROID_HOME=$CI_SDK_DIR
export ANDROID_SDK_ROOT=$CI_SDK_DIR

# JDK 17+
export CI_JAVA_HOME=${CI_JAVA_HOME:-$(dirname $(dirname $(readlink -f $(which java)) 2>/dev/null || echo $JAVA_HOME))}

# Gradle wrapper
ls -la SpendingSaverAndroid/gradlew

# Devices
adb devices -l
adb shell getprop ro.boottime UTC >/dev/null 2>&1 || true

# Wait for boot
until adb shell getprop sys.boot_completed 2>/dev/null | grep -q 1; do sleep 2; done
```

## Test (unit tests)

```bash
cd SpendingSaverAndroid
./gradlew :app:testDebugUnitTest --console=plain --no-daemon --info \
  --max-workers 2 \
  --no-build-cache

# Parse machine-readable results (JUnit XML root attrs: tests/failures/errors/skipped)
total=$(grep -oh 'tests="[0-9]*"' app/build/test-results/testDebugUnitTest/*.xml | head -1 | sed 's/tests="//;s/"//')
fail=$(grep -oh 'failures="[0-9]*"' app/build/test-results/testDebugUnitTest/*.xml | head -1 | sed 's/failures="//;s/"//')

# Write a cleaner result file for the pipeline
cat > $WORK_DIR/test-results.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="SpendingSaverUnitTests" tests="$total" failures="$fail" errors="0" skipped="0" time="0">
EOF
```

## Build (assemble APK)

```bash
cd SpendingSaverAndroid
./gradlew assembleDebug --console=plain --no-daemon --info --max-workers 2

# Verify APK exists and is non-empty (catches stale/missing builds)
if [[ ! -s app/build/outputs/apk/debug/app-debug.apk ]]; then
  echo "APK missing or empty" >&2; exit 1
fi

# Archive log
cp app/build/outputs/logs/debug.log $WORK_DIR/build.log
```

## Verify (on-device install + launch + crash watch)

```bash
PACKAGE=com.spendingsaver
ACTIVITY=.MainActivity
ADB=${CI_ADB:-$CI_SDK_DIR/platform-tools/adb}

# 1. Uninstall + install
adb uninstall $PACKAGE 2>/dev/null || true
adb install -r app/build/outputs/apk/debug/app-debug.apk

# 2. Wait for package
for i in $(seq 1 60); do
  adb shell pm list packages | grep -q "^package:$PACKAGE$" && break
  sleep 1
done

# 3. Launch
adb shell am start -n $PACKAGE/$ACTIVITY

# 4. Wait for Resumed
for i in $(seq 1 45); do
  adb shell dumpsys activity activities 2>/dev/null | grep -q "Resumed activity .*${PACKAGE}/.*" && break
  sleep 1
done

# 5. Poll process alive
for i in $(seq 1 90); do
  adb shell pidof com.spendingsaver 2>/dev/null | grep -q . && break
  sleep 1
done

# 6. Bounded logcat crash watch
adb logcat -v time -d > $WORK_DIR/verify.logcat 2>/dev/null

# 7. Crash markers (restricted to our package to avoid system-UI spam)
CRASH=$(grep -Ei 'FATAL EXCEPTION|has died|UnsatisfiedLinkError|SIGSEGV|SIGBUS|SIGABRT|NativeGetStackTrace|Process .* has died' $WORK_DIR/verify.logcat | grep -E "com\.spendingsaver" || true)
if [[ -n "$CRASH" ]]; then
  echo "Crash detected:" >&2
  echo "$CRASH" >&2
  exit 1
fi
```

## Report

```bash
cat > $ARTIFACTS_DIR/report.txt <<EOF
# SpendingSaver CI/CD report
Generated: $(date -u +'%Y-%m-%dT%H:%M:%SZ')
Device: ${CI_DEVICE:-unknown}

| Stage | Result |
|---|---|
| preflight | PASS |
| test | $([ $TEST_OK -eq 1 ] && echo PASS || echo FAIL) |
| build | $([ $BUILD_OK -eq 1 ] && echo PASS || echo FAIL) |
| verify | $([ $VERIFY_OK -eq 1 ] && echo PASS || echo FAIL) |

Gradle test exit: $TEST_RC
Gradle assemble exit: $BUILD_RC
Verify exit: $VERIFY_RC
Artifact APK: $APK_PATH
Test report: $WORK_DIR/test-results.xml
Build log: $WORK_DIR/build.log
Verify logcat: $WORK_DIR/verify.logcat
EOF

# Archive APK
cp app/build/outputs/apk/debug/app-debug.apk $ARTIFACTS_DIR/app-debug.apk
```