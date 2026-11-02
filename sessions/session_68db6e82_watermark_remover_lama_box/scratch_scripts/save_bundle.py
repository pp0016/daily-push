import re

with open(r"C:\Users\renu5\.gemini\antigravity\brain\68db6e82-6ec9-4f47-a039-6e7cc2557d48\scratch\bundle_search.py", "w") as f_out:
    pass

with open(r"C:\Users\renu5\.gemini\antigravity\brain\68db6e82-6ec9-4f47-a039-6e7cc2557d48\scratch\bundle_search.py", "w", encoding="utf-8") as f_out:
    f_out.write('''import urllib.request, re

with open("bundle.js", "rb") as f:
    content = f.read().decode("utf-8", errors="ignore")

# Find occurrences of 'jiraiya' or 'suigetsu'
for m in re.finditer(r'(?:suigetsu|transformation|pixelbin)[a-zA-Z0-9_\-\./]*', content, re.IGNORECASE):
    s = m.group(0)
    if len(s) > 10:
        pass

# Search for transformation plugins or function calls
print("--- SEARCH FOR TRANSFORMATION PATTERNS ---")
matches = re.findall(r'(\b[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+\([^)]*watermark[^)]*\))', content, re.IGNORECASE)
for m in matches[:10]:
    print(m)

# Find api calls or fetch/axios
print("--- SEARCH FOR URL ENDPOINTS IN BUNDLE ---")
urls = re.findall(r'["\'](/api/[^"\']+|https?://[^"\']+)["\']', content)
for u in set(urls):
    if any(k in u for k in ["transform", "watermark", "prediction", "upload", "suigetsu"]):
        print(u)
''')
