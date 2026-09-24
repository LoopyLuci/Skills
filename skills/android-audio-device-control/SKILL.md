---
name: android-audio-device-control
description: Control Android audio devices, routing, codecs, volume.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [android, audio, bluetooth, usb, kotlin]
---

# Android Audio Device Control

## When to Use

Building any app that enumerates, routes, or configures audio devices — 3.5mm headsets,
USB DACs, Bluetooth/BLE Audio earbuds, WiFi speakers — or that changes volume, codecs,
mic gain, or noise suppression on Android.

## Device enumeration — one API, all transports

`AudioManager.getDevices()` is the single source of truth. Do not hand-roll per-transport
lists; map `AudioDeviceInfo.type` instead:

| `AudioDeviceInfo.TYPE_*` | Transport |
|---|---|
| `WIRED_HEADSET`, `WIRED_HEADPHONES` | 3.5mm (HEADSET implies a mic) |
| `USB_DEVICE`, `USB_HEADSET`, `USB_ACCESSORY` | USB Audio Class |
| `BLUETOOTH_A2DP` | BT output (media) |
| `BLUETOOTH_SCO` | BT headset (call/mic path) |
| `BLE_HEADSET`, `BLE_SPEAKER`, `BLE_BROADCAST` | LE Audio (API 31+/33+) |
| `BUILTIN_SPEAKER`, `BUILTIN_MIC`, `BUILTIN_EARPIECE` | On-device |
| `HDMI`, `HDMI_ARC`, `HDMI_EARC` | TV/AVR |
| `REMOTE_SUBMIX` | Cast/WiFi virtual sink |

WiFi speakers (Chromecast/AirPlay/DLNA/Sonos) are **not** in `getDevices()` — discover
them yourself with `NsdManager` over mDNS (`_googlecast._tcp`, `_raop._tcp`, `_sonos._tcp`)
and model them as a separate device class.

Observe changes with `AudioDeviceCallback` wrapped in `callbackFlow` — it fires for
add/remove of every transport, replacing a pile of broadcast receivers:

```kotlin
fun AudioManager.observeDevices(): Flow<List<AudioDeviceInfo>> = callbackFlow {
    val cb = object : AudioDeviceCallback() {
        override fun onAudioDevicesAdded(added: Array<out AudioDeviceInfo>) = emit()
        override fun onAudioDevicesRemoved(removed: Array<out AudioDeviceInfo>) = emit()
        fun emit() { trySend(getDevices(GET_DEVICES_ALL).toList()) }
    }
    registerAudioDeviceCallback(cb, Handler(Looper.getMainLooper()))
    trySend(getDevices(GET_DEVICES_ALL).toList())
    awaitClose { unregisterAudioDeviceCallback(cb) }
}.conflate()
```

Capabilities come off the same object: `sampleRates`, `channelCounts`, `encodings`,
`isSink`/`isSource`, `address`, `productName`, `id`.

## Routing — API level is everything

- **API 31+ (preferred):** `AudioManager.setCommunicationDevice(AudioDeviceInfo)` for the
  call/mic path; `AudioTrack.setPreferredDevice(...)` per-stream for media.
- **API 23–30:** this is the dangerous range for A2DP speakers on MIUI/HyperOS.
  `AudioManager.setPreferredDevice()` does **not** exist on `AudioManager` — it is
  `AudioTrack.setPreferredDevice(...)` for streams **you own**. Calling it on
  `AudioManager` is a compile error.
- **The A2DP/SCO distinction on legacy Bluetooth:** `startBluetoothSco()` opens a
  **voice-call SCO channel** (`TYPE_BLUETOOTH_SCO`). It is correct for HFP headsets
  and phone calls, and **wrong for A2DP speakers like JBL Go**. On MIUI/HyperOS,
  SCO actively kills the A2DP media route — the platform treats SCO and A2DP as
  mutually exclusive transports and tears down A2DP when SCO is started.
- **Correct pre-31 behavior for A2DP speakers:** do **not** call `startBluetoothSco()`.
  Do **not** call `isBluetoothScoOn = true`. Instead, call `stopBluetoothSco()` and
  clear speakerphone, and let the platform route A2DP media natively. The app does
  not need to "do" anything to make A2DP work — the platform handles it once SCO
  is out of the way.
- **Never** claim you can force *another app's* audio to a different device without
  `MODIFY_AUDIO_ROUTING` (system-signature). Design the UI so per-app routing is honest:
  route your own capture/playback, and for foreign apps expose the system output switcher
  via `MediaRouter`/`MediaRouter2` instead of pretending.

