---
name: swarm-communication-protocols
description: "Use when designing agent-to-agent communication in swarms."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents, swarm, communication, protocols, messaging]
    related_skills: [agent-swarm-architectures, hierarchical-swarm-architectures, multi-agent-orchestration, tool-augmented-agents]
---

# Swarm Communication Protocols

Designing and implementing communication protocols between agents in a swarm — message formats, routing, synchronization, and conflict resolution.

## When to Use

- Designing how agents in a swarm talk to each other
- Building multi-agent systems where agents share context, results, or dependencies
- Implementing broadcast, multicast, or point-to-point agent messaging
- Handling agent synchronization, consensus, or conflict resolution
- Designing agent communication languages and schemas

## Communication Topologies

### Point-to-Point (Direct)
```
Agent A ──────→ Agent B
```
Best for: Known dependencies, task handoffs, private coordination.

### Broadcast
```
Agent A ──────→ All agents
```
Best for: Status updates, shared observations, emergency stops.

### Multicast (Group)
```
Agent A ──────→ Group X (agents B, C, D)
```
Best for: Team updates, shared task context, parallel sub-task coordination.

### Publish-Subscribe
```
Agent A (Publisher) → Message Bus → Subscribers (B, C, D)
```
Best for: Decoupled communication, event-driven swarms, scalable systems.

### Blackboard
```
All agents read/write to shared context store
```
Best for: Collaborative problem-solving, shared state, gradual convergence.

## Message Formats

### Structured Message Schema

```json
{
  "protocol_version": "1.0",
  "message_id": "msg_001",
  "sender": "agent_worker_3",
  "recipient": "agent_manager_1",
  "message_type": "task_result",
  "timestamp": "2026-07-28T12:00:00Z",
  "ttl": 300,
  "priority": "normal",
  "payload": {
    "task_id": "task_42",
    "status": "completed",
    "result_summary": "Rule parser processed 10K rules",
    "artifacts": ["/tmp/rules_parsed.json"],
    "metrics": {"duration_s": 2.3, "rules_per_second": 4348}
  },
  "context": {
    "parent_task": "task_40",
    "dependencies": ["task_41"],
    "blocked_tasks": []
  },
  "signature": "hmac_sha256_hash"
}
```

### Compact Message (Low-Overhead)

```json
{
  "id": "m_1",
  "from": "w3",
  "to": "m1",
  "type": "result",
  "task": "t42",
  "status": "ok",
  "ts": 1722172800
}
```

### Control Messages

| Type | Purpose | Example |
|------|---------|--------|
| `heartbeat` | Liveness check | `{"type": "hb", "from": "w3", "load": 0.7}` |
| `ack` | Acknowledgment | `{"type": "ack", "in_reply_to": "msg_001"}` |
| `nack` | Negative ack | `{"type": "nack", "in_reply_to": "msg_001", "reason": "busy"}` |
| `escalate` | Issue escalation | `{"type": "escalate", "issue": "timeout", "from": "w3", "to": "m1"}` |
| `sync_request` | State sync | `{"type": "sync_req", "from": "m1"}` |
| `sync_response` | State snapshot | `{"type": "sync_resp", "state": {...}}` |
| `cancel` | Cancel task | `{"type": "cancel", "task_id": "t42"}` |

## Synchronization Patterns

### Barrier Synchronization

All agents must reach a checkpoint before any proceeds:

```python
# Manager coordinates barrier
def barrier(agent_ids, timeout=60):
    ready = set()
    start = time.time()
    while len(ready) < len(agent_ids):
        if time.time() - start > timeout:
            raise TimeoutError(f"Barrier timeout: {agent_ids - ready}")
        for agent in agent_ids:
            if agent.reports("ready"):
                ready.add(agent)
        time.sleep(0.5)
    # All agents proceed
```

### Consensus Protocol

Agents agree on a value (e.g., classification, decision):

