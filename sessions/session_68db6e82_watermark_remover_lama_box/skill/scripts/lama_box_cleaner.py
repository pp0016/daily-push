#!/usr/bin/env python3
"""
LaMa Box Cleaner (Dedicated Watermark Remover)
Based on the exceptional 'Remover 1' Architecture:
1. Solid bounding-box encapsulation of Google Flow / Gemini / Veo sparkle
2. Localized tile crop with boundary padding (snapped to multiple of 8)
3. LaMa Fast Fourier Convolutions (FFC) inpainting
4. Native BGR preservation (zero channel swap)
5. Gaussian distance-transform boundary feathering (feather=6.0)
6. Canvas re-insertion (>99.4% original untouched canvas)
7. Full Unicode path safety for Windows.
"""

import cv2
import numpy as np
import os
import sys
import argparse
import glob

# Try loading iopaint LaMa model
try:
    from iopaint.model_manager import ModelManager
    from iopaint.schema import InpaintRequest
except ImportError:
    print("Error: 'iopaint' library is required. Install via: pip install iopaint")
    sys.exit(1)

def read_image_unicode(path):
    """Safely reads images with Unicode characters on Windows."""
    try:
        with open(path, "rb") as fp:
            data = fp.read()
        return cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"[LaMaBoxCleaner] Error reading {path}: {e}")
        return None

