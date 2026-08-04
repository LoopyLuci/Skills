---
name: skill-creator
description: Use when creating or improving skills with eval testing.
tags: [skill-creation, eval-testing, benchmarking, iteration]
related_skills: [skill-discovery, skill-development-workflow]
---

# Skill Creator

A skill for creating new skills and iteratively improving them through testing and evaluation.

## Core Loop

1. Decide what you want the skill to do and how
2. Write a draft of the skill
3. Create test prompts and run them
4. Evaluate results (qualitative and quantitative)
5. Rewrite based on feedback
6. Repeat until satisfied

## Creating a Skill

### Capture Intent
- What should this skill enable?
- When should it trigger?
- What's the expected output format?
- Set up test cases for objectively verifiable outputs

### Interview and Research
- Ask about edge cases, formats, success criteria
- Check available MCPs for research
- Come prepared with context

### Write the SKILL.md

**Structure:**
```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/
    ├── references/
    └── assets/
```

**Description field:** Include both what the skill does AND trigger contexts. Make descriptions slightly "pushy" to avoid undertriggering.

### Test Cases

Save to `evals/evals.json`:
```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

## Running Evaluations

1. Spawn with-skill AND baseline runs in parallel
2. Draft assertions while runs are in progress
3. Grade outputs against assertions
4. Aggregate into benchmark
5. Launch viewer for user review

## Improving the Skill

- Generalize from feedback — don't overfit to test cases
- Keep the prompt lean — remove things not pulling their weight
- Explain the why — LLMs work better with understanding
- Bundle repeated helper scripts

## Common Pitfalls

- ❌ **Overfitting to test cases** — Skills must generalize to many prompts
- ❌ **Heavy-handed MUSTs** — Explain reasoning instead
- ❌ **Skipping baseline comparisons** — Need to measure improvement
- ❌ **Not testing with real user prompts** — Artificial tests miss issues

## Verification Checklist

- [ ] Skill has clear name and description (≤60 chars)
- [ ] Test cases are realistic and diverse
- [ ] Baseline and with-skill runs completed
- [ ] Quantitative assertions defined (where applicable)
- [ ] User has reviewed outputs and provided feedback
- [ ] Description optimized for trigger accuracy
