---
name: prompt-engineering-patterns
description: "Use when designing prompts for LLMs."
category: mlops
tags: [prompt-engineering, llm, gpt, patterns, prompting]
---
# Prompt Engineering Patterns

Systematic patterns for designing effective LLM prompts.

## Core Prompt Structure

```
System:   [role + rules + constraints]
Context:  [background information]
Examples: [few-shot demonstrations]
Input:    [the actual query]
Output:   [format specification]
```

## Zero-Shot

```
System: You are a Docker expert. Answer concisely with commands.
User: How do I remove all stopped containers?
```

## Few-Shot

```
System: Translate Docker commands to explanations.
Examples:
  User: docker rm $(docker ps -aq)
  Assistant: Removes all containers (running and stopped).
  User: docker system prune -a -f --volumes
  Assistant: Removes all unused containers, networks, images, and volumes.
User: docker compose up -d --build
```

## Chain-of-Thought (CoT)

```
System: Solve step by step.
User: I have a Docker container that exits immediately.
Think through this step by step:
1. The container needs a foreground process to stay alive
2. Check the CMD/ENTRYPOINT in the Dockerfile
3. For nginx, the default CMD runs nginx in foreground
4. For custom apps, ensure they don't daemonize
```

## Role Assignment

```
System: You are a senior DevOps engineer specializing in Docker security.
You are strict about security best practices and always recommend:
- Non-root users in containers
- Read-only root filesystem
- Dropping unnecessary capabilities
- Using secrets management

User: Review this Dockerfile...
```

## Structured Output

```
System: Return valid JSON only.
User: List all Docker commands for container management.
Assistant: {
  "create": "docker create --name <name> <image>",
  "start": "docker start <name>",
  "stop": "docker stop <name>",
  "remove": "docker rm <name>",
  "list": "docker ps -a"
}
```

## Self-Correction

```
System: After giving your answer, evaluate it for errors.
If you find an error, say "CORRECTION:" followed by the fix.
```

## Persona Prompting

```
System: You are a Docker expert who has been using containers for 10 years.
You've seen every pitfall. Be direct and warn about common mistakes.
```

## Rule-Based

```
System: Rules:
1. Always include the exact command, not a description
2. Always include a pitfalls section
3. Never suggest docker-compose (v1), use docker compose (v2)
4. If the command needs admin, note it
```

## Pitfalls

- System prompt is most influential — invest time here
- Few-shot examples must be representative, not edge cases
- Chain-of-thought adds tokens — use only for reasoning tasks
- Structured output can fail with complex schemas
- Long prompts use context window — manage token budget carefully
