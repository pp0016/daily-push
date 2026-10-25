import urllib.request
import re

bundles = [
    "https://cdn.pixelbin.io/v2/dummy-cloudname/VtmFMH/original/bundle-a0659334433eb7df972c.js",
    "https://cdn.pixelbin.io/v2/dummy-cloudname/VtmFMH/original/bundle-825c1b60ea9beafeaadd.js"
]

for url in bundles:
    name = url.split("/")[-1]
    print("Downloading", name)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode("utf-8", errors="ignore")
        print(f"Downloaded {name}, size: {len(content)}")
        
        # Search for transformation keywords
        keywords = ["transformation", "jiraiya", "suigetsu", "watermark", "remove", "predict", "model", "detect_text", "wm_remove", "inpaint"]
        for kw in keywords:
            matches = [m.start() for m in re.finditer(kw, content, re.IGNORECASE)]
            print(f"  Keyword '{kw}': {len(matches)} occurrences")
            
        # Let's search for API endpoints or transformation URL patterns:
        patterns = re.findall(r'["\']([a-zA-Z0-9_\-\./~:]*(?:wm|watermark|transform|predict|jiraiya)[a-zA-Z0-9_\-\./~:]*)["\']', content)
        print("  Sample patterns:", set(patterns[:20]))
