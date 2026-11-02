import cv2
import numpy as np
import os
import sys

from iopaint.model_manager import ModelManager
from iopaint.schema import InpaintRequest

def magic_eraser_clone(image_path, mask_uint8, output_path, padding=32, device="cpu"):
    """
    Clones MagicStudio MagicEraser architecture:
    1. Finds bounding box of the mask.
    2. Crops image & mask to [ymin-pad:ymax+pad, xmin-pad:xmax+pad] (crop_coords).
    3. Runs LaMa FFC on ONLY the cropped patch.
    4. Pastes the inpainted patch back onto the 100% original high-res canvas at crop_coords.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image from {image_path}")
        
    h, w = img.shape[:2]
    
    # Find bounding box of mask
    y_indices, x_indices = np.where(mask_uint8 > 0)
    if len(y_indices) == 0:
        print("Warning: mask is empty, nothing to erase.")
        cv2.imwrite(output_path, img)
        return True
        
    x0 = max(0, int(np.min(x_indices)) - padding)
    y0 = max(0, int(np.min(y_indices)) - padding)
    x1 = min(w, int(np.max(x_indices)) + padding + 1)
    y1 = min(h, int(np.max(y_indices)) + padding + 1)
    
    # Snap to multiple of 8 for neural network efficiency
    tw = ((x1 - x0 + 7) // 8) * 8
    th = ((y1 - y0 + 7) // 8) * 8
    x1 = min(w, x0 + tw)
    y1 = min(h, y0 + th)
    tw = x1 - x0
    th = y1 - y0
    
    crop_coords = [x0, y0]
    print(f"[MagicEraser Clone] Cropping region: [{x0}, {y0}] to [{x1}, {y1}] (Tile: {tw}x{th})")
    print(f"[MagicEraser Clone] Canvas untouched: {(1 - (tw*th)/(w*h))*100:.2f}%")
    
    crop_img = img[y0:y1, x0:x1]
    crop_mask = mask_uint8[y0:y1, x0:x1]
    
    # Load model
    print("[MagicEraser Clone] Running LaMa FFC inpainting on crop...")
    model = ModelManager("lama", device=device)
    req = InpaintRequest()
    
    crop_rgb = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
    result_rgb = model(crop_rgb, crop_mask, req)
    result_bgr = cv2.cvtColor(result_rgb, cv2.COLOR_RGB2BGR)
    
    # Seamless edge feathering into original image
    dist = cv2.distanceTransform(cv2.bitwise_not(crop_mask), cv2.DIST_L2, 3)
    feather_band = 4.0
    alpha = np.clip(dist / feather_band, 0.0, 1.0)[:, :, None]
    
    blended_patch = (result_bgr * (1.0 - alpha) + crop_img * alpha).astype(np.uint8)
    
    # Exact Magic Studio Client-Side Canvas Assembly:
    # Original image is preserved 100%, patch drawn back at crop_coords
    final_img = img.copy()
    final_img[y0:y1, x0:x1] = blended_patch
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cv2.imwrite(output_path, final_img, [int(cv2.IMWRITE_JPEG_QUALITY), 98])
    print(f"[MagicEraser Clone] Saved result to: {output_path}")
    return True

if __name__ == "__main__":
    # Test on Coffee cup image with Gemini sparkle coordinates
    in_img = r"C:\Users\renu5\Downloads\Oct 24 - 23_36\Coffee_cup_in_car_console_20261025035921.jpg"
    out_img = r"C:\Users\renu5\.gemini\antigravity\brain\68db6e82-6ec9-4f47-a039-6e7cc2557d48\scratch\magic_eraser_test_output.jpg"
    
    # Generate mask for bottom right sparkle
    im = cv2.imread(in_img)
    h, w = im.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    # sparkle box: 1242, 634, 72, 72
    mask[634:634+72, 1242:1242+72] = 255
    
    magic_eraser_clone(in_img, mask, out_img)
