import urllib.request
import re

url = "https://magicstudio.com/_next/static/bncyrMv1Sk9uPufUK2H89/_buildManifest.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode("utf-8", errors="ignore")
        print("BuildManifest length:", len(content))
        # Print lines or pages in manifest
        pages = re.findall(r'["\'](/[^"\']+)["\']:\s*\[([^\]]+)\]', content)
        for p, chunks in pages:
            if any(k in p for k in ["eraser", "editor", "upload", "magic", "inpaint"]):
                print(f"Page {p} chunks:")
                for c in chunks.split(","):
                    print("  -", c.strip().strip('"').strip("'"))
except Exception as e:
    print("Error:", e)
