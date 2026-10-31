---
version: 1.0.0
author: Nous Research
license: MIT
metadata:
  hermes:
    tags: [subsecond, hotpatch, thinlink]
    related_skills: [agentic-rpc-framework]
---

## S3 — Subsecond jump-table hot-patching (ThinLink / `subsecond`)

The `subsecond` crate (`v0.7.10`) provides a `runtime` crate that links
(`subsecond::runtime`). It defines `HotFn` and thinlinking APIs (`dylib` / `fn_ptr`).

**Critical finding (verified):** ThinLink is NOT a standalone crate or
library. It is embedded ONLY in `dioxus-cli` (`dioxus-cli` binary, `dx serve
--hotpatch`). There is NO `subsecond-thinlink` crate on crates.io.

Implication: daemon-side hot-patching must shell out to `dx serve --hotpatch`
or replicate `dioxus-cli`'s embedded ThinLink logic manually. A standalone
`subsecond` runtime crate (`v0.7.10`) can link, but cannot compile the
patch compiler (thinlink generation) without the `dioxus-cli` embedded
source.

Reference code:
- `subsecond` crate docs: `subsecond` runtime, `subsecond-thinlink` (embedded)
- `try_rust_analyzer` repo: uses `subsecond` runtime only (no thinlink).
- `dioxus-cli` (`github.com/DioxusLabs/dioxus`): `dx serve --hotpatch`
  calls embedded ThinLink.
