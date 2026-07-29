---
name: container-networking-patterns
description: "Use when designing container and Kubernetes networking."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [container-networking, kubernetes, docker, CNI, service-mesh, overlay]
    related_skills: [service-mesh-patterns, api-gateway-load-balancing, docker-networking-troubleshoot, dns-implementation-patterns]
---

# Container Networking Patterns

Designing and implementing container networking for Docker, Kubernetes, and cloud-native environments — CNI plugins, overlay networks, service discovery, ingress, and network policies.

## When to Use

- Designing container network architecture (Docker, Kubernetes)
- Implementing CNI plugins for custom networking
- Configuring network policies and multi-tenancy isolation
- Troubleshooting container network connectivity
- Building secure multi-cluster communication

## Container Network Models

### Docker Networking

```bash
# Bridge (default): containers on same host communicate via docker0 bridge
docker network create --driver bridge my-network
docker run --network my-network my-app

# Host: containers use host network directly (no isolation)
docker run --network host my-app

# Overlay: multi-host networking (Docker Swarm or K8s)
docker network create --driver overlay my-overlay

# Macvlan: containers get MAC addresses on physical network
docker network create --driver macvlan --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 -o parent=eth0 my-macvlan
```

### Kubernetes Network Model (CNI)

```python
# K8s network fundamentals:
# 1. Every pod gets its own IP address
# 2. All pods can communicate with all other pods without NAT
# 3. Agents (kubelet) can communicate with all pods

# CNI plugins implement the K8s network model:
# - Calico: BGP-based, network policies, eBPF data plane
# - Flannel: VXLAN overlay, simple, no network policies
# - Cilium: eBPF-based, L3/L4/L7 policies, service mesh
# - Weave: mesh overlay, encryption, simple
# - Antrea: Open vSwitch-based, performance-focused
```

## CNI Plugin Architecture

```python
class CNIPlugin:
    """Simplified CNI plugin implementation.
    
    CNI is called by kubelet (or container runtime) to:
    ADD: set up container networking
    DEL: tear down container networking
    CHECK: verify networking is correct
    """
    
    def add(self, container_id: str, netns_path: str, 
            interface_name: str, pod_name: str, pod_namespace: str) -> dict:
        """Set up networking for a new pod."""
        
        # 1. Allocate IP address
        ip = self.ipam.allocate(pod_name, pod_namespace)
        
        # 2. Create veth pair (one end in container, one on host)
        host_iface = f"veth{container_id[:8]}"
        self._create_veth(host_iface, interface_name, netns_path)
        
        # 3. Move container end to pod network namespace
        self._move_to_netns(netns_path, interface_name)
        
        # 4. Configure IP address in container
        self._configure_ip(netns_path, interface_name, ip)
        
        # 5. Add route to default gateway
        self._add_default_route(netns_path, interface_name)
        
        # 6. Attach host end to the network bridge/overlay
        self._attach_to_bridge(host_iface)
        
        # 7. Apply network policies (if any)
        self._apply_policies(pod_name, pod_namespace, interface_name)
        
        return {
            "cniVersion": "1.0.0",
            "interfaces": [
                {"name": interface_name, "sandbox": netns_path},
                {"name": host_iface},
            ],
            "ips": [{"version": "4", "address": f"{ip}/24", "gateway": "10.0.0.1"}],
            "dns": {"nameservers": ["10.0.0.10"]}
        }
    
    def delete(self, container_id: str, netns_path: str, interface_name: str):
        """Tear down networking for a deleted pod."""
        host_iface = f"veth{container_id[:8]}"
        
        # Remove from bridge
        self._detach_from_bridge(host_iface)
        
        # Delete veth pair
        self._delete_veth(host_iface)
        
        # Release IP
        self.ipam.release(container_id)
```

## Overlay Networks

### VXLAN

