---
name: agent-fault-tolerance
description: "Use when implementing fault tolerance for agent systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [fault-tolerance, resilience, recovery, redundancy, agent-reliability]
    related_skills: [multi-agent-collaboration-patterns, agent-swarm-architectures, distributed-systems-patterns, agent-safety-monitoring]
---

# Agent Fault Tolerance

Implementing fault tolerance in agent systems — from redundancy and health checks through graceful degradation, recovery, and self-healing.

## When to Use

- Production agent systems that must be reliable
- Multi-agent swarms where individual agents may fail
- Long-running agent workflows that must survive failures
- Mission-critical agent deployments

## Fault Tolerance Patterns

```python
FAULT_TOLERANCE_PATTERNS = {
    'redundancy': 'Multiple agents with same capability; if one fails, others take over',
    'checkpointing': 'Regularly save agent state so it can resume after failure',
    'heartbeat_monitoring': 'Health check pings; failed agents are detected and replaced',
    'circuit_breaker': 'Stop sending to failing agent, retry after cooldown',
    'degradation': 'System continues with reduced functionality when agents fail',
    'retry_with_backoff': 'Retry failed operations with exponential backoff',
}

class AgentHealthMonitor:
    """Monitor agent health and trigger recovery."""
    def __init__(self, timeout: int = 30):
        self.agents = {}  # agent_id -> last_heartbeat
        self.timeout = timeout
    
    def record_heartbeat(self, agent_id: str):
        self.agents[agent_id] = time.time()
    
    def check_health(self, agent_id: str) -> bool:
        last = self.agents.get(agent_id)
        if last is None: return False
        return (time.time() - last) < self.timeout
    
    def get_failed_agents(self) -> List[str]:
        return [a for a in self.agents if not self.check_health(a)]
```

## Common Pitfalls

1. **Insufficient redundancy** — having only 2 agents for N tasks guarantees overload on failure
2. **No isolation** — cascade failures when one agent's failure triggers others
3. **Recovery without testing** — recovery paths often fail in production; test them
4. **State loss** — agent state not persisted; checkpoint critical state
5. **Silent failures** — agent fails without alerting; monitor liveness actively

## Verification Checklist

- [ ] Health monitoring with heartbeat/keepalive
- [ ] Redundancy factor defined (N+1 or 2N)
- [ ] State checkpointing implemented
- [ ] Failure detection time < recovery time
- [ ] Graceful degradation path defined
- [ ] Recovery procedures tested (chaos engineering)
