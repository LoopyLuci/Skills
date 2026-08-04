---
name: scaffold-exercises
description: Use when creating exercise directory structures with problems, solutions, and explainers
tags: [scaffolding, exercises, education, structure, linting]
related_skills: [teach, setup-matt-pocock-skills, writing-great-skills]
---

# Scaffold Exercises

Create exercise directory structures that pass linting validation, then commit.

## Directory naming
- Sections: `XX-section-name/` inside exercises/
- Exercises: `XX.YY-exercise-name/` inside a section
- Names are dash-case (lowercase, hyphens)

## Exercise variants
Each exercise needs at least one subfolder:
- `problem/` - student workspace with TODOs
- `solution/` - reference implementation
- `explainer/` - conceptual material, no TODOs

## Required files
Each variant folder needs a non-empty readme.md with real content. If the subfolder has code, it also needs a main.ts (>1 line).

## Workflow
1. Parse the plan - extract section names, exercise names, and variant types
2. Create directories with mkdir -p
3. Create stub readmes with title and description
4. Run lint to validate
5. Fix any errors until lint passes

## Common Pitfalls

- **Empty readme files**: Each variant folder's readme.md must have real content. An empty or near-empty readme fails linting.
- **Wrong directory naming convention**: Sections are XX-section-name, exercises are XX.YY-exercise-name. Wrong naming fails the linter.
- **Not running lint after creation**: Always run the linter after scaffolding. Fix errors before committing.

## Verification Checklist

- [ ] Section directories follow XX-section-name convention
- [ ] Exercise directories follow XX.YY-exercise-name convention
- [ ] Each variant folder has non-empty readme.md
- [ ] Code files have main.ts if needed
- [ ] Lint passes
