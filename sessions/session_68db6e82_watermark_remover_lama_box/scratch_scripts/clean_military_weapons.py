import os
import cv2
import sys

# Import our active skill engine
sys.path.append(r"C:\Users\renu5\.gemini\config\skills\watermark-remover-lama-box-cleaner\scripts")
from lama_box_cleaner import LaMaBoxCleaner, read_image_unicode, write_image_unicode

def main():
    folder = r"C:\Users\renu5\Downloads\watermark_mark_removers"
    out_dir = os.path.join(folder, "clean")
    os.makedirs(out_dir, exist_ok=True)
    
    files = [
        r"Nuclear_warhead_and_bullet_compa…_202608201544.jpeg",
        r"Six_banned_military_weapons_disp…_202608201544.jpeg",
        r"Classified_military_weapons_inve…_202608201544.jpeg"
    ]
    
    print("[Batch] Initializing LaMaBoxCleaner...")
    cleaner = LaMaBoxCleaner(device="cpu")
    print("[Batch] Model loaded. Processing 3 images concurrently...")
    
    for idx, f in enumerate(files, 1):
        in_path = os.path.join(folder, f)
        out_path = os.path.join(out_dir, f)
        
        print(f"\n[{idx}/3] Processing: {f}...")
        img = read_image_unicode(in_path)
        if img is None:
            print(f"Error reading {in_path}")
            continue
            
        cleaned = cleaner.erase_gemini_sparkle(img, padding=32, feather=6.0)
        write_image_unicode(out_path, cleaned, quality=98)
        print(f"  -> Successfully cleaned and saved to: {out_path}")
        
    print("\n[Complete] All 3 images processed successfully!")

if __name__ == "__main__":
    main()
