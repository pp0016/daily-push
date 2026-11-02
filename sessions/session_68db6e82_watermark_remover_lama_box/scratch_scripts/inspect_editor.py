import urllib.request
import re

base_url = "https://magicstudio.com/_next/"
chunks = [
    "static/chunks/1510-576bd7e89f99c7eb.js",
    "static/chunks/pages/magiceraser/editor-1dadff2e15579d4a.js"
]

for ch in chunks:
    url = base_url + ch
    name = ch.split("/")[-1]
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            print(f"Downloaded {name}, size: {len(content)}")
            
            # Find URLs, endpoints, API routes
            apis = re.findall(r'["\'](https?://[^"\']+|/[a-zA-Z0-9_\-\./~:]*(?:api|inpaint|erase|magic|model|predict|upload)[a-zA-Z0-9_\-\./~:]*)["\']', content)
            print(f"  Endpoints found in {name}:", len(set(apis)))
            for a in sorted(set(apis)):
                if any(k in a.lower() for k in ["api", "inpaint", "erase", "magic", "predict", "task"]):
                    print("    ->", a)
                    
            # Search for model or processing keywords
            for kw in ["inpaint", "mask", "brush", "lama", "sd", "diffusion", "resolution", "hd", "high_resolution", "canvas", "threshold"]:
                matches = list(re.finditer(r'\b' + kw + r'\b', content, re.I))
                print(f"    Keyword '{kw}': {len(matches)} occurrences")
    except Exception as e:
        print(f"Error {name}: {e}")
