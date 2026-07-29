---
name: iot-security-framework
description: "Use when securing IoT devices and networks."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [iot-security, device-security, firmware, embedded, OTA, mTLS]
    related_skills: [container-security-hardening, network-segmentation-strategies, certificate-management-pki, identity-access-management]
---

# IoT Security Framework

Securing IoT devices and networks — from device identity and firmware security through secure boot, OTA updates, network segmentation, and lifecycle management.

## When to Use

- Building secure IoT products and devices
- Securing IoT device communication and data
- Implementing firmware update mechanisms
- Managing device identities and certificates
- Isolating IoT devices on networks

## IoT Security Layers

```python
IOT_SECURITY_LAYERS = {
    'device_hardening': 'Disable unused ports, remove debug interfaces, tamper-resistant enclosures',
    'secure_boot': 'Verified boot chain — bootloader signs kernel, kernel signs filesystem',
    'firmware_security': 'Signed firmware, encrypted storage, secure OTA update mechanism',
    'identity': 'Unique device certificate (X.509), TPM or secure element for key storage',
    'communication': 'mTLS between device and cloud, certificate pinning, protocol buffers',
    'network': 'IoT VLAN segmentation, firewall between IoT and production, egress-only where possible',
}

# Secure OTA update flow
def secure_ota(current_version: str, update_package: bytes, 
               signature: bytes, device_cert: str) -> bool:
    import hashlib, json
    expected_hash = hashlib.sha256(update_package).digest()
    # Verify signature against device certificate
    if verify_signature(expected_hash, signature, device_cert):
        return apply_update(update_package)
    return False
```

## Verification Checklist

- [ ] Device identity provisioned (X.509 certificate per device)
- [ ] Secure boot enabled (verified boot chain)
- [ ] Firmware updates signed and verified before install
- [ ] mTLS for cloud communication
- [ ] IoT devices on isolated network segment (VLAN)
- [ ] Egress-only firewall rules (no inbound to IoT)
- [ ] TPM/secure element for key storage
- [ ] Device lifecycle management (decommissioning, credential revocation)
- [ ] Over-the-air (OTA) update mechanism tested and secure
