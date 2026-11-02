import cv2
import numpy as np
import base64
import os
import sys

# Load iopaint
from iopaint.model_manager import ModelManager
from iopaint.schema import InpaintRequest

def get_star_alpha(h, w):
    WEDGE_B64 = "paWlpaWlpaWlpaWlpaWmpaWlpaampaWlpaampqampKWlpqanp6WkpqWmpqempqalpaalpaWWYKinpqSlpaWcaCQAp6akpKWkn3QwAAAApaSjpKWkfzcQAAAAAJ+goqKjjUgQAAAAAAAAnJ6goJlfGAAAAAAAAAAAoqGhoHkvAAAAAAAAAAAAAKCho5JOEQAAAAAAAAAAAAAAnJ+icyUAAAAAAAAAAAAAAAAAnqCWTQAAAAAAAAAAAAAAAAAAAKGjeywAAAAAAAAAAAAAAAAAAAAAop5cEgAAAAAAAAAAAAAAAAAAAAAAoYw/AAAAAAAAAAAAAAAAAAAAAAAAAJ9yJgAAAAAAAAAAAAAAAAAAAAAAAAAAlVkRAAAAAAAAAAAAAAAAAAAAAAAAAAAATSoA"
    wedge_bytes = base64.b64decode(WEDGE_B64)
    star = np.zeros((65, 65), dtype=np.float32)
    for j in range(65):
        for i in range(65):
            dx, dy = abs(i - 32), abs(j - 32)
            mx, mn = max(dx, dy), min(dx, dy)
            idx = int(mx * (mx + 1) / 2 + mn)
            val = wedge_bytes[idx] if idx < len(wedge_bytes) else 0
            star[j, i] = (val / 255.0)
    
    s = w / 1376.0
    cx = w - 97.5 * s
    cy = h - 97.6 * s
    
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u = (xx - cx) / s + 32.0
    v = (yy - cy) / s + 32.0
    
    u0 = np.clip(np.floor(u).astype(np.int32), 0, 64)
    v0 = np.clip(np.floor(v).astype(np.int32), 0, 64)
    u1 = np.clip(u0 + 1, 0, 64)
    v1 = np.clip(v0 + 1, 0, 64)
    du = u - u0
    dv = v - v0
    
    oob = (u < 0) | (u > 64) | (v < 0) | (v > 64)
    a = (star[v0, u0]*(1-du) + star[v0, u1]*du)*(1-dv) + (star[v1, u0]*(1-du) + star[v1, u1]*du)*dv
    a = np.where(oob, 0.0, a)
    return a, (cx, cy, s)

