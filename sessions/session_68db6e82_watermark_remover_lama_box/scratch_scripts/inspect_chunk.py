import urllib.request
import re
import json

base_url = "https://magicstudio.com"
page_chunk = "/_next/static/chunks/pages/magiceraser-3a242c2e79a2db75.js"

req = urllib.request.Request(base_url + page_chunk, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode("utf-8", errors="ignore")
        print("Downloaded page chunk, length:", len(content))
        
        # Search for API endpoints
        endpoints = re.findall(r'["\'](/api/[^"\']+|https?://[^"\']+)["\']', content)
        print("Endpoints in page chunk:")
        for ep in set(endpoints):
            if any(k in ep.lower() for k in ["api", "inpaint", "erase", "magic", "upload", "prediction", "clean", "remove"]):
                print("  ->", ep)
                
        # Search for keywords
        kws = ["inpaint", "mask", "brush", "lama", "erase", "sd", "diffusion", "resolution", "hd", "model", "canvas"]
        for kw in kws:
            matches = [m.start() for m in re.finditer(r'\b' + kw + r'\b', content, re.I)]
            print(f"Keyword '{kw}': {len(matches)} occurrences")
            
        # Let's inspect some code snippets around 'erase' or 'inpaint' or 'fetch' or 'post'
        for m in re.finditer(r'(?:fetch|axios|\.post)\s*\([^)]+\)', content):
            snippet = content[max(0, m.start()-50):min(len(content), m.end()+150)]
            print("\nFetch snippet:\n", snippet)
            break
except Exception as e:
    print("Error:", e)
