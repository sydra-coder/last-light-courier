"""Screen all delivery orders for event-created topological dead ends.

This deliberately grants optional openings and ignores actor, light and timing
rules. A failure is conclusive for the represented road state; a pass is only
an optimistic topology check, not a full solvability proof.
"""
from collections import deque,Counter
from pathlib import Path
import json, os

root=Path(__file__).resolve().parents[2]
preview=Path(os.environ.get('LLC_PREVIEW_PATH',root/'design/campaign-2000-preview/index.html'))
line=next(s for s in preview.open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])

def reached(level,phase,signal=False,start=None):
    walls={tuple(map(int,s.split(','))) for s in level['walls']}
    for key in ('repair','lightBridge','hiddenRoad'):
        value=level.get(key)
        if not value:continue
        tile=value['tile'] if key=='repair' else value
        walls.discard(tuple(tile))
    quake=level.get('quakeEvent')
    if quake and phase>=1:
        for tile in quake['open']:walls.discard(tuple(tile))
        walls.add(tuple(quake['close']))
    if phase>=1 and level.get('authoredEvent'):
        event=level['authoredEvent']
        tile=level['phaseChoice']['alternateClose'] if signal and level.get('phaseChoice') else event['tile']
        walls.add(tuple(tile))
    chain=level.get('chainEvent')
    if chain and phase>=2:
        for tile in chain['open']:walls.discard(tuple(tile))
        walls.add(tuple(chain['close']))
    start=tuple(start or level['depot'])
    seen={start};queue=deque([start]);size=level['grid']
    stops=[tuple(p) for p in level.get('transitLink',{}).get('stops',[])]
    while queue:
        x,y=queue.popleft();neighbors=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        if len(stops)==2 and (x,y) in stops:neighbors.append(stops[1] if (x,y)==stops[0] else stops[0])
        for p in neighbors:
            if 0<=p[0]<size and 0<=p[1]<size and p not in walls and p not in seen:
                seen.add(p);queue.append(p)
    return seen

rows=[];orders_checked=0
for level in levels:
    if not (level.get('authoredEvent') or level.get('quakeEvent') or level.get('chainEvent')):continue
    houses=[tuple(h['p']) for h in level['homes']]
    initially=reached(level,0)
    for signal in ([False,True] if level.get('phaseChoice') else [False]):
        for first,p in enumerate(houses):
            if p not in initially:continue
            after_first=reached(level,1,signal,p)
            if not level.get('chainEvent'):
                orders_checked+=1
                remaining=sum(q in after_first for i,q in enumerate(houses) if i!=first)
                if tuple(level['depot']) not in after_first or remaining<level['required']-1:
                    rows.append({'level':level['n'],'phase':1,'signal':signal,'order':[first]})
                continue
            for second,q in enumerate(houses):
                if second==first or q not in after_first:continue
                orders_checked+=1
                after_second=reached(level,2,signal,q)
                remaining=sum(h in after_second for i,h in enumerate(houses) if i not in (first,second))
                if tuple(level['depot']) not in after_second or remaining<level['required']-2:
                    rows.append({'level':level['n'],'phase':2,'signal':signal,'order':[first,second]})
report={'preview':str(preview),'eventMaps':sum(bool(l.get('authoredEvent') or l.get('quakeEvent') or l.get('chainEvent')) for l in levels),
        'statesChecked':sum((2 if l.get('chainEvent') else 1)*(2 if l.get('phaseChoice') else 1) for l in levels if l.get('authoredEvent') or l.get('quakeEvent') or l.get('chainEvent')),
        'ordersChecked':orders_checked,'topologicalDeadEnds':len(rows),'affectedLevels':dict(Counter(x['level'] for x in rows)),'examples':rows[:30],
        'scope':'Optimistic road graph from each initially reachable first house and each second house reachable after the first event. Requires remaining houses and depot in the courier component after the last road event; ignores actor, light and timing viability.'}
(root/'campaign/enhanced/event-topology-audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
if rows:raise SystemExit(f'{len(rows)} optimistic event-state dead ends')
