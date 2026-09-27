import json

log_path = r'C:\Users\renu5\.gemini\antigravity\brain\9b063341-ea34-42bf-adeb-61eeb2c4701e\.system_generated\logs\transcript_full.jsonl'
with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        item = json.loads(line)
        if item.get('type') == 'PLANNER_RESPONSE':
            for tc in item.get('tool_calls', []):
                if 'write_to_file' in tc.get('name', ''):
                    print("Name:", tc.get('name'))
                    print("Keys:", tc.keys())
                    if 'arguments' in tc:
                        print("Arguments type:", type(tc['arguments']))
                        print("Arguments keys:", tc['arguments'].keys())