## Volume — the real API surface

```kotlin
audioManager.getStreamMaxVolume(STREAM_MUSIC)      // device-specific, 7..30+
audioManager.getStreamMinVolume(STREAM_MUSIC)      // API 28+
audioManager.setStreamVolume(STREAM_MUSIC, index, FLAG_SHOW_UI)
audioManager.adjustStreamVolume(STREAM_MUSIC, ADJUST_RAISE, 0)
```
- Streams that matter: `MUSIC`, `VOICE_CALL`, `RING`, `NOTIFICATION`, `ALARM`,
  `SYSTEM`, `ACCESSIBILITY`, `DTMF`.
- Percent↔index conversion must round-trip through the device's own max/min, and
  **finer-grained "volume steps" than the hardware provides require a software gain
  stage** (`AudioTrack.setVolume` or a DSP gain node) — the stream index cannot be
  subdivided. Say so in the UI rather than faking 100 steps.
- `setStreamVolume` on `STREAM_RING`/`NOTIFICATION` throws `SecurityException` in DND
  unless the app holds notification-policy access — request via
  `ACTION_NOTIFICATION_POLICY_ACCESS_SETTINGS`.
- Absolute-volume BT sync is controlled by the system; you can detect it
  (`AudioManager.isVolumeFixed`) but not toggle it without system perms.

## Bluetooth: battery, codec, LE Audio

- **Codec read/write:** `BluetoothA2dp.getCodecStatus(device)` /
  `setCodecConfigPreference(device, BluetoothCodecConfig)` are `@hide`/`@SystemApi`.
  Reflection works on many OEM builds and throws on others — wrap every call in
  `runCatching`, cache the result, and degrade to read-only display of the active codec.
  Never let a reflection failure crash or block the UI.
- **Battery:** `BluetoothDevice.getBatteryLevel()` is `@hide`; the supported path is the
  `android.bluetooth.device.action.BATTERY_LEVEL_CHANGED` broadcast plus HFP `AT+IPHONEACCEV`
  / BAS GATT (`0x180F`/`0x2A19`) for BLE. Treat battery as `Int?` and render "—" when null.
- **LE Audio:** `BluetoothLeAudio` profile (API 33+) exposes group IDs for TWS buds and
  `BluetoothLeBroadcast` for Auracast. Guard with `Build.VERSION.SDK_INT` + a
  `PackageManager.FEATURE_BLUETOOTH_LE` check.
- Permissions: `BLUETOOTH_CONNECT` + `BLUETOOTH_SCAN` (API 31+, runtime, `neverForLocation`
  on scan to avoid the location grant), legacy `BLUETOOTH`/`BLUETOOTH_ADMIN` below that.

## USB Audio Class

`UsbManager.deviceList` → filter interfaces where `interfaceClass == UsbConstants.USB_CLASS_AUDIO`.
Subclass 1 = control, 2 = streaming, 3 = MIDI. Descriptor parsing tells you UAC1 vs UAC2.
Android routes UAC devices automatically once attached; you get vendor/product IDs,
supported rates, and channel masks — but **bypassing the platform mixer (bit-perfect/DSD)
requires taking exclusive USB control yourself**, which means `USB_PERMISSION` and your own
UAC driver. Scope this honestly: expose rates/channels and hardware volume, and label
bit-perfect as an advanced/experimental path.

## Microphone input

```kotlin
AudioRecord.Builder()
    .setAudioSource(MediaRecorder.AudioSource.VOICE_RECOGNITION) // no auto-processing
    .setAudioFormat(AudioFormat.Builder()
        .setEncoding(AudioFormat.ENCODING_PCM_FLOAT)
        .setSampleRate(48_000).setChannelMask(CHANNEL_IN_MONO).build())
    .build()
```
- Source choice *is* the processing switch: `MIC` (raw-ish), `VOICE_RECOGNITION`
  (no AGC/NS), `VOICE_COMMUNICATION` (AEC+NS+AGC on), `UNPROCESSED` (flattest, needs
  `PROPERTY_SUPPORT_AUDIO_SOURCE_UNPROCESSED`).
- Platform effects, each `isAvailable()`-gated: `NoiseSuppressor`, `AcousticEchoCanceler`,
  `AutomaticGainControl`. Attach by `audioSessionId`.
- Mic *gain* has no public setter — implement it as software gain on the captured buffer,
  plus a noise gate / compressor / de-esser in your own DSP chain.
- `setPreferredDevice()` on `AudioRecord` selects which physical mic; `setPreferredMicrophoneDirection`
  / `setPreferredMicrophoneFieldDimension` (API 29+) give beamforming hints.

