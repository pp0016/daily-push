import urllib.request
import re

url = "https://magicstudio.com/_next/static/chunks/pages/magiceraser/editor-1dadff2e15579d4a.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

idx = content.find("https://ai-api.magicstudio.com/api")
while idx != -1:
    start = max(0, idx - 1500)
    end = min(len(content), idx + 1000)
    print("=== API CALL BLOCK ===")
    print(content[start:end])
    print("\n" + "="*80 + "\n")
    idx = content.find("https://ai-api.magicstudio.com/api", idx + 1)
