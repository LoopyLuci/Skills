# Device name sanitization for audio apps

## Signal
On Xiaomi/MIUI/HyperOS and some OEMs, audio device discovery paths may return
raw identifiers instead of user-facing names:
- `AudioDeviceInfo.productName` can be the phone model code, e.g. `22101316G`
- `BluetoothDevice.name` can be blank or equal to the MAC address
- mDNS `serviceName` can resolve to a model number, MAC-like string, or IP address
- USB audio descriptors can expose vendor/product IDs only

## Impact
If these raw values reach `AudioDevice.displayName` / `AudioDevice.label`,
the Devices UI shows codes and identifiers to users instead of friendly names.

## Fix
Sanitize at every mapping layer:

- `AudioDeviceMapper.displayNameFor(...)`: strip MAC addresses, IPv4 addresses,
  all-caps/digit model codes, then fall back to transport-specific copy.
- `BluetoothInfoProvider.detailFor(...)`: if `device.name` is blank or equals
  `device.address`, try bonded-device names before falling back to a generic
  Bluetooth speaker label.
- `WifiSpeakerDiscovery.toDevice(...)`: if the resolved mDNS name looks like an
  identifier, use `protocol.displayName` instead.

## Rules
- Never expose raw `address`, `ipAddress`, or `productName` as `displayName`.
- Never expose model-number-like strings (`22101316G`, `SM-G991B`, etc.) as
  device names without user-provided override.
- The UI should always render `device.label`, which resolves `userLabel ?: displayName`.
