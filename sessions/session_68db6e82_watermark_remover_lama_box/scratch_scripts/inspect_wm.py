import urllib.request
import re
import json

url = "https://www.watermarkremover.io/upload"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

idx = html.find("window._conf=")
if idx != -1:
    end_idx = html.find("</script>", idx)
    conf_str = html[idx + len("window._conf="):end_idx].strip()
    try:
        conf = json.loads(conf_str)
        print("window._conf parsed:")
        for k, v in conf.items():
            print(f"  {k}: {v}")
    except Exception as e:
        print("Error parsing json:", e)
        print(conf_str[:1500])
