"""Prove mandatory free-repair streets separate a required house from depot.

All other event-opened roads, the power bridge, and transit are optimistically
available. Reachability without the marked repair street is therefore a valid
necessary condition for a completion that skips the repair action.
"""
from collections import deque
from pathlib import Path
import json
import os

root=Path(__file__).resolve().parents[2]
preview=Path(os.environ.get('LLC_PREVIEW_PATH',root/'design/campaign-2000-preview/index.html'))
line=next(s for s in preview.open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
rows=[]
for level in levels:
    if not level.get('repairRequired'):continue
    assert level['repair']['cost']==0 and level['repair']['effect']=='open'
    walls={tuple(map(int,s.split(','))) for s in level['walls']}
    for name in ('quakeEvent','chainEvent'):
        p=level.get(name,{}).get('open')
        if p:
            for tile in ([p] if isinstance(p[0],int) else p):walls.discard(tuple(tile))
    if level.get('lightBridge'):walls.discard(tuple(level['lightBridge']))
    if level.get('hiddenRoad'):walls.discard(tuple(level['hiddenRoad']))
    repair=tuple(level['repair']['tile']);walls.add(repair)
    stops=[tuple(p) for p in level.get('transitLink',{}).get('stops',[])]
    start=tuple(level['depot']);seen={start};queue=deque([start]);size=level['grid']
    while queue:
        x,y=queue.popleft();neighbors=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        if stops and (x,y) in stops:neighbors.append(stops[1] if (x,y)==stops[0] else stops[0])
        for p in neighbors:
            if 0<=p[0]<size and 0<=p[1]<size and p not in walls and p not in seen:
                seen.add(p);queue.append(p)
    unreachable=[i for i,h in enumerate(level['homes']) if tuple(h['p']) not in seen]
    rows.append({'level':level['n'],'requiredHouses':level['required'],
                 'unreachableHouseIndices':unreachable,
                 'topologicallyRequired':len(level['homes'])-len(unreachable)<level['required']})
report={'scope':'Optimistic no-repair graph: all other event-opened roads, bridge and transit available; shadows, light and timing ignored.',
        'levels':len(rows),'topologicallyRequired':sum(x['topologicallyRequired'] for x in rows),
        'unproven':[x['level'] for x in rows if not x['topologicallyRequired']],'rows':rows}
output=root/'campaign/enhanced/free-repair-dependency-audit.json'
output.write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='rows'}))
