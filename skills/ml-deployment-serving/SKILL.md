---
name: ml-deployment-serving
description: "Use when deploying ML models to production."
category: mlops
tags: [ml, deployment, serving, inference, production]
---
# ML Model Deployment & Serving

Deploying ML models to production: serving, monitoring, and infrastructure.

## Deployment Options

```
┌─────────────────────────────────────────────────┐
│                    ML Serving                    │
├─────────────────┬───────────────────────────────┤
│ Batch Inference │  Real-time Inference          │
│ › Schedule jobs │  › REST/gRPC API              │
│ › Large volumes │  › Low latency (<100ms)        │
│ › Precompute    │  › Per-request processing     │
└─────────────────┴───────────────────────────────┘
```

## Model Export Formats

```python
# PyTorch → TorchScript
model.eval()
scripted = torch.jit.script(model)
scripted.save("model.pt")

# PyTorch → ONNX
dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(model, dummy_input, "model.onnx",
    input_names=['input'], output_names=['output'],
    dynamic_axes={'input': {0: 'batch_size'}})

# HuggingFace → ONNX
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer
model = ORTModelForSequenceClassification.from_pretrained("model")
tokenizer = AutoTokenizer.from_pretrained("model")
```

## Serving with FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch

app = FastAPI()
model = torch.jit.load("model.pt").cuda().eval()

class PredictionRequest(BaseModel):
    inputs: list[list[float]]
    model_version: str = "v1"

class PredictionResponse(BaseModel):
    predictions: list[float]
    model_version: str
    latency_ms: float

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    import time
    start = time.perf_counter()
    try:
        tensor = torch.tensor(request.inputs).cuda()
        with torch.no_grad():
            outputs = model(tensor)
        predictions = outputs.cpu().tolist()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    latency = (time.perf_counter() - start) * 1000
    return PredictionResponse(
        predictions=predictions,
        model_version=request.model_version,
        latency_ms=round(latency, 2),
    )
```

## Monitoring

```python
# Metrics to track
metrics = {
    "Latency": "p50, p95, p99 in ms",
    "Throughput": "requests per second",
    "Error Rate": "4xx, 5xx percentage",
    "Prediction Distribution": "are predictions drifting?",
    "Feature Distribution": "are input features changing?",
    "Model Freshness": "when was model last deployed?",
}

# Data drift detection
from scipy.stats import ks_2samp

def detect_drift(reference: list, production: list, threshold=0.05):
    stat, p_value = ks_2samp(reference, production)
    return {"drifted": p_value < threshold, "p_value": p_value}
```

## Batched Inference

```python
from fastapi import BackgroundTasks
import asyncio

class BatchInference:
    def __init__(self, model, max_batch=32, max_wait=0.01):
        self.model = model
        self.max_batch = max_batch
        self.max_wait = max_wait
        self.queue = asyncio.Queue()

    async def predict(self, inputs):
        future = asyncio.Future()
        await self.queue.put((inputs, future))
        return await future

    async def processor(self):
        while True:
            batch = []
            futures = []
            while len(batch) < self.max_batch:
                try:
                    item = await asyncio.wait_for(self.queue.get(), self.max_wait)
                    batch.append(item[0])
                    futures.append(item[1])
                except asyncio.TimeoutError:
                    break
            if batch:
                outputs = self.model(torch.stack(batch))
                for future, output in zip(futures, outputs):
                    future.set_result(output)
```

## Pitfalls

- GPU memory leaks — monitor with `torch.cuda.memory_summary()`
- Cold starts — pre-warm model on service startup
- Model versioning — never deploy without version tracking
- Input validation — malformed inputs can crash the model
- Batching improvements diminish past optimal batch size (measure!)
