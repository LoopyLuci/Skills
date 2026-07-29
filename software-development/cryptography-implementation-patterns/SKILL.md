---
name: cryptography-implementation-patterns
description: "Use when implementing cryptography securely in apps."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cryptography, encryption, hashing, signing, security, python, rust]
    related_skills: [formal-verification-methods, web-security-patterns, zero-trust-network-architecture]
---

# Cryptography Implementation Patterns

Implementing cryptographic primitives and protocols securely — hashing, encryption, signing, key exchange, and random number generation in Python and Rust.

## When to Use

- Implementing authentication or encryption in your application
- Designing secure communication protocols
- Storing secrets, passwords, or sensitive data
- Verifying data integrity and authenticity
- Building zero-trust or secure multi-party systems

## Golden Rules

```
1. DON'T roll your own crypto — use battle-tested libraries
2. DON'T use ECB mode — use AEAD (AES-GCM, ChaCha20-Poly1305)
3. DON'T compare secrets with == — use constant-time compare
4. DON'T use MD5 or SHA-1 — use SHA-256/3 or BLAKE2
5. DO use authenticated encryption — encryption without auth is broken
6. DO use established libraries — libsodium, cryptography, ring
```

## Password Hashing

```python
from argon2 import PasswordHasher

class PasswordManager:
    """Argon2id (winner of Password Hashing Competition)."""
    def __init__(self):
        self.ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)
    
    def hash_password(self, password: str) -> str:
        return self.ph.hash(password)  # Encoded string with salt
    
    def verify_password(self, password: str, hash_str: str) -> bool:
        try:
            return self.ph.verify(hash_str, password)
        except: return False
```

## Symmetric Encryption (AEAD)

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt(key: bytes, plaintext: bytes) -> bytes:
    """AES-256-GCM: nonce(12) + ciphertext + tag(16)."""
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    return nonce + aesgcm.encrypt(nonce, plaintext, None)

def decrypt(key: bytes, data: bytes) -> bytes:
    """Decrypt AES-256-GCM. Raises on tampering."""
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(data[:12], data[12:], None)
```

## Asymmetric Encryption

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def generate_keypair():
    key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    return key, key.public_key()

def encrypt(public_key, plaintext: bytes) -> bytes:
    return public_key.encrypt(plaintext, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(), label=None))

def sign(private_key, message: bytes) -> bytes:
    return private_key.sign(message, padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
```

## Key Derivation

```python
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(password: str, salt: bytes = None):
    if salt is None: salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000)
    return kdf.derive(password.encode()), salt
```

## Rust: ChaCha20-Poly1305

```rust
use chacha20poly1305::{ChaCha20Poly1305, KeyInit, Nonce, aead::Aead, OsRng};

fn encrypt(key: &[u8; 32], plaintext: &[u8]) -> Vec<u8> {
    let cipher = ChaCha20Poly1305::new(key.into());
    let nonce = ChaCha20Poly1305::generate_nonce(&mut OsRng);
    let ciphertext = cipher.encrypt(&nonce, plaintext).unwrap();
    [nonce.as_slice(), &ciphertext].concat()
}
```

## Common Pitfalls

1. **ECB mode** — same plaintext blocks produce same ciphertext; never use ECB
2. **Static nonces** — reusing a nonce with the same key destroys all security
3. **Padding oracle attacks** — don't reveal WHY decryption failed; use AEAD
4. **Keys in source code** — keys in git are compromised; use env vars or KMS
5. **Timing attacks** — string comparison of secrets leaks timing info
6. **Unvalidated decryption** — decrypting without auth allows chosen-ciphertext attacks

## Verification Checklist

- [ ] Passwords hashed with Argon2id or bcrypt
- [ ] All encryption uses authenticated mode (GCM, ChaCha20-Poly1305)
- [ ] Keys never stored in source code or logs
- [ ] Random nonces used (never reused with same key)
- [ ] Constant-time comparison for all secrets
- [ ] Libraries up to date (no known CVEs)

## See Also

- web-security-patterns — applying crypto in web apps
- formal-verification-methods — verifying crypto correctness
- zero-trust-network-architecture — network-level crypto
