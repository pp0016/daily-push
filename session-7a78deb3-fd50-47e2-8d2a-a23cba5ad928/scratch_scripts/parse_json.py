import json

with open('yt_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

videos = []

def extract(obj):
    if isinstance(obj, dict):
        if 'videoId' in obj and 'title' in obj:
            title = None
            if isinstance(obj['title'], dict) and 'runs' in obj['title']:
                title = "".join(r.get('text', '') for r in obj['title']['runs'])
            elif isinstance(obj['title'], dict) and 'simpleText' in obj['title']:
                title = obj['title']['simpleText']
            elif isinstance(obj['title'], str):
                title = obj['title']
                
            channel = "Unknown Channel"
            for key in ['ownerText', 'longBylineText', 'shortBylineText', 'authorText']:
                if key in obj and isinstance(obj[key], dict) and 'runs' in obj[key]:
                    channel = "".join(r.get('text', '') for r in obj[key]['runs'])
                    break
                elif key in obj and isinstance(obj[key], dict) and 'simpleText' in obj[key]:
                    channel = obj[key]['simpleText']
                    break
                    
            if title:
                videos.append(f"- **{title}** (Channel: {channel})")
        
        for k, v in obj.items():
            extract(v)
    elif isinstance(obj, list):
        for item in obj:
            extract(item)

extract(data)

# unique only
videos = list(dict.fromkeys(videos))

output_path = r"C:\Users\renu5\.gemini\antigravity\brain\7a78deb3-fd50-47e2-8d2a-a23cba5ad928\youtube_videos.md"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write("# YouTube Videos List\n\nHere are the videos extracted from your saved YouTube page:\n\n")
    for v in videos:
        f.write(v + "\n")

print(f"Extracted {len(videos)} videos to {output_path}")
