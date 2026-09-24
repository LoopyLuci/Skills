---
name: android-oem-audio-workarounds
version: 1.0.0
author: Hermes
license: MIT
description: Workaround Android OEM audio routing type mismatches.
metadata:
  hermes:
    tags: [android, audio, bluetooth, miui, workaround, oem]
    related_skills: [android-audio-device-control, android-instrumented-testing]
---

# Android OEM Audio Routing Workarounds

## When to Use

When an Android app correctly routes audio on AOSP/reference devices but breaks on
a specific OEM ROM (MIUI/HyperOS, OneUI, ColorOS) due to divergent implementations
of `AudioManager` / `AudioDeviceInfo`, device-type reporting mismatches, or
proprietary background-activity policies. Workarounds are **not portable** — guard
them with runtime ROM detection.

See `references/miui-audio-routing-errors.md` for raw logcat transcripts and
device dumps from the Redmi Note 12 Pro 5G investigation.

## Confirmed device under test
- **Phone:** Redmi Note 12 Pro 5G, model 22101316G
- **OS:** MIUI V816 / HyperOS, Android 14 (`ro.build.version.sdk=34`)
- **ADB serial:** `5xrsuka6gisgqgh6`
- **Speaker:** JBL Go 3 (A2DP)

## The MIUI A2DP/SCO type mismatch

### Symptom

1. The `JBL Go 3` Bluetooth speaker is paired and connected at the system level.
2. `dumpsys audio` confirms correct routing: `bt_a2dp(80)` is active and
   `Active communication device: bt_a2dp name=JBL Go 3`.
3. The app enumerates the device and shows it in the Devices UI (via
   `BluetoothManager.getConnectedDevices(A2DP)`).
4. When the user taps the device to select it for routing, a snackbar error
   appears: **"invalid device type: 8"**.
5. `AudioManager.getDevices()` reports the JBL as `TYPE_BLUETOOTH_SCO` (type 8)
   instead of `TYPE_BLUETOOTH_A2DP` (type 80).

This affects **both** routing paths:
- pre-API-31: `stopBluetoothSco()` throws because type 8 is not valid for an
  A2DP media device.
- API 31+: `setCommunicationDevice()` throws `IllegalArgumentException:
  invalid device type: 8` from `AudioService.setCommunicationDevice()` even
  though the same device is already correctly active as `bt_a2dp` in flinger.

### Root cause

MIUI's `AudioService` reports A2DP media speakers through the SCO device type in
the Java `AudioManager` API surface, while the native audio flinger correctly
routes media as A2DP. Calling `stopBluetoothSco()` (the pre-API-31 routing
primitive) throws because type 8 is not valid for an A2DP media device. On
newer MIUI builds the same type mismatch reaches `setCommunicationDevice()`.

Additionally, `AudioManager.getDevices()` on MIUI API 30 sometimes **omits**
connected Bluetooth A2DP devices entirely — requiring `BluetoothManager` as a
secondary enumeration source.

## Workarounds

### 1. Enrich device enumeration with BluetoothManager

```kotlin
@SuppressLint("MissingPermission")
fun getA2dpDevicesDirect(): List<BluetoothDeviceDetail> {
    val bluetoothManager = context.getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
    val a2dpDevices = bluetoothManager.getConnectedDevices(BluetoothProfile.A2DP)
    return a2dpDevices.map { device ->
        BluetoothDeviceDetail(
            stableKey = buildStableKey(device.address, DeviceType.BLUETOOTH_A2DP),
            name = device.name ?: "Unknown",
            address = device.address,
            type = DeviceType.BLUETOOTH_A2DP,
            transport = DeviceTransport.BLUETOOTH_CLASSIC,
            isConnected = true
        )
    }
}
```

`BluetoothManager.getConnectedDevices(BluetoothProfile.A2DP)` returns actual
`BluetoothDevice` objects with correct MAC addresses and names — no proxy callback
flow needed (synchronous, reliable across all OEMs).

### 2. Guard each SCO call individually in pre-31 routing

Never wrap all pre-31 routing calls in a single `runCatching` — one failing OEM-
specific call (like `stopBluetoothSco()` on MIUI) aborts the entire flow:

