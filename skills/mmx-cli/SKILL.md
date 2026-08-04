---
name: mmx-cli
description: Use when generating media via MiniMax API CLI scripts
tags: [minimax, media-generation, tts, video, image, music]
related_skills: [minimax-xlsx, pptx-generator, shader-dev]
---

# MiniMax CLI

## Overview

Command-line scripts and Python API for generating media assets using the MiniMax API. Requires `MINIMAX_API_KEY` environment variable.

## Audio (Text-to-Speech)

```bash
# Basic TTS
python scripts/minimax_tts.py "Hello world" -o output.mp3

# Chinese voice with emotion
python scripts/minimax_tts.py "你好" -o hi.mp3 -v female-shaonv

# Custom speed and format
python scripts/minimax_tts.py "Welcome" -o out.wav -v male-qn-jingying --speed 0.8 --format wav
```

**Programmatic:**
```python
from minimax_tts import tts
audio_bytes = tts("Hello", voice_id="female-shaonv")
```

## Video (Text-to-Video)

```bash
# Basic generation
python scripts/minimax_video.py "A cat playing piano" -o cat.mp4

# Camera motion and duration
python scripts/minimax_video.py "Ocean waves [Truck left]" -o waves.mp4 --duration 10

# Resolution control
python scripts/minimax_video.py "City skyline [Push in]" -o city.mp4 --resolution 1080P
```

**Programmatic:**
```python
from minimax_video import generate
generate("A cat playing piano", "cat.mp4", model="MiniMax-Hailuo-2.3", duration=6)
```

## Image (Text-to-Image)

```bash
# Basic image
python scripts/minimax_image.py "A cat astronaut in space" -o cat.png

# Aspect ratio control
python scripts/minimax_image.py "Mountain landscape" -o hero.png --ratio 16:9

# Batch generation
python scripts/minimax_image.py "Product icons, flat style" -o icons.png -n 4 --seed 42
```

**Programmatic:**
```python
from minimax_image import generate_image, download_and_save
result = generate_image("A cat in space", aspect_ratio="16:9")
download_and_save(result["data"]["image_urls"][0], "cat.png")
```

## Music (Text-to-Music)

```bash
# With lyrics
python scripts/minimax_music.py --prompt "Indie folk, melancholic" --lyrics "[Verse]\nStreetlights flicker" -o song.mp3

# Auto-lyrics
python scripts/minimax_music.py --prompt "Upbeat pop, energetic" --auto-lyrics -o pop.mp3

# Instrumental only
python scripts/minimax_music.py --prompt "Jazz piano, smooth, relaxing" --instrumental -o jazz.mp3
```

**Programmatic:**
```python
from minimax_music import generate_music
result = generate_music(prompt="Jazz piano", is_instrumental=True)
with open("jazz.mp3", "wb") as f:
    f.write(result["audio_bytes"])
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Missing MINIMAX_API_KEY | Set environment variable before running scripts |
| Camera commands not working | Use `[Command]` syntax like `[Push in]`, `[Truck left]` |
| Output format mismatch | Check format flags per script (mp3/wav/flac for audio, mp4 for video, png/jpg for image) |

## Verification Checklist

- [ ] MINIMAX_API_KEY environment variable set
- [ ] Correct script chosen for media type (tts/video/image/music)
- [ ] Output path specified with `-o`
- [ ] File generated and playable/viewable
- [ ] Programmatic API works if needed
