import cv2
import numpy as np
import os
import sys

# Add magic-eraser skill path
sys.path.insert(0, r"C:\Users\renu5\.gemini\config\skills\magic-eraser\scripts")
from magic_eraser import MagicEraserClone

artifact_dir = r"C:\Users\renu5\.gemini\antigravity\brain\68db6e82-6ec9-4f47-a039-6e7cc2557d48"
in_dir = r"C:\Users\renu5\Downloads\Oct 24 - 23_36"
out_dir = r"C:\Users\renu5\Downloads\Oct 24 - 23_36\magic_eraser_results"
preview_dir = os.path.join(artifact_dir, "previews")
os.makedirs(out_dir, exist_ok=True)
os.makedirs(preview_dir, exist_ok=True)

# Targets
target_names = [
    "Coworkers_in_underground_parking",
    "Driver_turning_car_into_parking",
    "Driver_view_inside_car_cabin",
    "Driving_car_in_underground_parking"
]

all_files = os.listdir(in_dir)
matched_targets = []
for kw in target_names:
    for f in all_files:
        if kw in f and f.endswith(".jpg"):
            matched_targets.append(os.path.join(in_dir, f))
            break

print(f"Matched {len(matched_targets)} files:")
for t in matched_targets:
    print(" -", os.path.basename(t))

eraser = MagicEraserClone(device="cpu")

results = []

for idx, in_path in enumerate(matched_targets, 1):
    fname = os.path.basename(in_path)
    base_name = f"image_{idx}"
    out_path = os.path.join(out_dir, fname)
    
    print(f"\n[{idx}/{len(matched_targets)}] Processing: {fname}...")
    
    # Read with unicode support
    with open(in_path, "rb") as fp:
        raw_bytes = np.frombuffer(fp.read(), dtype=np.uint8)
        img = cv2.imdecode(raw_bytes, cv2.IMREAD_COLOR)
        
    if img is None:
        print(f"Failed to decode: {fname}")
        continue
        
    cleaned = eraser.erase_gemini_sparkle(img)
    
    # Save full cleaned image with unicode support
    _, enc = cv2.imencode(".jpg", cleaned, [int(cv2.IMWRITE_JPEG_QUALITY), 98])
    with open(out_path, "wb") as fp:
        fp.write(enc)
    print(f"  -> Saved full cleaned image to: {out_path}")
    
    # Generate 200x200 zoom crop around watermark area
    # Watermark box center: (1278, 670)
    h, w = img.shape[:2]
    cx, cy = int(w - 97.5), int(h - 97.6)
    rad = 100
    y0, y1 = max(0, cy - rad), min(h, cy + rad)
    x0, x1 = max(0, cx - rad), min(w, cx + rad)
    
    crop_before = img[y0:y1, x0:x1]
    crop_after = cleaned[y0:y1, x0:x1]
    
    # Create side-by-side comparison image: Before | After
    # Add label header
    header_h = 30
    comp_w = crop_before.shape[1] * 2 + 10
    comp_h = crop_before.shape[0] + header_h
    comp = np.zeros((comp_h, comp_w, 3), dtype=np.uint8) + 30 # dark background
    
    # Place crops
    comp[header_h:, :crop_before.shape[1]] = crop_before
    comp[header_h:, crop_before.shape[1]+10:] = crop_after
    
    # Add text labels
    cv2.putText(comp, "BEFORE (Watermark)", (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (100, 100, 255), 1, cv2.LINE_AA)
    cv2.putText(comp, "AFTER (Magic Eraser)", (crop_before.shape[1] + 25, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (100, 255, 100), 1, cv2.LINE_AA)
    
    comp_filename = f"preview_comp_{idx}.jpg"
    comp_path = os.path.join(preview_dir, comp_filename)
    cv2.imwrite(comp_path, comp, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    
    # Also save separate before and after crops
    before_filename = f"crop_before_{idx}.jpg"
    after_filename = f"crop_after_{idx}.jpg"
    cv2.imwrite(os.path.join(preview_dir, before_filename), crop_before)
    cv2.imwrite(os.path.join(preview_dir, after_filename), crop_after)
    
    # Compute metrics
    diff = cv2.absdiff(img, cleaned)
    changed = (diff > 5).any(axis=2).sum()
    total = h * w
    untouched_pct = (1.0 - changed / total) * 100.0
    
    results.append({
        "index": idx,
        "filename": fname,
        "out_path": out_path,
        "comp_path": comp_path,
        "before_path": os.path.join(preview_dir, before_filename),
        "after_path": os.path.join(preview_dir, after_filename),
        "changed_px": changed,
        "total_px": total,
        "untouched_pct": untouched_pct
    })

print("\n--- SUMMARY REPORT ---")
for r in results:
    print(f"[{r['index']}] {r['filename'][:30]}...: Untouched: {r['untouched_pct']:.2f}%, Saved: {r['out_path']}")
