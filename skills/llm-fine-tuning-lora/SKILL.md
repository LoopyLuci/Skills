---
name: llm-fine-tuning-lora
description: "Use when fine-tuning LLMs with LoRA/QLoRA."
category: mlops
tags: [llm, fine-tuning, lora, qlora, peft, huggingface]
---
# LLM Fine-Tuning with LoRA/QLoRA

Efficiently fine-tuning large language models using PEFT, LoRA, and QLoRA.

## Setup

```python
from transformers import (
    AutoModelForCausalLM, AutoTokenizer,
    TrainingArguments, Trainer
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
import torch
```

## LoRA Configuration

```python
lora_config = LoraConfig(
    r=16,                    # rank — higher = more trainable params
    lora_alpha=32,           # scaling factor
    target_modules=[         # which modules to apply LoRA to
        "q_proj", "v_proj",
        "k_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
```

## QLoRA (4-bit Quantized)

```python
bnb_config = {
    "load_in_4bit": True,
    "bnb_4bit_compute_dtype": torch.bfloat16,
    "bnb_4bit_use_double_quant": True,
    "bnb_4bit_quant_type": "nf4",
}

model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    device_map="auto",
    torch_dtype=torch.bfloat16,
    quantization_config=bnb_config,
)

model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: ~8.4M / 7B = ~0.12%
```

## Training

```python
dataset = load_dataset("json", data_files="training_data.jsonl")

def format_prompt(example):
    return {
        "text": f"### Instruction: {example['instruction']}\n### Response: {example['response']}\n"
    }

dataset = dataset.map(format_prompt)

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
tokenizer.pad_token = tokenizer.eos_token

def tokenize(example):
    return tokenizer(example["text"], truncation=True, padding="max_length", max_length=512)

tokenized_dataset = dataset.map(tokenize)

training_args = TrainingArguments(
    output_dir="./lora-finetuned",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,       # effective batch = 16
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    optim="paged_adamw_8bit",
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    report_to="wandb",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
)

trainer.train()
```

## Merging & Saving

```python
# Save LoRA adapters only (small ~16MB)
model.save_pretrained("./lora-adapters")
tokenizer.save_pretrained("./lora-adapters")

# Merge LoRA into base model for inference
from peft import PeftModel
base_model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")
merged_model = PeftModel.from_pretrained(base_model, "./lora-adapters").merge_and_unload()
merged_model.save_pretrained("./merged-model")
```

## Inference

```python
from peft import PeftModel

model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")
model = PeftModel.from_pretrained(model, "./lora-adapters")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

prompt = "### Instruction: Explain Docker volumes\n### Response:"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0]))
```

## Pitfalls

- r=8~64 works for most tasks; higher r = more params but more overfitting
- target_modules depends on model architecture — check `model.named_modules()`
- QLoRA with 4-bit has minor quality loss vs 16-bit LoRA
- Training loss should be monitored — if nan, reduce learning rate
- Merge required for deployment without PEFT library
