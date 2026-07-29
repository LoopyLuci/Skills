---
name: deep-packet-inspection-engine
description: "Use when building deep packet inspection engine patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [dpi, packet-inspection, network, protocol-analysis, security]
    related_skills: [packet-capture-engine, pattern-matching-engine, protocol-identifier, http-https-inspector, tls-ssl-inspector]
---

# Deep Packet Inspection (DPI) Engine

Architecture and implementation patterns for building deep packet inspection engines — from protocol parsing and pattern matching through application layer identification to content extraction.

## When to Use

- Building a DPI engine for network security or monitoring
- Implementing custom protocol dissectors
- Identifying applications and protocols from traffic
- Extracting metadata and content from network flows
- Building next-generation firewall or QoS systems

## DPI Architecture

```
Raw Packets → Reassembly → Protocol Detection → Protocol Parsing → Content Extraction → Metadata
                    ↓               ↓                    ↓
              TCP Reorder      Fingerprinting        Application Logic
```

## Protocol Detection

### Port-Based Detection (Baseline)

```python
PORT_PROTOCOL_MAP = {
    80: 'http', 443: 'tls', 22: 'ssh', 53: 'dns',
    21: 'ftp', 25: 'smtp', 110: 'pop3', 143: 'imap',
    3306: 'mysql', 5432: 'postgresql', 6379: 'redis',
    8080: 'http-proxy', 8443: 'tls-proxy'
}

def detect_by_port(port):
    return PORT_PROTOCOL_MAP.get(port, 'unknown')
```

### Signature-Based Detection (nDPI-style)

```python
import struct
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ProtocolSignature:
    """Signature for protocol identification."""
    name: str
    pattern: bytes
    offset: int  # Starting offset in payload
    mask: Optional[bytes] = None
    priority: int = 0

class ProtocolDetector:
    """Multi-protocol detection engine (similar to nDPI)."""
    
    PROTOCOLS = [
        ProtocolSignature('dns', b'\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00', offset=2, priority=10),
        ProtocolSignature('dhcp', b'\x63\x82\x53\x63', offset=0, priority=5),
        ProtocolSignature('http', b'GET ', offset=0, priority=0),
        ProtocolSignature('http', b'POST ', offset=0, priority=0),
        ProtocolSignature('http', b'HTTP/', offset=0, priority=1),
        ProtocolSignature('tls', b'\x16\x03', offset=0, priority=5),  # TLS handshake
        ProtocolSignature('tls', b'\x16\x03\x01', offset=0, priority=6),
        ProtocolSignature('ssh', b'SSH-', offset=0, priority=3),
        ProtocolSignature('smtp', b'EHLO', offset=0, priority=2),
        ProtocolSignature('smtp', b'HELO', offset=0, priority=2),
        ProtocolSignature('ftp', b'220 ', offset=0, priority=2),
        ProtocolSignature('dns-over-https', b'application/dns-message', offset=0, priority=8),
    ]
    
    def __init__(self):
        # Sort by priority (highest first)
        self.protocols = sorted(self.PROTOCOLS, key=lambda p: -p.priority)
    
    def detect(self, payload: bytes, src_port=None, dst_port=None) -> List[str]:
        """Detect all matching protocols in payload."""
        matches = []
        
        for proto in self.protocols:
            if len(payload) < proto.offset + len(proto.pattern):
                continue
            
            sample = payload[proto.offset:proto.offset + len(proto.pattern)]
            
            if proto.mask:
                # Masked comparison (for bitwise matching)
                masked_sample = bytes(a & b for a, b in zip(sample, proto.mask))
                if masked_sample == proto.pattern:
                    matches.append(proto.name)
            else:
                if sample == proto.pattern:
                    matches.append(proto.name)
        
        # If no signature match, fall back to port-based
        if not matches and dst_port:
            port_match = PORT_PROTOCOL_MAP.get(dst_port)
            if port_match:
                matches.append(port_match)
        
        return matches


class NgramDetector:
    """Statistical protocol detection using n-gram fingerprints."""
    
    def __init__(self):
        self.fingerprints = {
            'http': self._build_ngram_fingerprint('GET POST HTTP/1.'),
            'ssh': self._build_ngram_fingerprint('SSH-2.0- OpenSSH'),
            'tls': self._build_ngram_fingerprint('\x16\x03\x01\x02\x00'),
        }
    
    def detect(self, payload):
        """Match payload against n-gram fingerprints."""
        scores = {}
        for protocol, fingerprint in self.fingerprints.items():
            score = self._ngram_similarity(payload[:64], fingerprint)
            if score > 0.6:  # Threshold
                scores[protocol] = score
        return scores
```

## Application Layer Parser

### HTTP Parser

```python
class HTTPParser:
    """Parse HTTP requests and responses from TCP streams."""
    
    def parse_request(self, data: bytes):
        """Parse HTTP request."""
        request = {}
        
        # Split headers and body
        if b'\r\n\r\n' in data:
            header_section, body = data.split(b'\r\n\r\n', 1)
        else:
            header_section, body = data, b''
        
        lines = header_section.split(b'\r\n')
        if not lines:
            return None
        
        # Request line: METHOD PATH VERSION
        request_line = lines[0].decode('utf-8', errors='replace')
        parts = request_line.split(' ')
        if len(parts) >= 2:
            request['method'] = parts[0]
            request['path'] = parts[1]
            request['version'] = parts[2] if len(parts) > 2 else 'HTTP/1.1'
        
        # Headers
        request['headers'] = {}
        for line in lines[1:]:
            if b':' in line:
                key, value = line.decode('utf-8', errors='replace').split(':', 1)
                request['headers'][key.strip().lower()] = value.strip()
        
        # Extract useful metadata
        request['host'] = request['headers'].get('host', '')
        request['user_agent'] = request['headers'].get('user-agent', '')
        request['content_type'] = request['headers'].get('content-type', '')
        
        # Body (if content-length present)
        content_length = int(request['headers'].get('content-length', 0))
        if content_length > 0:
            request['body'] = body[:content_length]
        
        return request
```

