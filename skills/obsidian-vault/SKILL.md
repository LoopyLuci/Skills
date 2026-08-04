---
name: obsidian-vault
description: Use when searching, creating, or managing notes in an Obsidian vault
tags: [obsidian, notes, knowledge, vault, wikilinks]
related_skills: [note-taking, ubiquitous-language, domain-modeling]
---

# Obsidian Vault

Search, create, and manage notes in an Obsidian vault with wikilinks and index notes for knowledge management.

## Vault conventions
- **Index notes**: aggregate related topics (e.g., "Ralph Wiggum Index", "Skills Index", "RAG Index")
- **Title case** for all note names
- No folders for organization - use links and index notes instead

## Linking
- Use Obsidian [[wikilinks]] syntax: [[Note Title]]
- Notes link to dependencies/related notes at the bottom
- Index notes are just lists of [[wikilinks]]

## Workflows
### Search for notes
Search by filename or content in the vault directory.

### Create a new note
Use Title Case for filename with content as a unit of learning. Add [[wikilinks]] to related notes at the bottom.

### Find related notes and backlinks
Search for [[Note Title]] across the vault to find backlinks.

> **Note**: The vault path is system-specific. Update the vault location for your environment.

## Common Pitfalls

- **Wrong vault path**: The vault path is system-specific. Always verify the vault location before creating or searching notes.
- **Not using wikilinks for navigation**: Obsidian relies on [[wikilinks]] for backlinks and graph view. Regular markdown links lose this functionality.
- **Creating too many nested folders**: The vault convention is flat with index notes, not nested folders. Fighting the convention makes notes hard to find.

## Code Examples

```bash
# Search for notes by name
find "/path/to/obsidian/vault" -name "*.md" | grep -i "keyword"

# Search note content
grep -rl "keyword" "/path/to/obsidian/vault" --include="*.md"

# Find index notes
find "/path/to/obsidian/vault" -name "*Index*"

# Find backlinks for "Note Title"
grep -rl '\[\[Note Title\]\]' "/path/to/obsidian/vault"
```

## Verification Checklist

- [ ] Vault path verified
- [ ] Search returns expected results
- [ ] New notes use Title Case for filenames
- [ ] Notes linked with [[wikilinks]] syntax
- [ ] Index notes aggregate related topics
