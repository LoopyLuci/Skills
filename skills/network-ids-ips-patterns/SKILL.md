---
name: network-ids-ips-patterns
description: "Use when implementing intrusion detection and prevention."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [network-security, IDS, IPS, intrusion-detection, suricata, snort]
    related_skills: [pattern-matching-engine, deep-packet-inspection-engine, port-scanner-detection, packet-capture-engine, firewall-rules-engine]
---

# Network IDS/IPS Patterns

Architecture and implementation patterns for Network Intrusion Detection Systems (NIDS) and Intrusion Prevention Systems (IPS) — from signature matching through anomaly detection to inline prevention.

## When to Use

- Building a network intrusion detection or prevention system
- Implementing custom IDS/IPS rules and signatures
- Integrating ML-based anomaly detection with signature-based IDS
- Building inline network security appliances
- Replacing or supplementing Snort/Suricata with custom logic

## Architecture

```
Packet Capture → Preprocessor → Detection Engine → Alert/Response
                                       ↓
                               Signature Database → Analysis → Log
```


## Signature-Based Detection

### Signature Format

```python
# Suricata/Snort-style rule format:
# alert tcp $HOME_NET any -> $EXTERNAL_NET 80 (msg:"SQL Injection Attempt"; content:"SELECT"; sid:100001;)

SIGNATURE = {
    'action': 'alert',       # alert, drop, reject, pass
    'protocol': 'tcp',       # tcp, udp, icmp
    'src': '$HOME_NET',      # Source network
    'src_port': 'any',
    'direction': '->',       # -> (one-way), <> (two-way)
    'dst': '$EXTERNAL_NET',
    'dst_port': 80,
    'signature_id': 100001,
    'revision': 1,
    'message': 'SQL Injection Attempt',
    'patterns': [            # Content matches
        {'content': 'SELECT', 'nocase': True},
        {'content': 'FROM', 'distance': 0, 'within': 50},
        {'content': 'WHERE', 'distance': 0, 'within': 100},
    ],
    'pcre': '/union\s+select/i',  # PCRE regex
    'metadata': {'cve': 'CVE-2023-XXXX', 'severity': 'high'}
}
```

## Detection Engine

