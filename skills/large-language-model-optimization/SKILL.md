---
name: large-language-model-optimization
description: "Use when optimizing LLMs for production deployment."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [LLM, optimization, quantization, vLLM, speculative-decoding, KV-cache]
    related_skills: [llama-cpp, ml-serving-optimization, knowledge-distillation, prompt-optimization-automation]
---

# Large Language Model Optimization

Optimizing LLMs for production deployment — from quantization (GPTQ, AWQ, GGUF) through inference optimization (vLLM, FlashAttention), speculative decoding, and KV-cache management.

## When to Use

- Deploying LLMs for production inference
- Reducing LLM latency and cost per request
- Serving LLMs at scale with batching
- Quantizing models for lower resource usage
- Implementing speculative decoding for speed

## Optimization Techniques

```python
LLM_OPTIMIZATIONS = {
    'quantization': 'GPTQ (4-bit), AWQ (4-bit), GGUF (2-8 bit), bitsandbytes — reduce memory 2-4x',
    'batching': 'Continuous batching (vLLM) — dynamic request coalescing for throughput',
    'kv_cache': 'PagedAttention (vLLM), Prefix caching, sliding window — manage KV cache memory',
    'speculative_decoding': 'Draft model generates candidates, target model verifies — 2x+ speedup',
    'flash_attention': 'IO-aware exact attention — 2-4x faster, lower memory',
}

def estimate_model_memory(model_size_b: int, quantization_bits: int = 16) -> Dict:
    """Estimate GPU memory required for an LLM."""
    params = model_size_b * 1e9
    weights_memory = params * quantization_bits / 8 / 1e9  # GB
    kv_cache_per_token = model_size_b * 2 * 2 / 1e9  # 2 bytes, 2 for K+V
    overhead = 0.1 * weights_memory  # Activations, optimizer states
    
    return {
        'weights_gb': round(weights_memory, 2),
        'kv_cache_per_token_gb': round(kv_cache_per_token, 6),
        'total_estimate_gb': round(weights_memory + overhead, 2)
    }
```

## Verification Checklist

- [ ] Quantization method chosen (GPTQ, AWQ, GGUF) matches deployment target
- [ ] Inference server selected (vLLM, llama.cpp, TGI) with continuous batching
- [ ] KV cache optimization (PagedAttention, prefix caching)
- [ ] Speculative decoding (if latency critical)
- [ ] FlashAttention enabled (Ampere+ GPUs)
- [ ] Throughput and latency benchmarked
- [ ] Accuracy validated post-quantization
