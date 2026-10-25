import cv2
import numpy as np
import os
import sys

# Load iopaint
from iopaint.model_manager import ModelManager
from iopaint.schema import InpaintRequest

def read_image_unicode(path):
    with open(path, "rb") as fp:
        data = fp.read()
    return cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

def write_image_unicode(path, img, quality=98):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    success, buf = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if success:
        with open(path, "wb") as fp:
            fp.write(buf)
        return True
    return False

def get_sparkle_box_coords(h, w):
    s = w / 1376.0
    cx = w - 97.5 * s
    cy = h - 97.6 * s
    rad = 36.0 * s
    
    x0 = max(0, int(round(cx - rad)))
    y0 = max(0, int(round(cy - rad)))
    x1 = min(w, int(round(cx + rad)))
    y1 = min(h, int(round(cy + rad)))
    return (x0, y0, x1, y1), (cx, cy, s)

# ==========================================
# REMOVER 1: Magic Studio LaMa Box Engine
# ==========================================
class Remover1_MagicStudioLaMa:
    """
    MagicStudio localized tile cropping with LaMa FFC inpainting on a solid box.
    Bug fix: Native BGR channel preservation (no channel swap) + Gaussian distance feathering.
    """
    def __init__(self, model, req):
        self.model = model
        self.req = req
        
    def process(self, img_bgr, padding=32, feather=6.0):
        h, w = img_bgr.shape[:2]
        (bx0, by0, bx1, by1), _ = get_sparkle_box_coords(h, w)
        
        # Local tile crop
        x0 = max(0, bx0 - padding)
        y0 = max(0, by0 - padding)
        x1 = min(w, bx1 + padding)
        y1 = min(h, by1 + padding)
        
        # Multiple of 8
        tw = ((x1 - x0 + 7) // 8) * 8
        th = ((y1 - y0 + 7) // 8) * 8
        x1 = min(w, x0 + tw)
        y1 = min(h, y0 + th)
        tw, th = x1 - x0, y1 - y0
        
        crop_img = img_bgr[y0:y1, x0:x1]
        
        # Box mask inside tile
        crop_mask = np.zeros((th, tw), dtype=np.uint8)
        mask_x0 = bx0 - x0
        mask_y0 = by0 - y0
        mask_x1 = bx1 - x0
        mask_y1 = by1 - y0
        crop_mask[mask_y0:mask_y1, mask_x0:mask_x1] = 255
        
        # Run LaMa (input RGB, output BGR)
        crop_rgb = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
        result_bgr = self.model(crop_rgb, crop_mask, self.req)
        
        # Distance-transform feathering
        dist = cv2.distanceTransform(cv2.bitwise_not(crop_mask), cv2.DIST_L2, 3)
        alpha = np.clip(dist / feather, 0.0, 1.0)[:, :, None]
        blended_tile = (result_bgr * (1.0 - alpha) + crop_img * alpha).astype(np.uint8)
        
        final_img = img_bgr.copy()
        final_img[y0:y1, x0:x1] = blended_tile
        return final_img

# ====================================================
# REMOVER 2: CIELAB-Harmonized LaMa Box Engine
# ====================================================
class Remover2_CIELABHarmonizedLaMa:
    """
    LaMa FFC on solid box + Reinhard CIELAB statistical color moment transfer
    matching the untouched surrounding collar's exact luminance and chromaticity.
    """
    def __init__(self, model, req):
        self.model = model
        self.req = req
        
    def process(self, img_bgr, padding=32, feather=6.0):
        h, w = img_bgr.shape[:2]
        (bx0, by0, bx1, by1), _ = get_sparkle_box_coords(h, w)
        
        x0 = max(0, bx0 - padding)
        y0 = max(0, by0 - padding)
        x1 = min(w, bx1 + padding)
        y1 = min(h, by1 + padding)
        
        tw = ((x1 - x0 + 7) // 8) * 8
        th = ((y1 - y0 + 7) // 8) * 8
        x1 = min(w, x0 + tw)
        y1 = min(h, y0 + th)
        tw, th = x1 - x0, y1 - y0
        
        crop_img = img_bgr[y0:y1, x0:x1]
        
        crop_mask = np.zeros((th, tw), dtype=np.uint8)
        mask_x0 = bx0 - x0
        mask_y0 = by0 - y0
        mask_x1 = bx1 - x0
        mask_y1 = by1 - y0
        crop_mask[mask_y0:mask_y1, mask_x0:mask_x1] = 255
        
        # Surrounding reference collar (untouched border of tile)
        ref_mask = np.zeros((th, tw), dtype=np.uint8)
        ref_mask[:8, :] = 255
        ref_mask[-8:, :] = 255
        ref_mask[:, :8] = 255
        ref_mask[:, -8:] = 255
        
        # Inpaint
        crop_rgb = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
        result_bgr = self.model(crop_rgb, crop_mask, self.req)
        
        # CIELAB Moment Matching
        res_lab = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
        ref_lab = cv2.cvtColor(crop_img, cv2.COLOR_BGR2LAB).astype(np.float32)
        
        inpaint_px = res_lab[crop_mask > 0]
        ref_px = ref_lab[ref_mask > 0]
        
        mu_ref, sig_ref = np.mean(ref_px, axis=0), np.std(ref_px, axis=0) + 1e-4
        mu_inp, sig_inp = np.mean(inpaint_px, axis=0), np.std(inpaint_px, axis=0) + 1e-4
        
        res_lab_corr = ((res_lab - mu_inp) / sig_inp) * sig_ref + mu_ref
        res_lab_corr = np.clip(res_lab_corr, 0, 255)
        
        m = (crop_mask.astype(np.float32) / 255.0)[:, :, None]
        res_lab_final = res_lab_corr * m + res_lab * (1.0 - m)
        harmonized_bgr = cv2.cvtColor(np.clip(res_lab_final, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
        
        # Feather
        dist = cv2.distanceTransform(cv2.bitwise_not(crop_mask), cv2.DIST_L2, 3)
        alpha = np.clip(dist / feather, 0.0, 1.0)[:, :, None]
        blended_tile = (harmonized_bgr * (1.0 - alpha) + crop_img * alpha).astype(np.uint8)
        
        final_img = img_bgr.copy()
        final_img[y0:y1, x0:x1] = blended_tile
        return final_img

# ===================================================================
# REMOVER 3: PhotoCraft / Seamless Poisson Clone Engine (Zero AI Drift)
# ===================================================================
class Remover3_PhotoCraftPoissonClone:
    """
    Photoshop / PhotoCraft Content-Aware style Poisson clone.
    Takes clean texture patches from the adjacent background, clones them seamlessly
    using Poisson partial differential equations. Zero AI color hallucination.
    """
    def process(self, img_bgr):
        h, w = img_bgr.shape[:2]
        (bx0, by0, bx1, by1), (cx, cy, s) = get_sparkle_box_coords(h, w)
        bw = bx1 - bx0
        bh = by1 - by0
        
        # Source patch: sample clean background directly to the left of the watermark
        src_x0 = max(0, bx0 - bw - 10)
        src_x1 = src_x0 + bw
        src_y0 = by0
        src_y1 = by1
        
        src_patch = img_bgr[src_y0:src_y1, src_x0:src_x1]
        
        # Destination center
        dest_center = (int((bx0 + bx1) / 2), int((by0 + by1) / 2))
        
        # Oval/smooth mask for seamless clone
        clone_mask = np.full((bh, bw), 255, dtype=np.uint8)
        clone_mask = cv2.copyMakeBorder(clone_mask[2:-2, 2:-2], 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=0)
        clone_mask = cv2.GaussianBlur(clone_mask, (5, 5), 0)
        
        try:
            # Poisson seamless clone (NORMAL_CLONE blends gradients with boundary color)
            cloned = cv2.seamlessClone(src_patch, img_bgr, clone_mask, dest_center, cv2.NORMAL_CLONE)
            return cloned
        except Exception as e:
            print(f"[Remover3] Fallback to Navier-Stokes: {e}")
            mask = np.zeros((h, w), dtype=np.uint8)
            mask[by0:by1, bx0:bx1] = 255
            return cv2.inpaint(img_bgr, mask, 5, cv2.INPAINT_NS)

print("All 3 removers defined successfully.")

if __name__ == "__main__":
    print("[Init] Loading LaMa Model for Removers 1 & 2...")
    model = ModelManager("lama", device="cpu")
    req = InpaintRequest()
    print("[Init] LaMa Model Ready.")
    
    r1 = Remover1_MagicStudioLaMa(model, req)
    r2 = Remover2_CIELABHarmonizedLaMa(model, req)
    r3 = Remover3_PhotoCraftPoissonClone()
    
    target_files = [
        r"C:\Users\renu5\Downloads\Oct 24 - 23_36\Coworkers_in_underground_parking…_20261025035921.jpg",
        r"C:\Users\renu5\Downloads\Oct 24 - 23_36\Driver_turning_car_into_parking_20261025035921.jpg",
        r"C:\Users\renu5\Downloads\Oct 24 - 23_36\Driver_view_inside_car_cabin_20261025035921.jpg",
        r"C:\Users\renu5\Downloads\Oct 24 - 23_36\Driving_car_in_underground_parking_20261025035921.jpg"
    ]
    
    base_out = r"C:\Users\renu5\Downloads\Oct 24 - 23_36"
    dir_r1 = os.path.join(base_out, "remover_1_lama_box")
    dir_r2 = os.path.join(base_out, "remover_2_cielab_box")
    dir_r3 = os.path.join(base_out, "remover_3_photocraft_blend")
    
    prev_dir = r"C:\Users\renu5\.gemini\antigravity\brain\68db6e82-6ec9-4f47-a039-6e7cc2557d48\three_removers_previews"
    os.makedirs(prev_dir, exist_ok=True)
    
    for idx, f in enumerate(target_files, 1):
        fname = os.path.basename(f)
        print(f"\n==========================================")
        print(f"[{idx}/4] Processing: {fname}")
        print(f"==========================================")
        
        orig = read_image_unicode(f)
        if orig is None:
            print(f"Failed to read: {f}")
            continue
            
        h, w = orig.shape[:2]
        s = w / 1376.0
        cx = int(round(w - 97.5 * s))
        cy = int(round(h - 97.6 * s))
        rad = 50
        crop_orig = orig[cy-rad:cy+rad, cx-rad:cx+rad]
        cv2.imwrite(os.path.join(prev_dir, f"orig_{idx}.jpg"), crop_orig)
        
        # --- Run Remover 1 ---
        print("  Running Remover 1 (MagicStudio LaMa Box)...")
        res1 = r1.process(orig)
        write_image_unicode(os.path.join(dir_r1, fname), res1)
        crop_r1 = res1[cy-rad:cy+rad, cx-rad:cx+rad]
        cv2.imwrite(os.path.join(prev_dir, f"r1_{idx}.jpg"), crop_r1)
        
        # --- Run Remover 2 ---
        print("  Running Remover 2 (CIELAB-Harmonized LaMa Box)...")
        res2 = r2.process(orig)
        write_image_unicode(os.path.join(dir_r2, fname), res2)
        crop_r2 = res2[cy-rad:cy+rad, cx-rad:cx+rad]
        cv2.imwrite(os.path.join(prev_dir, f"r2_{idx}.jpg"), crop_r2)
        
        # --- Run Remover 3 ---
        print("  Running Remover 3 (PhotoCraft Seamless Poisson Box)...")
        res3 = r3.process(orig)
        write_image_unicode(os.path.join(dir_r3, fname), res3)
        crop_r3 = res3[cy-rad:cy+rad, cx-rad:cx+rad]
        cv2.imwrite(os.path.join(prev_dir, f"r3_{idx}.jpg"), crop_r3)
        
        # Create 4-panel comparison strip: Orig | R1 | R2 | R3
        divider = np.full((crop_orig.shape[0], 3, 3), [0, 255, 0], dtype=np.uint8)
        comp_strip = np.hstack([crop_orig, divider, crop_r1, divider, crop_r2, divider, crop_r3])
        cv2.imwrite(os.path.join(prev_dir, f"comp_strip_{idx}.jpg"), comp_strip)
        print(f"  Comparison strip saved: comp_strip_{idx}.jpg")
        
    print("\n[Done] All 3 Removers finished on all 4 images successfully!")