```python
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Packet:
    """Representation of a network packet for analysis."""
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str  # tcp, udp, icmp
    payload: bytes
    flags: Dict[str, bool]  # SYN, ACK, FIN, RST, etc.
    timestamp: float
    flow_id: str  # Unique flow identifier

class SignatureEngine:
    """Multi-pattern matching engine for IDS signatures."""
    
    def __init__(self):
        self.signatures = []
        # Optimized data structures
        self.content_index = defaultdict(list)  # content -> [sig_ids]
        self.port_index = defaultdict(list)     # port -> [sig_ids]
        self.protocol_index = defaultdict(list) # protocol -> [sig_ids]
    
    def add_signature(self, sig):
        """Register a signature in the engine."""
        sig_id = len(self.signatures)
        self.signatures.append(sig)
        
        # Index by port
        if sig['dst_port'] != 'any':
            self.port_index[sig['dst_port']].append(sig_id)
        
        # Index by protocol
        self.protocol_index[sig['protocol']].append(sig_id)
        
        # Index by content (first content pattern)
        if sig.get('patterns'):
            first_content = sig['patterns'][0]['content']
            self.content_index[first_content].append(sig_id)
        
        self._build_aho_corasick()
    
    def _build_aho_corasick(self):
        """Build Aho-Corasick automaton for multi-pattern matching."""
        # Aho-Corasick enables O(n) matching of all patterns simultaneously
        # (vs O(n * m) for sequential pattern matching)
        self.ac_automaton = AhoCorasick()
        for sig in self.signatures:
            for pattern in sig.get('patterns', []):
                self.ac_automaton.add(pattern['content'], sig)
        self.ac_automaton.build_failure_links()
    
    def analyze_packet(self, packet: Packet) -> List[Dict]:
        """Analyze a single packet against all signatures."""
        alerts = []
        
        # 1. Quick filter: check protocol and port
        candidate_sigs = self._get_candidates(packet)
        if not candidate_sigs:
            return []
        
        # 2. Multi-pattern matching (Aho-Corasick)
        if hasattr(self, 'ac_automaton'):
            matches = self.ac_automaton.search(packet.payload)
            
            # 3. Signature-level validation
            for sig_id in candidate_sigs:
                sig = self.signatures[sig_id]
                if self._validate_signature(sig, packet, matches):
                    alerts.append(self._create_alert(sig, packet))
        
        return alerts
    
    def _get_candidates(self, packet):
        """Quick pre-filtering to reduce signatures to check."""
        candidates = set()
        
        # Match by protocol
        for sig_id in self.protocol_index.get(packet.protocol, []):
            candidates.add(sig_id)
        
        # Match by destination port
        for sig_id in self.port_index.get(packet.dst_port, []):
            candidates.add(sig_id)
        
        return candidates
    
    def _validate_signature(self, sig, packet, matches):
        """Validate that a signature fully matches the packet."""
        # Check content patterns with distance/within constraints
        for i, pattern in enumerate(sig.get('patterns', [])):
            content = pattern['content'].encode()
            
            # Check if content exists in payload
            if content not in packet.payload:
                return False
            
            # Check distance constraints
            if i > 0:
                prev_match = self._last_match(packet.payload, 
                    sig['patterns'][i-1]['content'].encode())
                current_pos = packet.payload.find(content, prev_match)
                
                if 'distance' in pattern:
                    if current_pos - prev_match > pattern['distance']:
                        return False
                if 'within' in pattern:
                    if current_pos - prev_match > pattern['within']:
                        return False
        
        # Check PCRE if present
        if sig.get('pcre'):
            if not re.search(sig['pcre'], packet.payload, re.IGNORECASE):
                return False
        
        return True


class AhoCorasick:
    """Aho-Corasick multi-pattern string matching."""
    
    def __init__(self):
        self.goto = {}  # state -> {char: next_state}
        self.fail = {}  # state -> failure_state
        self.output = {}  # state -> [patterns]
        self.next_state = 0
    
    def add(self, keyword, data=None):
        """Add a keyword to the automaton."""
        state = 0
        for char in keyword:
            if (state, char) not in self.goto:
                self.next_state += 1
                self.goto[(state, char)] = self.next_state
            state = self.goto[(state, char)]
        self.output.setdefault(state, []).append((keyword, data))
    
    def build_failure_links(self):
        """BFS to build failure links."""
        from collections import deque
        queue = deque()
        
        for char, state in [(c, s) for (st, c), s in self.goto.items() if st == 0]:
            self.fail[state] = 0
            queue.append(state)
        
        while queue:
            r = queue.popleft()
            for char, state in [(c, s) for (st, c), s in self.goto.items() if st == r]:
                queue.append(state)
                f = self.fail.get(r, 0)
                while f and (f, char) not in self.goto:
                    f = self.fail.get(f, 0)
                self.fail[state] = self.goto.get((f, char), 0)
                self.output[state] = self.output.get(state, []) + \
                    self.output.get(self.fail[state], [])
    
    def search(self, text):
        """Search for all keywords in text. Returns list of matches."""
        state = 0
        matches = []
        for i, char in enumerate(chr(b) if isinstance(text, bytes) else text):
            while state and (state, char) not in self.goto:
                state = self.fail.get(state, 0)
            state = self.goto.get((state, char), 0)
            for keyword, data in self.output.get(state, []):
                matches.append({
                    'position': i - len(keyword) + 1,
                    'keyword': keyword,
                    'data': data
                })
        return matches
```

## Anomaly-Based Detection

