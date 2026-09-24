---
name: zero-knowledge-proofs
description: Use when implementing zero-knowledge proof systems.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [zero-knowledge, zkp, zksnarks, zkstarks, circom, cryptography]
---

# Zero-Knowledge Proofs

Implementing zero-knowledge proof systems — from zkSNARKs and zkSTARKs through circuit design (Circom), proof generation/verification, and practical applications.

## When to Use

- Privacy-preserving transactions on blockchain
- Verifiable computation (prove computation is correct)
- Identity and credential verification without revealing data
- Scalability (zk-rollups for Ethereum)
- Confidential smart contracts

## ZKP Fundamentals

```python
ZKP_TYPES = {
    'snark': 'Succinct Non-interactive Argument of Knowledge — small proofs, trusted setup (Groth16, PLONK)',
    'stark': 'Scalable Transparent ARgument of Knowledge — no trusted setup, larger proofs, quantum-resistant',
    'bulletproofs': 'No trusted setup, short proofs, used in Monero',
}

"""
// Circom circuit: prove knowledge of hash preimage without revealing it
pragma circom 2.0.0;

template HashPreimage() {
    signal input preimage;
    signal output hash;
    
    component hasher = MiMC7(10);
    hasher.x_in <== preimage;
    hash <== hasher.out;
}

component main { public [hash] } = HashPreimage();
"""
```

## Verification Checklist

- [ ] ZKP system chosen (SNARK, STARK, Bulletproofs)
- [ ] Circuit defined in Circom or similar DSL
- [ ] Trusted setup ceremony completed (if SNARK)
- [ ] Proving key and verification key generated
- [ ] Proof generation time acceptable for use case
- [ ] Verification gas cost (if on-chain) measured
- [ ] Security: circuit soundness, no under-constrained signals
- [ ] Integration tested (prover in app, verifier in contract)
