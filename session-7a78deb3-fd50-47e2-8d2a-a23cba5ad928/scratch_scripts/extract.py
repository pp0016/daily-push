import json
import re

html_path = r'C:\Users\renu5\.gemini\antigravity\brain\e900d5b2-f367-42d4-9829-7fb6b2499468\.system_generated\steps\4\content.md'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

callbacks = re.findall(r'AF_initDataCallback\((.*?)\);', html, re.DOTALL)
for i, cb in enumerate(callbacks):
    with open(f'cb_{i}.txt', 'w', encoding='utf-8') as out:
        out.write(cb)
print(f"Found {len(callbacks)} callbacks.")
