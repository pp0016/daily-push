import urllib.request
import re

bundle_url = "https://cdn.pixelbin.io/v2/dummy-cloudname/VtmFMH/original/bundle-a0659334433eb7df972c.js"
req = urllib.request.Request(bundle_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

for term in ["verifyUploadedObject", "getUploadUrl", "predictionId"]:
    for m in re.finditer(re.escape(term), content):
        start = max(0, m.start() - 300)
        end = min(len(content), m.end() + 300)
        print(f"=== MATCH FOR {term} ===")
        print(content[start:end])
        print("\n" + "="*50 + "\n")
