---
name: soniccore-redmi-jbl-debug
description: Debug SonicCore JBL routing errors on Xiaomi/MIUI/HyperOS.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [soniccore, redmi, jbl]
---

# SonicCore Redmi + JBL MIUI Debug Skill

## When to use
- SonicCore shows error connecting to JBL speaker or invalid device type 8 on a Xiaomi/MIUI/HyperOS device.
- AudioRouter.routeCommunicationTo() throws IllegalArgumentException invalid device type 8 in logcat when tapping a Bluetooth A2DP device.
- Bluetooth A2DP devices are missing from the Devices screen on MIUI.

## Hard prerequisites
- Primary test target is the user's real phone. Do NOT switch to AVD for primary diagnosis.
- No phone reboots unless the user explicitly agrees.
- Do not change phone system settings without explicit permission.
- Every install may require user confirmation on MIUI if install_via_adb_enabled=1 and adb_install_need_confirm=0 are not set.

## Device preparation
```bash
ADB="/c/Users/Server/soniccore-toolchain/sdk/platform-tools/adb.exe"
"$ADB" -s <serial> shell svc power stayon true
"$ADB" -s <serial> shell settings put system screen_off_timeout 1800000
```

## Runtime permissions (grant out-of-band before testing)
```bash
"$ADB" -s <serial> shell pm grant com.soniccore.debug android.permission.RECORD_AUDIO
"$ADB" -s <serial> shell pm grant com.soniccore.debug android.permission.BLUETOOTH_CONNECT
"$ADB" -s <serial> shell pm grant com.soniccore.debug android.permission.POST_NOTIFICATIONS
```
Note: MODIFY_AUDIO_SETTINGS is a normal permission; pm grant will throw SecurityException. That is expected and harmless.

## Build and install
```bash
cd "$HOME/SonicCore"
bash build.sh :app:assembleFullDebug --no-daemon --rerun-tasks
"$ADB" -s <serial> install -r -t C:/Users/Server/SonicCore/app/build/outputs/apk/full/debug/app-full-debug.apk
```

## Activate debug logging
Ensure AudioRouter.kt contains Log.d("AudioRouter", ...) statements in:
- routeCommunicationTo
- findSystemDevice lookup
- setCommunicationDevice success/failure/exception paths

Rebuild and reinstall after adding logs.

## Live logcat capture
```bash
"$ADB" -s <serial> logcat -c
"$ADB" -s <serial> logcat -s AudioRouter:D SonicCore:D
```
Filter specifically for:
- routeCommunicationTo:
- findSystemDevice:
- setCommunicationDevice threw

## UI state inspection
If the error auto-dismisses and cannot be kept open:
```bash
"$ADB" -s <serial> shell uiautomator dump /sdcard/Download/ui.xml
"$ADB" -s <serial> shell cat /sdcard/Download/ui.xml | grep -oE 'text="[^"]{1,160}"'
```

To programmatically tap the JBL device card (no user interaction needed):
```bash
# First dump UI to confirm JBL bounds, then tap center of card
"$ADB" -s <serial> shell input tap <x> <y>
```

## Audio state verification
```bash
"$ADB" -s <serial> shell dumpsys audio | grep -E "Devices:|Active communication|bt_a2dp"
```
Success indicators:
- Devices: bt_a2dp(80) appears
- JBL Go 3 appears as active communication device or A2DP device

## Confirmed root cause on MIUI/HyperOS
Root cause is confirmed: on this Redmi, MIUI reports the JBL Go 3 as AudioDeviceInfo type 8, and AudioService.setCommunicationDevice() throws IllegalArgumentException: invalid device type: 8.
The app-side mitigation is already in AudioRouter.kt: the S+ path catches that exact MIUI quirk and treats it as success instead of showing an error.
I rebuilt with --no-build-cache, verified the fix is in the APK, installed it, and tested on the Redmi.

## Fix application
Edit core/audio/src/main/kotlin/com/soniccore/core/audio/routing/AudioRouter.kt.

