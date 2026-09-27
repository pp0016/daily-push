import json
import os

session_id = '9b063341-ea34-42bf-adeb-61eeb2c4701e'
log_path = f'C:\\Users\\renu5\\.gemini\\antigravity\\brain\\{session_id}\\.system_generated\\logs\\transcript_full.jsonl'
output_dir = 'sessions\\youtube-niche-research-9b0633'
artifacts_dir = os.path.join(output_dir, 'artifacts')

os.makedirs(output_dir, exist_ok=True)
os.makedirs(artifacts_dir, exist_ok=True)

md_lines = ["# Session History: YouTube Niche Research\\n"]
md_lines.append(f"**Session ID:** {session_id}\\n\\n")

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            item = json.loads(line)
        except:
            continue
            
        step_type = item.get('type')
        source = item.get('source')
        content = item.get('content', '')
        
        if step_type == 'USER_INPUT':
            md_lines.append(f"## 🧑 User\\n\\n{content}\\n\\n")
        elif step_type == 'PLANNER_RESPONSE' and source == 'MODEL':
            if content:
                md_lines.append(f"## 🤖 Antigravity\\n\\n{content}\\n\\n")
            
            tool_calls = item.get('tool_calls', [])
            for tc in tool_calls:
                t_name = tc.get('name', '')
                if 'write_to_file' in t_name:
                    args = tc.get('args', tc.get('arguments', {}))
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except:
                            args = {}
                    
                    fname = os.path.basename(args.get('TargetFile', 'unknown.md'))
                    code = args.get('CodeContent', '')
                    if code:
                        with open(os.path.join(artifacts_dir, fname), 'w', encoding='utf-8') as out_f:
                            out_f.write(code)
                        md_lines.append(f"*(Generated artifact: `{fname}`)*\\n\\n")
                    else:
                        print(f"No CodeContent for {fname}")

with open(os.path.join(output_dir, 'README.md'), 'w', encoding='utf-8') as f:
    f.writelines(md_lines)

print("Extraction complete.")
