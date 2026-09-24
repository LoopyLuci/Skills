---
name: multi-provider-ai-integration
description: Integrate multiple AI providers via live model discovery.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [ai, llm, multi-provider, live-discovery, model-routing, openai, anthropic, openrouter, xai, ollama]
---

# Multi-Provider AI Integration

Integrate multiple AI model providers with **live model discovery** — never hardcode model lists. Models are fetched directly from each provider's API, filtered by available API keys, cached, and routed with automatic fallback.

## Trigger

Use when the user wants to:
- Integrate AI chat into an application
- Support multiple AI providers (OpenAI, Anthropic, OpenRouter, xAI, etc.)
- Discover available models at runtime rather than hardcoding them
- Route requests across providers with fallback
- Show users only the models they have API keys for

## Core Principle

**NEVER hardcode AI models.** Provider model catalogs change constantly. Always fetch live from provider APIs.

```python
# WRONG — Hardcoded models
MODELS = [
    {"id": "gpt-4o", "name": "GPT-4o"},
    {"id": "claude-3-5-sonnet", "name": "Claude 3.5 Sonnet"},
]

# CORRECT — Live discovery
class BaseProvider(ABC):
    async def fetch_models(self) -> list[ModelInfo]:
        """Fetch models from provider API."""
```

## Architecture

```
ModelRouter
├── providers: dict[str, BaseProvider]
├── fallback_order: list[str]
├── get_all_models() → list[ModelInfo]
└── stream_chat(messages, model, provider_id=None) → AsyncIterator

BaseProvider (abstract)
├── api_key: str
├── _models_cache: list[ModelInfo]
├── _cache_ttl: timedelta  (default: 30 minutes)
├── fetch_models() → list[ModelInfo]
├── _fetch_models_impl() → list[ModelInfo]  (abstract)
└── stream_chat(messages, model, **kwargs) → AsyncIterator  (abstract)

ModelInfo (dataclass)
├── id: str
├── name: str
├── provider: str
├── provider_name: str
├── is_free: bool
├── context_length: int
├── input_cost: float
├── output_cost: float
├── capabilities: list[str]
└── description: str
```

## Provider Implementation

Each provider implements `BaseProvider` with its specific API:

| Provider | Models Endpoint | Auth Header | Free Detection |
|----------|----------------|-------------|----------------|
| **OpenAI** | `GET /v1/models` | `Authorization: Bearer <REDACTED>` | Model ID matching |
| **Anthropic** | `GET /v1/models` | `x-api-key` | Model ID matching |
| **OpenRouter** | `GET /api/v1/models` | `Authorization: Bearer <REDACTED>` | `pricing.prompt == 0` |
| **xAI Grok** | `GET /v1/models` | `Authorization: Bearer <REDACTED>` | Model ID matching |
| **Nous Research** | `GET /v1/models` | `Authorization: Bearer <REDACTED>` | All free (self-hosted) |
| **Ollama** | `GET /api/tags` | None | All free (local) |
| **LM Studio** | `GET /v1/models` | None | All free (local) |

### OpenAI Provider

```python
class OpenAIProvider(BaseProvider):
    base_url = "https://api.openai.com/v1"
    
    async def _fetch_models_impl(self) -> list[ModelInfo]:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/models", headers=headers) as resp:
                if resp.status != 200:
                    return []
                data = await resp.json()
                return [
                    ModelInfo(
                        id=m["id"],
                        name=m["id"].replace("-", " ").title(),
                        provider=self.provider_id,
                        provider_name=self.provider_name,
                        is_free=m["id"] in ["gpt-4o-mini", "gpt-3.5-turbo"],
                        context_length=self._get_context_length(m["id"]),
                    )
                    for m in data.get("data", [])
                ]
```

### OpenRouter Provider

OpenRouter returns pricing data, enabling automatic free-model detection:

```python
class OpenRouterProvider(BaseProvider):
    base_url = "https://openrouter.ai/api/v1"
    
    async def _fetch_models_impl(self) -> list[ModelInfo]:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/models?limit=500", headers=headers
            ) as resp:
                data = await resp.json()
                return [
                    ModelInfo(
                        id=m["id"],
                        name=m.get("name", m["id"]),
                        provider=self.provider_id,
                        provider_name=self.provider_name,
                        is_free=float(m.get("pricing", {}).get("prompt", "0")) == 0,
                        context_length=m.get("context_length", 4096),
                        input_cost=float(m.get("pricing", {}).get("prompt", "0")),
                        output_cost=float(m.get("pricing", {}).get("completion", "0")),
                    )
                    for m in data.get("data", [])
                ]
```

### Ollama Provider (Local)

```python
class OllamaProvider(BaseProvider):
    base_url = "http://localhost:11434"
    models_endpoint = f"{base_url}/api/tags"
    is_available = True  # No API key needed
    
    async def _fetch_models_impl(self) -> list[ModelInfo]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.models_endpoint) as resp:
                data = await resp.json()
                return [
                    ModelInfo(
                        id=m["name"],
                        name=m["name"],
                        provider=self.provider_id,
                        provider_name=self.provider_name,
                        is_free=True,
                        context_length=4096,
                    )
                    for m in data.get("models", [])
                ]
```

