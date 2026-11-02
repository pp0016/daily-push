import urllib.request
import re

url = "https://magicstudio.com/_next/static/chunks/pages/magiceraser/editor-1dadff2e15579d4a.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

for term in ["image_key", "upload", "s.Z"]:
    for m in re.finditer(re.escape(term), content):
        start = max(0, m.start() - 200)
        end = min(len(content), m.end() + 300)
        print(f"=== MATCH FOR '{term}' ===")
        print(content[start:end])
        print("\n" + "="*50 + "\n")
