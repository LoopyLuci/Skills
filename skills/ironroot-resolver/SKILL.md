---
name: ironroot-resolver
description: Use for the Ironroot DNSSEC resolver in DNS-Resolver.
version: 1
license: MIT
metadata:
  hermes:
    tags: [dns, resolver, dnssec, bpf, xdp, rust]
    related_skills: []
---

# Ironroot resolver

Recursive DNSSEC-validating resolver. Workspace `ironroot/`: `ironroot` (userspace),
`ironroot-common` (no_std shared parser), `ironroot-ebpf` (XDP L0). Spec `IDEA.md.txt`.

## When to use

Anything touching this resolver: the pipeline, the parsers, the caches, the DNSSEC
validator, or the XDP fast path. Read the trap sections before writing a test --
most of the cost here is a wrong assumption about an API, not a hard bug.

## Running it

- Bind flag is `--listen <SocketAddr>`, NOT `--bind`. Default `127.0.0.1:5353` collides
  with Windows mDNS, so use a high port (e.g. `--listen 127.0.0.1:15410`).
- `--no-validate` exists only with `--features diagnostics-no-validate`. Without it the
  field is not compiled in, so a production binary has no bypass to invoke.
- `--trust-anchor <path>` points at the RFC 5011 anchor file.

Differential suite (network-dependent):

    IRONROOT_UNDER_TEST=127.0.0.1:15411 IRONROOT_REFERENCE=8.8.8.8 \
      cargo test -p ironroot --test differential -- --ignored --test-threads=1

## Tests and gates

| Suite | Count | Network |
|---|---|---|
| unit | 106 | no |
| conformance | 49 | no |
| properties (proptest) | 16 | no |
| concurrency | 9 | partly |
| hermetic e2e | 4 + 10 ignored | no |
| common | 39 | no |
| differential | 9 | yes |

`scripts/verify.sh` runs 11 gates, logs each to `logs/`, prints a summary.
`--quick`, `--only <gate>`, `--list`. Treats a compiler *warning* as a failure:
`#![allow(dead_code)]` hid a real bug here.

`scripts/diagnose.{sh,py}` queries a live resolver and prints a full decode -- flags,
counts, a hand-rolled record walk reporting where a bad message stopped parsing, and a
TCP second opinion.

## Remote

Private repo: https://github.com/LoopyLuci/ironroot -- branch `main`, tag `v0.1.0`.
Four CI jobs: userspace tests, hermetic e2e, the validation-bypass binary grep, and
the TLC model check. The bypass grep is mutation-tested: it fails against a
`diagnostics-no-validate` build and passes against a secure one. `tla2tools.jar` is
fetched by `scripts/fetch-tla.sh`, not committed.

## Silent-wrong-value bugs found here

Every one produced plausible output, not a crash. That is why review missed them.

- **DO bit read from the OPT rclass** instead of bit 15 of the OPT TTL (RFC 6891
  §6.1.2). The XDP path did this, so the L0 key never matched a DO-bearing client:
  a silent 100% fast-path miss. Userspace had it right; pin the two together.
- **Rate limiter after the cache.** The limiter is the pipeline's first stage, but
  the L1 lookup ran *before* the pipeline, so cache hits skipped it and a client
  asking for one popular cached name got unlimited service. `Kernel` now holds the
  limiter and checks it before the cache.
- **`cacheable` accepted TTL 0** (RFC 2181 §5.2). Storing it is a correctness bug.
- **Referrals were cacheable and read as negative answers.** NOERROR-with-no-answers
  is both a referral's shape and NODATA's. Now `cacheable` requires `ancount > 0`
  and `is_negative` requires an SOA (RFC 2308 §2.1).
- **The validator built a fresh transport per request**, discarding
  `--upstream-timeout-ms`. Found only after the lib/bin split removed
  `#![allow(dead_code)]`.

## Test traps in this codebase

- `ttl::for_each_section(msg, start, count, f)`: `start` is **how many records to
  skip**, not a section ordinal. Use `(msg, 0, ancount)` for answers,
  `(msg, ancount, nscount)` for authority. Passing `1` silently reads the wrong
  records with no error.
- `wire::resolve_name` returns labels **without** the root byte; decode with
  `dnsname::wire_to_name_labels`. `Question.qname` *does* include it, so
  `Name::from_wire` is right there.
- In an integration test `crate::` is the test binary, not the library. Fixtures must
  say `ironroot::wire::...`.
- `Kernel` is single-owner; `Services` is not `Clone`. Use
  `Kernel::shared_services()` to keep observing services after `transport::run`
  consumes the kernel. `Kernel` itself is now `Clone` (all `Arc` fields).
- `Kernel::handle` is async: each test thread needs its own current-thread runtime.
- `clap` reports an unknown flag on **stderr**; a shell gate checking
  `binary --flag 2>&1 | grep` must capture both or it fails a correct binary.
- In a `{ }` group, `exit` ends the whole script. Use `( ... )` for a subshell.
- Generate proptest inputs from `prop::sample::select(ALPHABET)`, not
  `any::<char>()` plus a filter: filtering to ASCII rejects ~95% of draws and
  proptest aborts with "Too many local rejects", which looks like a pass and is not.