## Model Router

The router manages providers, caches models, and handles fallback:

```python
class ModelRouter:
    def __init__(self):
        self.providers: dict[str, BaseProvider] = {}
        self._fallback_order: list[str] = []

    def register_provider(self, provider: BaseProvider):
        self.providers[provider.provider_id] = provider
        if provider.provider_id not in self._fallback_order:
            self._fallback_order.append(provider.provider_id)

    async def get_all_models(self) -> list[ModelInfo]:
        all_models = []
        for provider in self.providers.values():
            models = await provider.fetch_models()
            all_models.extend(models)
        return all_models

    async def stream_chat(
        self, messages, model, provider_id=None
    ) -> AsyncIterator[str]:
        if provider_id and provider_id in self.providers:
            async for chunk in self.providers[provider_id].stream_chat(messages, model):
                yield chunk
            return
        # Fallback: try each provider
        for pid in self._fallback_order:
            try:
                async for chunk in self.providers[pid].stream_chat(messages, model):
                    yield chunk
                return
            except Exception:
                continue
        yield "Error: All providers failed"
```

## Caching Strategy

- **30-minute TTL** per provider to avoid repeated API calls
- **Manual refresh** capability to force reload
- **Graceful degradation** when providers are unavailable (logs error, continues)

```python
class BaseProvider(ABC):
    _cache_ttl = timedelta(minutes=30)
    
    async def fetch_models(self) -> list[ModelInfo]:
        if self.has_cached_models():
            return self._models_cache
        try:
            models = await self._fetch_models_impl()
            self._models_cache = models
            self._cache_time = datetime.now()
            return models
        except Exception as e:
            logger.error(f"Failed to fetch from {self.provider_name}: {e}")
            return []
```

## GUI Integration (PyQt5)

Fetch models asynchronously to avoid blocking the UI:

```python
class FetchModelsThread(QThread):
    models_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def run(self):
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async def fetch():
            from webbuilder.ai import get_router, setup_providers
            import os
            config = {
                "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
                "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
                "openrouter_api_key": os.environ.get("OPENROUTER_API_KEY", ""),
                "xai_api_key": os.environ.get("XAI_API_KEY", ""),
                "nous_api_key": os.environ.get("NOUS_API_KEY", ""),
            }
            router = setup_providers(config)
            models = await router.get_all_models()
            self.models_loaded.emit(models)
        loop.run_until_complete(fetch())
        loop.close()

class ChatPanel(QWidget):
    def _populate_models(self):
        self.model_combo.clear()
        self.model_combo.addItem("Loading models...", "")
        self._fetch_models_thread = FetchModelsThread()
        self._fetch_models_thread.models_loaded.connect(self._on_models_loaded)
        self._fetch_models_thread.start()

    def _on_models_loaded(self, models):
        self.model_combo.clear()
        # Group by provider, sort free first
        providers = {}
        for m in models:
            providers.setdefault(m.provider, []).append(m)
        for pid, pmodels in sorted(providers.items()):
            self.model_combo.addItem(f"── {pmodels[0].provider_name} ──", "")
            for m in sorted(pmodels, key=lambda x: (not x.is_free, x.name)):
                label = f"{m.name} (Free)" if m.is_free else m.name
                self.model_combo.addItem(label, m.id)
```

## Environment Variable Configuration

Users set API keys via environment variables. Only providers with keys are registered:

```python
import os

config = {
    "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
    "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
    "openrouter_api_key": os.environ.get("OPENROUTER_API_KEY", ""),
    "xai_api_key": os.environ.get("XAI_API_KEY", ""),
    "nous_api_key": os.environ.get("NOUS_API_KEY", ""),
}
router = setup_providers(config)
# Only providers with non-empty keys are registered
# Ollama and LM Studio are always registered (no key needed)
```

## Encrypted Key Storage

API keys must NEVER be stored in plaintext. Use Fernet symmetric encryption with a PBKDF2-derived master key:

```python
from cryptography.fernet import Fernet

class ProviderStore:
    """Encrypted storage for AI provider configurations."""
    
    def __init__(self):
        self._fernet = self._init_encryption()
        self._providers: dict[str, ProviderConfig] = {}
        self._usage: list[UsageRecord] = []
    
    def _init_encryption(self) -> Fernet:
        """Initialize or load encryption key."""
        if MASTER_KEY_FILE.exists():
            key = MASTER_KEY_FILE.read_bytes()
        else:
            key = Fernet.generate_key()
            MASTER_KEY_FILE.write_bytes(key)
            MASTER_KEY_FILE.chmod(0o600)
        return Fernet(key)
    
    def _save(self):
        """Encrypt and save provider configs to disk."""
        data = {
            "providers": {
                name: {
                    "name": p.name,
                    "api_key": p.api_key,
                    "base_url": p.base_url,
                    "model": p.model,
                    "enabled": p.enabled,
                    "priority": p.priority,
                }
                for name, p in self._providers.items()
            },
            "usage": [...],
        }
        encrypted = self._fernet.encrypt(json.dumps(data).encode())
        PROVIDER_STORE_FILE.write_bytes(encrypted)
        PROVIDER_STORE_FILE.chmod(0o600)
```

