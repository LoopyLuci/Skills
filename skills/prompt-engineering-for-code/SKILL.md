---
name: prompt-engineering-for-code
description: "Use when writing prompts for code generation tasks."
category: software-development
tags: [prompt, code-generation, llm, programming, copilot]
---
# Prompt Engineering for Code

Writing effective prompts for code generation with LLMs.

## Prompt Structure for Code

```
CONTEXT: [language, framework, project structure]
TASK: [what to build/fix]
CONSTRAINTS: [style, conventions, dependencies]
OUTPUT: [file format, structure]
EXAMPLES: [before/after if refactoring]
```

## Code Generation Prompts

```
Write a Python function that:
- Takes a list of Docker container stats (CPU, memory, name)
- Returns the top 3 containers by memory usage
- Uses proper type hints
- Includes error handling for empty input
- Follows PEP 8
```

## Refactoring Prompts

```
Refactor this function to:
- Use async/await instead of threading
- Add proper error handling with try/except
- Include docstrings following Google style
- Use type hints throughout
- Extract the parsing logic into a helper function

[PASTE CODE HERE]
```

## Debugging Prompts

```
I'm getting this error:
[ERROR MESSAGE]

When running this code:
[CODE]

The expected behavior is:
[DESCRIPTION]

What's wrong and how do I fix it?
Consider: imports, types, async context, edge cases.
```

## Code Review Prompts

```
Review this code for:
1. Security vulnerabilities (injection, XSS, auth)
2. Performance issues (N+1 queries, memory leaks)
3. Maintainability (naming, complexity, duplication)
4. Error handling (missing try/catch, silent failures)
5. Testing (untestable patterns, missing edge cases)

Be specific with line numbers for each issue.
```

## Pitfalls

- Be specific about language and framework — "Python" vs "use FastAPI with SQLAlchemy"
- Include error messages verbatim for debugging
- Specify output format for consistent results
- Large code blocks in context window consume tokens — trim to relevant parts
- Test-generated code before claiming it works
