---
name: fine-tuning-workflow
description: "Prepare datasets run LoRA fine tuning evaluate and deploy"
---

# Fine-Tuning Workflow

## Data Format
```jsonl
{"messages": [
  {"role": "system", "content": "You are helpful"},
  {"role": "user", "content": "What is Python?"},
  {"role": "assistant", "content": "Python is..."}
]}
```

## LoRA (Unsloth)
```python
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained("unsloth/Llama-3.2-3B")
model = FastLanguageModel.get_peft_model(model, r=16)
# Train...
model.save_pretrained("lora-output")
```
