---
name: agent-reasoning-patterns
description: "Use when implementing agent reasoning: ReAct, CoT, Plan-Solve."
category: mlops
tags: [agents, reasoning, react, chain-of-thought, planning]
---
# Agent Reasoning Patterns

Reasoning architectures for AI agents: ReAct, Chain-of-Thought, Plan-and-Solve.

## ReAct (Reasoning + Acting)

```
Thought: I need to find Docker disk usage.
Action: run_command["docker system df"]
Observation: TYPE        TOTAL   SIZE
             Images      5      2.3GB
             Containers  12     500MB
             Volumes     3      1.2GB
Thought: The total Docker disk usage is ~4GB.
Final Answer: Docker is using approximately 4GB of disk space.
```

```python
class ReActAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools

    def run(self, task):
        prompt = f"""Task: {task}
Available tools: {', '.join(self.tools.keys())}

Respond with alternating Thought/Action/Observation steps.
End with "Final Answer:" when complete.
"""
        return self.llm.invoke(prompt, max_tokens=1000)
```

## Chain-of-Thought (CoT)

```python
def zero_shot_cot(llm, question: str) -> str:
    prompt = f"""{question}

Let's think step by step:"""
    return llm.invoke(prompt)

def few_shot_cot(llm, question: str) -> str:
    prompt = """Q: How many containers can run on 32GB RAM if each needs 512MB?
A: 32GB = 32768MB. 32768 / 512 = 64 containers. So 64 containers.

Q: If Docker image layers total 2.5GB and bandwidth is 50Mbps, how long to pull?
A: 2.5GB = 2500MB. 50Mbps = 6.25MB/s. 2500 / 6.25 = 400 seconds. So about 6.7 minutes.

Q: {question}
A: Let's think step by step."""
    return llm.invoke(prompt)
```

## Plan-and-Solve

```python
class PlanAndSolveAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools

    def run(self, task):
        # Phase 1: Plan
        plan_prompt = f"""Decompose this task into subtasks:
Task: {task}
Format:
1. Subtask description [tool_needed]
2. Subtask description [tool_needed]
..."""
        plan = self.llm.invoke(plan_prompt)

        # Phase 2: Execute plan
        results = []
        for subtask in parse_plan(plan):
            result = self.execute_subtask(subtask)
            results.append(result)

        # Phase 3: Synthesize
        synthesis = self.llm.invoke(
            f"Based on these results, answer the original task: {task}\nResults: {results}"
        )
        return synthesis
```

## Reflection (Self-Correction)

```python
class ReflectiveAgent(ReActAgent):
    def run(self, task):
        answer = super().run(task)

        # Critique
        critique_prompt = f"""Task: {task}
Proposed answer: {answer}
Evaluate this answer. Is it correct and complete?
If not, explain what's missing and provide the correct answer."""
        critique = self.llm.invoke(critique_prompt)
        return critique
```

## Tree-of-Thoughts

```python
class TreeOfThoughts:
    def __init__(self, llm, branching=3, depth=3):
        self.llm = llm
        self.branching = branching
        self.depth = depth

    def solve(self, problem):
        states = [(problem, 0)]

        for level in range(self.depth):
            new_states = []
            for state, _ in states:
                prompt = f"""Problem: {problem}
Current state: {state}
Generate {self.branching} possible next steps:"""
                candidates = self.llm.invoke(prompt)

                for candidate in parse(candidates):
                    eval_prompt = f"Rate the likelihood this leads to solution (1-10): {candidate}"
                    score = int(self.llm.invoke(eval_prompt))
                    new_states.append((candidate, score))

            states = sorted(new_states, key=lambda x: -x[1])[:self.branching]

        return states[0][0]
```

## Pitfalls

- ReAct can loop between same thought-action pairs — add diversity penalty
- CoT adds tokens — budget carefully for long reasoning chains
- Plan-and-Solve is brittle if subtasks depend on each other
- Reflection doubles token usage
- Tree-of-Thoughts is expensive (branching * depth LLM calls)
