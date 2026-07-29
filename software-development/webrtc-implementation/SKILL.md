---
name: webrtc-implementation
description: "Use when implementing WebRTC for real-time communication."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [webrtc, video, audio, p2p, signaling, STUN, TURN, ICE, real-time-communication]
    related_skills: [mdns-discovery, p2p-lan-transfer, instanttransfer-protocol, cross-thread-async]
---

# WebRTC Implementation

Implementing WebRTC for real-time audio, video, and data communication — from signaling and peer connection through NAT traversal, media streams, and data channels.

## When to Use

- Building video/audio conferencing applications
- Implementing peer-to-peer file transfer
- Adding real-time data channels to web applications
- Building screen sharing or remote desktop tools
- Creating real-time collaboration features

## WebRTC Connection Flow

```python
WEBRTC_FLOW = {
    'signaling': 'Peers exchange session metadata (SDP offers/answers) via server',
    'ICE': 'Interactive Connectivity Establishment — finds best network path',
    'STUN': 'Session Traversal Utilities for NAT — determines public IP/port',
    'TURN': 'Traversal Using Relays around NAT — relay when P2P fails',
    'DTLS': 'Datagram Transport Layer Security — encrypts all media/data',
}

class SignalingServer:
    """WebSocket-based signaling server for WebRTC."""
    def __init__(self):
        self.clients = {}  # client_id -> websocket
    
    def relay_sdp(self, sender: str, receiver: str, sdp: dict):
        """Relay SDP offer/answer between peers."""
        if receiver in self.clients:
            self.clients[receiver].send_json({
                'type': 'sdp',
                'from': sender,
                'sdp': sdp
            })
    
    def relay_ice(self, sender: str, receiver: str, candidate: dict):
        """Relay ICE candidates between peers."""
        if receiver in self.clients:
            self.clients[receiver].send_json({
                'type': 'ice_candidate',
                'from': sender,
                'candidate': candidate
            })
```

## Common Pitfalls

1. **TURN server not configured** — only STUN works for 80% of connections; TURN needed for the rest
2. **Signaling bottleneck** — signaling must be fast (WebSocket); slow signaling breaks connections
3. **No connection state handling** — WebRTC connections change state; handle all states (disconnected, failed)
4. **Codec compatibility** — not all browsers support all codecs; check in advance (H.264, VP8, VP9, AV1)
5. **Bandwidth estimation** — sending HD video on slow connections causes buffering; use SVC or simulcast

## Verification Checklist

- [ ] STUN server configured (Google's stun.l.google.com or custom)
- [ ] TURN server configured for NAT traversal fallback
- [ ] Signaling via WebSocket (reliable, low-latency)
- [ ] ICE candidate gathering and exchange working
- [ ] Media stream constraints (resolution, frame rate) configured
- [ ] Data channel (if used) established and reliable/unreliable mode chosen
- [ ] Connection state monitoring (oniceconnectionstatechange)
- [ ] Codec negotiation (H.264/VP8 for compatibility, AV1 for quality)
- [ ] Bandwidth estimation (cc.bitrate) and adaptation
