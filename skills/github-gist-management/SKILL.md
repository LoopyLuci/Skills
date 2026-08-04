---

name: github-gist-management
description: Create, edit, and manage GitHub Gists for code snippets.

---

# GitHub Gist Management

**Trigger**: Use when creating code snippets, sharing debug logs, or managing public/private gists.

## Creating Gists

### Via gh CLI
```bash
# Create from file(s)
gh gist create script.py

# Create with description
gh gist create script.py -d "Backup script for database"

# Public gist (default: secret)
gh gist create --public script.py

# Multiple files
gh gist create src/main.py src/utils.py config.yaml

# Create from stdin
echo "console.log('hello')" | gh gist create -
```

### Via API
```bash
gh api gists \
  --method POST \
  --input - << 'EOF'
{
  "description": "Example gist",
  "public": true,
  "files": {
    "hello.py": {"content": "print('hello world')"},
    "README.md": {"content": "# Example\nA simple example gist"}
  }
}
EOF
```

## Managing Gists

```bash
# List your gists
gh gist list
gh gist list --limit 50
gh gist list --public          # Only public

# View gist
gh gist view <id>
gh gist view <id> --raw        # Raw content

# Edit gist (opens editor)
gh gist edit <id>

# Add/update file
gh gist edit <id> -a newfile.py

# Delete gist
gh gist delete <id>

# Fork a gist
gh gist fork <id>
```

## Use Cases

### Debug Logs (never paste secrets)
```bash
# Share CI logs
gh run view <id> --log > build.log
echo "CI logs from run $RUN_ID" | gh gist create -d "Build logs" build.log -

# Share config for troubleshooting
gh gist create ~/.gitconfig -d "Git config for debugging"
```

### Quick Script Sharing
```bash
# Share a utility script
gh gist create deploy.sh docker-compose.yml -d "Deployment helpers"

# Clone a gist locally
gh gist clone <id>
cd <id>
```

## Gist as a Data Store

```yaml
# Store config in a gist, fetch in your workflow
name: Fetch Config
on: [workflow_dispatch]
jobs:
  fetch:
    runs-on: ubuntu-latest
    steps:
      - run: |
          gh gist view <gist-id> --raw > config.json
          cat config.json
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Pitfalls
- **Gists are NOT private**: "Secret" gists aren't encrypted — anyone with the URL can see them
- **No directory support**: Gists are flat — all files at root level
- **Size limit**: 1 MB per gist, 10 MB per file
- **No collaboration**: Gists don't support issues, PRs, or multiple contributors
- **API rate limits**: Gist creation counts toward API rate limit

## Verification
```bash
gh gist list --limit 3
gh gist view $(gh gist list --json id --jq '.[0].id') --raw | head -20
```
