---
name: advanced-reasoning-patterns
description: "Use when implementing CoT, ToT, GoT, and ReAct patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [reasoning, chain-of-thought, tree-of-thought, react, prompt-engineering]
    related_skills: [agent-reasoning-patterns, prompt-engineering-patterns, agent-framework-design, tool-augmented-agents]
---

# Advanced Reasoning Patterns — CoT, ToT, GoT, ReAct

Implementing advanced reasoning patterns for LLMs and agents — from Chain-of-Thought through Tree-of-Thought, Graph-of-Thought, ReAct, and beyond, with practical implementation patterns for each.

## When to Use

- Improving LLM accuracy on complex reasoning tasks (math, logic, multi-step)
- Building agents that need to reason before acting
- Combining multiple reasoning paths for more robust answers
- Debugging why a model made an incorrect inference
- Implementing self-correcting or self-improving reasoning loops

## Pattern Comparison

| Pattern | Search Space | Parallelism | Best For | Token Cost |
|---------|-------------|-------------|----------|-----------|
| CoT | Single path | No | Sequential reasoning | 1x |
| CoT-SC | Multiple paths | Yes | High-stakes accuracy | N× |
| ToT | Tree search | Selective | Planning, puzzles | 10–100× |
| GoT | Graph | Selective | Multi-faceted problems | 10–50× |
| ReAct | Linear + tools | No | Agentic tasks | 2–5× |
| Self-Consistency | Parallel CoT | Yes | Verification | N× |
| Reflection | Iterative | No | Self-correction | 2–5× |

## Chain-of-Thought (CoT)

### Zero-Shot CoT

```python
def zero_shot_cot(prompt, model):
    """Zero-shot Chain-of-Thought: just add 'Let's think step by step'.
    Simple but effective for many reasoning tasks."""
    cot_prompt = f"{prompt}\n\nLet's think step by step."
    response = model.generate(cot_prompt)
    return response
```

### Few-Shot CoT

```python
def few_shot_cot(question, model, examples=None):
    """Few-shot Chain-of-Thought with worked examples."""
    if examples is None:
        examples = [
            {
                "question": "If John has 5 apples and gives 2 to Mary, how many does he have left?",
                "reasoning": "John starts with 5 apples. He gives 2 away. 5 - 2 = 3.",
                "answer": "3 apples"
            },
            {
                "question": "A train travels 60 miles in 1 hour. How far in 3 hours?",
                "reasoning": "Speed = 60 mph. Distance = speed × time = 60 × 3 = 180.",
                "answer": "180 miles"
            }
        ]
    
    # Format examples
    prompt = ""
    for ex in examples:
        prompt += f"Q: {ex['question']}\nReasoning: {ex['reasoning']}\nAnswer: {ex['answer']}\n\n"
    
    prompt += f"Q: {question}\nReasoning:"
    return model.generate(prompt)
```

### CoT with Self-Consistency (CoT-SC)

```python
def cot_self_consistency(question, model, num_samples=5, temperature=0.7):
    """Sample multiple reasoning paths, then vote on the final answer.
    Improves accuracy by 5-15% on math reasoning tasks."""
    responses = []
    
    for i in range(num_samples):
        prompt = f"Q: {question}\nReasoning: Let's think step by step.\n"
        response = model.generate(prompt, temperature=temperature + 0.1 * i)
        responses.append(extract_answer(response))
    
    # Majority vote on final answers
    from collections import Counter
    answer_counts = Counter(responses)
    most_common = answer_counts.most_common(1)[0][0]
    confidence = answer_counts.most_common(1)[0][1] / num_samples
    
    return most_common, confidence, responses
```

## Tree-of-Thought (ToT)

### ToT Implementation