```python
def simple_majority_consensus(agent_votes):
    """Each agent votes; majority wins."""
    counts = {}
    for vote in agent_votes:
        counts[vote] = counts.get(vote, 0) + 1
    winner = max(counts, key=counts.get)
    threshold = len(agent_votes) * 0.5 + 1
    if counts[winner] >= threshold:
        return winner
    raise ConsensusError("No majority reached")
```

### Quorum Protocol

For critical decisions, require N confirmations before acting:

```python
def quorum_check(confirmations, total_agents, quorum_pct=0.66):
    return len(confirmations) >= total_agents * quorum_pct
```

## Conflict Resolution

### Resource Conflicts
Multiple agents need the same resource (file, tool, API):

```python
# Lock-based resolution
import threading
resource_locks = {}

def acquire_resource(resource_id, agent_id, timeout=10):
    lock = resource_locks.setdefault(resource_id, threading.Lock())
    if lock.acquire(timeout=timeout):
        return True
    # Conflict: manager arbitrates
    manager_arbitrate(resource_id, agent_id)
    return False
```

### Priority-Based Resolution
Higher-priority agents preempt lower-priority ones:

```python
PRIORITY_MAP = {"critical": 5, "high": 4, "normal": 3, "low": 2, "background": 1}

def resolve_conflict(agents_contending, resource):
    return max(agents_contending, key=lambda a: PRIORITY_MAP.get(a.priority, 3))
```

## Agent Communication Languages

### Hermes Delegation Protocol (via delegate_task)

```python
# Built-in: sub-agents communicate through delegate_task
# The tool itself handles serialization, routing, result collection
result = delegate_task(
    goal="Analyze network traffic patterns",
    context=f"Raw data from agent-alpha: {traffic_data}"
)
```

### Custom MCP-Based Agent Communication

```python
# Agents communicate through MCP tools exposed by each other
# Agent A calls Agent B's MCP endpoint
response = call_agent_mcp(
    agent_id="b",
    tool="analyze_traffic",
    parameters={"data": traffic_sample}
)
```

### Structured Context Passing

```python
# Shared blackboard pattern
class AgentBlackboard:
    def __init__(self):
        self.store = {}
        self.subscribers = {}
    
    def write(self, key, value, publisher):
        self.store[key] = {"value": value, "publisher": publisher, "ts": time.time()}
        self._notify(key, value)
    
    def read(self, key):
        return self.store.get(key)
    
    def subscribe(self, key_pattern, callback):
        self.subscribers.setdefault(key_pattern, []).append(callback)
    
    def _notify(self, key, value):
        for pattern, callbacks in self.subscribers.items():
            if fnmatch.fnmatch(key, pattern):
                for cb in callbacks:
                    cb(key, value)
```

## Common Pitfalls

1. **Message storms** — N agents broadcasting to each other creates O(N²) traffic; use pub/sub or hierarchical routing
2. **Infinite waits** — always set timeouts on inter-agent communication
3. **Stale state** — agents operating on outdated shared state; use versioned or timestamped data
4. **Serialization mismatches** — agents must agree on message schemas; use protobuf/avro for cross-language
5. **Deadlocks** — circular dependencies in resource allocation; use timeout-based backoff
6. **Security** — unauthenticated agent messages; implement signatures or tokens for critical operations

## Verification Checklist

- [ ] Communication topology matches swarm structure (flat/pub-sub/hierarchical)
- [ ] Message format schema is documented and versioned
- [ ] Timeouts defined for every message type
- [ ] Conflict resolution strategy documented
- [ ] Heartbeat/liveness monitoring configured
- [ ] Synchronization barriers at critical dependency points
- [ ] Fallback for unresponsive agents defined

## See Also

- agent-swarm-architectures — flat swarm topology design
- hierarchical-swarm-architectures — multi-level hierarchy patterns
- multi-agent-orchestration — orchestrating multiple agents
- tool-augmented-agents — building tools for agents
