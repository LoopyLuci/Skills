---

name: github-actions-reusable
description: Share workflows and actions to avoid duplication.

---

# GitHub Actions Reusable Workflows

**Trigger**: Use when you have identical CI/CD steps across multiple repos or want to share action logic.

## Reusable Workflows (called from other workflows)

### Step 1: Create the Called Workflow
`.github/workflows/deploy.yml`:
```yaml
name: Deploy
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      version:
        required: false
        type: string
        default: latest
    secrets:
      CLOUD_TOKEN:
        required: true
    outputs:
      url:
        value: ${{ jobs.deploy.outputs.url }}
jobs:
  deploy:
    runs-on: ubuntu-latest
    outputs:
      url: ${{ steps.set-url.outputs.url }}
    steps:
      - id: set-url
        run: echo "url=https://${{ inputs.environment }}.example.com" >> $GITHUB_OUTPUT
```

### Step 2: Call It
```yaml
jobs:
  deploy:
    uses: org/repo/.github/workflows/deploy.yml@v1
    with:
      environment: staging
      version: v1.2.0
    secrets:
      CLOUD_TOKEN: ${{ secrets.CLOUD_TOKEN }}
```

## Composite Actions

`.github/actions/setup-rust/action.yml`:
```yaml
name: "Setup Rust"
description: "Install Rust toolchain with caching"
inputs:
  toolchain:
    required: false
    default: stable
runs:
  using: "composite"
  steps:
    - run: rustup toolchain install ${{ inputs.toolchain }}
      shell: bash
    - uses: actions/cache@v4
      with:
        path: ~/.cargo/registry
        key: cargo-${{ hashFiles('**/Cargo.lock') }}
```

### Use the Composite
```yaml
steps:
  - uses: actions/checkout@v4
  - uses: ./.github/actions/setup-rust
    with:
      toolchain: nightly
  - run: cargo build
```

## Best Practices
- **Version with tags**: `uses: org/repo/.github/workflows/ci.yml@v1` not `@main`
- **Validate inputs**: Use `type: boolean` for type safety
- **Map secrets explicitly**: They don't auto-flow to called workflows

## Pitfalls
- **No `env` context in reusable workflows**: Pass values as inputs instead
- **Composite actions**: Don't run in caller's workspace — use `${{ github.workspace }}`
- **Max depth**: 4 levels of nested reusable workflows

## Verification
```bash
grep -r "uses:.*/" .github/workflows/ | grep -v "actions/"
```
