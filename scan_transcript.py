import json
import re

t = '/Users/amitshah/.gemini/antigravity-ide/brain/0842d917-37aa-4401-807d-6392b89f5c9a/.system_generated/logs/transcript_full.jsonl'
with open(t, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        try:
            obj = json.loads(line)
            content = obj.get('content', '')
            if 'File Path:' in content:
                m = re.search(r'File Path: `file://([^`]+)`', content)
                lines_m = re.search(r'Total Lines: (\d+)', content)
                show_m = re.search(r'Showing lines (\d+) to (\d+)', content)
                fp = m.group(1) if m else 'unknown'
                total = lines_m.group(1) if lines_m else '?'
                show = f'{show_m.group(1)}-{show_m.group(2)}' if show_m else '?'
                print(f'Line {i}: {fp} (Total: {total}, Showing: {show})')
        except Exception as e:
            pass