```python
import json

class TreeOfThought:
    """Tree-of-Thought: explore multiple reasoning paths with BFS/DFS.
    
    At each step, generate multiple possible next thoughts,
    evaluate them, and explore the most promising paths.
    """
    
    def __init__(self, model, max_branches=3, max_depth=5, 
                 eval_method='self_eval'):
        self.model = model
        self.max_branches = max_branches
        self.max_depth = max_depth
        self.eval_method = eval_method
    
    def solve(self, problem):
        """Solve using BFS tree search."""
        # Root node
        root = {"thought": "", "depth": 0, "value": 1.0, "parent": None, "children": []}
        frontier = [root]
        
        for depth in range(self.max_depth):
            new_frontier = []
            
            for node in frontier:
                if self._is_solution(node['thought']):
                    return self._extract_solution(node)
                
                # Generate candidate next thoughts
                candidates = self._generate_thoughts(problem, node['thought'])
                
                # Evaluate candidates
                for candidate in candidates:
                    value = self._evaluate_thought(problem, candidate)
                    child = {
                        "thought": candidate,
                        "depth": depth + 1,
                        "value": value,
                        "parent": node,
                        "children": []
                    }
                    node['children'].append(child)
                    new_frontier.append(child)
            
            # Prune to top-k
            new_frontier.sort(key=lambda n: n['value'], reverse=True)
            frontier = new_frontier[:self.max_branches]
            
            if not frontier:
                break
        
        # Return best leaf
        best_leaf = max(self._get_leaves(root), key=lambda n: n['value'])
        return self._extract_solution(best_leaf)
    
    def _generate_thoughts(self, problem, context):
        """Generate possible next thoughts.
        Uses the model to propose continuations."""
        prompt = f"""Problem: {problem}
Current reasoning: {context}

Propose {self.max_branches} distinct next steps or thoughts.
Each should be a different approach or angle.
List them numbered:"""
        
        response = self.model.generate(prompt)
        thoughts = self._parse_numbered_list(response)
        return thoughts[:self.max_branches]
    
    def _evaluate_thought(self, problem, thought):
        """Evaluate how promising a thought is (0-1 scale)."""
        if self.eval_method == 'self_eval':
            prompt = f"""Problem: {problem}
Proposed next step: {thought}

Rate this step's promise (0 = hopeless, 1 = very promising).
Just output a number:"""
            response = self.model.generate(prompt)
            try:
                return float(response.strip()[:3])
            except:
                return 0.5
        
        elif self.eval_method == 'voting':
            # Vote from multiple evaluators
            votes = []
            for _ in range(3):
                prompt = f"Is this step on the right track? (yes/no)\nStep: {thought}"
                response = self.model.generate(prompt)
                votes.append('yes' in response.lower())
            return sum(votes) / len(votes)
    
    def _is_solution(self, thought):
        """Check if thought contains a final answer."""
        markers = ['answer is', 'therefore', 'solution:', 'final answer:']
        return any(m in thought.lower() for m in markers)
    
    def _get_leaves(self, node):
        """Get all leaf nodes."""
        if not node['children']:
            return [node]
        leaves = []
        for child in node['children']:
            leaves.extend(self._get_leaves(child))
        return leaves


def tot_solve(problem, model):
    """Convenience wrapper."""
    solver = TreeOfThought(model)
    return solver.solve(problem)
```

## Graph-of-Thought (GoT)

```python
class GraphOfThought:
    """Graph-of-Thought: like ToT but thoughts can combine and merge.
    Thoughts are nodes, relationships are edges.
    Enables synthesis of multiple reasoning branches."""
    
    def __init__(self, model):
        self.model = model
        self.graph = {
            'nodes': [],  # [{id, thought, depth, value}]
            'edges': []   # [{source, target, type: 'extends'|'contradicts'|'synthesizes'}]
        }
    
    def add_thought(self, thought, depth, parent_ids=None, edge_type='extends'):
        node = {
            'id': len(self.graph['nodes']),
            'thought': thought,
            'depth': depth,
            'value': 0.5
        }
        self.graph['nodes'].append(node)
        
        if parent_ids:
            for pid in parent_ids:
                self.graph['edges'].append({
                    'source': pid,
                    'target': node['id'],
                    'type': edge_type
                })
    
    def synthesize(self, node_ids):
        """Combine multiple thoughts into a synthesis."""
        thoughts = [self.graph['nodes'][i]['thought'] for i in node_ids]
        
        prompt = f"""Multiple perspectives on a problem:
{chr(10).join(f'- {t}' for t in thoughts)}

Synthesize these perspectives into a coherent conclusion.
Address agreements, contradictions, and the integrated answer:"""
        
        synthesis = self.model.generate(prompt)
        
        self.add_thought(
            synthesis, 
            depth=max(self.graph['nodes'][i]['depth'] for i in node_ids) + 1,
            parent_ids=node_ids,
            edge_type='synthesizes'
        )
        
        return synthesis
```

## ReAct (Reasoning + Acting)

