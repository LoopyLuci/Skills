---
name: rust-ai-resilience
description: Add resilience patterns to Rust async AI engines.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [rust, async, ai, resilience, retry, caching, rate-limiting, streaming]
    related_skills: [software-development/systematic-debugging]
---

# Rust AI Engine Resilience

For async AI engines in Rust that need retry, caching, rate limiting, and streaming.
The recurring failure is a blocking, fragile engine that fails on transient errors,
wastes tokens on repeated prompts, and provides no streaming feedback.

## When to Use

- Adding retry with exponential backoff to an AI engine
- Adding response caching to avoid duplicate API calls
- Adding rate limiting to avoid 429 errors
- Adding streaming support for token-by-token display
- Debugging AI engine resilience issues
- Implementing AI provider resilience in any Rust async codebase

## Always-on rules

- **Retry only transient errors.** 429, 503, 529, and "rate limit" messages are worth
  retrying. 400, 401, 403, 404 are not. Check the error message, not just the
  status code. A 404 means the model doesn't exist — retrying won't help.
- **Use `tokio::sync::Semaphore` for concurrent request limiting.** Acquire a permit
  before each request, drop it after. The semaphore should be a field on the
  engine struct, wrapped in `Arc`. Default to 4 concurrent requests.
- **Use `lru::LruCache` for response caching.** Key by a hash of (prompt, model,
  temperature, max_tokens, tier, history). Set a TTL (5 minutes is reasonable
  for chat responses). Only cache non-streaming requests.
- **Hash `Option<f32>` via `to_bits()`.** `f32` doesn't implement `Hash`, so
  `Option<f32>` doesn't either. Use `req.temperature.map(|t| t.to_bits()).hash(&mut hasher)`.
- **Hash enums via `format!("{:?}", value)`.** If an enum doesn't derive `Hash`,
  convert it to a string first.
- **Stream bytes to String via `from_utf8_lossy`.** `reqwest` bytes streams yield
  `Bytes`, not `String`. Convert with `String::from_utf8_lossy(&bytes).to_string()`.
- **Wrap Win32 API calls in `unsafe`.** `InvalidateRect`, `SetWindowPos`, etc. are
  unsafe in Rust. `unsafe { InvalidateRect(hwnd, ptr::null_mut(), 0); }`
- **Don't use `self` in window procs.** Get the state pointer from
  `GetWindowLongPtrW` first. See win32-gui-rendering skill.
- **Integration tests hang when external services aren't running.** Check if the
  service is running before running integration tests. Use `curl` or a health check.
  A hanging integration test is an environment issue, not a code issue.
- **Build locks on Windows.** If `cargo build` fails with "failed to remove file",
  kill the running process first: `taskkill -f -im app.exe`.

## Patterns

### Retry with exponential backoff

```rust
async fn retry<F, Fut, T>(&self, operation: F) -> Result<T>
where
    F: Fn() -> Fut,
    Fut: std::future::Future<Output = Result<T>>,
{
    let mut attempts = 0;
    let max_attempts = 3;
    let mut delay = Duration::from_millis(500);
    loop {
        match operation().await {
            Ok(result) => return Ok(result),
            Err(e) if attempts < max_attempts && Self::is_retryable(&e) => {
                attempts += 1;
                tokio::time::sleep(delay).await;
                delay *= 2;
            }
            Err(e) => return Err(e),
        }
    }
}

fn is_retryable(error: &Error) -> bool {
    let text = error.to_string().to_ascii_lowercase();
    text.contains("429") || text.contains("503") || text.contains("529")
        || text.contains("rate limit") || text.contains("too many requests")
}
```

### Response caching

```rust
use lru::LruCache;
use std::num::NonZeroUsize;

// Field on engine:
response_cache: Arc<Mutex<LruCache<u64, (AiResponse, Instant)>>>,

// In constructor:
response_cache: Arc::new(Mutex::new(LruCache::new(
    NonZeroUsize::new(128).unwrap(),
))),

// Check cache before request:
let cache_key = Self::cache_key(&req);
{
    let mut cache = self.response_cache.lock().unwrap();
    if let Some((response, timestamp)) = cache.get(&cache_key) {
        if timestamp.elapsed() < Duration::from_secs(300) {
            return Ok(response.clone());
        }
    }
}

// Store after success:
if let Ok(ref response) = result {
    let mut cache = self.response_cache.lock().unwrap();
    cache.put(cache_key, (response.clone(), Instant::now()));
}
```

### Rate limiting

```rust
use tokio::sync::Semaphore;

// Field on engine:
request_semaphore: Arc<Semaphore>,

// In constructor:
request_semaphore: Arc::new(Semaphore::new(4)),

// Acquire before request:
let _permit = self
    .request_semaphore
    .acquire()
    .await
    .map_err(|e| Error::Network(e.to_string()))?;
```

### Streaming

```rust
use futures::StreamExt;

pub async fn generate_stream(
    &self,
    req: AiRequest,
) -> Result<impl futures::Stream<Item = Result<String>>> {
    // ... build request ...
    let response = self.client.post(&url).json(&body).send().await?;
    let byte_stream = response.bytes_stream();
    let stream = byte_stream.map(|chunk| {
        chunk
            .map(|bytes| String::from_utf8_lossy(&bytes).to_string())
            .map_err(|e| Error::Network(e.to_string()))
    });
    Ok(stream)
}
```

### Cache key hashing

```rust
fn cache_key(req: &AiRequest) -> u64 {
    use std::hash::{Hash, Hasher};
    let mut hasher = std::collections::hash_map::DefaultHasher::new();
    req.prompt.hash(&mut hasher);
    req.force_model.hash(&mut hasher);
    req.temperature.map(|t| t.to_bits()).hash(&mut hasher);
    req.max_tokens.hash(&mut hasher);
    req.force_tier.hash(&mut hasher);
    if let Some(ref history) = req.history {
        for msg in history {
            format!("{:?}", msg.role).hash(&mut hasher);
            msg.content.hash(&mut hasher);
        }
    }
    hasher.finish()
}
```

## Dependencies

```toml
reqwest = { version = "0.12", features = ["json", "stream"] }
lru = "0.12"
futures = "0.3"
```

## Pitfalls

- **`resolve_local_model()` returns `String`, not `ModelInfo`.** Wrap with
  `self.resolved_local(...)` when the caller expects a `ModelInfo`.
- **`Option<f32>` doesn't implement `Hash`.** Use `.map(|t| t.to_bits())` before hashing.
- **Enums without `Hash` derive.** Use `format!("{:?}", value).hash(&mut hasher)`.
- **`Bytes` vs `String` in streams.** `reqwest` yields `Bytes`, convert with
  `from_utf8_lossy`.
- **`InvalidateRect` is unsafe.** Wrap in `unsafe { }` blocks.
- **`self` doesn't exist in window procs.** Get pointer from `GetWindowLongPtrW`.
- **Integration tests hang when external services aren't running.** Check if the
  service is running before running integration tests.
- **Build locks on Windows.** Kill the running process before rebuilding.
- **`label_w` variable removed by patch but still referenced.** When a patch removes
  a variable declaration, check all references to that variable in the surrounding
  scope. A removed declaration with live references is a compile error.
- **`C_BORDER` and other constants appear multiple times.** Use `replace_all=true`
  when patching a constant that appears in multiple locations. A non-unique match
  causes the patch to fail.
