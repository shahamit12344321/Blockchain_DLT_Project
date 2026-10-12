#!/usr/bin/env python3
import json
import re
import os

transcript_path = '/Users/amitshah/.gemini/antigravity-ide/brain/0842d917-37aa-4401-807d-6392b89f5c9a/.system_generated/logs/transcript_full.jsonl'

# Extract written files
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            obj = json.loads(line)
            for tc in obj.get('tool_calls', []):
                args = tc.get('args', {})
                tf = args.get('TargetFile')
                cc = args.get('CodeContent')
                if tf and cc:
                    os.makedirs(os.path.dirname(tf), exist_ok=True)
                    with open(tf, 'w', encoding='utf-8') as out:
                        out.write(cc)
                    print(f"Extracted written file: {tf} ({len(cc)} bytes)")
        except Exception as e:
            pass

# Extract viewed files
extracted_views = {}
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            obj = json.loads(line)
            content = obj.get('content', '')
            if 'File Path: `file://' in content:
                m = re.search(r'File Path: `file://([^`]+)`', content)
                if m:
                    fp = m.group(1)
                    if fp not in extracted_views:
                        extracted_views[fp] = {}
                    for l in content.split('\n'):
                        lm = re.match(r'^\s*(\d+):\s?(.*)$', l)
                        if lm:
                            extracted_views[fp][int(lm.group(1))] = lm.group(2)
        except Exception as e:
            pass

for fp, lines_dict in extracted_views.items():
    if lines_dict:
        sorted_keys = sorted(lines_dict.keys())
        min_k, max_k = min(sorted_keys), max(sorted_keys)
        print(f"Viewed file {fp}: lines {min_k} to {max_k} (total {len(sorted_keys)})")
        # reconstruct file
        reconstructed = []
        for i in range(1, max_k + 1):
            if i in lines_dict:
                reconstructed.append(lines_dict[i])
            else:
                reconstructed.append("")
        file_text = '\n'.join(reconstructed)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, 'w', encoding='utf-8') as out:
            out.write(file_text)
        print(f"Saved: {fp} ({len(file_text)} bytes)")
