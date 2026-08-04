---
name: ubiquitous-language
description: Use when defining domain terms, building a glossary, or creating a ubiquitous language
tags: [DDD, glossary, terminology, domain, language]
related_skills: [domain-modeling, codebase-design]
---

# Ubiquitous Language

Extract and formalize domain terminology from the current conversation into a consistent glossary saved to UBIQUITOUS_LANGUAGE.md.

## Process
1. **Scan the conversation** for domain-relevant nouns, verbs, and concepts
2. **Identify problems**:
   - Same word used for different concepts (ambiguity)
   - Different words used for the same concept (synonyms)
   - Vague or overloaded terms
3. **Propose a canonical glossary** with opinionated term choices
4. **Write to UBIQUITOUS_LANGUAGE.md** in the working directory
5. **Output a summary** inline in the conversation

## Common Pitfalls

- **Overloading existing terms**: Using the same word for different concepts creates ambiguity. Flag and rename before it spreads.
- **Creating too many terms too early**: Do not carve out terms for everything upfront. Let the model emerge from real usage and only formalize terms that matter.
- **Not updating existing documentation**: New terms must be propagated to existing docs, ADRs, and code comments to avoid confusion.

## Verification Checklist

- [ ] Conversation scanned for domain-relevant terms
- [ ] Ambiguities and synonyms identified and flagged
- [ ] Canonical glossary proposed with opinionated choices
- [ ] UBIQUITOUS_LANGUAGE.md written to working directory
- [ ] Summary output inline in conversation
