---
name: ironroot-resolver
description: Use for the Ironroot DNSSEC resolver in DNS-Resolver.
---

# Ironroot resolver

Recursive DNSSEC-validating resolver. Workspace `ironroot/` with `ironroot` (userspace),
`ironroot-common` (no_std shared parser), `ironroot-ebpf` (XDP L0). Spec: `IDEA.md.txt`.

## Running it

- Bind flag is `--listen <SocketAddr>`, NOT `--bind`. Default `127.0.0.1:5353` collides
  with Windows mDNS, so always use a high port (e.g. `--listen 127.0.0.1:15410`).
- `--no-validate` disables DNSSEC; AD is then never set and the AD differential tests
  fail by construction. Run the differential suite against a *validating* server.
- `--trust-anchor <path>` points at the RFC 5011 anchor file.

Differential suite (9 cases, `--ignored`, network-dependent):

    IRONROOT_UNDER_TEST=127.0.0.1:15411 IRONROOT_REFERENCE=8.8.8.8 \
      cargo test -p ironroot --test differential -- --ignored --test-threads=1

## Known live bugs (confirmed, not flaky)

- **Glue-less referral fails**: `referral for <name> had name servers with no usable
  glue address` when an NS RRset has no A/AAAA glue and the NS name must be resolved
  first. The iterator needs to fall back to resolving an NS target.
- **Intermittent spurious bogus**: `DNSSEC validation failed: bogus` for names that
  validate on retry. The validator's referral/address queue is the suspect.

## BPF verifier rules (ironroot-ebpf)

Hard-won; violating any of these costs a full rebuild cycle.

- Every packet access must be a **constant offset** from one base pointer. A
  variable-offset loop yields `invalid access to packet`.
- **Integer** bounds checks (`offset < len`) prove nothing to the verifier. Bounds-check
  with a **pointer comparison against `pkt_end`**.
- Any `[u8; N]` with a fill byte (`[0u8; N]`, `[1u8; N]`) compiles to a **memset**, which
  pulls compiler-builtins into `.text`; aya concatenates `.text` into the program. Use
  `MaybeUninit` and write the bytes before reading them.
- Prefer a **const ladder** (64/32/16/8/4/2/1) over one fixed block size: a 13-byte name
  is shorter than a 64-byte window, and a 255-byte name overflows the 512-byte stack.
- For whole-header rewrites use `Packet::read_span`/`write_span`: one pointer-checked
  span read, edit in a stack copy, one span write. Per-field `write_u8` each carry their
  own integer check and get rejected.

## Verifier harness pitfall

The QEMU harness lives in `~/vm` (Debian WSL). When iterating, **rebuild the initramfs
from a freshly written init script** and verify with `zcat <img> | cpio -t`. A cumulative
`sed` chain once left a stale `.o` in the image, so programs of very different sizes all
reported the identical `processed 2822 insns`. Verify image contents before trusting any
verifier verdict.

## Evidence discipline

Mutation-test assertions before claiming they work (force the AD bit, confirm the
expected cases fail, revert). The differential suite is live-network, so keep hermetic
packet fixtures for CI too.
