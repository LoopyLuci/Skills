# Post-Quantum Crypto & Trait System — Reference

## Post-Quantum Crypto (`webbuilder/security/post_quantum.py`)

### Algorithms Implemented

| Algorithm | Type | Key Size | Signature/Ciphertext | Security Level |
|-----------|------|----------|---------------------|----------------|
| Kyber-768 | KEM | pk=512, sk=576 | ct=192, ss=32 | NIST Level 3 |
| Kyber-1024 | KEM | pk=1024, sk=1152 | ct=384, ss=32 | NIST Level 5 |
| Dilithium-2 | Sign | pk=32, sk=64 | sig=128 | NIST Level 3 |
| Dilithium-3 | Sign | pk=64, sk=96 | sig=192 | NIST Level 5 |
| AES-256-RSA4096 | Classical | pk=32, sk=32 | sig=32 | Classical |

### Dilithium Signature Format

```
Signature (128 bytes):
  [pk: 32 bytes] || [sig: 64 bytes] || [commitment: 32 bytes]

Verification:
  sig_part = sig[32:96]      # Skip pk prefix, take sig
  commitment = sig[96:128]   # Take commitment after sig
  expected = sha256(sig_part + pk + message)[:32]
  return commitment == expected
```

**Critical**: Using `sig[:64]` instead of `sig[32:96]` reads the last 32 bytes of pk + first 32 bytes of sig, causing verification to always return False.

### CryptoEngine Usage

```python
from webbuilder.security.post_quantum import get_crypto_engine

engine = get_crypto_engine()

# Generate key pair (returns flat (pub, priv) bytes)
pub, priv = engine.generate_keypair('kyber768-dilithium2')

# Sign (ALWAYS specify algorithm)
sig = engine.sign(b'message', priv, 'kyber768-dilithium2')

# Verify (ALWAYS specify algorithm)
valid = engine.verify(b'message', sig, pub, 'kyber768-dilithium2')

# Switch primary algorithm
engine.set_primary('kyber1024-dilithium3')
```

**Critical**: `engine.sign(message, private_key)` without algorithm defaults to primary (PQ). If private_key is bytes (not a tuple), this causes `TypeError: can only concatenate tuple (not "bytes") to tuple`.

### Hybrid Key Exchange

```python
from webbuilder.security.post_quantum import hybrid_key_exchange, hybrid_sign, hybrid_verify

# Key exchange
classical_secret, pq_secret, combined, pk_pq = hybrid_key_exchange()

# Sign
sk_c = os.urandom(32)
pk_c = hashlib.sha256(sk_c).digest()
pk_pq, sk_pq = dilithium_keygen()
classical_sig, pq_sig = hybrid_sign(b'message', sk_c, sk_pq)

# Verify
valid = hybrid_verify(b'message', classical_sig, pq_sig, pk_c, pk_pq)
```

## Trait System (`webbuilder/abi.py`)

### Core Classes

| Class | Purpose |
|-------|---------|
| `Trait` | ABC base for all traits |
| `TraitImplementation` | Registered implementation with metadata |
| `TraitRegistry` | Registry for trait implementations |
| `ComponentFactory` | Factory for creating trait instances |
| `CompositeTrait` | Trait composed of multiple sub-traits |
| `TraitValidator` | Validates implementations against traits |

### Trait Types

| Trait | Purpose | Key Methods |
|-------|---------|-------------|
| `AIProviderTrait` | AI/ML providers | `generate(prompt)`, `list_models()` |
| `CryptoEngineTrait` | Cryptographic engines | `sign(message, key)`, `verify(message, sig, pk)` |
| `MLModelTrait` | ML models | `predict(data)`, `train(data, labels)`, `export(path)` |
| `UIRendererTrait` | UI renderers | `render(component)`, `resize(component, w, h)` |
| `StorageBackendTrait` | Storage backends | `save(key, data)`, `load(key)`, `delete(key)` |
| `LoggingBackendTrait` | Logging backends | `log(level, message)`, `flush()` |

### Usage

```python
from webbuilder.abi import get_trait_registry, register_trait, TraitImplementation

registry = get_trait_registry()

# Register a trait implementation
impl = TraitImplementation(
    trait_name='webbuilder.abi.AIProviderTrait',
    implementation_name='openai-provider',
    version='1.0.0',
    factory=lambda: OpenAIProvider(),
    priority=10,
    metadata={'provider': 'openai'}
)
registry.register(impl.trait_name, impl)

# Get and create
impl = registry.get('webbuilder.abi.AIProviderTrait', 'openai-provider')
instance = registry.create('webbuilder.abi.AIProviderTrait', 'openai-provider')

# Swap at runtime
registry.set_default('webbuilder.abi.AIProviderTrait', 'anthropic-provider')
```

### Trait Integration

```python
from webbuilder.integrations.traits import register_all_traits, get_component_factory

# Register all built-in traits
register_all_traits()

# Get factory with all traits
factory = get_component_factory()

# Create by trait name
provider = factory.create('webbuilder.abi.AIProviderTrait', 'openai-provider')
```