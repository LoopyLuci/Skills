---
name: network-sniffing-packet-capture
description: "Use when sniffing networks and analyzing packet captures."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [network-sniffing, tcpdump, Wireshark, pcap, packet-analysis, ARP-spoof]
    related_skills: [network-forensics-analysis, packet-capture-engine, network-scanning-enumeration, traffic-analyzer]
---

# Network Sniffing and Packet Capture

Sniffing networks and analyzing packet captures — from tcpdump and Wireshark through ARP spoofing, protocol analysis, and traffic decryption.

## When to Use

- Capturing and analyzing network traffic during pentests
- Debugging network protocols and applications
- Analyzing malware network behavior
- Performing man-in-the-middle testing
- Extracting data from pcap files

## Sniffing Techniques

```python
# tcpdump basics
TCPDUMP_CAPTURES = {
    'capture_interface': "tcpdump -i eth0 -w capture.pcap",
    'capture_specific_host': "tcpdump host 10.0.0.5 -w host_traffic.pcap",
    'capture_http': "tcpdump port 80 or port 443 -w web_traffic.pcap",
    'filter_by_proto': "tcpdump 'tcp[tcpflags] & tcp-syn != 0' -w syns.pcap",
}

# Wireshark display filters
WIRESHARK_FILTERS = {
    'http_requests': "http.request",
    'tls_handshakes': "tls.handshake.type == 1",
    'dns_queries': "dns.flags.response == 0",
    'specific_ip': "ip.addr == 10.0.0.1",
    'credentials': "http.request.method == POST || ftp.request.command == USER",
    'follow_stream': "Right-click → Follow → TCP/UDP/HTTP Stream",
}

# Simple ARP spoofing for MITM (educational purposes)
def arp_spoof_demo(target_ip: str, gateway_ip: str, interface: str = 'eth0'):
    """
    Demonstration: ARP cache poisoning for network testing.
    Actual implementation requires scapy and proper authorization.
    """
    pass
```

## Verification Checklist

- [ ] Proper authorization obtained before sniffing
- [ ] Interface in promiscuous mode (if needed)
- [ ] Capture filters applied to reduce file size
- [ ] Wireshark display filters used for analysis
- [ ] TLS traffic decrypted (if keys available)
- [ ] Extracted artifacts (files, credentials, sessions)
- [ ] Network captures stored securely and destroyed post-engagement
- [ ] Legal/compliance reviewed (wiretap laws, ToS)
