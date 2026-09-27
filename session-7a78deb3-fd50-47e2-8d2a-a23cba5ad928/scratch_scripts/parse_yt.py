import os
from bs4 import BeautifulSoup
import sys

html_path = r"C:\Users\renu5\Downloads\YouTube.html"
if not os.path.exists(html_path):
    print("File not found")
    sys.exit(1)

with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

# YouTube elements
results = []
# Many times aria-label on the link has the full text: "Video Title by Channel Name ... views ..."
links = soup.find_all('a', id='video-title-link')
if links:
    for link in links:
        title = link.get('title') or link.text.strip()
        # Find closest channel name
        parent = link.find_parent('ytd-rich-grid-media')
        channel = "Unknown Channel"
        if parent:
            channel_elem = parent.select_one('ytd-channel-name yt-formatted-string a')
            if not channel_elem:
                channel_elem = parent.select_one('ytd-channel-name yt-formatted-string')
            if channel_elem:
                channel = channel_elem.text.strip()
        
        results.append(f"- **{title}** (Channel: {channel})")
else:
    # try aria-label
    for a in soup.find_all('a', id='video-title'):
        title = a.get('title') or a.text.strip()
        aria = a.get('aria-label', '')
        if aria:
            results.append(f"- {title} | Aria: {aria}")
        else:
            results.append(f"- {title}")
            
if not results:
    print("Could not find standard YouTube title elements. Searching for any titles...")
    for t in soup.select('h3'):
        results.append(f"- {t.text.strip()}")

for i, r in enumerate(results):
    print(r)
