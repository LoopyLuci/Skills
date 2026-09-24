# Network Speaker Audio Routing — Session Notes

## Problem
- User reported "Sound does not actually get directed to any speakers" for network speakers.
- Existing `DlnaAudioStreamer`, `SpotifyConnectStreamer`, `GenericNetworkStreamer` only contained `startActivity()` intent placeholders.
- No audio pipeline connected `PlaybackEngine` output to network targets.

## Implemented
- Raw UPnP/DLNA control path: `DlnaControlPoint`, `DlnaActions`, `DlnaAudioStreamer`.
- Local HTTP server: `LocalMediaServer` using `NanoHTTPD`.
- Network bridge: `NetworkAudioBridge` with `NetworkStreamingBridge` for PCM-to-file export.
- `PlaybackEngine.pcmOutput: Flow<FloatArray>` for downstream encoding.
- `StreamingCoordinator.connect(device: AudioDevice)` already maps protocols.
- Wired new streamers in `StreamingModule`.
- Replaced non-buildable Cling/Cybergarage dependencies with stdlib HTTP/XML + `NanoHTTPD`.
- All streaming module unit tests pass; full `:app:assembleFullDebug` build succeeds.

## Remaining
- Encode PCM to MP3/AAC in `NetworkAudioBridge` and call `play(mediaUrl, title)`.
- Wire UI: `DevicesViewModel.routeTo()` / `PlaybackEngine.start()` to use bridge when `wifiProtocol != null`.
- AirPlay 1/2 and Chromecast remain unimplemented beyond existing stubs.
