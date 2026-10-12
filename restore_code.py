#!/usr/bin/env python3
import json
import re
import os

transcripts = [
    '/Users/amitshah/.gemini/antigravity-ide/brain/0842d917-37aa-4401-807d-6392b89f5c9a/.system_generated/logs/transcript_full.jsonl',
    '/Users/amitshah/.gemini/antigravity-ide/brain/66a15c6f-a3a3-429a-9380-0776eba734ef/.system_generated/logs/transcript_full.jsonl'
]

recovered = {}

for path in transcripts:
    print('Processing transcript:', path)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                obj = json.loads(line)
                # 1. tool calls with write_to_file
                for tc in obj.get('tool_calls', []):
                    if tc.get('name') in ['write_to_file', 'create_file']:
                        args = tc.get('args', {})
                        tf = args.get('TargetFile') or args.get('FilePath')
                        cc = args.get('CodeContent')
                        if tf and cc:
                            recovered[tf] = ('write_to_file', cc)
                
                # 2. tool responses with view_file
                content = obj.get('content', '')
                if 'File Path: `file://' in content:
                    m = re.search(r'File Path: `file://([^`]+)`', content)
                    if m:
                        filepath = m.group(1)
                        lines_extracted = []
                        for l in content.split('\n'):
                            lm = re.match(r'^\s*(\d+):\s?(.*)$', l)
                            if lm:
                                lines_extracted.append((int(lm.group(1)), lm.group(2)))
                        if lines_extracted:
                            lines_extracted.sort(key=lambda x: x[0])
                            # Check completeness: check if continuous from 1 to max
                            text_lines = [x[1] for x in lines_extracted]
                            file_text = '\n'.join(text_lines)
                            cur_len = len(recovered.get(filepath, ('', ''))[1].splitlines())
                            if len(lines_extracted) > cur_len:
                                recovered[filepath] = ('view_file', file_text)
            except Exception as e:
                pass

print(f'\nTotal files found across transcripts: {len(recovered)}')
for k, (src, text) in sorted(recovered.items()):
    lines = text.splitlines()
    print(f'  {k} ({src}): {len(lines)} lines, {len(text)} bytes')
