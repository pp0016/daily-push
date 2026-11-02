import urllib.request
import re

bundle_url = "https://cdn.pixelbin.io/v2/dummy-cloudname/VtmFMH/original/bundle-a0659334433eb7df972c.js"
print("Downloading bundle...")
req = urllib.request.Request(bundle_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

print("Bundle size:", len(content))

# Look for patterns like .post( or fetch( or endpoints
endpoints = re.findall(r'["\']([a-zA-Z0-9_\-\./~:]*(?:prediction|upload|transformation|watermark)[a-zA-Z0-9_\-\./~:]*)["\']', content)
print("Unique endpoints/patterns found:", len(set(endpoints)))
for ep in sorted(set(endpoints)):
    if any(k in ep.lower() for k in ["/api", "/service", "prediction", "transform", "wm_"]):
        print(" ->", ep)

# Search for context around "watermark" or "remove"
print("\n--- SNIPPETS WITH 'removeWatermark' or similar ---")
for m in re.finditer(r'([a-zA-Z0-9_]{1,30}watermark[a-zA-Z0-9_]{0,30})', content, re.IGNORECASE):
    word = m.group(1)
    if word not in ["watermark", "watermarks", "Watermark", "Watermarks"]:
        start = max(0, m.start() - 100)
        end = min(len(content), m.end() + 100)
        # print first 5 unique
        pass

# Let's search for PixelBin transformation syntax: e.g. "wmark.remove" or "erase" or plugin names
plugins = re.findall(r'([a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+\([^)]*\))', content)
wm_plugins = [p for p in plugins if "watermark" in p.lower() or "text" in p.lower()]
print("\nPlugin calls found:")
for p in set(wm_plugins[:15]):
    print(" *", p)
