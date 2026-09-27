import re
import json

html_path = r'C:\Users\renu5\.gemini\antigravity\brain\e900d5b2-f367-42d4-9829-7fb6b2499468\.system_generated\steps\4\content.md'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# The data is probably in a <script> tag. Let's find all text between script tags.
scripts = re.findall(r'<script.*?>.*?</script>', html, re.DOTALL)
print(f"Found {len(scripts)} script tags.")

# Let's extract anything that looks like a JSON array [ ... ]
arrays = re.findall(r'(\[.*?\])', html)
print(f"Found {len(arrays)} arrays.")

# Let's write a generic string extractor to find human readable text
strings = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', html)
long_strings = [s for s in strings if len(s) > 50 and ' ' in s and not s.startswith('http')]

with open('strings.txt', 'w', encoding='utf-8') as out:
    for s in set(long_strings):
        out.write(s + '\n')
print(f"Dumped {len(set(long_strings))} long strings.")