```python
class VXLANOverlay:
    """VXLAN-based overlay network for cross-host container communication.
    
    VXLAN encapsulates Layer 2 frames in UDP packets (port 4789).
    VTEP (VXLAN Tunnel Endpoint) at each host."""
    
    def __init__(self, vni=100, mtu=1450):
        self.vni = vni  # VXLAN Network Identifier (24-bit)
        self.mtu = mtu
    
    def setup_vtep(self, local_ip, remote_ips):
        """Configure VXLAN tunnel on a host."""
        vxlan_commands = [
            # Create VXLAN interface
            f"ip link add vxlan{self.vni} type vxlan id {self.vni} "
            f"local {local_ip} dstport 4789 dev eth0",
            
            # Set MTU (lower to account for VXLAN header overhead)
            f"ip link set mtu {self.mtu} dev vxlan{self.vni}",
            
            # Add remote VTEPs
            *[f"bridge fdb append to 00:00:00:00:00:00 dst {rip} dev vxlan{self.vni}"
              for rip in remote_ips],
            
            # Bring interface up
            f"ip link set vxlan{self.vni} up",
        ]
        return vxlan_commands
    
    def add_container(self, container_ip, vxlan_iface="vxlan100"):
        """Connect a container bridge to the VXLAN."""
        return [
            f"ip link add br-{vni}" type bridge",
            f"ip link set {vxlan_iface} master br-{vni}",
            f"ip addr add {container_ip}/24 dev br-{vni}",
        ]
```

## Network Policies

```python
class KubernetesNetworkPolicy:
    """Kubernetes NetworkPolicy examples for pod-level isolation."""
    
    @staticmethod
    def deny_all_ingress():
        return {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {"name": "deny-all-ingress"},
            "spec": {
                "podSelector": {},  # All pods
                "policyTypes": ["Ingress"],
                "ingress": []  # No ingress rules = deny all
            }
        }
    
    @staticmethod
    def allow_from_namespace(namespace: str, app_label: str):
        """Allow ingress only from specific namespace and app."""
        return {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {"name": f"allow-from-{namespace}"},
            "spec": {
                "podSelector": {"matchLabels": {"app": app_label}},
                "policyTypes": ["Ingress"],
                "ingress": [{
                    "from": [{
                        "namespaceSelector": {
                            "matchLabels": {"kubernetes.io/metadata.name": namespace}
                        }
                    }]
                }]
            }
        }
    
    @staticmethod
    def allow_egress_to_dns():
        """Allow DNS resolution only."""
        return {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {"name": "allow-dns-egress"},
            "spec": {
                "podSelector": {},
                "policyTypes": ["Egress"],
                "egress": [{
                    "to": [{"ipBlock": {"cidr": "10.0.0.0/8"}}],
                    "ports": [{"protocol": "UDP", "port": 53}]
                }]
            }
        }
```

## Common Pitfalls

1. **MTU issues** — overlay headers add 20-50 bytes; reduce MTU or enable MSS clamping
2. **ARP storm** — large overlay networks flood ARP; use ARP proxy or L3 routing
3. **Policy enforcement order** — NetworkPolicy ordering matters in some implementations
4. **DNS resolution** — pod DNS config can prevent service discovery; check resolv.conf
5. **VXLAN scalability** — head-end replication doesn't scale; use multicast or EVPN for large clusters
6. **kube-proxy vs Cilium** — iptables-based kube-proxy is slow for many services; use eBPF/IPVS

## Verification Checklist

- [ ] Pod-to-pod communication works across hosts (not just same host)
- [ ] Pod-to-service communication works (ClusterIP resolves correctly)
- [ ] Network policies enforced (deny-all blocks unexpected traffic)
- [ ] DNS resolution within cluster works
- [ ] MTU properly configured (test with large packets, no fragmentation)
- [ ] No hairpin NAT issues (pod accessing its own service via ClusterIP)
- [ ] Throughput between containers on different hosts matches expectation

## See Also

- service-mesh-patterns — L7 traffic management on top of container networking
- api-gateway-load-balancing — ingress and north-south traffic
- docker-networking-troubleshoot — debugging container connectivity
- dns-implementation-patterns — DNS for service discovery
