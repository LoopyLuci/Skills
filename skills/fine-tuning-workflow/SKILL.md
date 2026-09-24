---
name: fine-tuning-workflow
description: Prepare datasets run LoRA fine tuning evaluate and deploy
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [fine, tuning, workflow]
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

## Trigger

Activate this skill when the user mentions:
- fine, tuning, workflow workflows or issues
- Building, fixing, or optimizing fine tuning workflow


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
