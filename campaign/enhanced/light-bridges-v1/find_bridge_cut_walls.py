"""Find a single wall that makes the supplied bridge geometrically necessary.

This is a design screen, not a game-rule proof until the candidate is promoted
and all recorded routes are replayed.
"""
from collections import deque
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[3]
line=next(line for line in (ROOT/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if line.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
archive=json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))['levels']

def reachable(level,walls):
    start=tuple(level['depot']);seen={start};queue=deque([start]);size=level['grid']
    while queue:
        x,y=queue.popleft()
        for point in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=point[0]<size and 0<=point[1]<size and point not in seen and point not in walls:
                seen.add(point);queue.append(point)
    return seen

rows=[]
for number in range(701,801):
    level=levels[number-1]
    walls={tuple(map(int,key.split(','))) for key in level['walls']}
    repair=level.get('repair')
    if repair and repair.get('effect')=='open':walls.discard(tuple(repair['tile']))
    bridge=tuple(level['lightBridge']);homes={tuple(h['p']) for h in level['homes']}
    no_bridge=walls|{bridge}
    baseline=reachable(level,no_bridge)
    reference={tuple(step['p']) for step in archive[number-1]['solutions'][0]['route']}
    protected=reference|homes|{tuple(level['depot']),bridge}
    candidates=[]
    for y in range(level['grid']):
        for x in range(level['grid']):
            tile=(x,y)
            if tile in no_bridge or tile in protected:continue
            if not homes.issubset(reachable(level,no_bridge|{tile})) and homes.issubset(reachable(level,walls|{tile})):
                candidates.append(tile)
    rows.append({'level':number,'alreadyBridgeRequired':not homes.issubset(baseline),
                 'singleWallCandidates':[list(p) for p in candidates]})
output=Path(__file__).with_name('bridge_cut_walls_screen.json')
output.write_text(json.dumps({'scope':'Static connectivity with required repair open; candidate walls avoid recorded powered route. Full rule replay required before promotion.','rows':rows},indent=2),encoding='utf-8')
print('Already required:',sum(r['alreadyBridgeRequired'] for r in rows),'single-wall candidates:',sum(bool(r['singleWallCandidates']) for r in rows),'neither:',[r['level'] for r in rows if not r['alreadyBridgeRequired'] and not r['singleWallCandidates']])
