import json
import re

html_path = r"C:\Users\renu5\Downloads\YouTube.html"
output_path = r"C:\Users\renu5\.gemini\antigravity\brain\7a78deb3-fd50-47e2-8d2a-a23cba5ad928\youtube_videos.md"

with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Approach 1: Parse ytInitialData correctly
# Find the start of ytInitialData
start_str = 'var ytInitialData = {'
start_idx = content.find(start_str)
videos_json = []

if start_idx != -1:
    start_idx += len('var ytInitialData = ')
    # Extract the json object by counting brackets
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
        try:
            data = json.loads(json_str)
            
            # recursive search
            def extract_videos(obj):
                if isinstance(obj, dict):
                    if 'videoId' in obj and 'title' in obj and 'runs' in obj['title']:
                        title = "".join(r.get('text', '') for r in obj['title']['runs'])
                        channel = "Unknown Channel"
                        for key in ['ownerText', 'longBylineText', 'shortBylineText']:
                            if key in obj and 'runs' in obj[key]:
                                channel = "".join(r.get('text', '') for r in obj[key]['runs'])
                                break
                        if title:
                            videos_json.append(f"- **{title}** (Channel: {channel})")
                    for k, v in obj.items():
                        extract_videos(v)
                elif isinstance(obj, list):
                    for item in obj:
                        extract_videos(item)
            
            extract_videos(data)
        except Exception as e:
            print(f"JSON parse error: {e}")

# Approach 2: Extract all aria-labels that look like "Title by Channel"
videos_aria = []
matches = re.findall(r'aria-label="([^"]+ by [^"]+)"', content)
for m in matches:
    # Basic filtering to avoid UI elements
    if 'views' in m or 'ago' in m or 'play Short' in m:
        # try to split title and channel
        parts = m.split(' by ')
        title = parts[0].replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
        rest = ' by '.join(parts[1:]).replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
        videos_aria.append(f"- **{title}** | {rest}")

# Approach 3: <a title="xxx"> inside something
from bs4 import BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')
videos_html = []
for a in soup.find_all('a', id='video-title-link'):
    title = a.get('title') or a.text.strip()
    if title:
        videos_html.append(f"- **{title}**")

all_videos = list(set(videos_json + videos_aria + videos_html))

with open(output_path, 'w', encoding='utf-8') as f:
    f.write("# YouTube Videos List\n\nHere are the videos extracted from your saved YouTube page:\n\n")
    for v in all_videos:
        f.write(v + "\n")

print(f"Extracted {len(all_videos)} videos to markdown file.")
