---

name: github-projects-management
description: Manage GitHub Projects for issue/PR tracking and planning.

---

# GitHub Projects Management

**Trigger**: Use when setting up project boards, tracking issues across milestones, or organizing work with GitHub Projects.

## GitHub Projects v2 (modern)

```bash
# Create a project (org-level)
gh api orgs/:org/projects \
  --method POST \
  -f name="Q4 Planning" \
  -f body="Quarterly planning board"

# Create repo-level project
gh api repos/:owner/:repo/projects \
  --method POST \
  -f name="Sprint Board"
```

### Project Views
```bash
# Add items to project
# Currently requires GraphQL:
gh api graphql -f query='
  mutation {
    addProjectV2ItemById(input: {
      projectId: "PROJECT_ID"
      contentId: "ISSUE_OR_PR_NODE_ID"
    }) { item { id } }
  }
'
```

### Classic Projects (Web UI)
GitHub Projects Classic supports three layouts:
- **Board**: Kanban-style columns (To Do, In Progress, Done)
- **Table**: Spreadsheet-style with custom fields
- **Roadmap**: Timeline view for milestones

## Automation

### Issue → Project Auto-Add
```yaml
# .github/workflows/project-automation.yml
name: Auto Add to Project
on:
  issues:
    types: [opened]
jobs:
  add-to-project:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/add-to-project@v1
        with:
          project-url: https://github.com/orgs/my-org/projects/123
          github-token: ${{ secrets.GH_PROJECT_TOKEN }}
```

### Label → Column Automation
Use the built-in project automation (Web UI):
- **Issues labeled `bug`** → Move to "Bug Triage" column
- **PRs merged** → Move to "Done" column
- **Issues closed** → Move to "Done" column

## CLI Workflow

```bash
# List org projects
gh api orgs/:org/projects --jq '.[].name'

# List project columns
gh api repos/:owner/:repo/projects --jq '.[] | {name, columns_url}'
gh api <columns_url> --jq '.[].name'

# Add issue to project (classic)
gh api repos/:owner/:repo/issues/42 \
  --method PATCH \
  -f project_ids='[12345]'
```

## Best Practices

1. **One project per milestone/release**: Keeps scope focused
2. **Automate column moves**: Reduce manual drag-and-drop
3. **Use labels for triage**: `needs-triage` → project auto-adds
4. **Archive completed projects**: Don't delete — keep historical records
5. **Project templates**: Create reusable project templates for standard workflows

## Pitfalls
- **v1 vs v2 APIs**: Classic Projects use `projects` endpoint; v2 uses GraphQL exclusively
- **Org vs repo projects**: Org projects can include issues from multiple repos; repo projects only that repo
- **Automation limits**: Classic project automation runs on issue/PR events only, not on schedule
- **500 item limit per project column**: Classic projects hit performance issues past 500 items
- **GraphQL node IDs**: Need to resolve issue/PR node IDs before adding to v2 projects

## Verification
```bash
gh api repos/:owner/:repo/projects --jq '.[].name'    # Classic
gh api orgs/:org/projects --jq '.[].title'            # v2
```