```python
class ReActAgent:
    """Reasoning + Acting: interleave reasoning traces with tool calls.
    Each step: Thought → Action → Observation → Thought → ...
    
    Key insight: reasoning trace helps model recover from errors
    and maintain coherent strategy across multiple tool calls.
    """
    
    def __init__(self, model, tools):
        self.model = model
        self.tools = {t.name: t for t in tools}
    
    def run(self, task, max_steps=10):
        """Run ReAct loop until task is complete."""
        context = f"Task: {task}\n\nAvailable tools:\n"
        for name, tool in self.tools.items():
            context += f"- {name}: {tool.description}\n"
        
        context += "\nLet's work through this step by step."
        
        for step in range(max_steps):
            # Generate thought + action
            prompt = f"""{context}

{self._format_step_prompt(step)}"""
            
            response = self.model.generate(prompt, max_length=512)
            
            # Parse response for thought and action
            thought = self._extract_thought(response)
            action = self._extract_action(response)
            
            # Execute action if present
            if action:
                tool_name = action.get('tool')
                tool_args = action.get('args', {})
                
                if tool_name in self.tools:
                    try:
                        observation = self.tools[tool_name].run(**tool_args)
                    except Exception as e:
                        observation = f"Error: {e}"
                else:
                    observation = f"Error: Unknown tool '{tool_name}'"
                
                context += f"\nThought: {thought}\nAction: {action}\nObservation: {observation}"
            else:
                # Final answer
                return self._extract_answer(response)
        
        return self._extract_answer(context)
    
    def _format_step_prompt(self, step):
        if step == 0:
            return "Thought: Let me think about what to do first."
        return "Thought:"
    
    def _extract_thought(self, response):
        """Extract reasoning thought from model response."""
        import re
        match = re.search(r'Thought:\s*(.+?)(?=Action:|$)', response, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def _extract_action(self, response):
        """Extract tool call from response."""
        import json, re
        # Pattern 1: JSON action
        match = re.search(r'Action:\s*(\{[^}]+\})', response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except:
                pass
        
        # Pattern 2: function_call format
        match = re.search(r'```(?:json)?\s*(\{[^}]+\})\s*```', response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except:
                pass
        
        return None
```

## Reflection Pattern

```python
class ReflectiveReasoning:
    """Two-stage reasoning: generate + reflect.
    
    Stage 1: Generate initial reasoning/answer.
    Stage 2: Critique and refine.
    Can repeat for multiple rounds.
    """
    
    def __init__(self, model, max_rounds=3):
        self.model = model
        self.max_rounds = max_rounds
    
    def solve(self, problem):
        """Solve with iterative reflection."""
        current_solution = ""
        
        for round in range(self.max_rounds):
            if round == 0:
                # Initial generation
                prompt = f"Problem: {problem}\nLet's solve this step by step:"
                current_solution = self.model.generate(prompt)
            else:
                # Reflection and refinement
                prompt = f"""Problem: {problem}

Previous solution attempt:
{current_solution}

Critique the above solution. What's correct? What's wrong or missing?
- Check each step for logical errors
- Verify calculations
- Look for assumptions

After critique, provide an improved solution:"""
                current_solution = self.model.generate(prompt)
        
        return current_solution
```

## Hybrid Patterns

### CoT + ReAct (Reasoning before acting)

```python
def reasoned_react(task, model, tools):
    """First reason deeply, then act.
    Better than pure ReAct for complex planning tasks."""
    
    # Phase 1: Deep reasoning
    plan_prompt = f"""Task: {task}

Available tools: {[t.name for t in tools]}

First, reason deeply about the problem. What do you need to do?
What's the plan? Think step by step.
Then output a numbered plan."""
    
    plan = model.generate(plan_prompt)
    
    # Phase 2: Execute plan with ReAct
    agent = ReActAgent(model, tools)
    result = agent.run(f"Execute this plan:\n{plan}\n\nOriginal task: {task}")
    
    return result
```

### ToT + ReAct (Explore multiple action paths)

```python
class TreeReAct:
    """Tree-of-Thought for action selection.
    At each step, consider multiple possible actions
    and evaluate which is most promising."""
    
    def __init__(self, model, tools):
        self.tot = TreeOfThought(model)
        self.react = ReActAgent(model, tools)
    
    def solve(self, task):
        # Use ToT to plan action sequence
        plan = self.tot.solve(f"Plan the steps to: {task}")
        # Execute with ReAct
        return self.react.run(plan)
```

## Common Pitfalls

1. **CoT hallucination** — model invents plausible-looking but wrong reasoning; use self-consistency
2. **ToT cost explosion** — 5 branches × 5 depth × 3 evaluations = 75 calls; use efficient pruning
3. **ReAct action looping** — model repeats same action after failure; add "try a different approach" prompt
4. **Reflection degradation** — successive reflections don't improve; limit to 2-3 rounds
5. **Context window overflow** — long reasoning traces exceed context; use summarization or sliding window
6. **Evaluation inconsistency** — self-evaluation is unreliable; use voting or tool-based verification

## Verification Checklist

- [ ] CoT improves accuracy over direct answer on reasoning benchmark (e.g., GSM8K subset)
- [ ] Self-consistency improves accuracy over single CoT
- [ ] ToT finds solutions when CoT fails (test with planning puzzle)
- [ ] ReAct successfully completes tool-based tasks
- [ ] Reflection actually corrects errors (measure error rate before vs after)
- [ ] Cost vs. benefit: accuracy gain justifies additional token cost
- [ ] No infinite loops in ReAct (max_steps safety limit set)

## See Also

- agent-reasoning-patterns — basic agent reasoning patterns
- prompt-engineering-patterns — prompt design for reasoning
- agent-framework-design — integrating reasoning in agents
- tool-augmented-agents — tools for ReAct agents