### TLS Parser

```python
class TLSParser:
    """Parse TLS handshake metadata without decryption."""
    
    def parse_client_hello(self, data):
        """Extract metadata from TLS ClientHello."""
        if len(data) < 5:
            return None
        
        # TLS record layer
        content_type = data[0]
        version = struct.unpack('!H', data[3:5])[0]
        
        if content_type != 0x16:  # Handshake
            return None
        
        result = {
            'version': self._version_string(version),
            'sni': None,
            'alpn': [],
            'cipher_suites': [],
            'ja3_hash': None
        }
        
        # Parse handshake
        handshake = data[5:]
        if len(handshake) < 4:
            return result
        
        handshake_type = handshake[0]
        if handshake_type != 0x01:  # ClientHello
            return result
        
        # Extract SNI
        sni = self._extract_sni(handshake)
        if sni:
            result['sni'] = sni
        
        # Extract ALPN
        result['alpn'] = self._extract_alpn(handshake)
        
        # JA3 fingerprint
        result['ja3'] = self._compute_ja3(handshake)
        
        return result
    
    def _extract_sni(self, handshake):
        """Extract Server Name Indication from ClientHello."""
        try:
            # Skip past fixed fields to extensions
            pos = handshake[4] + 5 + 32 + 2 + handshake[7+32+2]  # Complex offsets
            # Simplified: find SNI extension type 0x0000
            while pos < len(handshake) - 4:
                ext_type = struct.unpack('!H', handshake[pos:pos+2])[0]
                ext_len = struct.unpack('!H', handshake[pos+2:pos+4])[0]
                if ext_type == 0x0000:  # SNI
                    sni_len = struct.unpack('!H', handshake[pos+5:pos+7])[0]
                    return handshake[pos+7:pos+7+sni_len].decode('utf-8', errors='replace')
                pos += 4 + ext_len
        except:
            pass
        return None
```

## Content Extraction

```python
class ContentExtractor:
    """Extract and categorize content from inspected packets."""
    
    def extract_metadata(self, protocol, parsed_data):
        """Extract metadata based on detected protocol."""
        metadata = {
            'protocol': protocol,
            'timestamp': time.time(),
            'size': 0,
            'entities': []
        }
        
        if protocol == 'http' and parsed_data:
            metadata.update({
                'method': parsed_data.get('method'),
                'host': parsed_data.get('host'),
                'path': parsed_data.get('path'),
                'user_agent': parsed_data.get('user_agent'),
                'content_type': parsed_data.get('content_type'),
            })
        
        elif protocol == 'tls' and parsed_data:
            metadata.update({
                'sni': parsed_data.get('sni'),
                'version': parsed_data.get('version'),
                'ja3': parsed_data.get('ja3'),
                'alpn': parsed_data.get('alpn'),
            })
        
        return metadata
```

## Performance Optimization

```python
class OptimizedDPI:
    """Performance optimizations for DPI at line rate."""
    
    def __init__(self):
        # 1. Use SIMD for pattern matching
        # 2. Skip inspection for known-clean traffic (allowlist)
        # 3. Sample large flows instead of full inspection
        # 4. Use GPU for parallel packet processing
        # 5. Early termination on protocol mismatch
        pass
    
    def should_skip_inspection(self, flow):
        """Fast-path: skip inspection for known-clean flows."""
        # CDNs, trusted services, internal backhaul
        trusted_domains = ['cdn.example.com', 'internal-service.local']
        if flow.get('sni') in trusted_domains:
            return True
        return False
```

## Common Pitfalls

1. **Encrypted traffic blindness** — most traffic is now TLS; rely on SNI, JA3, and flow metadata
2. **Performance degradation** — full DPI on every packet is expensive; use sampling for large flows
3. **Protocol evasion** — attackers fragment, pad, or obfuscate; reassemble and normalize
4. **False positives** — binary pattern matching can misidentify; use multi-signature verification
5. **Privacy concerns** — DPI can extract sensitive data; implement data minimization and retention policies
6. **IPv6 complexity** — extension headers, fragmentation, and addressing differ from IPv4

## Verification Checklist

- [ ] Correctly identifies HTTP, TLS, DNS, SSH, SMTP, FTP
- [ ] Extracts SNI from TLS ClientHello accurately
- [ ] Handles HTTP/2 and QUIC (HTTP/3) in addition to HTTP/1.1
- [ ] Reassembles fragmented TCP streams correctly
- [ ] Performance: handles 10Gbps line rate on test hardware
- [ ] No false positives on binary data that matches signatures
- [ ] Extracted metadata is accurate and complete

## See Also

- packet-capture-engine — capturing raw packets for DPI
- pattern-matching-engine — high-performance pattern matching
- protocol-identifier — protocol recognition patterns
- http-https-inspector — HTTP-specific inspection
- tls-ssl-inspector — TLS-specific inspection
