import urllib.request
from bs4 import BeautifulSoup
import re

url = "https://www.pixelbin.io/docs/transformations/ai/watermark-remover/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)
        print("Page fetched, length:", len(text))
        print("Preview:", text[:1000])
        # Find any mention of model, architecture, neural network, etc.
        for kw in ["model", "algorithm", "neural", "deep learning", "inpaint", "gan", "lama", "mask"]:
            matches = [m.start() for m in re.finditer(kw, text, re.IGNORECASE)]
            print(f"Keyword '{kw}': {len(matches)} occurrences")
            for idx in matches[:3]:
                print(f"  [{kw}] ...{text[max(0, idx-80):min(len(text), idx+120)]}...")
except Exception as e:
    print("Error:", e)
