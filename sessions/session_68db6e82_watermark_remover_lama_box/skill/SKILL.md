---
name: watermark-remover-lama-box-cleaner
description: >
  Watermark Remover LaMa Box Cleaner. Dedicated high-precision watermark and object remover using the exceptional LaMa Box Architecture. Encapsulates watermarks (such as Google Flow, Gemini, and Veo sparkles) in a solid bounding box with localized tile cropping, native BGR Fast Fourier Convolution (FFC) inpainting, and sub-pixel distance-transform boundary feathering. Leaves zero star ghosting, zero color shift, and keeps >99.4% of the canvas untouched.
---

# Watermark Remover LaMa Box Cleaner

Dedicated watermark and object removal skill powered by the **Remover 1 (LaMa Box Architecture)**.

### Why This Engine is Exceptional:
1. **Zero Star Ghosting**: Encapsulates the watermark in a solid bounding box rather than a star silhouette, completely eliminating any trace, outline, or inverted watermark ghosting.
2. **Native BGR Channel Preservation**: Zero color channel inversion — dark car interiors, asphalt, concrete, and deep shadows preserve their exact native color temperature without any brownish tint.
3. **Localized Tile Cropping**: Only crops a small boundary tile around the watermark, running Fast Fourier Convolution inpainting strictly on that region while leaving **>99.4% of the original canvas 100% untouched**.
4. **Gaussian Distance-Transform Feathering**: Tapers the boundary with a 6px Euclidean distance transform so the transition between the inpainted patch and the original background is seamless.
5. **Full Unicode Support**: Reads and writes filenames with special characters (ellipses `…`, accents, symbols) safely on Windows.

---

## Usage

The script is located at:
`C:\Users\renu5\.gemini\config\skills\watermark-remover-lama-box-cleaner\scripts\lama_box_cleaner.py`

### 1. Remove Google Flow / Gemini / Veo Sparkle (Default)

**Single Image:**
```powershell
python "C:\Users\renu5\.gemini\config\skills\watermark-remover-lama-box-cleaner\scripts\lama_box_cleaner.py" "C:\path\to\image.jpg"
```

**Save to Custom Destination:**
```powershell
python "C:\Users\renu5\.gemini\config\skills\watermark-remover-lama-box-cleaner\scripts\lama_box_cleaner.py" "C:\path\to\image.jpg" -o "C:\path\to\output.jpg"
```

**Process an Entire Directory (Batch Mode):**
```powershell
python "C:\Users\renu5\.gemini\config\skills\watermark-remover-lama-box-cleaner\scripts\lama_box_cleaner.py" "C:\path\to\folder" -o "C:\path\to\cleaned_folder"
```

---

### 2. Remove Arbitrary Objects or Watermarks

**By Bounding Box (`--mode box --box x0,y0,x1,y1`):**
```powershell
# Using exact pixel coordinates:
python "C:\Users\renu5\.gemini\config\skills\watermark-remover-lama-box-cleaner\scripts\lama_box_cleaner.py" "C:\path\to\image.jpg" --mode box --box 1242,634,1314,706 -o "cleaned.jpg"

# Using normalized (0.0 to 1.0) coordinates:
python "C:\Users\renu5\.gemini\config\skills\watermark-remover-lama-box-cleaner\scripts\lama_box_cleaner.py" "C:\path\to\image.jpg" --mode box --box 0.85,0.85,0.98,0.98 -o "cleaned.jpg"
```

**By Custom Binary Mask (`--mode mask --mask mask.png`):**
```powershell
python "C:\Users\renu5\.gemini\config\skills\watermark-remover-lama-box-cleaner\scripts\lama_box_cleaner.py" "C:\path\to\image.jpg" --mode mask --mask "mask.png" -o "cleaned.jpg"
```

---

### Options
* `-o, --output`: Output file or directory path.
* `--mode`: Erase mode: `gemini` (default), `box`, or `mask`.
* `--feather`: Boundary feather radius (default: `6.0`).
* `--quality`: JPEG output quality (default: `98`).
* `--device`: Compute device: `cpu` (default) or `cuda`.
