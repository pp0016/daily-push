import urllib.request
import re

url = "https://magicstudio.com/magiceraser/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
        print("Fetched HTML, length:", len(html))
        
        # Look for script tags
        scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html)
        print("Scripts count:", len(scripts))
        for s in scripts:
            print("  Script:", s)
                
        # Look for API endpoints in HTML
        apis = re.findall(r'https?://[^\s"\'<>]+', html)
        relevant_apis = [a for a in set(apis) if any(k in a.lower() for k in ["api", "magicstudio", "eraser", "ai", "model"])]
        print("Relevant URLs in HTML:")
        for a in relevant_apis[:15]:
            print("  -", a)
except Exception as e:
    print("Error:", e)
