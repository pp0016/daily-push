import urllib.request
import re

url = "https://magicstudio.com/_next/static/chunks/pages/magiceraser/editor-1dadff2e15579d4a.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

terms = ["ai-api.magicstudio.com", "/magic-erase", "/pro/magic-erase", "FormData", "image", "mask"]
for term in ["ai-api.magicstudio.com", "magic-erase"]:
    for m in re.finditer(re.escape(term), content):
        start = max(0, m.start() - 300)
        end = min(len(content), m.end() + 500)
        print(f"=== MATCH FOR '{term}' ===")
        print(content[start:end])
        print("\n" + "="*50 + "\n")
