import os, json, glob
from pathlib import Path

MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace-owl/memory")
all_pellets = []
for filepath in sorted(glob.glob(os.path.join(MEMORY_DIR, '*.md'))):
    date_str = Path(filepath).stem
    current = None
    with open(filepath) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith("## "):
                if current and current['content'].strip():
                    all_pellets.append(current)
                parts = line[3:].strip().split(' ', 1)
                current = {'type': parts[0].upper(), 'time': parts[1].strip() if len(parts) > 1 else '', 'date': date_str, 'content': ''}
            elif current is not None:
                current["content"] += ("\n" if current["content"] else "") + line
    if current and current['content'].strip():
        all_pellets.append(current)
for p in all_pellets:
    p['content'] = p['content'].strip()
all_pellets.sort(key=lambda p: p['date'] + p.get('time', ''), reverse=True)
with open('pellets.json', 'w') as f:
    json.dump(all_pellets, f, indent=2)