def write_image_unicode(path, img, quality=98):
    """Safely writes images with Unicode characters on Windows."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        ext = os.path.splitext(path)[1].lower()
        if ext in [".jpg", ".jpeg"]:
            params = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        elif ext == ".png":
            params = [int(cv2.IMWRITE_PNG_COMPRESSION), 3]
        elif ext == ".webp":
            params = [int(cv2.IMWRITE_WEBP_QUALITY), quality]
        else:
            params = []
            
        success, buf = cv2.imencode(ext if ext else ".jpg", img, params)
        if success:
            with open(path, "wb") as fp:
                fp.write(buf)
            return True
        return False
    except Exception as e:
        print(f"[LaMaBoxCleaner] Error writing {path}: {e}")
        return False

def get_sparkle_box_coords(h, w):
    """
    Computes exact bounding box for Google Flow / Gemini / Veo sparkle.
    Encapsulates the entire watermark in a solid box to prevent any star silhouette or ghosting.
    """
    s = w / 1376.0
    cx = w - 97.5 * s
    cy = h - 97.6 * s
    rad = 36.0 * s
    
    x0 = max(0, int(round(cx - rad)))
    y0 = max(0, int(round(cy - rad)))
    x1 = min(w, int(round(cx + rad)))
    y1 = min(h, int(round(cy + rad)))
    return (x0, y0, x1, y1), (cx, cy, s)

class LaMaBoxCleaner:
    def __init__(self, device="cpu"):
        self.device = device
        print(f"[LaMaBoxCleaner] Loading LaMa FFC Model on {device}...")
        self.model = ModelManager("lama", device=device)
        self.req = InpaintRequest()
        print("[LaMaBoxCleaner] Model ready.")

    def erase_mask(self, img_bgr, mask_uint8, padding=32, feather=6.0):
        """
        Generic localized tile crop & inpaint for any binary mask.
        """
        h, w = img_bgr.shape[:2]
        y_indices, x_indices = np.where(mask_uint8 > 0)
        if len(y_indices) == 0:
            print("[LaMaBoxCleaner] Warning: Mask is empty. Returning original.")
            return img_bgr.copy()
            
        x0 = max(0, int(np.min(x_indices)) - padding)
        y0 = max(0, int(np.min(y_indices)) - padding)
        x1 = min(w, int(np.max(x_indices)) + padding + 1)
        y1 = min(h, int(np.max(y_indices)) + padding + 1)
        
        tw = ((x1 - x0 + 7) // 8) * 8
        th = ((y1 - y0 + 7) // 8) * 8
        x1 = min(w, x0 + tw)
        y1 = min(h, y0 + th)
        tw, th = x1 - x0, y1 - y0
        
        crop_img = img_bgr[y0:y1, x0:x1]
        crop_mask = mask_uint8[y0:y1, x0:x1]
        
        crop_rgb = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
        result_bgr = self.model(crop_rgb, crop_mask, self.req)
        
        dist = cv2.distanceTransform(cv2.bitwise_not(crop_mask), cv2.DIST_L2, 3)
        alpha = np.clip(dist / feather, 0.0, 1.0)[:, :, None]
        blended_tile = (result_bgr * (1.0 - alpha) + crop_img * alpha).astype(np.uint8)
        
        final_img = img_bgr.copy()
        final_img[y0:y1, x0:x1] = blended_tile
        
        mod_px = np.sum(cv2.cvtColor(cv2.absdiff(crop_img, blended_tile), cv2.COLOR_BGR2GRAY) > 3)
        untouched_pct = (1.0 - mod_px / (w * h)) * 100.0
        print(f"[LaMaBoxCleaner] Tile: {tw}x{th}. Untouched canvas: {untouched_pct:.2f}% (modified {mod_px} px)")
        return final_img

    def erase_box(self, img_bgr, box_coords, padding=32, feather=6.0):
        """
        Executes Remover 1 solid box architecture:
        - Creates solid box mask inside the tile
        - Crops local tile around the box with padding
        - Runs LaMa FFC inpainting
        - Preserves native BGR format
        - Blends with Euclidean distance-transform boundary feathering
        - Re-composites onto untouched canvas
        """
        h, w = img_bgr.shape[:2]
        bx0, by0, bx1, by1 = box_coords
        
        mask = np.zeros((h, w), dtype=np.uint8)
        mask[by0:by1, bx0:bx1] = 255
        return self.erase_mask(img_bgr, mask, padding=padding, feather=feather)

    def erase_gemini_sparkle(self, img_bgr, padding=32, feather=6.0):
        """Erase Google Flow / Gemini / Veo sparkle using solid box encapsulation."""
        h, w = img_bgr.shape[:2]
        box_coords, _ = get_sparkle_box_coords(h, w)
        return self.erase_box(img_bgr, box_coords, padding=padding, feather=feather)

def main():
    parser = argparse.ArgumentParser(description="LaMa Box Cleaner (Dedicated Watermark Remover)")
    parser.add_argument("input", help="Input image file or directory")
    parser.add_argument("-o", "--output", help="Output image file or directory")
    parser.add_argument("--mode", choices=["gemini", "box", "mask"], default="gemini",
                        help="Mode: gemini (default bottom-right sparkle), box (bounding box), or mask (image file)")
    parser.add_argument("--box", help="Custom bounding box x0,y0,x1,y1 (e.g. 1242,634,1314,706 or 0.8,0.8,1.0,1.0)")
    parser.add_argument("--mask", help="Path to custom binary mask image file")
    parser.add_argument("--feather", type=float, default=6.0, help="Boundary feather radius (default: 6.0)")
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu", help="Compute device (default: cpu)")
    parser.add_argument("--quality", type=int, default=98, help="Output image quality (default: 98)")
    
    args = parser.parse_args()
    
    in_path = os.path.abspath(args.input)
    if not os.path.exists(in_path):
        print(f"Error: '{in_path}' does not exist.")
        sys.exit(1)
        
    cleaner = LaMaBoxCleaner(device=args.device)
    
    supported_exts = {".jpg", ".jpeg", ".png", ".webp"}
    if os.path.isdir(in_path):
        files = []
        for ext in supported_exts:
            files.extend(glob.glob(os.path.join(in_path, f"*{ext}")))
            files.extend(glob.glob(os.path.join(in_path, f"*{ext.upper()}")))
        files = sorted(list(set(files)))
        
        out_dir = os.path.abspath(args.output) if args.output else os.path.join(in_path, "lama_cleaned")
        os.makedirs(out_dir, exist_ok=True)
        
        print(f"Found {len(files)} image(s) to process.")
        for idx, f in enumerate(files, 1):
            fname = os.path.basename(f)
            out_file = os.path.join(out_dir, fname)
            print(f"\n[{idx}/{len(files)}] Processing: {fname}...")
            img = read_image_unicode(f)
            if img is None:
                continue
            cleaned = cleaner.erase_gemini_sparkle(img, feather=args.feather)
            write_image_unicode(out_file, cleaned, quality=args.quality)
            print(f"  -> Saved to: {out_file}")
    else:
        out_file = os.path.abspath(args.output) if args.output else in_path.replace(".jpg", "-cleaned.jpg").replace(".png", "-cleaned.png")
        img = read_image_unicode(in_path)
        if img is None:
            print("Failed to read image.")
            sys.exit(1)
            
        h, w = img.shape[:2]
        if args.mode == "gemini":
            cleaned = cleaner.erase_gemini_sparkle(img, feather=args.feather)
        elif args.mode == "box" and args.box:
            parts = [float(p.strip()) for p in args.box.split(",")]
            if all(0.0 <= p <= 1.0 for p in parts):
                bx0, by0, bx1, by1 = int(parts[0]*w), int(parts[1]*h), int(parts[2]*w), int(parts[3]*h)
            else:
                bx0, by0, bx1, by1 = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
            cleaned = cleaner.erase_box(img, (bx0, by0, bx1, by1), feather=args.feather)
        elif args.mode == "mask" and args.mask:
            m_img = read_image_unicode(args.mask)
            if m_img is not None:
                if len(m_img.shape) == 3:
                    m_img = cv2.cvtColor(m_img, cv2.COLOR_BGR2GRAY)
                cleaned = cleaner.erase_mask(img, m_img, feather=args.feather)
            else:
                print("Failed to read mask file.")
                sys.exit(1)
        else:
            cleaned = cleaner.erase_gemini_sparkle(img, feather=args.feather)
            
        write_image_unicode(out_file, cleaned, quality=args.quality)
        print(f"\n[LaMaBoxCleaner] Finished! Cleaned image saved to: {out_file}")

if __name__ == "__main__":
    main()
