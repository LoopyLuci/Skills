# Credential Vault — Encrypted Storage for Desktop Apps

Store passwords, API keys, SSH keys, and other secrets in an encrypted local file
using Fernet symmetric encryption. Values are never stored or exposed in plaintext
outside the add/edit dialog.

## When to Use

- Desktop apps that need to persist user secrets between sessions
- Apps that must keep secrets hidden from logs, screenshots, and process listings
- Any app where the user must be able to add/edit/delete credentials through a UI

## Architecture

```
CredentialStore  →  Fernet encryption  →  JSON file on disk (encrypted blobs)
                        ↑
                 PBKDF2-derived key OR random per-install key
```

**Two modes:**
1. **Password-derived:** Master password → PBKDF2 (SHA-256, 600k iterations) → Fernet key.
   Use when a user must remember one password to unlock all credentials.
2. **Per-install random:** A random Fernet key stored in a `.master_key` file on disk.
   Simpler but the key file must be protected (chmod 600). Use for local-only apps.

## Implementation (Fernet + PBKDF2)

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import json, os
from pathlib import Path
from datetime import datetime, timezone

class CredentialStore:
    def __init__(self, store_path=None, master_password=None):
        self._store_path = Path(store_path) if store_path else self._default_path()
        self._master_password = master_password or os.getenv("GUI_MASTER_PASSWORD", "")
        self._fernet = None
        self._creds = {}
        self._load()

    def _ensure_fernet(self):
        if self._fernet:
            return
        if not self._master_password:
            # Per-install random key
            key_file = self._store_path.parent / ".master_key"
            if key_file.exists():
                self._fernet = Fernet(key_file.read_bytes())
            else:
                key = Fernet.generate_key()
                key_file.write_bytes(key)
                key_file.chmod(0o600)
                self._fernet = Fernet(key)
            return
        # Password-derived
        salt = b"fixed-salt-change-in-production"
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                          salt=salt, iterations=600_000,
                          backend=default_backend())
        self._fernet = Fernet(kdf.derive(self._master_password.encode()))

    def add(self, name, cred_type, value, description=""):
        self._ensure_fernet()
        cid = f"cred_{datetime.now(timezone.utc).timestamp()}_{len(self._creds)}"
        encrypted = self._fernet.encrypt(value.encode()).decode()
        self._creds[cid] = {
            "name": name, "type": cred_type,
            "value": encrypted, "description": description,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        self._save()
        return cid

    def get(self, cid):
        if cid not in self._creds:
            return None
        self._ensure_fernet()
        entry = dict(self._creds[cid])
        try:
            entry["value"] = self._fernet.decrypt(entry["value"].encode()).decode()
        except Exception:
            entry["value"] = "[decryption failed]"
        return entry

    def get_all(self):
        self._ensure_fernet()
        result = []
        for cid, entry in self._creds.items():
            try:
                decrypted = self._fernet.decrypt(entry["value"].encode()).decode()
            except Exception:
                decrypted = "[decryption failed]"
            result.append({"id": cid, **entry, "value": decrypted})
        return result

    def update(self, cid, value, description=None):
        if cid not in self._creds:
            raise KeyError(cid)
        self._ensure_fernet()
        self._creds[cid]["value"] = self._fernet.encrypt(value.encode()).decode()
        if description is not None:
            self._creds[cid]["description"] = description
        self._creds[cid]["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._save()

    def delete(self, cid):
        if cid not in self._creds:
            raise KeyError(cid)
        del self._creds[cid]
        self._save()

    def _save(self):
        self._store_path.parent.mkdir(parents=True, exist_ok=True)
        data = {"version": 1, "updated_at": datetime.now(timezone.utc).isoformat(),
                "credentials": self._creds}
        self._store_path.write_text(json.dumps(data, indent=2))
        self._store_path.chmod(0o600)

    def _load(self):
        if not self._store_path.exists():
            self._creds = {}
            return
        try:
            data = json.loads(self._store_path.read_text())
            self._creds = data.get("credentials", {})
        except (json.JSONDecodeError, OSError):
            self._creds = {}

    @staticmethod
    def _default_path():
        data_dir = Path(os.getenv("XDG_DATA_HOME", "")) or Path.home() / ".local" / "share"
        return data_dir / "yourapp" / "credentials.json"

    @property
    def count(self):
        return len(self._creds)
```

## UI Patterns

### Credential List (QTreeWidget)
- Columns: Name | Type | Description | Updated
- Color-code the Type column by credential kind (password=amber, ssh_key=purple, api_key=green, qmp_pass=blue)
- Double-click to view detail; single-click to select for edit/delete

### Add/Edit Dialog (QDialog)
- Fields: Name (required), Type (combo: password/ssh_key/api_key/qmp_pass/other),
  Secret Value (password field, required), Description (optional)
- **Critical:** Never pre-fill the value field. Ask the user explicitly before showing
  an existing credential's plaintext value — it will briefly appear in the dialog.
- Save button validates (name + value required) then calls `store.add()` or `store.update()`

### Masked Display
- Show only first 2 + last 2 chars: `ab******cd`
- For values ≤ 4 chars, show `***`
- Copy button copies the masked value, not the real one

### Delete Confirmation
- Always require explicit confirmation before deleting
- Show the credential name in the confirmation dialog
- "This action cannot be undone."

## Security Rules

1. **Never log decrypted values.** Log only the credential ID and type.
2. **Never expose values in status bars, tooltips, or list views.** Only in the add/edit
   dialog after explicit user confirmation.
3. **Store file permissions 0o600** (owner read/write only).
4. **Master password prompt** should happen once per session, not per operation.
   Cache the derived Fernet key in memory (it's 안전한 there).
5. **Credential types** are labels for UI organization only — they don't affect encryption.
6. **The `.master_key` file** (per-install mode) is as sensitive as the credentials themselves.
   Protect it with filesystem permissions and exclude from backups/version control.
7. **PBKDF2 iterations:** 600,000 is the current OWASP recommendation for SHA-256.
   Increase over time as hardware improves.

## Common Pitfalls

- **Deriving Fernet key incorrectly:** `Fernet.generate_key()` generates a random key, it does
  NOT derive from a password. Use `PBKDF2HMAC(...).derive(password_bytes)` then wrap in
  `Fernet(kdf_output)`.
- **Fixed salt reuse:** A fixed salt is acceptable for a single-user desktop app but should be
  unique per installation. Store the salt alongside the encrypted data or use a per-install
  random salt stored in the same file.
- **Storing the master password:** Never persist the master password itself. Only the derived
  Fernet key (in memory) or the random per-install key (in `.master_key` file).
- **Accidental plaintext in logs:** `str(credential)` or `repr(credential)` on a dict containing
  the decrypted value will leak it. Use a masked representation for any logging.
- **JSON serialization of Fernet bytes:** Fernet.encrypt() returns bytes. Call `.decode()` before
  storing in JSON. Call `.encode()` before passing to `fernet.decrypt()`.
