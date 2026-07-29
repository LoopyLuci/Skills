---
name: wsl2-gpu-cuda
description: "Use when enabling GPU/CUDA acceleration in WSL2."
category: software-development
tags: [wsl2, gpu, cuda, nvidia, vulkan, directml]
---
# WSL2 GPU / CUDA

Enabling GPU acceleration (CUDA, Vulkan, DirectML) in WSL2.

## Prerequisites

```powershell
# 1. Windows 11 or Windows 10 21H2+
# 2. WSL2 with GPU paravirtualization
wsl --set-default-version 2

# 3. Install NVIDIA drivers on Windows (covers WSL2 too)
# Download from: https://www.nvidia.com/Download/index.aspx
# DO NOT install Linux drivers inside WSL2 -- Windows driver covers both
```

## CUDA in WSL2

```bash
# Verify GPU is visible from WSL2
nvidia-smi

# Should show: Driver Version matches Windows driver
# CUDA Version: 12.x

# Run CUDA containers
docker run --gpus all nvidia/cuda:12.2-runtime-ubuntu22.04 nvidia-smi
```

## Docker with GPU

```powershell
docker run --gpus all -it nvidia/cuda:12.2-runtime-ubuntu22.04 bash
# Inside container: nvidia-smi should work
```

## PyTorch/TensorFlow with GPU

```bash
# CUDA toolkit inside WSL2 (for native, not Docker)
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get install -y cuda-toolkit-12-2

# Verify
nvcc --version
```

## Vulkan in WSL2

```bash
# Install Vulkan SDK and tools
sudo apt-get update
sudo apt-get install -y vulkan-tools mesa-vulkan-drivers

# Verify
vulkaninfo
vkcube
```

## DirectML (for AMD/Intel GPUs)

```bash
# DirectML in WSL2 doesn't need special drivers
# Windows GPU drivers are forwarded

# For PyTorch with DirectML
pip install torch-directml
```

## Performance Notes

```bash
# GPU in WSL2 is near-native performance for compute (CUDA)
# Graphics/display is paravirtualized -- slightly lower perf than native

# Monitor GPU usage
nvidia-smi -l 1
watch -n 1 nvidia-smi
```

## Troubleshooting

```bash
# nvidia-smi: "command not found"
# Install NVIDIA CUDA tools on WSL2:
sudo apt-get install -y nvidia-utils-545

# nvidia-smi: "No devices were found"
# Check Windows drivers are installed
# Check `wsl --shutdown` then restart

# Docker --gpus all: "could not select device driver"
# Install nvidia-container-toolkit inside WSL2:
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

## Pitfalls

- **Windows GPU drivers** cover WSL2 -- do NOT install Linux GPU drivers inside WSL2
- **nvidia-smi** shows Windows driver version, not a WSL2 version
- **--gpus all** requires `nvidia-container-toolkit` installed in the Docker host (WSL2)
- **Not all CUDA versions** are supported -- check NVIDIA's WSL2 compatibility matrix
- **GPU compute** works; GPU display/output may have limitations
