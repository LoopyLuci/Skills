---
name: certificate-management-pki
description: "Use when managing PKI and TLS certificate lifecycles."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [PKI, certificates, TLS, SSL, ACME, cert-manager, CA, certificate-lifecycle]
    related_skills: [identity-access-management, cryptography-implementation-patterns, security-incident-response, dns-implementation-patterns]
---

# Certificate Management and PKI

Managing public key infrastructure and TLS certificate lifecycles — from CA setup and certificate issuance through automated renewal with ACME, revocation, and monitoring.

## When to Use

- Managing TLS certificates for web services and APIs
- Building an internal PKI for service-to-service mTLS
- Automating certificate renewal with Let's Encrypt or cert-manager
- Implementing certificate revocation and rotation
- Complying with security standards requiring certificate management

## Certificate Lifecycle

```python
CERTIFICATE_LIFECYCLE = {
    'request': 'Generate CSR, submit to CA (internal or public)',
    'issue': 'CA signs certificate after validation (DV, OV, or EV)',
    'deploy': 'Install on servers, load balancers, or applications',
    'monitor': 'Track expiry dates, start renewal at 30 days',
    'renew': 'Re-issue before expiry (automated with ACME)',
    'revoke': 'Immediately revoke if compromised (CRL/OCSP)',
}

class CertificateManager:
    """Track and manage certificate lifecycles."""
    def __init__(self):
        self.certs = {}
    
    def add_certificate(self, domain: str, issuer: str, 
                        expiry: str, auto_renew: bool = True):
        self.certs[domain] = {
            'issuer': issuer, 'expiry': expiry,
            'auto_renew': auto_renew, 'status': 'valid',
            'renewal_in_days': None,
        }
    
    def get_expiring_certs(self, days: int = 30) -> List[Dict]:
        from datetime import datetime, timedelta
        threshold = datetime.now() + timedelta(days=days)
        expiring = []
        for domain, info in self.certs.items():
            expiry = datetime.fromisoformat(info['expiry'])
            if expiry <= threshold:
                expiring.append({'domain': domain, 'expiry': info['expiry']})
        return expiring
```

## Common Pitfalls

1. **Certificate expiry** — expired certs cause outages; automate renewal with ACME
2. **Manual processes** — manual renewal on 100+ certs guarantees some will expire
3. **Weak key sizes** — use 2048+ bit RSA or ECDSA P-256/P-384
4. **No monitoring** — no alert when cert is expiring or has been revoked
5. **Self-signed certs everywhere** — breaks trust; use internal CA or public trusted certs

## Verification Checklist

- [ ] Certificate inventory maintained (all domains, issuers, expiry dates)
- [ ] Automated renewal configured (ACME/cert-manager)
- [ ] Monitoring on certificate expiry (alert at 30, 14, 7 days)
- [ ] OCSP stapling enabled on web servers
- [ ] Certificate revocation procedure documented
- [ ] Key sizes meet security requirements (≥2048-bit RSA or P-256 ECDSA)
- [ ] Internal CA configured for service mesh mTLS (if applicable)
