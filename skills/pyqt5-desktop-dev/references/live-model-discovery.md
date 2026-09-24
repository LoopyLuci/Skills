# Live AI Model Discovery from Provider APIs

This reference covers the implementation of live model discovery from AI provider APIs — no hardcoded models.

## Why Live Discovery?

Users explicitly demand: **"NO hardcoded API models."**
- Models must be fetched live from provider APIs
- Only display models available to the keys present
- Load them live for users to select from

## Provider API Endpoints

| Provider | Models Endpoint | Auth |
|----------|-----------------|------|
| OpenAI | `GET /v1/models` | Bearer token |
| Anthropic | `GET /v1/models` | x-api-key header |
| OpenRouter | `GET /api/v1/models?limit=500` | Bearer token (optional for listing) |
| xAI Grok | `GET /v1/models` | Bearer token |
| Nous Research | `GET /v1/models` | Bearer token |
| Ollama | `GET /api/tags` | None (local) |
| LM Studio | `GET /v1/models` | None (local) |

## Implementation Pattern

```python
class BaseProvider(ABC):
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self._models_cache: list[ModelInfo] = []
        self._cache_time: Optional[datetime] = None
        self._cache_ttl = timedelta(minutes=30)

    @property
    @abstractmethod
    def provider_id(self) -> str: ...

    @property
    @abstractmethod
    def provider_name(self) -> str: ...

    @property
    @abstractmethod
    def base_url(self) -> str: ...

    @property
    def models_endpoint(self) -> str:
        return f"{self.base_url}/models"

    @property
    def is_available(self) -> bool:
        return bool(self.api_key)

    def has_cached_models(self) -> bool:
        if not self._models_cache or not self._cache_time:
            return False
        return datetime.now() - self._cache_time < self._cache_ttl

    async def fetch_models(self) -> list[ModelInfo]:
        if self.has_cached_models():
            return self._models_cache
        try:
            models = await self._fetch_models_impl()
            self._models_cache = models
            self._cache_time = datetime.now()
            return models
        except Exception as e:
            logger.error(f"Failed to fetch models from {self.provider_name}: {e}")
            return []

    @abstractmethod
    async def _fetch_models_impl(self) -> list[ModelInfo]: ...

    @abstractmethod
    async def stream_chat(
        self, messages: list[dict[str, str]], model: str, **kwargs
    ) -> AsyncIterator[str]: ...
```

## OpenRouter Response Format

```json
{
  "data": [
    {
      "id": "anthropic/claude-3.5-sonnet",
      "name": "Claude 3.5 Sonnet",
      "description": "...",
      "context_length": 200000,
      "pricing": {
        "prompt": "0.000003",
        "completion": "0.000015"
      },
      "architecture": {
        "modality": "text"
      }
    }
  ]
}
```

## OpenRouter Free Models

- OpenRouter provides free models (pricing.prompt = 0, pricing.completion = 0)
- Use `openrouter/free` router to get random free models
- Free models should be displayed first in dropdown

## Ollama Response Format

```json
{
  "models": [
    {
      "name": "llama3.2:latest",
      "size": ...
    }
  ]
}
```

## Error Handling

- Provider unavailable → return empty list (don't crash)
- Invalid API key → return empty list
- Network error → log error, return empty list
- Cache for 30 minutes to avoid repeated calls

## GUI Integration

```python
class FetchModelsThread(QThread):
    models_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def run(self):
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async def fetch():
            try:
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
            except Exception as e:
                self.error_occurred.emit(str(e))
        loop.run_until_complete(fetch())
        loop.close()
```

## Dropdown Population

```python
def _on_models_loaded(self, models: list):
    self.model_combo.clear()
    if not models:
        self.model_combo.addItem("No models available - Set API keys", "")
        return
    
    # Group by provider
    providers = {}
    for m in models:
        if m.provider not in providers:
            providers[m.provider] = []
        providers[m.provider].append(m)
    
    # Add models grouped by provider
    for provider_id, provider_models in sorted(providers.items()):
        provider_name = provider_models[0].provider_name if provider_models else provider_id
        self.model_combo.addItem(f"── {provider_name} ──", "")
        for m in sorted(provider_models, key=lambda x: (not x.is_free, x.name)):
            label = f"{m.name}"
            if m.is_free:
                label += " (Free)"
            elif m.input_cost > 0:
                label += f" (${m.input_cost:.2f}/1M)"
            self.model_combo.addItem(label, m.id)
```

## Environment Variables

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENROUTER_API_KEY="sk-or-..."
export XAI_API_KEY="xai-..."
export NOUS_API_KEY="..."
```

## Setup Function

```python
def setup_providers(config: dict[str, str]) -> ModelRouter:
    router = get_router()
    
    if config.get("openai_api_key"):
        router.register_provider(OpenAIProvider(config["openai_api_key"]))
    
    if config.get("anthropic_api_key"):
        router.register_provider(AnthropicProvider(config["anthropic_api_key"]))
    
    if config.get("openrouter_api_key"):
        router.register_provider(OpenRouterProvider(config["openrouter_api_key"]))
    
    if config.get("xai_api_key"):
        router.register_provider(GrokProvider(config["xai_api_key"]))
    
    if config.get("nous_api_key"):
        router.register_provider(NousProvider(config["nous_api_key"]))
    
    # Local providers (no key needed)
    router.register_provider(OllamaProvider())
    router.register_provider(LMStudioProvider())
    
    return router
```