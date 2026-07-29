# Qwen3 Q2_K GGUF Parameter Reference

Values verified against `Bonsai-1.7B-Q2_K.gguf` (Qwen3 1.7B, Q2_K, GGUF v3).

## Header
- **Magic**: 0x46554747 ("GGUF" LE)
- **Version**: 3
- **Tensor count**: 310
- **Metadata KV count**: 36
- **File size**: 624,458,560 bytes (0.62 GB)

## Model Parameters

| Parameter | Value | Metadata key | Type |
|-----------|-------|-------------|------|
| architecture | qwen3 | `general.architecture` | string |
| vocab_size | 32,000 (default) | `qwen3.vocab_size` | u32 |
| hidden_size | 2,048 | `qwen3.embedding_length` | u32 |
| intermediate_size | 6,144 | `qwen3.feed_forward_length` | u32 |
| num_layers | 28 | `qwen3.block_count` | u32 |
| num_heads | 16 | `qwen3.attention.head_count` | u32 |
| num_kv_heads | 8 | `qwen3.attention.head_count_kv` | u32 |
| head_dim | 128 | derived: hidden / heads | — |
| max_seq_len | 32,768 | `qwen3.context_length` | u32 |
| rms_norm_eps | 1e-6 | `qwen3.attention.layer_norm_rms_epsilon` | f32* |
| rope_theta | 1,000,000 | `qwen3.rope.freq_base` | f32* |
| bos_token_id | 1 | `tokenizer.ggml.bos_token_id` | u32 |
| eos_token_id | 151,645 | `tokenizer.ggml.eos_token_id` | u32 |

*These are stored as f32 (type tag 6), NOT u32! A parser that only reads u32 will silently return None/default for these.*

## Tokenizer Arrays

| Array | Element Type | Count |
|-------|-------------|-------|
| `tokenizer.ggml.tokens` | string | 151,669 |
| `tokenizer.ggml.scores` | f32 | 151,669 |
| `tokenizer.ggml.token_type` | i32 | 151,387 |

## Metadata Section Size

- **Metadata section ends at**: byte 5,927,097 (from file start)
- **Tensor info section starts**: byte 5,927,097 (no padding between metadata and tensor infos)

## Quantization

All weight tensors use Q2_K (type 10) quantization except:
- Layer norm weights/scales: F32 (type 0)
- Output norm weights: F32 (type 0)

## Tensor Info Entry (v3 format, per tensor)

```
string name   (u64 len + bytes)       — e.g. "output_norm.weight" (18 bytes)
u32 n_dims                            — e.g. 1
u64 dims[n_dims]                      — e.g. [2048]
u32 quant_type                        — e.g. 0 (F32) or 10 (Q2_K)
u64 offset (v3 only!)                 — offset relative to tensor data section start
```

**Total per tensor info entry**: 8 (name_len) + name_len + 4 (n_dims) + 8*n_dims + 4 (quant_type) + 8 (v3 offset) = 42 + name_len bytes for a 1-D tensor.

## First Tensor Info Example

```
Position: 5,927,097
name_len: 18 (0x12)
name:     "output_norm.weight" (18 bytes)
n_dims:   1
dims[0]:  2048 (0x800)
quant:    0 (F32)
offset:   (v3 field, 8 bytes)
Total:    50 bytes
Next at:  5,927,147
```
