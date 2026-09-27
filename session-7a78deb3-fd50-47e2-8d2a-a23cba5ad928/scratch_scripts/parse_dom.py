from bs4 import BeautifulSoup
import re

html_path = r"C:\Users\renu5\Downloads\YouTube.html"
output_path = r"C:\Users\renu5\.gemini\antigravity\brain\7a78deb3-fd50-47e2-8d2a-a23cba5ad928\youtube_videos.md"

with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

videos = []

# Method 1: All a tags with href containing watch or shorts
for a in soup.find_all('a', href=True):
    href = a['href']
    if '/watch' in href or '/shorts/' in href:
        title = a.get('title')
        aria_label = a.get('aria-label')
        
        # if there's aria-label, it usually has "Title by Channel views ago"
        text = aria_label or title or a.text.strip()
        if text:
            # clean up newlines
            text = re.sub(r'\s+', ' ', text)
            if len(text) > 5:  # skip UI things
                videos.append(text)

# Method 2: ytLockupMetadataViewModelHeadingReset
for h3 in soup.find_all('h3', class_=lambda c: c and 'ytLockupMetadataViewModelHeadingReset' in c):
    title = h3.get('title')
    if title:
        videos.append(title.strip())

# Method 3: id="video-title"
for elem in soup.find_all(id='video-title'):
    title = elem.text.strip()
    if title:
        videos.append(re.sub(r'\s+', ' ', title))

# Deduplicate
unique_vids = []
seen = set()
for v in videos:
    v = v.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    if v not in seen and v not in ["Shorts", "Play all", "Watch later", "Save to playlist", "Share", "More actions", "Report"]:
        seen.add(v)
        unique_vids.append(v)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write("# YouTube Videos List\n\nHere are the videos extracted from your saved YouTube page:\n\n")
    for v in unique_vids:
        # If it looks like "Title by Channel X views", format it nicely
        if ' by ' in v and (' views' in v or ' ago' in v):
            parts = v.split(' by ')
            title = parts[0]
            rest = ' by '.join(parts[1:])
            f.write(f"- **{title}** | {rest}\n")
        else:
            f.write(f"- {v}\n")

print(f"Extracted {len(unique_vids)} videos to {output_path}")
