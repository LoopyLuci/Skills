---
name: software-design-patterns
description: "Use when applying design patterns: creational, structural, behavioral."
category: software-development
tags: [design-patterns, architecture, gof, software-engineering]
---
# Software Design Patterns

Gang of Four and modern design patterns for production software.

## Creational Patterns

```python
# Factory Method
class ModelFactory:
    _models = {"transformer": TransformerModel, "lstm": LSTMModel}
    
    @classmethod
    def create(cls, name: str, **kwargs):
        if name not in cls._models:
            raise ValueError(f"Unknown model: {name}")
        return cls._models[name](**kwargs)

# Singleton (metaclass)
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=Singleton):
    pass  # only one instance

# Builder
config = (ModelConfig.Builder()
    .learning_rate(0.001)
    .hidden_size(768)
    .num_layers(12)
    .build())
```

## Structural Patterns

```python
# Adapter (make incompatible interfaces work)
class HuggingFaceModel:
    def generate(self, prompt: str) -> str: ...

class CustomModel:
    def forward(self, input_ids: list) -> list: ...

class ModelAdapter:
    def __init__(self, model: CustomModel, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
    def generate(self, prompt: str) -> str:
        ids = self.tokenizer.encode(prompt)
        out = self.model.forward(ids)
        return self.tokenizer.decode(out)

# Proxy (lazy/controlled access)
class ModelProxy:
    def __init__(self, model_class):
        self.model_class = model_class
        self._model = None
    def predict(self, data):
        if self._model is None:
            self._model = self.model_class()
        return self._model.predict(data)
```

## Behavioral Patterns

```python
# Strategy (swap algorithms at runtime)
class TokenizationStrategy:
    def tokenize(self, text: str) -> list: ...

class BPETokenizer(TokenizationStrategy):
    def tokenize(self, text): ...

class WordPieceTokenizer(TokenizationStrategy):
    def tokenize(self, text): ...

class Trainer:
    def __init__(self, tokenizer: TokenizationStrategy):
        self.tokenizer = tokenizer

# Observer (event system)
class EventBus:
    def __init__(self):
        self._handlers = defaultdict(list)
    def on(self, event: str, handler):
        self._handlers[event].append(handler)
    def emit(self, event: str, **data):
        for handler in self._handlers[event]:
            handler(**data)
```

## Pitfalls

- Don't force patterns where simpler code works
- Singleton is a global state — testability suffers
- Over-abstracting with factories reduces readability
- Strategy pattern works best for 3+ variants
- Observer patterns can cause memory leaks without weak references
