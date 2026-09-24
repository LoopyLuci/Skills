# Visual Asset Generation & Verification

Generate icons, splash screens, and visual assets programmatically with Pillow, then verify with vision_analyze.

## When to use
- App icon needs redesign
- Generating multi-density Android icons (mdpi → xxxhdpi)
- Verifying visual quality before build/install

## Icon generation with Pillow

```python
from PIL import Image, ImageDraw, ImageFont

# Create at target size (e.g., 144x144 for xxhdpi)
img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# ... draw shapes, gradients, text ...
img.save(output_path, "PNG")
```

## Android adaptive icon sizes

| Density | Size (px) | Path |
|---------|-----------|------|
| mdpi | 48×48 | `mipmap-mdpi/ic_launcher.png` |
| hdpi | 72×72 | `mipmap-hdpi/ic_launcher.png` |
| xhdpi | 96×96 | `mipmap-xhdpi/ic_launcher.png` |
| xxhdpi | 144×144 | `mipmap-xxhdpi/ic_launcher.png` |
| xxxhdpi | 192×192 | `mipmap-xxxhdpi/ic_launcher.png` |

Also generate `ic_launcher_round.png` at each density for the circular mask variant.

Update `mipmap-anydpi-v26/ic_launcher.xml` to reference a custom background color:
```xml
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/app_purple_bg"/>
    <foreground android:drawable="@mipmap/ic_launcher"/>
</adaptive-icon>
```

And define the color in `values/colors.xml`:
```xml
<color name="app_purple_bg">#7c3aed</color>
```

## Verification workflow

1. Generate icon at largest density (xxxhdpi or xxhdpi)
2. Verify with `vision_analyze` at the largest size to confirm:
   - Colors render correctly (gradient visible, no banding)
   - Shapes are crisp and centered
   - Overall aesthetic matches intent ("cute yet production-grade")
3. Only then build and install

**Pillow availability:** On this host, Pillow is installed in the Hermes venv at `C:\Users\Server\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`. The system Python may not have it. Use the full venv path for icon generation scripts.

## Pitfalls

- **Adaptive icon safe zone:** Android masks the icon to a circle/squircle. Keep critical content within the central 66% of the canvas; the outer ~17% may be clipped on some shapes.
- **Transparent background:** Always use `Image.new("RGBA", ...)` with `(0,0,0,0)` — not `(255,255,255,0)` (white transparent) which can render as white on dark backgrounds.
- **Rounded rectangle mask:** Create gradient on full-size image, then composite with a rounded-rect mask for squircle shape. `Image.composite(gradient, transparent_bg, mask)` where mask is an L-mode image with `rounded_rectangle(..., fill=255)`.
- **Vision analysis at multiple sizes:** Check the largest icon; if it's crisp there, smaller densities will be fine (downscaling preserves quality better than upscaling).