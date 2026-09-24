---
name: android-network-audio-streaming
description: Route Android app audio to network speakers: DLNA, AirPlay, Cast, local HTTP serving, and PlaybackEngine PCM bridging.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [android, dlna, airplay, chromecast, streaming, audio, kotlin, upnp]
---

# Android Network Audio Streaming

## When to use
- The user wants audio from an Android app to reach DLNA, AirPlay, Chromecast, or
  other network speakers.
- Network devices are discovered but the app shows "protocol not supported yet".
- You need a local media server so renderers can fetch audio from the phone.
- You need a bridge from `PlaybackEngine` PCM output into a network streamer.

## Core truth

Network speakers are not in `AudioManager.getDevices()` and Android does not allow
third-party apps to capture system-wide audio without `CAPTURE_AUDIO_OUTPUT`
(signature-level). The app must therefore:

1. Stream **its own media** to network renderers.
2. Provide that media at a URL the renderer can reach, usually via an embedded HTTP server.
3. Drive the renderer through its vendor protocol: DLNA/UPnP, AirPlay RAOP, Cast SDK.

## DLNA without external UPnP libraries

If Cling/Cybergarage is unavailable, implement DLNA with raw HTTP + XML:

- SSDP discovery: send `M-SEARCH * HTTP/1.1` to `239.255.255.250:1900` with
  header `ST: urn:schemas-upnp-org:device:MediaRenderer:1`. Parse `Location`
  from responses.
- Device description: GET the XML at `Location`. Find the service with
  `serviceId=urn:upnp-org:serviceId:AVTransport`. Extract `controlURL` and
  `controlURL` base path.
- SOAP control: POST XML to the resolved control URL with
  `Content-Type: text/xml; charset="utf-8"` and `SOAPAction` header.
  Required actions:
  - `SetAVTransportURI` with `CurrentURI` and `CurrentURIMetaData`
  - `Play` with `InstanceID=0`, `Speed=1`
  - `Pause`, `Stop`, `Seek` with `InstanceID=0`
  - `GetTransportInfo` to observe state transitions
- Resolve relative `controlURL` values against the device description base URL.
- Wrap every network call in `withContext(Dispatchers.IO)` + `try/catch`.
  Return `false` on failure; never let IO exceptions escape to the UI layer.

## Local media server

Network renderers need a reachable URL:

- Embed a lightweight HTTP server: `NanoHTTPD` is the standard choice.
- Bind to port `0` to get an OS-assigned port. Expose the assigned port via
  `StateFlow<String?>` or `start()` returning the base URL.
- Serve files with `Content-Type: audio/mpeg` or the appropriate MIME type.
- Keep the server in a `@Singleton` so it survives config changes.
- If `NanoHTTPD` is not on the classpath, use `ServerSocket` + manual HTTP parsing.

## Network audio bridge

Bridge from `PlaybackEngine.pcmOutput: Flow<FloatArray>` to a network target:

- `NetworkAudioBridge.startStreaming(device)` connects through `StreamingCoordinator`.
- Starts the local media server if not already running.
- Consumes PCM frames from the engine, encodes to MP3/AAC, writes to a temp file
  served by the local server.
- Calls `streamingCoordinator.play(mediaUrl, title)` once the file is reachable.
- `stopStreaming()` cancels the encoding job, disconnects the coordinator, and
  clears state.
- Use `Dispatchers.IO` for all encoding and file I/O; never block the main looper.

## PlaybackEngine PCM output

Add an internal `_pcmOutput = MutableSharedFlow<FloatArray>` with
`BufferOverflow.DROP_OLDEST`. After DSP processing and before `AudioTrack.write()`,
emit the float PCM buffer. Network bridges subscribe to this flow for encoding.
Keep `replay=0` to avoid stale audio backlog.

## Streaming coordinator contract

```kotlin
sealed class StreamingResult {
    object Success : StreamingResult()
    data class Unavailable(val reason: String) : StreamingResult()
    data class Failed(val reason: String) : StreamingResult()
}
```

Never crash on `ActivityNotFoundException` or network timeouts. Return
`Unavailable("Install a ... app")` or `Failed("... failed: ...")` with a
user-actionable message. Update `StreamingState` to match so the UI shows the
reason instead of a spinner.

## FOSS/protocol support matrix

| Protocol | FOSS-safe path | Notes |
|----------|---------------|-------|
| DLNA | Raw UPnP/SSDP + SOAP | Works without external SDKs |
| AirPlay 1 | RAOP + RTSP | Manual implementation needed |
| AirPlay 2 | Not FOSS-safe | Requires Curve25519 pair-verify |
| Chromecast | Play Services SDK | Not FOSS-safe; guard availability |
| Spotify Connect | Spotify SDK | Not FOSS-safe; intent fallback only |
| Generic | Unavailable in FOSS | Hide in UI or show unsupported message |

## Common pitfalls

- Relative URLs in UPnP: device description XML often uses relative `controlURL`
  values; always resolve against the `Location` base URL.
- Network on main thread: all UPnP/HTTP calls must run on `Dispatchers.IO`.
- Missing AVTransport service: some renderers expose `RenderingControl` but not
  `AVTransport`; check service types before casting.
- AirPlay 2 rejection: v1 RAOP handshake gets `470`/`403` from HomeKit receivers;
  detect status codes and surface "requires AirPlay 2 pairing" instead of retrying.
- Server port reuse: binding to port `0` avoids conflicts, but cache the assigned
  port; changing it breaks renderer `SetAVTransportURI` mid-session.