### S+ path fix
Replace the runCatching audioManager.setCommunicationDevice(target) block with explicit try/catch:
```kotlin
return try {
    if (audioManager.setCommunicationDevice(target)) {
        RoutingResult.Success
    } else {
        RoutingResult.Failed("The system declined the routing request")
    }
} catch (e: IllegalArgumentException) {
    if (e.message?.contains("invalid device type", ignoreCase = true) == true &&
        device.transport in setOf(
            DeviceTransport.BLUETOOTH_CLASSIC,
            DeviceTransport.BLUETOOTH_LE,
        )
    ) {
        Log.d(
            "AudioRouter",
            "setCommunicationDevice threw invalid device type for BT device; treating as success because A2DP is handled by the platform",
        )
        RoutingResult.Success
    } else {
        Log.e("AudioRouter", "setCommunicationDevice threw", e)
        RoutingResult.Failed(e.message ?: "Routing failed")
    }
}
```

### Pre-31 path fix
Keep SCO calls individually guarded:
```kotlin
runCatching { audioManager.isSpeakerphoneOn = false }
runCatching { @Suppress("DEPRECATION") audioManager.stopBluetoothSco() }
runCatching { @Suppress("DEPRECATION") audioManager.isBluetoothScoOn = false }
return RoutingResult.Success
```

## Bluetooth A2DP enumeration fix
Ensure AudioDeviceRegistry / BluetoothInfoProvider uses:
```kotlin
BluetoothManager.getConnectedDevices(BluetoothProfile.A2DP)
```
to supplement AudioManager.getDevices() on MIUI, which can omit connected A2DP devices.

## Verification after fix
1. Rebuild with --rerun-tasks and clean build cache if stale: bash build.sh clean && bash build.sh :app:assembleFullDebug --no-daemon --rerun-tasks
2. Install APK.
3. Grant runtime permissions.
4. Launch SonicCore.
5. Tap JBL Go 3 programmatically or via UI.
6. Confirm via logcat that no AudioRouter: setCommunicationDevice threw appears.
7. Confirm via dumpsys audio that bt_a2dp remains active.
8. Confirm user no longer sees the error snackbar.

## Common pitfalls
- Stale APK: Always rebuild with --rerun-tasks after routing changes; Gradle build cache can serve old code.
- Windows file locking: If Gradle reports Couldn't delete R.jar or MD5 hash failures, kill stuck Java/Gradle processes and clear app/build/outputs/androidTest-results/.
- MIUI install gate: adb install may require user confirmation. If INSTALL_FAILED_USER_RESTRICTED appears, ask the user to enable install_via_adb_enabled=1 and adb_install_need_confirm=0.
- Permission controller blocking foreground: After pm clear, MIUI may show GrantPermissionsActivity on top. Dismiss with KEYCODE_ESCAPE before relaunching the app.
- Logcat noise: Use logcat -c before each capture. Filter with -s AudioRouter:D SonicCore:D.

## Permanent reference
Full fix log for this device: docs/REDMI_JBL_FIX_LOG.md

## Related topic: discovered network-speaker streamers
Use this when a discovered network device shows: "uses a protocol SonicCore cannot stream to yet".
Gap: WifiSpeakerDiscovery can surface DLNA, Spotify Connect, or generic network targets, but the streaming layer may not have streamers for them.

Current defaults in SonicCore's streaming module:
- CHROMECAST: CastStreamer
- AIRPLAY / SONOS: AirPlayAudioStreamer
- DLNA: DlnaAudioStreamer
- SPOTIFY_CONNECT: SpotifyConnectStreamer
- GENERIC / unknown/null: GenericNetworkStreamer

Temporary check: If a network device still shows unsupported, confirm its protocol mapping in `StreamingCoordinator.protocolFor(...)` and `StreamingCoordinator.streamerFor(...)`.
FOSS-safe approach: intent-based fallback streamers; they do not require closed-source SDKs, but they do connect instead of dead-ending.
