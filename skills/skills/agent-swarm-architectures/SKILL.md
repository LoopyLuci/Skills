---
name: agent-swarm-architectures
description: "Use when designing agent swarm topology and communication."
category: mlops
tags: [agents, swarms, architecture, topology, communication]
---
# Agent Swarm Architectures

Designing topology, communication, and coordination patterns for agent swarms.

## Swarm Topologies

```
Star (Hub-and-Spoke)         Ring                     Mesh (Fully Connected)
    C1                       C1──C2                       C1──C2
     \                      /      \                     /│\ │
      H──C2                H        C3                  │ │ \│/
     /                      \      /                     │ │ /│\
    C3                       C5──C4                       C3──C4
```

### When to Use Each

| Topology | Pros | Cons | Best For |
|----------|------|------|----------|
| Star | Simple, central control | SPOF, bottleneck | Manager-worker |
| Ring | No SPOF, simple routing | Slow propagation | Consensus chains |
| Mesh | Redundant, fast | O(n²) connections | Small, critical teams |
| Tree | Scalable, hierarchical | Rigid | Large organizations |
| Dynamic | Adaptive | Complex | Unknown task domains |

## Dynamic Swarm Formation

```python
class SwarmFormationAgent:
    def __init__(self, llm, available_agents: list):
        self.llm = llm
        self.agents = available_agents

    def form_swarm(self, task: str) -> list:
        """Determine optimal agent composition for a task."""
        prompt = f"""Task: {task}
Available agents: {[(a.name, a.capabilities) for a in self.agents]}
Select the optimal subset of agents and specify their roles.
Format: agent_name: role (coordinator|worker|observer|critic)"""
        formation = self.llm.invoke(prompt)
        return self._parse_formation(formation)

    def rebalance(self, swarm: list, performance: dict) -> list:
        """Adjust swarm composition based on performance."""
        underperforming = [a for a in swarm if performance.get(a.name, 1.0) < 0.5]
        if underperforming:
            prompt = f"Replace underperforming agents {underperforming} with alternatives from {self.agents}"
            replacements = self.llm.invoke(prompt)
            swarm = [a for a in swarm if a not in underperforming] + replacements
        return swarm
```

## Communication Protocols

```python
class Message:
    def __init__(self, sender: str, receiver: str, msg_type: str,
                 content: str, priority: int = 0):
        self.sender = sender
        self.receiver = receiver
        self.type = msg_type  # request, response, broadcast, error
        self.content = content
        self.priority = priority
        self.id = f"{sender}_{id(self)}"

class MessageBus:
    def __init__(self):
        self.queues = {}       # agent_name → [Message]
        self.topics = {}        # topic → [subscriber_agents]

    def send(self, message: Message):
        if message.type == "broadcast":
            self._broadcast(message)
        else:
            self.queues.setdefault(message.receiver, []).append(message)

    def _broadcast(self, message: Message):
        for agent in self.topics.get("all", []):
            self.queues.setdefault(agent, []).append(message)

    def receive(self, agent_name: str) -> list[Message]:
        messages = self.queues.get(agent_name, [])
        self.queues[agent_name] = []
        return messages

    def subscribe(self, agent_name: str, topic: str = "all"):
        self.topics.setdefault(topic, set()).add(agent_name)
```

## Coordination Strategies

```python
class Coordinator:
    def __init__(self, strategy: str = "voting"):
        self.strategy = strategy
        self.votes = []

    def coordinate(self, agents: list, task: str) -> str:
        if self.strategy == "voting":
            return self._voting(agents, task)
        elif self.strategy == "ranking":
            return self._ranking(agents, task)
        elif self.strategy == "consensus":
            return self._consensus(agents, task)
        elif self.strategy == "best_of_n":
            return self._best_of_n(agents, task)

    def _voting(self, agents, task):
        responses = [a.execute(task) for a in agents]
        return max(set(responses), key=responses.count)  # majority

    def _ranking(self, agents, task):
        responses = [a.execute(task) for a in agents]
        scored = [(self._rate_response(r), r) for r in responses]
        return max(scored, key=lambda x: x[0])[1]

    def _best_of_n(self, agents, task):
        n_responses = 5
        all_responses = [agents[0].execute(task) for _ in range(n_responses)]
        # Pick the most consistent (similar to self-consistency)
        return max(set(all_responses), key=all_responses.count)
```

## Pitfalls

- Star topology: coordinator is bottleneck and SPOF
- Full mesh: O(n²) connections don't scale past ~10 agents
- Dynamic formation: LLM decisions about agent roles can be wrong
- Broadcast storms: too many broadcast messages degrade performance
- Agent departure: design for graceful degradation when agents fail
