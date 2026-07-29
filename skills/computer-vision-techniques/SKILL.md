---
name: computer-vision-techniques
description: "Use when implementing CV: classification, detection, segmentation."
category: mlops
tags: [computer-vision, cnn, detection, segmentation, classification]
---
# Computer Vision Techniques

Core CV techniques: classification, object detection, segmentation.

## Image Classification

```python
import torch
import torchvision.transforms as T
from torchvision.models import resnet50, ResNet50_Weights

# Standard preprocessing
transform = T.Compose([
    T.Resize(256),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

model = resnet50(weights=ResNet50_Weights.DEFAULT)
model.eval()

# Prediction
with torch.no_grad():
    output = model(transform(image).unsqueeze(0))
    predicted_class = output.argmax(-1).item()
```

## Object Detection

```python
from transformers import DetrImageProcessor, DetrForObjectDetection

processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)

# Convert outputs
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(
    outputs, target_sizes=target_sizes, threshold=0.7)[0]

for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    print(f"{model.config.id2label[label.item()]}: {score:.2f} at {box.tolist()}")
```

## Image Segmentation

```python
from transformers import MaskFormerImageProcessor, MaskFormerForInstanceSegmentation

processor = MaskFormerImageProcessor.from_pretrained("facebook/maskformer-swin-base-ade")
model = MaskFormerForInstanceSegmentation.from_pretrained("facebook/maskformer-swin-base-ade")

inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)
result = processor.post_process_instance_segmentation(
    outputs, target_sizes=[image.size[::-1]])[0]

# result["segmentation"]: (H, W) tensor with segment IDs
# result["segments_info"]: list of {id, label_id, score}
```

## Data Augmentation for CV

```python
import albumentations as A

train_transform = A.Compose([
    A.RandomResizedCrop(224, 224, scale=(0.8, 1.0)),
    A.HorizontalFlip(p=0.5),
    A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# For detection (bounding boxes need to be transformed)
detection_transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.2),
], bbox_params=A.BboxParams(format="pascal_voc", label_fields=["labels"]))
```

## Pitfalls

- ImageNet normalization (imagenet_mean/std) is required for pretrained models
- Object detection models have different output formats (YOLO: xywh vs DETR: xyxy)
- Segmentation models return ID maps, not RGB — use colormaps for visualization
- Augmentation transforms affect bounding boxes — use library that handles this (albumentations)
- GPU memory for detection scales with input resolution — resize large images
