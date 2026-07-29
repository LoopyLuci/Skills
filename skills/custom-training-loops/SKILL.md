---
name: custom-training-loops
description: "Use when writing custom PyTorch training loops."
category: mlops
tags: [pytorch, training, loops, custom, gradient]
---
# Custom Training Loops

Writing custom PyTorch training loops beyond the standard Trainer.

## Basic Custom Loop

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm

def train_epoch(model, dataloader, optimizer, criterion, device, clip_grad=1.0):
    model.train()
    total_loss = 0

    for batch in tqdm(dataloader, desc="Training"):
        inputs, labels = [x.to(device) for x in batch]

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()

        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), clip_grad)

        optimizer.step()
        total_loss += loss.item()

    return total_loss / len(dataloader)
```

## Training Loop with Scheduler

```python
def train(model, train_loader, val_loader, config):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    optimizer = torch.optim.AdamW(model.parameters(), lr=config["lr"], weight_decay=0.01)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=config["epochs"])
    criterion = nn.CrossEntropyLoss()

    best_val_loss = float('inf')

    for epoch in range(config["epochs"]):
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)
        val_loss = evaluate(model, val_loader, criterion, device)

        scheduler.step()
        current_lr = scheduler.get_last_lr()[0]

        print(f"Epoch {epoch+1}: train_loss={train_loss:.4f}, val_loss={val_loss:.4f}, lr={current_lr:.2e}")

        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), "best_model.pt")

    return model
```

## Mixed Precision Training

```python
from torch.cuda.amp import autocast, GradScaler

def train_amp(model, dataloader, optimizer, criterion, device):
    scaler = GradScaler()
    model.train()

    for batch in dataloader:
        inputs, labels = [x.to(device) for x in batch]

        optimizer.zero_grad()

        with autocast():
            outputs = model(inputs)
            loss = criterion(outputs, labels)

        scaler.scale(loss).backward()
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(optimizer)
        scaler.update()
```

## Gradient Accumulation

```python
def train_with_accumulation(model, dataloader, optimizer, criterion, device,
                            accumulation_steps=4):
    model.train()
    optimizer.zero_grad()

    for i, batch in enumerate(dataloader):
        inputs, labels = [x.to(device) for x in batch]
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss = loss / accumulation_steps  # normalize
        loss.backward()

        if (i + 1) % accumulation_steps == 0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            optimizer.zero_grad()
```

## Distributed Training (DDP)

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def setup_ddp(rank, world_size):
    dist.init_process_group("nccl", rank=rank, world_size=world_size)
    torch.cuda.set_device(rank)

def train_ddp(rank, world_size, model, dataset):
    setup_ddp(rank, world_size)
    model = model.to(rank)
    ddp_model = DDP(model, device_ids=[rank])

    sampler = torch.utils.data.distributed.DistributedSampler(dataset, num_replicas=world_size, rank=rank)
    loader = DataLoader(dataset, batch_size=32, sampler=sampler)

    optimizer = torch.optim.AdamW(ddp_model.parameters(), lr=0.001)

    for epoch in range(10):
        sampler.set_epoch(epoch)
        for batch in loader:
            inputs, labels = [x.to(rank) for x in batch]
            optimizer.zero_grad()
            loss = nn.CrossEntropyLoss()(ddp_model(inputs), labels)
            loss.backward()
            optimizer.step()

    dist.destroy_process_group()
```

## Pitfalls

- Always call `model.train()` and `model.eval()` for different modes
- Zero gradients BEFORE each backward pass (or accumulate intentionally)
- Gradient clipping prevents explosion — critical for transformers
- Mixed precision: loss scaling avoids underflow for small gradients
- DDP: each process should have different batch (sampler shuffles differently)