**Key rules:**
- Master key stored in user home directory with 0o600 permissions
- Provider configs encrypted as a single blob on disk
- API keys are NEVER logged, printed, or exposed in error messages
- Usage records stored alongside provider configs in the same encrypted file

## Usage Tracking and Cost Estimation

Track every API call for cost visibility and debugging:

```python
@dataclass
class UsageRecord:
    timestamp: float
    provider: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float
    latency_ms: float
    success: bool
    error: str = ""

class APIProviders:
    """LLM API calls with usage tracking and cost estimation."""
    
    COST_PER_1M_TOKENS = {
        "openrouter": {"default": 0.50},
        "anthropic": {
            "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
        },
        "openai": {
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "gpt-4o": {"input": 2.50, "output": 10.00},
        },
        "google": {
            "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
        },
        "ollama": {"default": 0.0},
    }
    
    def _estimate_cost(self, provider: str, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Estimate cost in USD for a request."""
        provider_costs = self.COST_PER_1M_TOKENS.get(provider, {})
        if "default" in provider_costs:
            rate = provider_costs["default"]
            return (prompt_tokens + completion_tokens) * rate / 1_000_000
        model_costs = provider_costs.get(model, {})
        if not model_costs:
            return 0.0
        input_cost = prompt_tokens * model_costs.get("input", 0) / 1_000_000
        output_cost = completion_tokens * model_costs.get("output", 0) / 1_000_000
        return input_cost + output_cost
```

**Usage summary aggregation:**
- Total requests, cost, tokens
- Per-provider breakdown
- Success rate and average latency
- Keep last 1000 records (configurable)

## Agentic Chat with Tool Execution

For built-in agentic chat, the LLM needs tools to control the application:

```python
class ChatEngine:
    """Agentic chat engine that can execute tools."""
    
    TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "vm_status",
                "description": "Get current VM running status",
                "parameters": {"type": "object", "properties": {}},
            },
        },
        # ... more tools
    ]
    
    async def send_message(self, user_input: str) -> AsyncGenerator[ChatMessage, None]:
        """Send a user message and stream the response."""
        self.add_message(ChatMessage("user", user_input))
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        for msg in self._history:
            messages.append({"role": msg.role, "content": msg.content})
        response = await self._providers.call(messages, tools=self.TOOLS)
        # Handle tool calls in response
        if response.tool_calls:
            for tool_call in response.tool_calls:
                result = await self._execute_tool(tool_call)
                self.add_message(ChatMessage("tool", result))
        yield ChatMessage("assistant", response.content)
```

**Tool schema rules:**
- Each tool MUST have a valid JSON Schema with `type`, `properties`, and `description`
- Tool names MUST be snake_case and descriptive
- Tool descriptions MUST explain what the tool does AND when to use it
- System prompt MUST list all available tools with their purposes

## Pitfalls

1. **Hardcoding models**: NEVER hardcode model lists. Provider catalogs change constantly. Always fetch live.
2. **Blocking the GUI**: Always fetch models asynchronously (QThread, asyncio) to avoid freezing the UI.
3. **Missing API keys**: Only register providers that have API keys. Don't show models from providers the user can't access.
4. **No error handling**: Each provider fetch should be wrapped in try/except. One provider failing shouldn't break others.
5. **No caching**: Fetching models on every UI interaction wastes API calls. Cache for 30 minutes.
6. **Ignoring free models**: Sort free models first so users see accessible options immediately.
7. **Missing local providers**: Always include Ollama and LM Studio — they need no API key and work offline.
8. **Forgetting to refresh**: Provide a refresh button so users can reload models after adding API keys.
9. **Not showing pricing**: When available (OpenRouter), show pricing so users can make informed choices.
10. **Assuming OpenAI compatibility**: Not all providers use the same auth headers or response formats. Implement each provider separately.
11. **Plaintext API keys**: NEVER store API keys in plaintext. Always encrypt with Fernet before writing to disk.
12. **No usage tracking**: Track every API call — users need visibility into costs and token usage.
13. **No cost estimation**: Estimate costs from token counts and per-model pricing. Show in UI.
14. **No failover**: Implement automatic failover across providers. If one fails, try the next in priority order.
15. **Missing tool schemas**: Agentic chat requires properly defined JSON Schema tools for LLM function calling.
16. **Not handling tool results**: When LLM invokes a tool, execute it and feed the result back into the conversation.

## Verification

After implementation:

1. **Test with no keys**: Only local providers (Ollama, LM Studio) should appear.
2. **Test with one key**: Only that provider's models should appear.
3. **Test with multiple keys**: All providers with keys should appear, grouped by provider.
4. **Test fallback**: If one provider fails, others should still work.
5. **Test caching**: Models should not refetch within 30 minutes.
6. **Test refresh**: Manual refresh should force refetch.

## Reference

For provider-specific API details, see [references/provider-apis.md](references/provider-apis.md).
