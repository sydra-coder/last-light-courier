"""Prove bridge-house reachability under optimistic, bridge-free street rules."""
from collections import deque
from pathlib import Path
import json
import os

HERE=Path(__file__).parent
preview=Path(os.environ.get('LLC_PREVIEW_PATH',HERE/'all_spurs_candidate.html'))
line=next(line for line in preview.open(encoding='utf-8') if line.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2]);rows=[]
for level in levels[700:800]:
    walls={tuple(map(int,s.split(','))) for s in level['walls']}
    repair=level.get('repair')
    if repair and repair.get('effect')=='open':walls.discard(tuple(repair['tile']))
    walls.add(tuple(level['lightBridge']))
    start=tuple(level['depot']);seen={start};queue=deque([start])
    while queue:
        x,y=queue.popleft()
        for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if not (0<=p[0]<level['grid'] and 0<=p[1]<level['grid']) or p in walls or p in seen:continue
            if p==tuple(level['oneWayTile']) and (x,y)!=tuple(level['oneWayFrom']):continue
            seen.add(p);queue.append(p)
    bridge_house=tuple(level['homes'][level['bridgeHouseIndex']]['p'])
    rows.append({'level':level['n'],'bridgeHouse':list(bridge_house),'reachableWithoutBridge':bridge_house in seen,
                 'reachableHouseCountWithoutBridge':sum(tuple(h['p']) in seen for h in level['homes'])})
report={'scope':'Optimistic no-bridge graph: free repair open, no shadows, no light/time limit. One-way entry enforced.','rows':rows}
(HERE/'all_spurs_dependency.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
failed=[r['level'] for r in rows if r['reachableWithoutBridge']]
print('Bridge-house unreachable without supplied bridge:',len(rows)-len(failed),'/100; failed',failed)
if failed:raise SystemExit(1)
