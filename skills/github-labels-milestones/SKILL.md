---
name: github-labels-milestones
description: Manage labels, milestones, and saved replies for repos.
---

# GitHub Labels & Milestones

**Trigger**: Use when organizing issues and PRs with labels, setting milestones for releases, or creating saved replies.

## Labels

### Default Labels
```bash
# List all labels in a repo
gh label list

# Create a label
gh label create "bug" --description "Something isn't working" --color "d73a4a"
gh label create "enhancement" --description "New feature or request" --color "a2eeef"
```

### Recommended Label Set
```bash
# Type
gh label create "bug" -d "Bug or regression" -c "d73a4a"
gh label create "feature" -d "New feature request" -c "a2eeef"
gh label create "enhancement" -d "Improvement to existing feature" -c "84b6eb"
gh label create "documentation" -d "Docs or comments" -c "0075ca"
gh label create "refactor" -d "Code restructuring" -c "b07219"

# Status
gh label create "needs-triage" -d "Needs review" -c "fbca04"
gh label create "needs-reproduction" -d "Can't reproduce yet" -c "d876e3"
gh label create "needs-design" -d "Design discussion needed" -c "0e8a16"
gh label create "blocked" -d "Blocked on something else" -c "000000"
gh label create "good-first-issue" -d "Good for newcomers" -c "7057ff"

# Priority
gh label create "priority:high" -d "Critical, needs immediate attention" -c "b60205"
gh label create "priority:medium" -d "Should be addressed soon" -c "fbca04"
gh label create "priority:low" -d "Nice to have" -c "0e8a16"

# Resolution
gh label create "duplicate" -d "Already reported" -c "cfd3d7"
gh label create "wontfix" -d "Won't be addressed" -c "ffffff"
gh label create "invalid" -d "Not a valid issue" -c "e4e669"
gh label create "question" -d "Further info needed" -c "d876e3"
```

### Bulk Label Operations
```bash
# Delete a label
gh label delete "wontfix"

# Update label
gh label edit "bug" --name "type:bug" --color "b60205"
```

## Milestones

```bash
# Create a milestone
gh api repos/:owner/:repo/milestones \
  --method POST \
  --field title="v1.2.0" \
  --field description="Authentication overhaul" \
  --field due_on="2025-03-15T00:00:00Z"

# List milestones
gh api repos/:owner/:repo/milestones --jq '.[].title'

# View milestone progress
gh api repos/:owner/:repo/milestones --jq '.[] | {title, open_issues, closed_issues, state}'

# Close a milestone
gh api repos/:owner/:repo/milestones/1 --method PATCH --field state=closed

# Assign issues to milestone
gh issue edit 42 --milestone "v1.2.0"
```

## Saved Replies

```bash
# List saved replies
gh api user/saved_replies --jq '.[].body'

# Key saved replies to create
# "Duplicate" — reference + close
# "Needs more info" — request details
# "Fixed in latest" — reference commit
# "Thanks for contributing" — appreciation
```

## Automated Label Management

```yaml
# .github/workflows/label-management.yml
name: Label Management
on:
  issues:
    types: [opened]
jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v7
        with:
          script: |
            const body = context.payload.issue.body;
            const labels = [];
            if (body.includes('bug')) labels.push('needs-triage');
            if (body.includes('security')) labels.push('priority:high');
            if (labels.length > 0) {
              await github.rest.issues.addLabels({
                ...context.repo,
                issue_number: context.issue.number,
                labels
              });
            }
```

## Pitfalls
- **Label color contrast**: Light text on light background is unreadable — use dark colors for white text
- **Too many labels**: Over 20 labels becomes unwieldy — stick to type + priority + status
- **Milestone scope creep**: Milestones are for releases — use project boards for task tracking
- **Slug vs display name**: Label display names are case-sensitive; API slugs are lowercase with dashes

## Verification
```bash
gh label list --json name,color,description
gh api repos/:owner/:repo/milestones --jq '.[].title'
```
