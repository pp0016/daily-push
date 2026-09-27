from bs4 import BeautifulSoup
import re

html_path = r"C:\Users\renu5\Downloads\New folder\YouTube.html"
with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

results = []

def parse_count(text):
    text = text.lower().replace('subscribers', '').replace('views', '').replace(',', '').strip()
    multiplier = 1
    if 'k' in text:
        multiplier = 1000
        text = text.replace('k', '')
    elif 'm' in text:
        multiplier = 1000000
        text = text.replace('m', '')
    elif 'b' in text:
        multiplier = 1000000000
        text = text.replace('b', '')
    
    try:
        return float(text) * multiplier
    except:
        return 0

# The subscriber counts in HTML are mostly in data-vidiq-subscriber-count elements
# Or in aria-labels of some elements.
# Let's find all video renderers (ytd-rich-grid-media, ytd-video-renderer, yt-lockup-view-model)
for renderer in soup.find_all(['ytd-rich-item-renderer', 'ytd-rich-grid-media', 'yt-lockup-view-model', 'ytd-video-renderer']):
    title_elem = renderer.find(id='video-title')
    if not title_elem:
        title_elem = renderer.find('h3')
    
    title = title_elem.text.strip() if title_elem else ""
    if not title:
        continue
        
    # Get views
    views_elem = renderer.find(string=re.compile(r'views', re.IGNORECASE))
    views_text = ""
    if views_elem:
        views_text = views_elem.strip()
    else:
        # try aria-label on the title link
        link = renderer.find('a', id='video-title-link')
        if link and link.get('aria-label'):
            m = re.search(r'([\d,KMB\.]+)\s+views', link.get('aria-label'), re.IGNORECASE)
            if m:
                views_text = m.group(1) + " views"
                
    # Get subscribers
    subs = 0
    subs_text = ""
    vidiq_sub = renderer.find(attrs={"data-vidiq-subscriber-count": True})
    if vidiq_sub:
        subs_text = vidiq_sub.text.strip()
        subs = parse_count(subs_text)
    else:
        # Check text containing 'subscriber'
        sub_elem = renderer.find(string=re.compile(r'subscriber', re.IGNORECASE))
        if sub_elem:
            m = re.search(r'([\d,KMB\.]+)\s+subscriber', sub_elem, re.IGNORECASE)
            if m:
                subs_text = m.group(1)
                subs = parse_count(subs_text)

    if views_text and subs > 0:
        views_count = parse_count(views_text)
        if views_count > 0:
            ratio = views_count / subs
            results.append({
                'title': re.sub(r'\s+', ' ', title),
                'views': views_text,
                'subs': subs_text,
                'ratio': ratio
            })

# Sort by ratio descending
results.sort(key=lambda x: x['ratio'], reverse=True)

md = "# Outlier Videos (View-to-Subscriber Ratio)\n\n"
md += "*Note: Since you requested I use ONLY the HTML file and not MCP tools, I could only calculate the ratio for the videos where vidIQ injected the subscriber count directly into the HTML code. (The homepage HTML does not load subscriber counts for all videos).* \n\n"

if not results:
    md += "No videos with both views and subscriber counts were found in the HTML.\n"
else:
    for r in results:
        md += f"### {r['title']}\n"
        md += f"- **Views:** {r['views']}\n"
        md += f"- **Subscribers:** {r['subs']}\n"
        md += f"- **Ratio (Outlier Score):** {r['ratio']:.2f}x\n\n"

out_path = r"C:\Users\renu5\.gemini\antigravity\brain\7a78deb3-fd50-47e2-8d2a-a23cba5ad928\outlier_videos.md"
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(md)
print(f"Found {len(results)} outlier videos")