## Low latency

## Polish, performance and stability (audit before shipping)

Full findings with measured numbers:
`references/audio-app-performance-and-stability.md`

1. **Audio focus** — `grep -rc "requestAudioFocus" --include=*.kt .` returning 0 on an
   audio app is a Play policy violation, not a nitpick. Duck yourself AFTER the DSP
   chain (so effects behave identically), and always `abandon()` on stop.
2. **`ERROR_DEAD_OBJECT`** — `AudioTrack.write`/`AudioRecord.read` return it when the
   device is unplugged mid-stream. Rebuild the track against the new route; never
   reuse the dead handle or spin on it.
3. **`runCatching` without logging** — necessary for OEM quirks, useless for debugging
   unless failures are recorded. A bounded ring buffer + `platformCall` helper fixes it
   (catch `Throwable`: hidden-API reflection throws `NoSuchMethodError`).
4. **Baseline Profile** — rigorously measured 712 ms → 517 ms median cold start (27%),
   matching full AOT within 7 ms and cutting variance from 139 ms to 29 ms. Ad-hoc
   `am start -W` loops overstated this as 42% — use macrobenchmark for published numbers.
   Verify `baseline.prof` is really in the AAB rather than trusting the config.
5. **Compose unstable params** — a `List` parameter on a `@Composable` forces
   recomposition; use `ImmutableList` and export it as `api`.
6. **Hot-path allocations** — one `listOf(...)` inside biquad coefficient updates
   allocated on every EQ band drag.


Request `AudioTrack` with `PERFORMANCE_MODE_LOW_LATENCY`, buffer =
`PROPERTY_OUTPUT_FRAMES_PER_BUFFER`, rate = `PROPERTY_OUTPUT_SAMPLE_RATE`. Under the hood
this is AAudio. Only reach for NDK/AAudio-in-C++ (or Oboe) when you need <10ms round trip;
Kotlin `AudioTrack` in low-latency mode is enough for playback EQ.

## Foreground service rules (API 34+)

Any always-on audio work needs `foregroundServiceType="mediaPlayback"` (playback) or
`"microphone"` (capture), the matching `FOREGROUND_SERVICE_*` permission, and a started
service — you cannot start a mic FGS from the background. `POST_NOTIFICATIONS` is runtime
on 33+.

## Pitfalls

- **Nullable properties from another Gradle module never smart-cast.** `AudioDevice.batteryPercent`,
  `AppAudioSession.volumePercent` etc. live in a `:core:model` module, so
  `if (x.field != null) { use(x.field) }` fails to compile with *"Smart cast is impossible,
  because it is a public API property declared in different module"*. Bind a local first:
  `val v = x.field; if (v != null) use(v)` — or use `x.field?.let { … }`. This bites in every
  feature module that renders optional device facts.
- `getStreamMaxVolume` differs per device *and* per stream — never hardcode 15.
- Effects attached to session `0` apply globally and are silently ignored on some OEMs;
  prefer attaching to your own session and be explicit in the UI about what is global.
- `AudioDeviceInfo.id` is not stable across reconnects; persist profiles keyed on
  `address` + `productName` + type, with `id` as a transient handle.
- Always `conflate()` device flows — enumeration storms on BT connect.
- Test with nothing connected: `getActiveOutput()` must never NPE.

## MIUI/HyperOS A2DP routing quirk

On Xiaomi/MIUI/HyperOS, connected JBL-style A2DP speakers can appear as
`AudioDeviceInfo.TYPE_BLUETOOTH_SCO` (`type 8`) to `AudioService`. In that state:

- `AudioManager.setCommunicationDevice()` throws `IllegalArgumentException:
  invalid device type: 8`.
- Pre-31 SCO calls (`startBluetoothSco()`, `isBluetoothScoOn = true`) can actively
  tear down A2DP media routing.

Mitigation:

1. **API 31+:** wrap `setCommunicationDevice()` in a targeted `try/catch`
   `IllegalArgumentException`. If the message contains `invalid device type` and
   the target transport is Bluetooth Classic/BLE, treat it as success because the
   platform is already handling A2DP.
2. **Pre-31:** never start SCO for A2DP speakers. Only clear speakerphone and stop
   SCO if it was somehow started; guard each call individually so one failure does
   not abort the whole routing operation.
3. **Enumeration:** supplement `AudioManager.getDevices()` with
   `BluetoothManager.getConnectedDevices(BluetoothProfile.A2DP)`; MIUI may omit
   connected A2DP devices from the system list.

Reference: `references/miui-a2dp-routing.md`
