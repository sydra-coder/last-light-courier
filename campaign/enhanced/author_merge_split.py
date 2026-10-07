"""Author deterministic merge/split phases on safe Breachlands spawner maps."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'campaign/enhanced/spawners-v1/authored_levels.json'
ROUTES = ROOT / 'campaign/enhanced/road-events-v1/post_event_routes.json'
OUT = ROOT / 'campaign/enhanced/merge-split-v1'
OUT.mkdir(exist_ok=True)
levels = json.loads(SRC.read_text(encoding='utf-8'))
proofs = json.loads(ROUTES.read_text(encoding='utf-8'))[200:300]
authored = []
records = []
for level, proof in zip(levels, proofs):
    assert level['n'] == proof['level']
    x, y = level['shadowSpawner']['origin']
    route = proof['route']
    trigger = proof['triggerStep']
    options = []
    for dx in (-1, 0):
        for dy in (-1, 0):
            cells = [(x + dx + i, y + dy + j) for j in range(3) for i in range(3)]
            zone = set(cells)
            if not all(0 <= a < level['grid'] and 0 <= b < level['grid']
                       and f'{a},{b}' not in level['walls'] for a, b in zone):
                continue
            if any(tuple(step['p']) in zone for step in route[trigger + 9:trigger + 13]):
                continue
            split = [cells[0], cells[-1]]
            if any(tuple(step['p']) in set(split) for step in route[trigger + 13:]):
                continue
            proximity = min(abs(step['p'][0]-a)+abs(step['p'][1]-b)
                            for step in route[trigger+9:] for a, b in zone)
            options.append((proximity, dx, dy, cells, split))
    if not options:
        continue
    proximity, dx, dy, cells, split = min(options, key=lambda o: (o[0], o[1], o[2]))
    level['mergeSplit'] = {'mergedCells': [list(p) for p in cells],
                           'splitCells': [list(p) for p in split],
                           'mergeAfter': 9, 'splitAfter': 13}
    authored.append(level)
    records.append({'level': level['n'], 'triggerStep': trigger,
                    'mergedCells': level['mergeSplit']['mergedCells'],
                    'splitCells': level['mergeSplit']['splitCells'],
                    'proximity': proximity, 'routeSteps': len(route)-1})

assert len(authored) >= 20, len(authored)
(OUT / 'authored_levels.json').write_text(json.dumps(authored, separators=(',', ':')), encoding='utf-8')
(OUT / 'route_proofs.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
print(f'Authored {len(authored)} merge/split maps, {sum(r["proximity"]<=1 for r in records)} near the recorded route')
