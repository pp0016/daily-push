import json
import re

html_path = r"C:\Users\renu5\Downloads\YouTube.html"
with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

start_str = 'var ytInitialData = {'
start_idx = content.find(start_str)
if start_idx != -1:
    start_idx += len('var ytInitialData = ')
    bracket_count = 0
    end_idx = -1
    for i in range(start_idx, len(content)):
        if content[i] == '{':
            bracket_count += 1
        elif content[i] == '}':
            bracket_count -= 1
            if bracket_count == 0:
                end_idx = i + 1
                break
    
    if end_idx != -1:
        json_str = content[start_idx:end_idx]
        with open('yt_data.json', 'w', encoding='utf-8') as out:
            out.write(json_str)
        print(f"Wrote {len(json_str)} bytes to yt_data.json")
    else:
        print("Could not find end of JSON")
else:
    print("Could not find start of JSON")
