---
name: to-questionnaire
description: Use when turning an unanswered decision into a questionnaire for someone else
tags: [questionnaire, research, decisions, interview, async]
related_skills: [to-spec, ubiquitous-language, wayfinder]
---

# To Questionnaire

Turn something the user cannot answer alone into a questionnaire - a Markdown document they hand to someone to fill in async, or fill out together over a meeting.

## Process
1. **Who is it going to?** Ask the recipient's role, expertise, and relationship to the user. This fixes the tone and context level.
2. **What do you need back?** Ask the specific decisions or facts the user cannot resolve alone.
3. **Write the questionnaire.** Draft questions aimed at the gap. Write to to-questionnaire-<slug>.md.

## Document structure
Frame the document as a discovery questionnaire: the user lacks context, the recipient holds it. Order questions most-important-first and group under headings by theme.

## Common Pitfalls

- **Tone mismatch with the recipient**: A questionnaire for an executive reads differently than one for a domain expert. Adjust tone and context level.
- **Questions that assume the answer**: Leading questions bias the response. Frame questions as open-ended discovery.
- **Too many questions**: Async questionnaires compete for attention. Prioritize the most important questions - you may only get one pass.

## Verification Checklist

- [ ] Recipient identified (role, expertise, relationship)
- [ ] Decisions or facts needed from recipient listed
- [ ] Questionnaire written to to-questionnaire-<slug>.md
- [ ] Questions ordered most-important-first
- [ ] All user's named needs covered by a question