- `MAX_TTL` clamps a 136-year TTL to one day deliberately. A property asserting
  `cached_ttl >= record_ttl` fails above 86400 and looks like a resolver bug.
- Run new suites three times. A stress test whose *final* assertion does a real
  upstream lookup will flake, because the test just exhausted that path.
- A **readiness poll must use a short timeout.** `TestServer::wait_until_ready` once
  used the same 10s read timeout as a real query inside a 10s deadline, so one
  unanswered probe ate the whole budget and the loop could not retry. It passed on
  Windows and failed on the CI runner only because startup was slower (21.5s of
  doomed waiting versus 0.5s). Hence `try_query_within(msg, timeout)`: 200ms to
  poll, 10s to ask a real question.
- **Green locally is not green on Linux.** CI runs ubuntu; the BPF toolchain lives
  in Debian WSL. Check both before pushing, and install `rustfmt`/`clippy` for the
  *stable* toolchain in WSL, not just nightly, or `cargo fmt` fails there.
- `cargo clippy` finds real defects, not just style: it caught a retry loop that
  returned on its first iteration and so could never retry, and a `u16 | u8`
  mismatch when a "redundant" cast was removed. Trust its `-- -D warnings` run.
- The BPF target's nightly rejects `fn f<N: usize>`; write `fn f<const N: usize>`.

## BPF verifier

Use `vm/bisect_bpf.py`, `vm/bisect_reads.py`, `vm/bisect_bounds.py` -- each edits,
rebuilds in WSL, reports, reverts. A round costs ~4 min and eliminates a category.

Rules, all hard-won:

- Every packet access must be a **constant offset** from one base pointer.
- **Integer** bounds checks (`offset < len`) prove nothing. Compare a derived
  pointer against `pkt_end`. Arithmetic *on* `pkt_end` is forbidden; derive one
  pointer and add a constant to it.
- Any `[u8; N]` with a fill byte is a **memset**, pulling compiler-builtins into
  `.text`, which aya concatenates into the program. Use `MaybeUninit`.
- Prefer a **const ladder** (64/32/16/8/4/2/1): a 13-byte name is shorter than a
  64-byte window and a 255-byte name overflows the 512-byte stack.
- `read_u8`, `read_be16`, `write_be16` must all go through `read_span`/`write_span`.
  A bare `get` or two separate byte reads fails verification while passing every
  host test.

Harness: `~/vm` in Debian WSL, `vm/verify-bpf.sh` MD5-checks the object against the
copy embedded in the initramfs. Never trust a verdict without that match.

**Status: not accepted.** `invalid access to packet, off=0 size=1, R1(id=30,off=0,r=0)`
at insn 260-262. The trace shows a backwards jump with the bound in `R2` as a
*scalar*, which is the tell: the pkt_end comparison has been hoisted above the
loop, so it no longer dominates that iteration's load.

Rounds 1-5 eliminated every write, then `read_be16`, `read_u8`,
`count_labels_in`'s `get`, and `skip_name`'s bound -- `off=21` is gone. Stubbing
`count_labels_in` out moves the error elsewhere, so it is the remaining site.

Tried, still failing:

- pointer compare in `span_in_bounds` instead of the integer `end <= self.proven`
- `const_span_in_bounds::<N>` so the pointer addition is constant-width
- `count_labels_in`'s loop bounded on `ctx.len()` and on the pointer proof
- `read_span` out of line behind `#[inline(never)] fn bounded<const N: usize>`, to
  stop LLVM hoisting the compare (moved 262 -> 260)

Next, in order:

1. `bounded` derives its pointer from `self.data`, a *struct field*, not from the XDP
   context registers. The verifier only tracks ranges on registers originating at
   `ctx`. Try passing the raw context pointers into the read helpers.
2. Check `llvm-objdump` on the xdp section: is `bounded` a real call, or did it get
   folded back despite `#[inline(never)]`?
3. If hoisting persists, read each label byte at a *fixed* offset from a pointer
   proven once at function entry, rather than per iteration.

## Hermetic end-to-end: blocked on per-resolver config

A mock root and a mock authority must be **different sockets** -- the resolver
expects a referral from one and a final answer from the other.

**Blocker:** a delegation's glue carries only an IP, so the resolver always follows
a referral to **port 53**. The mock binds an ephemeral port and there is no seam for
it, so the referral walk cannot complete. Ten cases are `#[ignore]`d with this
reason; four needing no network pass.

Two approaches tried and rejected:

- Env var read once per process: every test after the first was silently pinned to
  the first test's root -- a false pass, not a failure.
- Env var read live, plus an upstream-port var: correct per test, but env is
  process-global, so each test overwrote the previous mock and the suite timed out.

The right fix is per-resolver config -- root set and upstream port on `Services`,
which the iterator and validator already receive -- not process-global state.

Also note: a mock cannot mint a signature that verifies, so no hermetic case can
assert a genuinely *secure* verdict. That path is the differential suite's job;
these pin the shape of each outcome (bogus fails closed, insecure returns with AD
clear).