---
name: skill-prompt-chaining
description: Chain skill invocations together across turns.
---

# Skill Prompt Chaining

**Trigger**: Use when building on previous skill output, or passing results from one skill as input to another.

## What Is Prompt Chaining?

Chaining is using the output of one skill invocation as the input to another — either within the same message (stacking) or across turns (sequencing).

## Chain Types

### 1. Sequential (across turns)
```
Turn 1:   Load skill A → produce output
Turn 2:   Use output as context → load skill B
Turn 3:   Combine A + B outputs → load skill C
```

### 2. Parallel (same turn stacking)
```
/github-code-review /test-driven-development fix issue #123
→ Both skills loaded, both inform the response
```

### 3. Pipelined (output → input)
```
Turn 1: /dockerfile-optimization build container
  → Output: Dockerfile created, tagged as myapp:latest

Turn 2: /kubernetes-deployment deploy myapp:latest
  → Input: Uses the image from Turn 1's output
```

## Chain Management

```markdown
When chaining across turns, maintain context continuity:

BEFORE (breaks chain):  
"Using kubernetes-deployment to deploy the app."

AFTER (maintains chain):
"Continuing from the Docker build (myapp:latest from step 1),
now deploying to the k8s cluster using kubernetes-deployment..."
```

### Context Handoff Template

```markdown
Handoff from: <skill-name>
Result:       <what was produced>
State:        <configs created, files written, etc.>
Next step:    <what the next skill should do>
---
Now using:    <next-skill-name>
```

## Practical Chain Example

```markdown
TASK: "Build and ship a Python CLI tool"

Chain:
1. python-package-build
   → Creates pyproject.toml, src/, tests/
   
2. test-driven-development
   → Writes tests for the CLI
   → Updates pyproject.toml with test config
   
3. github-actions-workflows
   → Creates CI workflow that runs tests on PR
   
4. github-releases-notes
   → Creates release workflow for tag pushes
```

## Avoiding Broken Chains

```markdown
A chain breaks when:

1. TURN GAP: Too many turns between chain steps
   → Skill A loaded, then 10 other turns happen before skill B
   → You've forgotten what skill A produced
   → Fix: Explicitly state what was achieved before moving on

2. PARALLEL OVERLOAD: Too many skills in one turn
   → All instructions merge into a confusing blob
   → Fix: Limit to 3 skills per turn, use sequential for more

3. CONTEXT LOSS: Switching topics mid-chain
   → "Let me also check the weather" → chain broken
   → Fix: Complete the chain before new topics
```

## Chaining with Slash Commands

```markdown
# /skill1 /skill2 description
# Both load, instructions merge in order

/app pentesting:
/sql-injection /api-pentesting test the auth endpoint

Result: Both sql-injection AND api-pentesting skills loaded.
The agent has both contexts available in one turn.

# Limits: max 5 /skills per message
```

## Pitfalls
- **Lost context**: Output from skill A is consumed by skill B, but not explicitly documented — B produces wrong result
- **Circular chains**: Skill A expects B's output, B expects A's — break the cycle with explicit data
- **Over-chaining**: Every tiny step doesn't need its own skill — only chain when each step has significant complexity
- **Implicit dependencies**: Skill B assumes skill A was loaded — it might not be in context anymore

## Verification
```markdown
After a chain, verify:
- Did each link in the chain receive the correct input?
- Was any context lost between turns?
- Could any links be merged into one skill invocation?
```
