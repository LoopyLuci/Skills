---
name: computational-photography
description: "Use when implementing computational photography pipelines."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [computational-photography, HDR, image-processing, burst, denoising, super-resolution]
    related_skills: [computer-vision-techniques, audio-processing-deep-learning, custom-training-loops, data-augmentation-techniques]
---

# Computational Photography

Implementing computational photography pipelines — from HDR merging and burst processing through denoising, super-resolution, and neural rendering.

## When to Use

- Building camera apps with advanced features
- Implementing HDR, night mode, or portrait mode
- Image enhancement (denoising, super-resolution)
- Computational imaging pipelines
- Neural rendering and image synthesis

## Photography Pipeline

```python
import cv2
import numpy as np

class ComputationalPhotography:
    """Computational photography pipeline components."""
    
    @staticmethod
    def hdr_merge(images: List[np.array], exposures: List[float]) -> np.array:
        """Merge multiple exposures into HDR image."""
        merge_debevec = cv2.createMergeDebevec()
        hdr = merge_debevec.process(images, times=np.array(exposures))
        tonemap = cv2.createTonemapReinhard(gamma=2.2)
        ldr = tonemap.process(hdr)
        return np.clip(ldr * 255, 0, 255).astype(np.uint8)
    
    @staticmethod
    def burst_denoise(burst: List[np.array]) -> np.array:
        """Denoise by averaging aligned burst frames."""
        aligned = []
        for i, frame in enumerate(burst):
            if i == 0:
                aligned.append(frame)
            else:
                # Align frames (simplified)
                warp_matrix = np.eye(2, 3, dtype=np.float32)
                aligned_frame = cv2.warpAffine(frame, warp_matrix, 
                                                (frame.shape[1], frame.shape[0]))
                aligned.append(aligned_frame)
        return np.mean(aligned, axis=0).astype(np.uint8)
```

## Verification Checklist

- [ ] Image capture pipeline defined (raw → processed → output)
- [ ] HDR merging working across exposure brackets
- [ ] Denoising effective (PSNR, SSIM vs ground truth)
- [ ] Super-resolution produces real detail (not just sharpening)
- [ ] Alignment robust to handheld motion
- [ ] Processing time < capture interval for real-time
- [ ] Memory-efficient processing for high-resolution images
- [ ] Neural methods (if used) have acceptable latency
