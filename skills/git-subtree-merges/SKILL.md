---
name: git-subtree-merges
description: Merge external projects into your repo without submodules.
---

# Git Subtree Merges

**Trigger**: Use when incorporating an external project into your repo without submodules, or splitting out a subdirectory into its own repo.

## When to Use Subtree vs Submodules

| Aspect | Subtree | Submodule |
|--------|---------|-----------|
| Clone simplicity | Single `git clone` | `--recurse-submodules` needed |
| Pinning version | By commit SHA or tag | By commit in `.gitmodules` |
| Making local edits | Directly in repo | Must go to submodule repo |
| Contributing upstream | `git subtree push` | PR in submodule repo |
| History size | Full history merged | Pointer only |

## Adding a Subtree

```bash
git subtree add --prefix=vendor/logger \
  https://github.com/owner/logger.git main --squash

git subtree add --prefix=vendor/lib \
  https://github.com/owner/lib.git v1.0.0 --squash
```

## Pulling Updates

```bash
git subtree pull --prefix=vendor/logger \
  https://github.com/owner/logger.git main --squash

git subtree pull --prefix=vendor/logger \
  https://github.com/owner/logger.git v1.2.0 --squash
```

## Contributing Back

```bash
git subtree push --prefix=vendor/logger \
  https://github.com/owner/logger.git my-feature-branch

git remote add logger-upstream https://github.com/owner/logger.git
git subtree push --prefix=vendor/logger logger-upstream main
```

## Splitting Into a New Repo

```bash
git subtree split --prefix=src/lib --branch=lib-split

mkdir ../new-lib && cd ../new-lib
git init
git pull ../original-repo lib-split
git remote add origin https://github.com/owner/new-lib.git
git push origin main
```

## Managing Multiple Subtrees

```bash
git remote add logger-upstream https://github.com/owner/logger.git
git remote add parser-upstream https://github.com/owner/parser.git

git subtree add --prefix=vendor/logger logger-upstream main --squash
git subtree add --prefix=vendor/parser parser-upstream main --squash
```

## Pitfalls
- **Large history**: Use `--squash` to keep history clean
- **Merge conflicts**: Harder to resolve than regular merges
- **git log duplication**: Upstream commits appear twice
- **Performance**: Slower than regular git on large repos
- **No auto-updates**: Must manually pull subtree updates

## Verification
```bash
git log --oneline --all -- vendor/
```
