import subprocess
import os
import json

cli = r"C:\Users\renu5\.gemini\config\skills\photocraft\bin\photocraft-0.15.1-windows-x64-portable\photocraft-cli.exe"
in_dir = r"C:\Users\renu5\Downloads\Oct 24 - 23_36"
out_dir = r"C:\Users\renu5\Downloads\Oct 24 - 23_36\photocraft_cleaned_results"
os.makedirs(out_dir, exist_ok=True)

target_keywords = [
    "Coworkers_in_underground_parking",
    "Driver_turning_car_into_parking",
    "Driver_view_inside_car_cabin",
    "Driving_car_in_underground_parking"
]

all_files = os.listdir(in_dir)
targets = []
for kw in target_keywords:
    for f in all_files:
        if kw in f and f.endswith(".jpg"):
            targets.append(os.path.join(in_dir, f))
            break

print(f"Found {len(targets)} targets:")
for t in targets:
    print(" -", os.path.basename(t))

# Gemini sparkle box at 1376x768:
# x: 1242, y: 634, width: 72, height: 72
for idx, in_file in enumerate(targets, 1):
    fname = os.path.basename(in_file)
    out_file = os.path.join(out_dir, fname)
    print(f"\n[{idx}/{len(targets)}] Running PhotoCraft on: {fname}...")
    
    cmd = [
        cli, "run", in_file,
        "--cmd", "select.rect",
        "--params", json.dumps({"x": 1242, "y": 634, "width": 72, "height": 72, "feather": 2}),
        "--cmd", "edit.deleteAndFillSelection",
        "--cmd", "select.deselect",
        "--out", out_file,
        "--quality", "98"
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode == 0 and os.path.exists(out_file):
        print(f"  -> SUCCESS! Output saved to: {out_file}")
    else:
        print(f"  -> Failed (code {res.returncode}):", res.stderr.decode('utf-8', errors='ignore'))

print("\nFinished processing all 4 images with PhotoCraft!")
