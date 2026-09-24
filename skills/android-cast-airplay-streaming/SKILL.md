---
name: android-cast-airplay-streaming
description: Stream audio to Chromecast and AirPlay from Android.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [android, chromecast, airplay, raop, streaming, kotlin]
---

# Casting and AirPlay from Android

## When to Use

Sending audio from an Android app to a Chromecast, Google TV, AirPlay receiver, or
Sonos speaker — or discovering those devices at all.

## The rule that shapes everything

Network speakers are **not** in `AudioManager.getDevices()` and are **not** reachable
through Android audio routing. They need their vendor protocol. And neither Cast nor
AirPlay can receive a capture of another app's output without `CAPTURE_AUDIO_OUTPUT`
(signature-level), so a third-party app streams **its own media**, not "the system
mix". Design the UI around that instead of implying otherwise.

## Discovery: mDNS service types

```
_googlecast._tcp          Chromecast / Google TV / Nest
_raop._tcp                AirPlay 1 audio (RAOP)
_airplay._tcp             AirPlay 2
_sonos._tcp               Sonos
_spotify-connect._tcp     Spotify Connect
```

Use `NsdManager` + `PROTOCOL_DNS_SD`. Needs `INTERNET`,
`ACCESS_NETWORK_STATE`, `ACCESS_WIFI_STATE`, and `CHANGE_WIFI_MULTICAST_STATE`.
`resolveService` is deprecated on API 34+ but still the compatible path; wrap it.

## Chromecast (Cast SDK)

```kotlin
implementation("com.google.android.gms:play-services-cast-framework:21.5.0")
implementation("androidx.mediarouter:mediarouter:1.7.0")
```

**PITFALL #1 — the single most common Cast failure.** `CastContext.getSharedInstance()`
throws unless an `OptionsProvider` is declared in the manifest:

```xml
<meta-data
    android:name="com.google.android.gms.cast.framework.OPTIONS_PROVIDER_CLASS_NAME"
    android:value="com.yourapp.CastOptionsProvider" />
```

```kotlin
class CastOptionsProvider : OptionsProvider {
    override fun getCastOptions(context: Context) = CastOptions.Builder()
        .setReceiverApplicationId(CastMediaControlIntent.DEFAULT_MEDIA_RECEIVER_APPLICATION_ID)
        .setStopReceiverApplicationWhenEndingSession(true)
        .build()
    override fun getAdditionalSessionProviders(context: Context) = null
}
```

Use `DEFAULT_MEDIA_RECEIVER_APPLICATION_ID` unless you have registered a receiver app.

**PITFALL #2 — Cast requires Play Services.** Guard with
`GoogleApiAvailability.isGooglePlayServicesAvailable(context) == ConnectionResult.SUCCESS`
and every `getSharedInstance()` in `runCatching`. AOSP/de-Googled devices have none.

**PITFALL #3 — route selection belongs to MediaRouter, not your mDNS scan.** Select via
`MediaRouter.getInstance(context).selectRoute(route)` on the **main thread**, matching
your discovered name/id against `router.routes`.

Session start is async: register a `SessionManagerListener<CastSession>` and await it
(`suspendCancellableCoroutine` + `withTimeoutOrNull`), since `currentCastSession` is
null immediately after selecting a route.

Playback is URL based via `RemoteMediaClient.load(MediaLoadRequestData)`. Volume is
**session level**: `session.volume = 0.0..1.0`, `session.isMute`. All Cast calls must
run on the main thread.

## AirPlay 1 / RAOP (no SDK exists — implement RTSP yourself)

Handshake against port 5000:

1. `ANNOUNCE rtsp://<host>/<clientInstance>` with an SDP body containing
   `a=rtpmap:96 AppleLossless`, `a=fmtp:96 352 0 16 40 10 14 2 255 0 0 44100`,
   `a=rsaaeskey:<RSA-OAEP(AES key), base64, '=' stripped>`, `a=aesiv:<iv>`
2. `SETUP` with `Transport: RTP/AVP/UDP;unicast;mode=record;control_port=…;timing_port=…`
   → response carries the `Session` header and the server's ports
3. `RECORD` with `RTP-Info: seq=0;rtptime=0`
4. `SET_PARAMETER` body `volume: <dB>` — **RAOP volume is dB, not percent**:
   `-144` = muted, useful range `-30..0`. A linear percent sounds wrong.
5. `TEARDOWN` to release; `FLUSH` to pause

Audio is 352-frame ALAC packets over RTP, AES-128-CBC encrypted **whole blocks only**
(the tail goes in the clear). RTP header is 12 bytes, payload type 96, marker bit set
on the first packet.

**PITFALL #4 — AirPlay 2 rejects this path.** HomeKit/AirPlay-2 receivers answer
`470`/`403` to a v1 ANNOUNCE because they require Curve25519 pair-verify. Detect the
status code and tell the user, rather than retrying or hanging. `453` means another
sender already owns the receiver.

Base64 in SDP has its `=` padding **stripped**; pad it back before decoding.

## Architecture that keeps the UI simple

Put both behind one interface (`connect / play / pause / setVolume / disconnect /
observeState`) and a coordinator that maps a discovered device's protocol to the right
implementation. Return a sealed `Success | Unavailable(reason) | Failed(reason)` so the
UI can explain *why* — "needs Play Services", "requires AirPlay 2 pairing", "receiver
busy" are all normal outcomes.

Latency for lip-sync hints: Cast ~1500 ms, RAOP ~2000 ms.

## Hilt gotcha

A streaming module must **not** provide `Context` if another module already does —
Dagger fails with `[Dagger/DuplicateBindings] android.content.Context is bound
multiple times`. Annotate the constructor param `@ApplicationContext` and add no
module at all.

## ProGuard/R8

```proguard
-keep class * implements com.google.android.gms.cast.framework.OptionsProvider { *; }
-keep class com.yourapp.CastOptionsProvider { *; }
-keep class com.google.android.gms.cast.** { *; }
-keep class androidx.mediarouter.** { *; }
-keep class javax.crypto.** { *; }   # RAOP looks up JCE transformations by name
```