```python
class AnomalyDetector:
    """Statistical anomaly detection for network traffic."""
    
    def __init__(self):
        # Baseline statistics
        self.baselines = {
            'packet_rate': 0,
            'byte_rate': 0,
            'connection_rate': 0,
            'protocol_distribution': {},
            'port_distribution': {}
        }
    
    def update_baseline(self, flow_stats):
        """Update baseline statistics (exponential moving average)."""
        alpha = 0.05  # Learning rate
        for key in self.baselines:
            if key in flow_stats:
                self.baselines[key] = (1 - alpha) * self.baselines[key] + \
                                     alpha * flow_stats[key]
    
    def detect_anomaly(self, current_stats):
        """Detect if current traffic is anomalous."""
        anomalies = []
        
        for metric, value in current_stats.items():
            if metric in self.baselines:
                baseline = self.baselines[metric]
                if baseline > 0:
                    deviation = abs(value - baseline) / baseline
                    if deviation > 3:  # 3x standard deviation
                        anomalies.append({
                            'metric': metric,
                            'current': value,
                            'baseline': baseline,
                            'deviation': deviation
                        })
        
        return anomalies
```

## Flow-Based Analysis

```python
class FlowAnalyzer:
    """TCP/UDP flow tracking and analysis."""
    
    def __init__(self, flow_timeout=300):
        self.flows = {}  # flow_id -> FlowState
        self.flow_timeout = flow_timeout
    
    def process_packet(self, packet):
        flow_id = self._get_flow_id(packet)
        
        if flow_id not in self.flows:
            self.flows[flow_id] = FlowState(packet)
        
        flow = self.flows[flow_id]
        flow.update(packet)
        
        # Detect anomalies within the flow
        alerts = []
        
        # Port scan detection
        if flow.packet_count > 10 and flow.unique_ports > 5:
            alerts.append({
                'type': 'port_scan',
                'src_ip': packet.src_ip,
                'target_ports': flow.ports,
                'confidence': min(flow.unique_ports / 20, 1.0)
            })
        
        # Data exfiltration detection
        if flow.bytes_sent > 10_000_000:  # 10MB
            if flow.bytes_received < 1000:  # Asymmetric
                alerts.append({
                    'type': 'data_exfil',
                    'flow_id': flow_id,
                    'bytes_sent': flow.bytes_sent
                })
        
        return alerts
```

## Prevention Actions

```python
class IPSAction:
    """Actions the IPS can take on detected threats."""
    
    def __init__(self):
        self.actions = []
    
    def drop_packet(self, packet):
        """Drop the offending packet.
        Requires inline (not tap/mirror) deployment."""
        # Mark for dropping at the kernel level
        pass
    
    def reset_connection(self, flow_id):
        """Send TCP RST to both ends of the connection."""
        # Craft and inject TCP reset packets
        pass
    
    def rate_limit(self, src_ip, rate=100):
        """Rate-limit traffic from a source."""
        # Use iptables or eBPF for rate limiting
        pass
    
    def block_ip(self, ip, duration=3600):
        """Temporarily block an IP address."""
        # Add to dynamic block list
        pass
```

## Common Pitfalls

1. **False positives overload** — too many alerts desensitize operators; tune signatures carefully
2. **Encryption bypass** — TLS encrypts payload content; decrypt at proxy or use metadata-based detection
3. **Performance at line rate** — full DPI at 10Gbps+ is hard; use flow sampling and GPU acceleration
4. **Signature maintenance** — signatures become stale; automate rule updates from threat feeds
5. **Evasion techniques** — fragmentation, TTL tricks, encoding; normalize packets before analysis
6. **Inline vs. passive** — IPS must be inline but introduces latency; use fail-open for critical infrastructure

## Verification Checklist

- [ ] Known attack signatures detected correctly (test with CVE PoCs)
- [ ] False positive rate < 1% on normal traffic
- [ ] Performance: handles line rate without dropping packets
- [ ] Flow reassembly works correctly (TCP fragments reconstructed)
- [ ] Anomaly detection baseline adapts to normal traffic patterns
- [ ] Prevention actions work (packets dropped, connections reset)
- [ ] Logging and alerting integrated with SIEM format

## See Also

- pattern-matching-engine — high-performance content matching
- deep-packet-inspection-engine — advanced DPI patterns
- port-scanner-detection — dedicated scan detection
- packet-capture-engine — capturing packets for analysis
- firewall-rules-engine — blocking rules implementation
