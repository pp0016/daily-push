import json

log_path = r'C:\Users\renu5\.gemini\antigravity\brain\9b063341-ea34-42bf-adeb-61eeb2c4701e\.system_generated\logs\transcript_full.jsonl'
found = False
with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        item = json.loads(line)
        if item.get('type') == 'PLANNER_RESPONSE':
            tool_calls = item.get('tool_calls', [])
            for tc in tool_calls:
                if 'write_to_file' in tc.get('name', ''):
                    print(json.dumps(tc, indent=2))
                    found = True
                    break
        if found: break