def harmonize_color_cielab(patch_bgr, mask_uint8, surround_mask_uint8):
    """
    Transfers CIELAB color moments (mean and std) from the surrounding untouched border
    to the inpainted patch, eliminating any hue, saturation, or luminance drift.
    """
    if np.sum(mask_uint8 > 0) == 0 or np.sum(surround_mask_uint8 > 0) == 0:
        return patch_bgr
        
    patch_lab = cv2.cvtColor(patch_bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    
    surround_pixels = patch_lab[surround_mask_uint8 > 0]
    inpaint_pixels = patch_lab[mask_uint8 > 0]
    
    mu_target = np.mean(surround_pixels, axis=0)
    sigma_target = np.std(surround_pixels, axis=0) + 1e-5
    
    mu_inpaint = np.mean(inpaint_pixels, axis=0)
    sigma_inpaint = np.std(inpaint_pixels, axis=0) + 1e-5
    
    # Reinhard color transfer on inpainted region
    result_lab = patch_lab.copy()
    corrected = ((patch_lab - mu_inpaint) / sigma_inpaint) * sigma_target + mu_target
    corrected = np.clip(corrected, 0, 255)
    
    # Apply only to masked pixels with smooth feathering
    m_norm = (mask_uint8.astype(np.float32) / 255.0)[:, :, None]
    result_lab = corrected * m_norm + patch_lab * (1.0 - m_norm)
    
    result_bgr = cv2.cvtColor(np.clip(result_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    return result_bgr

class ZeroDiscolorationEraser:
    def __init__(self, device="cpu"):
        print(f"[Init] Loading LaMa model on {device}...")
        self.model = ModelManager("lama", device=device)
        self.req = InpaintRequest()
        print("[Init] Model ready.")

    def erase_gemini_sparkle(self, img_bgr, dilate_px=2, padding=32, feather=3.0):
        h, w = img_bgr.shape[:2]
        
        # 1. Compute exact continuous alpha map of Gemini sparkle
        alpha_map, (cx, cy, s) = get_star_alpha(h, w)
        
        # 2. Binary star mask (star silhouette only, NOT a square box!)
        star_mask = np.zeros((h, w), dtype=np.uint8)
        star_mask[alpha_map > 0.025] = 255
        if dilate_px > 0:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_px * 2 + 1, dilate_px * 2 + 1))
            star_mask = cv2.dilate(star_mask, kernel, iterations=1)
            
        y_indices, x_indices = np.where(star_mask > 0)
        if len(y_indices) == 0:
            return img_bgr.copy()
            
        # 3. Local tile crop bounding box with padding
        x0 = max(0, int(np.min(x_indices)) - padding)
        y0 = max(0, int(np.min(y_indices)) - padding)
        x1 = min(w, int(np.max(x_indices)) + padding + 1)
        y1 = min(h, int(np.max(y_indices)) + padding + 1)
        
        # Snap dimensions to multiple of 8 for LaMa FFC
        tw = ((x1 - x0 + 7) // 8) * 8
        th = ((y1 - y0 + 7) // 8) * 8
        x1 = min(w, x0 + tw)
        y1 = min(h, y0 + th)
        tw = x1 - x0
        th = y1 - y0
        
        crop_img = img_bgr[y0:y1, x0:x1]
        crop_mask = star_mask[y0:y1, x0:x1]
        
        # 4. Define surrounding reference collar (pixels inside tile that are clean and NOT masked)
        # Dilate mask by 12px to define an exclusion zone around the star
        exclusion = cv2.dilate(crop_mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25)), iterations=1)
        surround_mask = np.zeros((th, tw), dtype=np.uint8)
        surround_mask[exclusion == 0] = 255
        
        # If surrounding reference is too small, fallback to tile perimeter
        if np.sum(surround_mask > 0) < 100:
            surround_mask[:8, :] = 255
            surround_mask[-8:, :] = 255
            surround_mask[:, :8] = 255
            surround_mask[:, -8:] = 255
            
        # 5. Run LaMa strictly on tile
        crop_rgb = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
        result_rgb = self.model(crop_rgb, crop_mask, self.req)
        result_bgr = cv2.cvtColor(result_rgb, cv2.COLOR_RGB2BGR)
        
        # 6. CIELAB Color Harmonization: lock mean and std of L*, a*, b* to surrounding background
        harmonized_bgr = harmonize_color_cielab(result_bgr, crop_mask, surround_mask)
        
        # 7. Distance-transform seamless edge feathering
        dist = cv2.distanceTransform(cv2.bitwise_not(crop_mask), cv2.DIST_L2, 3)
        alpha_feather = np.clip(dist / feather, 0.0, 1.0)[:, :, None]
        blended_tile = (harmonized_bgr * (1.0 - alpha_feather) + crop_img * alpha_feather).astype(np.uint8)
        
        # 8. Re-insert onto 100% untouched canvas
        final_img = img_bgr.copy()
        final_img[y0:y1, x0:x1] = blended_tile
        
        # Compute stats
        diff = cv2.absdiff(crop_img, blended_tile)
        mod_px = np.sum(cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) > 3)
        total_px = w * h
        canvas_untouched = (1.0 - mod_px / total_px) * 100.0
        
        return final_img, (x0, y0, tw, th), canvas_untouched

if __name__ == "__main__":
    eraser = ZeroDiscolorationEraser(device="cpu")
    
    test_files = [
        r"C:\Users\renu5\Downloads\Oct 24 - 23_36\Driver_view_inside_car_cabin_20261025035921.jpg",
        r"C:\Users\renu5\Downloads\Oct 24 - 23_36\Driving_car_in_underground_parking_20261025035921.jpg"
    ]
    
    out_dir = r"C:\Users\renu5\Downloads\Oct 24 - 23_36\zero_color_shift_test"
    os.makedirs(out_dir, exist_ok=True)
    
    for p in test_files:
        fname = os.path.basename(p)
        print(f"\nProcessing: {fname}...")
        with open(p, "rb") as fp:
            img = cv2.imdecode(np.frombuffer(fp.read(), np.uint8), cv2.IMREAD_COLOR)
            
        clean_img, crop_box, untouched = eraser.erase_gemini_sparkle(img)
        
        out_p = os.path.join(out_dir, fname)
        _, buf = cv2.imencode(".jpg", clean_img, [int(cv2.IMWRITE_JPEG_QUALITY), 98])
        with open(out_p, "wb") as fp:
            fp.write(buf)
            
        print(f"  Saved to: {out_p}")
        print(f"  Canvas untouched: {untouched:.2f}%")
        
        # Inspect colors of the watermark center
        h, w = img.shape[:2]
        s = w / 1376.0
        cx = int(round(w - 97.5 * s))
        cy = int(round(h - 97.6 * s))
        
        patch_clean = clean_img[cy-20:cy+20, cx-20:cx+20]
        surround_ring = clean_img[cy-60:cy+60, cx-60:cx-30] # clean region to the left
        
        lab_clean = cv2.cvtColor(patch_clean, cv2.COLOR_BGR2LAB).mean(axis=(0,1))
        lab_surround = cv2.cvtColor(surround_ring, cv2.COLOR_BGR2LAB).mean(axis=(0,1))
        
        delta_E = np.sqrt(np.sum((lab_clean - lab_surround)**2))
        print(f"  Clean Patch LAB: L={lab_clean[0]:.2f}, A={lab_clean[1]:.2f}, B={lab_clean[2]:.2f}")
        print(f"  Surround    LAB: L={lab_surround[0]:.2f}, A={lab_surround[1]:.2f}, B={lab_surround[2]:.2f}")
        print(f"  Delta E (color difference): {delta_E:.2f}")
