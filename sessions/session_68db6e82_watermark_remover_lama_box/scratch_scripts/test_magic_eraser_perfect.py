import cv2
import numpy as np
import base64
import os
import sys
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
        print(f"Error reading {path}: {e}")
        return None

def write_image_unicode(path, img, quality=98):
    """Safely writes images with Unicode characters on Windows."""
    try:
        ext = os.path.splitext(path)[1].lower()
        if ext in [".jpg", ".jpeg"]:
            params = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        elif ext == ".png":
            params = [int(cv2.IMWRITE_PNG_COMPRESSION), 3]
        else:
            params = []
            
        success, buf = cv2.imencode(ext if ext else ".jpg", img, params)
        if success:
            with open(path, "wb") as fp:
                fp.write(buf)
            return True
        return False
    except Exception as e:
        print(f"Error writing {path}: {e}")
        return False

def get_gemini_star_alpha(h, w):
    """
    Synthesizes the exact continuous alpha map of Google Flow / Gemini / Veo sparkle
    using Google's native 65x65 octant wedge distance table with sub-pixel bilinear sampling.
    """
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

def harmonize_cielab(patch_bgr, mask_uint8, reference_bgr, ref_mask_uint8):
    """
    Harmonizes CIELAB color distribution of the inpainted patch to match
    the exact mean and standard deviation of the untouched surrounding background.
    Eliminates all color cast, brownish tint, or luminance shifts.
    """
    if np.sum(mask_uint8 > 0) == 0 or np.sum(ref_mask_uint8 > 0) == 0:
        return patch_bgr
        
    patch_lab = cv2.cvtColor(patch_bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    ref_lab = cv2.cvtColor(reference_bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    
    ref_pixels = ref_lab[ref_mask_uint8 > 0]
    inpaint_pixels = patch_lab[mask_uint8 > 0]
    
    mu_ref = np.mean(ref_pixels, axis=0)
    sigma_ref = np.std(ref_pixels, axis=0) + 1e-4
    
    mu_inp = np.mean(inpaint_pixels, axis=0)
    sigma_inp = np.std(inpaint_pixels, axis=0) + 1e-4
    
    # Reinhard color moment transfer
    normalized = (patch_lab - mu_inp) / sigma_inp
    harmonized = normalized * sigma_ref + mu_ref
    harmonized = np.clip(harmonized, 0, 255)
    
    # Apply strictly to masked region
    m = (mask_uint8.astype(np.float32) / 255.0)[:, :, None]
    final_lab = harmonized * m + patch_lab * (1.0 - m)
    
    final_bgr = cv2.cvtColor(np.clip(final_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    return final_bgr

class MagicEraserEngine:
    def __init__(self, device="cpu"):
        print(f"[MagicEraser] Initializing LaMa FFC Model on {device}...")
        self.model = ModelManager("lama", device=device)
        self.req = InpaintRequest()
        print("[MagicEraser] Engine ready.")

    def erase(self, img_bgr, mask_uint8, padding=32, feather=3.0, harmonize=True):
        h, w = img_bgr.shape[:2]
        
        y_indices, x_indices = np.where(mask_uint8 > 0)
        if len(y_indices) == 0:
            print("[MagicEraser] Warning: Empty mask, returning original.")
            return img_bgr.copy()
            
        x0 = max(0, int(np.min(x_indices)) - padding)
        y0 = max(0, int(np.min(y_indices)) - padding)
        x1 = min(w, int(np.max(x_indices)) + padding + 1)
        y1 = min(h, int(np.max(y_indices)) + padding + 1)
        
        # Dimensions multiple of 8
        tw = ((x1 - x0 + 7) // 8) * 8
        th = ((y1 - y0 + 7) // 8) * 8
        x1 = min(w, x0 + tw)
        y1 = min(h, y0 + th)
        tw = x1 - x0
        th = y1 - y0
        
        crop_coords = (x0, y0)
        crop_img = img_bgr[y0:y1, x0:x1]
        crop_mask = mask_uint8[y0:y1, x0:x1]
        
        # Clean background collar (pixels inside tile not touched by the mask or its 10px dilation)
        exclusion = cv2.dilate(crop_mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)), iterations=1)
        ref_mask = np.zeros((th, tw), dtype=np.uint8)
        ref_mask[exclusion == 0] = 255
        if np.sum(ref_mask > 0) < 50:
            ref_mask[:6, :] = 255
            ref_mask[-6:, :] = 255
            ref_mask[:, :6] = 255
            ref_mask[:, -6:] = 255
            
        # Model input: RGB
        crop_rgb = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
        
        # CRITICAL FIX: iopaint's ModelManager returns BGR directly!
        result_bgr = self.model(crop_rgb, crop_mask, self.req)
        
        # Color harmonization against untouched surrounding collar
        if harmonize:
            result_bgr = harmonize_cielab(result_bgr, crop_mask, crop_img, ref_mask)
            
        # Edge feathering
        dist = cv2.distanceTransform(cv2.bitwise_not(crop_mask), cv2.DIST_L2, 3)
        alpha_feather = np.clip(dist / feather, 0.0, 1.0)[:, :, None]
        blended_tile = (result_bgr * (1.0 - alpha_feather) + crop_img * alpha_feather).astype(np.uint8)
        
        # Re-composite onto untouched canvas
        final_img = img_bgr.copy()
        final_img[y0:y1, x0:x1] = blended_tile
        
        # Stats
        mod_px = np.sum(cv2.cvtColor(cv2.absdiff(crop_img, blended_tile), cv2.COLOR_BGR2GRAY) > 3)
        untouched_pct = (1.0 - mod_px / (w * h)) * 100.0
        print(f"[MagicEraser] Tile: {tw}x{th} at {crop_coords}. Canvas untouched: {untouched_pct:.3f}% (modified {mod_px} px)")
        return final_img

    def erase_gemini_sparkle(self, img_bgr, dilate_px=2):
        """
        Generates procedural star silhouette mask for Google Flow / Gemini / Veo sparkle.
        Masks ONLY the thin star rays with 2px dilation (1,300 px), NEVER a solid box (5,184 px).
        """
        h, w = img_bgr.shape[:2]
        alpha_map, (cx, cy, s) = get_gemini_star_alpha(h, w)
        
        star_mask = np.zeros((h, w), dtype=np.uint8)
        star_mask[alpha_map > 0.025] = 255
        if dilate_px > 0:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_px * 2 + 1, dilate_px * 2 + 1))
            star_mask = cv2.dilate(star_mask, kernel, iterations=1)
            
        return self.erase(img_bgr, star_mask, padding=int(round(32 * s)), feather=3.0, harmonize=True)

if __name__ == "__main__":
    engine = MagicEraserEngine(device="cpu")
    
    target_files = [
        r"C:\Users\renu5\Downloads\Oct 24 - 23_36\Coworkers_in_underground_parking…_20261025035921.jpg",
        r"C:\Users\renu5\Downloads\Oct 24 - 23_36\Driver_turning_car_into_parking_20261025035921.jpg",
        r"C:\Users\renu5\Downloads\Oct 24 - 23_36\Driver_view_inside_car_cabin_20261025035921.jpg",
        r"C:\Users\renu5\Downloads\Oct 24 - 23_36\Driving_car_in_underground_parking_20261025035921.jpg"
    ]
    
    out_dir = r"C:\Users\renu5\Downloads\Oct 24 - 23_36\magic_eraser_results"
    os.makedirs(out_dir, exist_ok=True)
    
    print("\n--- Running Zero-Discoloration Trial on 4 Target Images ---")
    for idx, f in enumerate(target_files, 1):
        fname = os.path.basename(f)
        out_file = os.path.join(out_dir, fname)
        print(f"\n[{idx}/4] Processing: {fname}")
        
        img = read_image_unicode(f)
        if img is None:
            print(f"Error reading {f}")
            continue
            
        cleaned = engine.erase_gemini_sparkle(img)
        write_image_unicode(out_file, cleaned, quality=98)
        print(f"  -> Successfully saved: {out_file}")
        
        # Color consistency verification
        h, w = img.shape[:2]
        s = w / 1376.0
        cx = int(round(w - 97.5 * s))
        cy = int(round(h - 97.6 * s))
        
        patch_clean = cleaned[cy-15:cy+15, cx-15:cx+15]
        collar_left = cleaned[cy-35:cy+35, cx-55:cx-25]
        
        lab_clean = cv2.cvtColor(patch_clean, cv2.COLOR_BGR2LAB).mean(axis=(0,1))
        lab_collar = cv2.cvtColor(collar_left, cv2.COLOR_BGR2LAB).mean(axis=(0,1))
        delta_E = np.sqrt(np.sum((lab_clean - lab_collar)**2))
        
        bgr_clean = patch_clean.mean(axis=(0,1))
        bgr_collar = collar_left.mean(axis=(0,1))
        
        print(f"  Collar BGR: [B={bgr_collar[0]:.1f}, G={bgr_collar[1]:.1f}, R={bgr_collar[2]:.1f}]")
        print(f"  Patch  BGR: [B={bgr_clean[0]:.1f}, G={bgr_clean[1]:.1f}, R={bgr_clean[2]:.1f}]")
        print(f"  Delta E: {delta_E:.2f} (Delta E < 2.0 = imperceptible color difference)")
