---
name: zero-trust-network-architecture
description: "Use when designing zero-trust network architecture patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [zero-trust, network-security, segmentation, ZTA, architecture]
    related_skills: [firewall-rules-engine, network-segmentation-strategies, vpn-tunnel-engine, wireguard-vpn-controller]
---

# Zero-Trust Network Architecture (ZTA)

Designing and implementing zero-trust network architectures — where no entity is trusted by default, every access is authenticated and authorized, and the network is assumed to be hostile.

## When to Use

- Modernizing network security from perimeter-based to zero-trust
- Building secure architectures for hybrid/remote work
- Designing micro-segmented networks for cloud-native apps
- Replacing or supplementing VPN-based access
- Regulatory compliance requiring least-privilege access

## Core Principles

```
1. Verify explicitly — always authenticate and authorize based on all available data
2. Least-privilege access — limit access to only what's needed
3. Assume breach — segment access, encrypt everything, monitor continuously
```

## Architecture Components

```
User/Device → Policy Engine → Policy Administrator → Policy Enforcement Point → Resource
                   ↓                ↓
              Continuous      Threat Intelligence
              Verification

Components:
- PEP (Policy Enforcement Point): gateway that enforces access
- PDP (Policy Decision Point): decides whether to allow access
- PA (Policy Administrator): provisions access based on PDP decision
- CE (Continuous Evaluation): monitors for changes in trust
```

## Implementation Patterns

### BeyondCorp-style (Google)

```python
class BeyondCorpGateway:
    """Application-level access proxy (like Google's IAP).
    No VPN needed — access is based on device + user + context."""
    
    def __init__(self):
        self.access_policy = {
            'allow_all_staff': {'condition': 'user.is_employee'},
            'allow_engineering': {'condition': 'user.dept == "engineering"'},
            'allow_admin': {'condition': 'user.role == "admin" AND device.managed'},
        }
    
    def check_access(self, request, user_context, device_context):
        """Check if access should be granted."""
        
        # 1. Device posture check
        if not self._verify_device_health(device_context):
            return False
        
        # 2. User authentication
        if not self._verify_user(request, user_context):
            return False
        
        # 3. Authorization
        resource = self._get_resource(request.url)
        policy = self.access_policy.get(resource.required_policy)
        
        if not policy:
            return False
        
        # 4. Context-aware evaluation
        if not self._evaluate_policy(policy['condition'], user_context, device_context):
            return False
        
        # 5. Just-in-time access
        session = self._create_jit_session(user_context, resource, ttl=3600)
        
        return True, session
```

### Micro-Segmentation

```python
class MicroSegmenter:
    """Network micro-segmentation using eBPF or iptables.
    Each workload gets its own security group."""
    
    def __init__(self):
        self.segments = {
            'web-frontend': {
                'allowed_ingress': ['internet:443'],
                'allowed_egress': ['api-backend:8080'],
                'policies': ['user-auth:required']
            },
            'api-backend': {
                'allowed_ingress': ['web-frontend:8080'],
                'allowed_egress': ['database:5432', 'cache:6379'],
                'policies': ['mTLS:required', 'rate-limit:1000/s']
            },
            'database': {
                'allowed_ingress': ['api-backend:5432'],
                'allowed_egress': [],
                'policies': ['mTLS:required', 'encryption-at-rest']
            }
        }
    
    def get_segment_rules(self, segment_name):
        """Generate firewall rules for a segment."""
        segment = self.segments[segment_name]
        rules = []
        
        for ingress in segment['allowed_ingress']:
            source, port = ingress.split(':')
            rules.append({
                'direction': 'ingress',
                'source': source,
                'protocol': 'tcp',
                'port': int(port),
                'action': 'allow'
            })
        
        return rules
```

### Service Identity and mTLS

```python
class ServiceIdentity:
    """Service-to-service mTLS with SPIFFE identities."""
    
    def issue_identity(self, service_name, namespace):
        """Issue a SPIFFE-compatible identity certificate."""
        return {
            'spiffe_id': f'spiffe://cluster.local/ns/{namespace}/sa/{service_name}',
            'certificate': self._generate_x509(),
            'ttl': 86400,  # 24 hours
            'trust_domain': 'cluster.local'
        }
    
    def verify_identity(self, presented_cert, expected_service):
        """Verify presented certificate matches expected service."""
        spiffe_id = self._extract_spiffe(presented_cert)
        return spiffe_id.endswith(f'/sa/{expected_service}')
```

### Continuous Verification

```python
class ContinuousVerifier:
    """Continuous evaluation of trust — never assume static trust."""
    
    def __init__(self):
        self.trust_scores = {}  # entity -> score (0.0-1.0)
    
    def evaluate(self, entity_id, context):
        """Re-evaluate trust score based on current context."""
        score = 0.5  # Start neutral
        
        # Device factors
        if context.get('device_patch_level') == 'up_to_date':
            score += 0.15
        if context.get('device_encrypted'):
            score += 0.1
        if context.get('device_has_malware'):
            score -= 0.5
        
        # User factors
        if context.get('recent_mfa'):
            score += 0.15
        if context.get('unusual_location'):
            score -= 0.2
        if context.get('failed_auth_attempts', 0) > 3:
            score -= 0.3
        
        # Behavioral factors
        if context.get('access_pattern_anomaly'):
            score -= 0.2
        if context.get('data_access_volume') > 1000:
            score -= 0.1
        
        self.trust_scores[entity_id] = max(0.0, min(1.0, score))
        return self.trust_scores[entity_id]
```

## Common Pitfalls

1. **VPN replacement envy** — ZTA isn't just "VPN 2.0"; it requires fundamental architecture change
2. **Certificate management complexity** — mTLS at scale requires robust PKI; use cert-manager or SPIFFE
3. **Performance overhead** — every request requires authN/authZ; use caching and session tokens wisely
4. **Legacy application support** — apps that assume network trust need adaptation; use sidecars for transparent mTLS
5. **Monitoring blind spots** — encrypted traffic hides content; rely on metadata and flow analysis
6. **User friction** — continuous verification can interrupt workflow; balance security with usability

## Verification Checklist

- [ ] All traffic encrypted (no plaintext services)
- [ ] Every request authenticated and authorized
- [ ] Micro-segmentation prevents lateral movement
- [ ] Service identities verified via mTLS
- [ ] Trust continuously re-evaluated (time-based sessions)
- [ ] No implicit trust between services
- [ ] Audit logging captures all access decisions

## See Also

- firewall-rules-engine — implementing ZTA firewall rules
- network-segmentation-strategies — segmenting networks
- vpn-tunnel-engine — traditional VPN (transitioning from)
- wireguard-vpn-controller — securing inter-service comms
