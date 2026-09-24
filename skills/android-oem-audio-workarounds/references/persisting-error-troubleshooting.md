# User Reports Error Persists but Evidence Is Clean

Use this checklist when the user says the routing/runtime error is still present,
but your on-device verification shows clean logs and correct system routing.

## MIUI-specific causes

1. **Stale build/install state** — Gradle build cache on Windows can serve stale
   compiled classes/dex even with `--rerun-tasks`. When the fix seems ineffective:
   - delete the module `.gradle/` directory,
   - verify the fix symbol is present in the rebuilt APK dex,
   - reinstall the APK.
2. **adb install gate** — `INSTALL_FAILED_USER_RESTRICTED` on Xiaomi/HyperOS
   blocks uninstalls/reinstalls without on-device confirmation. Watch the phone
   for confirmation dialogs.
3. **uiautomator dump may be empty** — some MIUI builds write the dump file but
   populate no nodes. Treat empty dump output as inconclusive; rely on
   `dumpsys audio` + app logcat instead.
4. **SmartPower/system-kill side effects** — a background task may have been
   aborted shortly before your check. Verify foreground app focus and logcat
   for process-kill markers.
5. **Different interaction path** — the user may be tapping a different button
   or automation path than the one you tested. Confirm exact screen path or
   coordinates.

## Verification sequence

```bash
# 1. confirm package present
adb shell pm list packages | grep soniccore

# 2. confirm foreground app
adb shell dumpsys window | grep mCurrentFocus

# 3. clear logs, perform fresh tap, wait
adb shell input tap X Y
sleep 2

# 4. confirm routing at system level
adb shell dumpsys audio | grep -E "Active communication device|bt_a2dp"

# 5. check app logcat specifically
adb logcat -d | grep "com.soniccore"
```

## Preferred evidence

- system-level `dumpsys audio` showing `bt_a2dp` active
- app logcat without the old error string
- fresh APK with the fix symbol present in dex
