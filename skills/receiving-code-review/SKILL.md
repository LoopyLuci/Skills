---
name: receiving-code-review
description: Use when receiving and integrating feedback from code reviews
tags: [code-review, feedback, pull-request, quality]
related_skills: [finishing-a-development-branch, code-review-checklist]
---

# Receiving Code Review

## Overview

Code review is about improving the codebase, not about being right. Approach feedback with an open mind — the reviewer is investing time to help make the system better.

## Mindset

- **Don't take it personally.** Feedback is about the code, not about you.
- **Assume positive intent.** The reviewer wants the codebase to be better.
- **You are not your code.** Separation of identity from output is healthy.
- **The reviewer is right more often than you think.** Even when you disagree, they've identified something worth discussing.
- **Goal:** Merge better code, not "win" arguments.

## Process

### 1. Read Everything First

Read all comments before responding. A comment that seems unreasonable may make sense in context of later comments.

### 2. Categorize Each Comment

| Type | Response |
|------|----------|
| Clear bug / issue | Fix it. Thank the reviewer. |
| Style preference | Consider adopting for consistency. Don't argue style. |
| Suggestion / alternative | Evaluate trade-offs. Respond with your reasoning. |
| Clarification question | Answer clearly. Update comments/docs if needed. |
| You disagree | Explain your reasoning politely. Be open to being wrong. |

### 3. Respond and Fix

- Thank the reviewer for each comment
- Fix issues or explain why you won't
- Ask clarifying questions if needed
- Push fixes as new commits (don't rebase until review is done)

### 4. Request Re-review

After addressing all feedback, request another look.

## Code Example: Good Review Response

```
Reviewer: "This function is doing too much. Consider splitting it."

You: "Good point. I've extracted the validation logic into
validateInput() and the formatting into formatOutput(). The
main function now only orchestrates the two. PTAL."
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Taking feedback personally | Remember: feedback is about the code, not you |
| Arguing every point | Choose your battles — some things aren't worth contesting |
| Ignoring comments | Acknowledge every comment, even to say "fixed" |
| Rebasing during review | Add fix commits — rebase only after approval |
| Defensive responses | Thank the reviewer, then address the substance |

## Verification Checklist

- [ ] Read all reviewer comments before responding
- [ ] Each comment acknowledged and addressed
- [ ] Fixes committed (not squashed) for reviewer clarity
- [ ] Re-review requested after addressing feedback
- [ ] All discussions resolved before merge
