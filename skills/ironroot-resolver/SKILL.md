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

## Measure the running resolver; do not read it

Reading the code found nothing. Timing it found three bugs in one pass:

- `h0.debian.org` took **14 s**, with a visible 10 s gap between two hops. The
  per-attempt timeout doubled per retry (RFC 1035 §4.2.2) with no total cap, so
  one dead server cost 1.5 + 3 + 6 s. Now bounded by `max_total_per_server`.
- `--upstream-timeout-ms` reached only the validator, so it had no effect on the
  iterator -- the part that waits most. It now lives on `UpstreamConfig`.
- UDP datagrams were **dropped by the kernel** under burst, because the socket
  used the OS default buffer. A dropped query is indistinguishable from being
  down. Buffers now requested at 4 MiB; the kernel grants 8.

Probed and found correct, so left alone: TCP, 14 hostile datagrams, flag hygiene
across TC/opcode/AA/CD/RD/Z, and the rate limiter (207/193 at defaults).

### Two measurement errors that first looked like resolver bugs

Both are worth remembering because each reads as a server fault:

- **Firing 400 datagrams in a tight loop tests the socket buffer, not the
  limiter.** The tokio task never gets scheduled, so the buffer absorbs them and
  the limiter sees nothing. Pace the burst or yield between sends.
- **A UDP socket reused after a timeout reports a spurious ICMP reset on
  Windows.** Zero resets on a fresh socket for the same queries. Use one socket
  per query when measuring.

### `#[cfg(unix)]` code that only ever ran on Linux

Socket buffer tuning took three attempts that all compiled and passed on Windows
while panicking every runtime worker on Linux, because the block was `cfg(unix)`
and never executed there. `UdpSocket::from_std` registers a *blocking* socket,
which tokio permits only where blocking is legal, and an `async fn` body never is
-- on any platform. Tuning belongs in `main`, before the runtime exists, where it
is merely a syscall.

The general rule: anything behind a platform cfg has never been executed unless it
was run on that platform. `cargo build` on Windows is not a test of it.

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

**Status: not accepted, but the cause is now pinned.** Staging the QNAME into a
stack buffer *does* clear the verifier's packet-access complaint. The blocker
moved to a different wall, and it is a specific one:

> The write into the staging buffer must leave **no panic call**. aya concatenates
> `.text.unlikely` into the program, so any panic the compiler cannot prove
> unreachable becomes a trailing `call` the loader cannot resolve -- and the
> symptom is "last insn is not an exit or jmp", which says nothing about panics.

Five shapes tried, one failure each:

| shape | leaves |
|---|---|
| `copy_from_slice` at a runtime length | `memmove` |
| `buf[i + k]` | a bounds-check panic |
| `buf.get_mut(a..b)` | a range-check panic |
| `buf.as_mut_ptr().add(i)` cast to `[u8; N]` | an alignment panic |
| nested `[[u8; BLOCK]; N]` | two index checks |

The nested array ships (correct, tested, two panics left). Next: a fixed-width
`copy_from_slice::<$n>` between two arrays of the same compile-time width -- no
runtime length anywhere in it, so the remaining checks are over constants.

Also learned the hard way:

- The ladder's width must come from what the **packet** offers, not the buffer's
  remaining space. Backwards stages nothing for any query shorter than STAGE.
- A name longer than one block crosses the boundary; dropping the spilled bytes
  silently changes the hashed name, so the key stops matching the userspace
  formula. Mutation testing caught this one.
- STAGE must fit the 512-byte frame alongside `build_reply`'s buffers: 64 works,
  128 does not. A longer name than STAGE is an L0 miss, which is correct.
- The staged length is a **lower bound** when the packet is short; the walk must
  stop there rather than read uninitialised stack.
- `rm` the panic and the check becomes redundant: the compression-pointer guard is
  subsumed by `label_len > 63`. Kept and documented as defence in depth with the
  mutation result, rather than implied to be load-bearing.

`vm/bisect_*.py` are the tools that got here; a round is ~4 min.

## Hermetic end-to-end: per-resolver config, and what it unblocked

A mock root and a mock authority must be **different sockets** -- the resolver
expects a referral from one and a final answer from the other.

`UpstreamConfig` carries the root set and the delegation port on the resolver
itself, reached via `RuntimeConfig` and `Services`. It must be per-resolver, not
process-global: env vars were tried twice and both failed -- read once per process
pinned every test to the first test's root (a silent false pass), read live each
test overwrote the previous mock (wholesale timeout).

**The root's port and the delegation port are different fields.** A glue record
carries only an IP, so the delegation port is ours to choose; the root's port is
part of a real address we were handed. Collapsing them points root queries at the
authority's socket.

Defects that surfaced only once the suite could run:

- `TestServer::_mock` was `Option`, so a second `with_mock` silently dropped the
  first -- the mock authority, whose socket closed on drop. Indistinguishable from
  a resolver that cannot reach its delegated server. It is a `Vec` now.
- **A negative answer was treated as a referral.** Empty answer + populated
  authority is both shapes; the code discriminated on section *counts*. NXDOMAIN
  carries an SOA there (RFC 2308 2.1), so it went back to the root and died as a
  referral loop. Check for actual NS records.
- `resolve_name` returns **labels, not encoded bytes**. Reading qtype at
  `12 + resolve_name(..).len()` silently decodes 0.
- A mock that echoes a hardcoded qtype gets its referral rejected as a mismatch --
  correctly. Echo the query's type.

Still ignored, each with its reason: two need an NSEC proof of DS absence to
establish an insecure delegation (needs a signed parent zone); one needs
per-query rcodes from the mock. The resolver is *right* in the first two --
unable to distinguish unsigned from forged, it says bogus, which is correct.

A mock cannot mint a signature that verifies, so no hermetic case can assert a
genuinely *secure* verdict; the differential suite covers that.

### Mocks must serve TCP, and truncation must be transport-specific

RFC 1035 §4.2.1 makes the resolver retry a truncated UDP response over TCP, so a
UDP-only mock cannot test it at all. Serve UDP and TCP on the *same* port -- a
referral gives one address, so the resolver must not need a second for TCP.

Mutation testing caught a **false pass** here: with the mock truncating over
*both* transports, the retry got nothing back, so disabling the resolver's TCP
fallback still left the test green. Truncation is a property of the transport,
not of the zone -- `respond_on(query, Transport::Udp)` rather than `respond()`.
After that fix, disabling the fallback fails the test.

That is the general lesson: a mock that cannot express the *distinction* the test
is about makes the test vacuous, and it passes under mutation without anyone
noticing. If a mutation does not fail the test, the test is not testing anything.