```kotlin
// WRONG — single try: one failure aborts all routing
return runCatching {
    audioManager.isSpeakerphoneOn = false
    audioManager.stopBluetoothSco()
    audioManager.isBluetoothScoOn = false
}.getOrElse { error -> RoutingResult.Failed(error.message ?: "Routing failed") }

// CORRECT — individual guards
if (device.transport == DeviceTransport.BLUETOOTH_CLASSIC ||
    device.transport == DeviceTransport.BLUETOOTH_LE) {
    // stopBluetoothSco() throws "invalid device type: 8" on MIUI — ignore
    runCatching { audioManager.stopBluetoothSco() }
    runCatching { audioManager.isBluetoothScoOn = false }
    runCatching { audioManager.isSpeakerphoneOn = false }
    // Platform routes A2DP media natively once SCO is disabled
    return RoutingResult.Success
}
```

**Never call `startBluetoothSco()` for A2DP speakers** — SCO opens a voice-call
channel, not the A2DP media path. On MIUI, SCO actively kills A2DP routing to
paired speakers.

### 3. Catch the MIUI S+ `setCommunicationDevice()` type-8 throw

On API 31+, MIUI can report a connected A2DP sink as `AudioDeviceInfo` type 8
and `AudioManager.setCommunicationDevice()` then throws:

```
IllegalArgumentException: invalid device type: 8
    at android.media.AudioManager.setCommunicationDevice(AudioManager.java:...)
    at com.android.server.audio.AudioService.setCommunicationDevice(AudioService.java:...)
```

The platform has already routed media correctly as `bt_a2dp`; this API path is
simply not usable for that device on MIUI. Convert that specific exception into
success for Bluetooth devices instead of surfacing it as a routing failure:

```kotlin
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
    return try {
        if (audioManager.setCommunicationDevice(target)) RoutingResult.Success
        else RoutingResult.Failed("The system declined the routing request")
    } catch (e: IllegalArgumentException) {
        if (e.message?.contains("invalid device type", ignoreCase = true) == true &&
            device.transport in setOf(
                DeviceTransport.BLUETOOTH_CLASSIC,
                DeviceTransport.BLUETOOTH_LE,
            )
        ) {
            RoutingResult.Success
        } else {
            RoutingResult.Failed(e.message ?: "Routing failed")
        }
    }
}
```

Only treat type-8 Bluetooth routes as success. Do not swallow other
`IllegalArgumentException` cases.

### 4. Verify on-device

```bash
# Confirm system-level connection
adb shell dumpsys bluetooth_manager | grep -A5 "JBL"
# Confirm audio routing (should show bt_a2dp active)
adb shell dumpsys audio | grep -E "Active communication device|bt_a2dp"
# Dump app UI
adb shell uiautomator dump /sdcard/ui.xml
adb shell cat /sdcard/ui.xml | grep -o 'text="[^"]*"' | grep -i "jbl"
```

## ROM detection

```kotlin
fun isMiui(): Boolean = try {
    Class.forName("miui.os.Build").isInitialized
} catch (e: Throwable) { false }
// Or check system property: ro.miui.ui.version.name (non-null on MIUI)
```

## Related

- `android-audio-device-control` — canonical routing patterns (API 31+ vs 23–30)
- `android-instrumented-testing` — SmartPower aborts and MIUI install gates

## Pitfalls

- **Don't wrap SCO calls in one `runCatching`** — individual guards let the
  platform-default A2DP route succeed even if SCO toggles fail.
- **SCO ≠ A2DP** — `startBluetoothSco()` is for voice calls; using it on an A2DP
  speaker tears down the media route on MIUI.
- **`AudioDeviceInfo.id` is unstable** across reconnects — key profiles on
  MAC address + product name, not the system-assigned ID.
- **Don't assume type 8 = SCO** — MIUI reports A2DP speakers at type 8. Use
  `BluetoothManager.getConnectedDevices(A2DP)` as the authoritative source.
- **Friendly names are not guaranteed on Xiaomi/mDNS/Bluetooth stacks.** On MIUI,
  mDNS/Spotify Connect entries can surface as model numbers or raw identifiers in
  the Devices UI. Apply display-name sanitization at the mapping layer so
  addresses/MACs/IPs/identifier-only strings do not reach the UI.
- **Wireless debugging reliability on HyperOS:** long ADB operations can exceed
  the Xiaomi keepalive window; keep the screen awake and prefer USB for
  repeated install/run loops.