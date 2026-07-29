---
name: git-signing-commits
description: Sign commits and tags with GPG or SSH keys for verification.
---

# Git Signing Commits

**Trigger**: Use when setting up commit or tag signing, enabling verified badges on GitHub, or configuring signing keys.

## Signing Methods

| Method | Supports | GitHub verified badge |
|--------|----------|----------------------|
| GPG | Commits + tags | ✅ Shows "Verified" |
| SSH | Commits + tags | ✅ Shows "Verified" |
| S/MIME | Commits + tags | ✅ (org-managed) |

## GPG Signing

### Generate GPG Key
```bash
# Generate a key
gpg --full-generate-key
# Type: RSA (default)
# Size: 4096
# Expiry: 0 (never)
# Name: Your Name
# Email: your@email.com

# List keys
gpg --list-secret-keys --keyid-format=long

# Export public key for GitHub
gpg --armor --export <KEY-ID>
# Add at: https://github.com/settings/gpg/keys
```

### Configure Git
```bash
# Set signing key
git config --global user.signingkey <KEY-ID>

# Sign all commits by default
git config --global commit.gpgSign true

# Sign tags by default
git config --global tag.gpgSign true
```

### Signing Commits
```bash
# Sign a commit (one-off)
git commit -S -m "feat: add authentication"

# Sign with specific key
git commit -S --gpg-sign=<KEY-ID> -m "feat: new feature"

# Sign a tag
git tag -s v1.0.0 -m "Release v1.0.0"
```

## SSH Signing

### Generate SSH Key (if needed)
```bash
ssh-keygen -t ed25519 -C "your@email.com" -f ~/.ssh/id_ed25519
# Add public key: https://github.com/settings/ssh
```

### Configure Git
```bash
# Configure SSH signing
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgSign true
```

### Allowed Signers File
```bash
# Tell git who to trust
echo "your@email.com ssh-ed25519 AAAAC3..." > ~/.ssh/allowed_signers
git config --global gpg.ssh.allowedSignersFile ~/.ssh/allowed_signers
```

## Verifying Signatures

```bash
# Check if commit is signed
git log --show-signature -1

# Check all unsigned commits
git log --format="%h %G? %s"
# G = good (valid signature)
# B = bad
# N = no signature

# Verify a tag
git tag -v v1.0.0

# Check on GitHub
gh api repos/:owner/:repo/commits/main --jq '.commit.verification.verified'
```

## CI Verification

```yaml
# .github/workflows/verify-signatures.yml
name: Verify Commit Signatures
on: [pull_request]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Check all commits are signed
        run: |
          git log --format="%H %G?" origin/main..HEAD | while read sha status; do
            if [ "$status" != "G" ]; then
              echo "Unsigned commit: $sha"
              exit 1
            fi
          done
```

## Key Management

```bash
# Export private key (backup)
gpg --export-secret-keys --armor <KEY-ID> > backup.asc

# Import key
gpg --import backup.asc

# Revoke key
gpg --gen-revoke <KEY-ID> > revoke.asc
gpg --import revoke.asc
gpg --send-keys <KEY-ID>
```

## Pitfalls
- **Email mismatch**: The email in the key must match the email in `user.email` and GitHub account
- **Lost private key**: Without backup, you can't sign new commits — GitHub shows "Unverified" for old signed ones
- **GPG agent**: `gpg-agent` must be running — `gpgconf --launch gpg-agent`
- **SSH key passphrase**: `ssh-add ~/.ssh/key` each session, or use `--apple-use-keychain` on macOS
- **CI signing**: Using `actions/checkout` doesn't preserve GPG agent — CI typically doesn't sign

## Verification
```bash
git log --show-signature -1           # Current commit
git log --format="%h %G? %s" -10      # Last 10 sig statuses
gpg --list-secret-keys                # Available signing keys
```
