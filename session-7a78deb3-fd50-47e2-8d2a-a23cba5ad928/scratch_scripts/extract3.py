import re

html_path = r'C:\Users\renu5\.gemini\antigravity\brain\e900d5b2-f367-42d4-9829-7fb6b2499468\.system_generated\steps\4\content.md'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

print('Titles:', re.findall(r'<title.*?>(.*?)</title>', html))
print('OG Title:', re.findall(r'og:title.*?content="(.*?)"', html))
print('OG Desc:', re.findall(r'og:description.*?content="(.*?)"', html))

# Let's extract specific text fields from the massive arrays
# A typical prompt/response in the WIZ payload is usually surrounded by brackets and quotes.
# Let's dump text that looks like conversation text.
import json

def extract_strings(text):
    return re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', text)

all_strings = extract_strings(html)
# filter for typical conversation lengths
possible_conv = [s for s in all_strings if len(s) > 20 and ' ' in s and not s.startswith('http') and not '{' in s and not '<' in s]

with open('possible_conv.txt', 'w', encoding='utf-8') as out:
    for s in possible_conv:
        out.write(s + '\n')
print(f"Dumped {len(possible_conv)} strings.")
