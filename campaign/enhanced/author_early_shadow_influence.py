"""Place deterministic 2x2 shadow fields near proven routes in early districts."""
from pathlib import Path
import argparse,json

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'campaign' / 'enhanced'
parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design'/'map-solutions-1000.json')
parser.add_argument('--hidden',type=Path,default=BASE/'hidden-routes-v1/authored_levels.json')
parser.add_argument('--out',type=Path,default=BASE/'shadow-influence-v1')
args=parser.parse_args()
OUT = args.out
OUT.mkdir(exist_ok=True)
levels = json.loads(args.hidden.read_text(encoding='utf-8'))
routes = json.loads(args.solutions.read_text(encoding='utf-8'))['levels']
authored, proofs = [], []
for level in levels[:50]:
    route = routes[level['n']-1]['solutions'][0]['route']
    first = next(i for i, step in enumerate(route) if step['mask'])
    walked = {tuple(step['p']) for step in route}
    after = {tuple(step['p']) for step in route[first:]}
    occupied = {tuple(h['p']) for h in level['homes']}
    occupied.update(tuple(p) for p in level['patrol'])
    occupied.update(tuple(p) for p in (level.get('patrol2') or []))
    occupied.add(tuple(level['depot']))
    for key in ('fade', 'ice', 'dark', 'switch', 'gate', 'hiddenRoad'):
        if level.get(key): occupied.add(tuple(level[key]))
    walls = set(level['walls'])
    choices = []
    for x in range(level['grid']-1):
        for y in range(level['grid']-1):
            cells = {(x,y),(x+1,y),(x,y+1),(x+1,y+1)}
            if cells & (walked | occupied) or any(f'{a},{b}' in walls for a,b in cells): continue
            neighbors = {p for a,b in cells for p in ((a+1,b),(a-1,b),(a,b+1),(a,b-1))} - cells
            contact = len(neighbors & after)
            if contact:
                choices.append((contact, -abs(x-level['depot'][0])-abs(y-level['depot'][1]), x, y, cells))
    if not choices: continue
    _, _, x, y, cells = max(choices)
    level['shadowInfluence2x2'] = {'trigger': 'first_delivery', 'origin': [x,y], 'cells': [[x,y],[x+1,y],[x,y+1],[x+1,y+1]]}
    level['brief'] += ' After the first delivery, a marked 2×2 shadow field blocks four streets.'
    authored.append(level)
    proofs.append({'level':level['n'], 'origin':[x,y], 'triggerStep':first, 'routeSteps':len(route)-1,
                   'adjacentRouteCells':len(({p for a,b in cells for p in ((a+1,b),(a-1,b),(a,b+1),(a,b-1))}-cells)&after)})
    if len(authored)==25: break
assert len(authored)==25, f'Only found {len(authored)} suitable fields'
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(proofs,indent=2),encoding='utf-8')
print(f'Authored {len(authored)} early 2x2 shadow fields, levels {authored[0]["n"]}–{authored[-1]["n"]}')
