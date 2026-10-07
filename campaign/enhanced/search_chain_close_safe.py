"""Find second-delivery closure tiles that cannot strand an optimistic house order."""
from collections import deque
from pathlib import Path
import json

root=Path(__file__).resolve().parents[2]
line=next(s for s in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
routes={x['level']:x['route'] for x in json.loads((root/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text())}
affected=[1602,1646,1668,1901,1914,1941,1954,1965]

def coords(value):
    if isinstance(value,list):
        if len(value)==2 and all(isinstance(x,int) for x in value):yield tuple(value)
        else:
            for item in value:yield from coords(item)
    elif isinstance(value,dict):
        for name,item in value.items():
            if name not in ('walls','spine','route'):yield from coords(item)

def seen(level,phase,signal,start):
    walls={tuple(map(int,s.split(','))) for s in level['walls']}
    if level.get('repair'):walls.discard(tuple(level['repair']['tile']))
    if level.get('hiddenRoad'):walls.discard(tuple(level['hiddenRoad']))
    if level.get('lightBridge'):walls.discard(tuple(level['lightBridge']))
    if phase and level.get('authoredEvent'):
        tile=level['phaseChoice']['alternateClose'] if signal and level.get('phaseChoice') else level['authoredEvent']['tile']
        walls.add(tuple(tile))
    if phase>=2:
        for p in level['chainEvent']['open']:walls.discard(tuple(p))
        walls.add(tuple(level['chainEvent']['close']))
    if phase and level.get('quakeEvent'):
        for p in level['quakeEvent']['open']:walls.discard(tuple(p))
        walls.add(tuple(level['quakeEvent']['close']))
    start=tuple(start);result={start};queue=deque([start]);size=level['grid']
    stops=[tuple(p) for p in level.get('transitLink',{}).get('stops',[])]
    while queue:
        x,y=queue.popleft();adj=((x+1,y),(x-1,y),(x,y+1),(x,y-1))
        if len(stops)==2 and (x,y) in stops:adj+= (stops[1] if (x,y)==stops[0] else stops[0],)
        for q in adj:
            if 0<=q[0]<size and 0<=q[1]<size and q not in walls and q not in result:
                result.add(q);queue.append(q)
    return result

def distance(level,start,walls):
    result={start:0};queue=deque([start]);size=level['grid']
    while queue:
        x,y=queue.popleft()
        for q in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=q[0]<size and 0<=q[1]<size and q not in walls and q not in result:
                result[q]=result[(x,y)]+1;queue.append(q)
    return result

report=[]
for n in affected:
    level=levels[n-1];houses=[tuple(h['p']) for h in level['homes']];depot=tuple(level['depot']);route=routes[n]
    second_step=next(i for i,x in enumerate(route) if x['mask'].bit_count()==2)
    post={tuple(x['p']) for x in route[second_step+1:]}
    old=tuple(level['chainEvent']['close']);walls={tuple(map(int,s.split(','))) for s in level['walls']}
    protected=set(coords(level))
    orders=[]
    for signal in ([False,True] if level.get('phaseChoice') else [False]):
        initial=seen(level,0,signal,depot)
        for first,p in enumerate(houses):
            if p not in initial:continue
            after_first=seen(level,1,signal,p)
            for second,q in enumerate(houses):
                if second!=first and q in after_first:orders.append((signal,first,second))
    candidates=[]
    second_house=tuple(route[second_step]['p'])
    base_walls=walls-{tuple(level['repair']['tile'])}-{tuple(p) for p in level['chainEvent']['open']}
    base_walls.add(tuple(level['authoredEvent']['tile']))
    base_distance=distance(level,second_house,base_walls)
    targets=[depot,*[h for h in houses if h!=second_house]]
    for x in range(level['grid']):
        for y in range(level['grid']):
            tile=(x,y)
            if tile in walls or tile in protected or tile in post or abs(x-old[0])+abs(y-old[1])>10:continue
            level['chainEvent']['close']=[x,y]
            for signal,first,second in orders:
                component=seen(level,2,signal,houses[second])
                remaining=sum(h in component for i,h in enumerate(houses) if i not in (first,second))
                if depot not in component or remaining<level['required']-2:break
            else:
                changed_distance=distance(level,second_house,base_walls|{tile})
                affected_targets=sum(t in base_distance and (t not in changed_distance or changed_distance[t]>base_distance[t]) for t in targets)
                candidates.append({'tile':[x,y],'distanceOld':abs(x-old[0])+abs(y-old[1]),
                                   'affectedTargets':affected_targets,
                                   'routeBeforeSecond':tile in {tuple(s['p']) for s in route[:second_step+1]}})
    level['chainEvent']['close']=list(old)
    candidates.sort(key=lambda c:(-c['affectedTargets'],c['distanceOld'],not c['routeBeforeSecond']))
    report.append({'level':n,'old':list(old),'ordersChecked':len(orders),'candidates':candidates})
(root/'campaign/enhanced/chain-close-safe-candidates.json').write_text(json.dumps(report,indent=2))
print(json.dumps([{'level':r['level'],'count':len(r['candidates']),'first':r['candidates'][:8]} for r in report]))
