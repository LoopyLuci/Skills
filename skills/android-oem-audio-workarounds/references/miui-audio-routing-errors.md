# MIUI Audio Routing Errors — Raw Session Data

## Device

- **Model:** Redmi Note 12 Pro 5G (22101316G)
- **OS:** MIUI V816 / HyperOS, base Android 11 (API 30)
- **Bluetooth device:** JBL Go 3 (paired, A2DP connected)

## Key observations from `dumpsys audio`

```
bt_a2dp(80)   ← A2DP media route is active (type 0x80 = TYPE_BLUETOOTH_A2DP)
Active communication device: bt_a2dp name=JBL Go 3
```

The system audio flinger correctly identifies the device as A2DP. However:

## Key observations from `dumpsys bluetooth_manager`

```
Bluetooth A2DP Profile: connected
Device: JBL Go 3  [MAC: xx:xx:xx:xx:xx:xx]
stream type: 0x80 (bt_a2dp)
```

## Root cause: Java AudioManager reports type 8 (SCO)

`AudioManager.getDevices()` on this MIUI build returns the JBL Go 3 with
`AudioDeviceInfo.getType() == 8` (`TYPE_BLUETOOTH_SCO`) instead of the
correct `TYPE_BLUETOOTH_A2DP` (type 80).

## Logcat snippet — snackbar error

```
08-23 17:09:55.234 23372 23372 W SonicCore: routeCommunicationTo: invalid device type: 8
```

This error originates from the pre-31 `AudioRouter.routeCommunicationTo()` path
when `stopBluetoothSco()` is called on a device that the platform knows is
A2DP, not SCO.

## Logcat snippet — successful route after fix

After splitting SCO calls into individual `runCatching` blocks:

```
08-23 18:07:51.645 22265 22265 W Heap:   at android.app.Instrumentation.callApplicationOnCreate
(no "invalid device type" error)
```

And `dumpsys audio` post-tap:

```
Active communication device: bt_a2dp name=JBL Go 3
```

## Build verification

- `:app:compileFullDebugKotlin` — BUILD SUCCESSFUL
- `:app:assembleFullDebug` — BUILD SUCCESSFUL (APK 23M)
- `:app:testFullDebugUnitTest` — 1794/1794 passing
- `:app:testFossDebugUnitTest` — all passing
- `:app:compileFullReleaseKotlin` — BUILD SUCCESSFUL
- `:core:audio:test` — all passing
- `:app:compileFullDebugAndroidTestKotlin` — BUILD SUCCESSFUL