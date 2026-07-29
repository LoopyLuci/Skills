---
name: gguf-format-parsing
description: "Use when parsing GGUF model files from scratch."
---

# GGUF Format Parsing

GGUF (GGML Universal Format) is the binary format used for quantized neural network weights.

## File Layout

```
Magic: u32 = 0x46554747 "GGUF"
Version: u32
Tensor count: u64
Metadata KV count: u64
Metadata KVs
Tensor Info entries
Padding to 32 bytes
Tensor Data (block-aligned)
```

## v3 vs v2 Tensor Info — Critical

GGUF v3 adds a `u64 offset` field AFTER `u32 quant_type` in each tensor info entry.

**v2 layout:** name → n_dims → dims[] → quant_type
**v3 layout:** name → n_dims → dims[] → quant_type → **u64 offset**

If the first tensor name is correct but the second is garbage, this is the #1 cause.

## Metadata Key Patterns

Read `general.architecture` first, then prefix keys:

| arch | prefix |
|------|--------|
| llama/mistral | `llama.` |
| qwen2 | `qwen2.` |
| qwen3 | `qwen3.` |
| gemma | `gemma.` |
| phi3 | `phi3.` |

Key params: `block_count`, `embedding_length`, `feed_forward_length`, `attention.head_count`, `attention.head_count_kv`, `context_length`.

## Float Metadata Trap

`attention.layer_norm_rms_epsilon` and `rope.freq_base` are stored as **f32** (type tag 6), not u32. Provide both `get_meta_u32()` and `get_meta_f32()`.

## Debugging Desync

1. Verify magic: `0x46554747` = "GGUF" LE
2. Check version: >= 3 means extra `u64 offset` per tensor
3. Fast-skip all metadata, then hex-dump the transition
4. Garbage after first tensor name = missed v3 offset field
