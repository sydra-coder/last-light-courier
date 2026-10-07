"""Rebuild proposed 801–1000 delivery orders with Echo-safe street legs.

This still ignores moving actors, lantern and aftershock timing. Replay every
candidate in the full runtime before using it in the campaign.
"""
from collections import deque
from pathlib import Path
import argparse,json,os

root=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--input',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--neighbor-order',default='EWSN')
args=parser.parse_args()
assert sorted(args.neighbor_order)==sorted('EWSN')
directions={'E':(1,0),'W':(-1,0),'S':(0,1),'N':(0,-1)}
preview=Path(os.environ.get('LLC_PREVIEW_PATH',root/'design/campaign-2000-preview/index.html'))
line=next(s for s in preview.open(encoding='utf-8') if s.startswith('const LEVELS='))
levels={x['n']:x for x in json.loads(line[13:-2])}
source=json.loads(args.input.read_text(encoding='utf-8'))

def walls_for(level,mask):
    walls={tuple(map(int,s.split(','))) for s in level['walls']}
    repair=level.get('repair')
    if level.get('repairRequired') and repair and repair.get('effect')=='open' and repair.get('cost')==0:
        walls.discard(tuple(repair['tile']))
    if mask and level.get('quakeEvent'):
        quake=level['quakeEvent']
        walls.add(tuple(quake['close']))
        for point in quake['open']:walls.discard(tuple(point))
    return walls

def leg(level,points,mask,route,target_index):
    start=tuple(route[-1]);target=points[target_index]
    previous=tuple(route[-2]) if len(route)>=2 else None
    before=tuple(route[-3]) if len(route)>=3 else None
    walls=walls_for(level,mask)
    forbidden={points[0]} if target_index else set()
    forbidden.update(point for i,point in enumerate(points[1:],1)
                     if not mask&(1<<(i-1)) and i!=target_index)
    initial=(start,previous,before)
    queue=deque([initial]);parent={initial:None};size=level['grid'];end=None
    while queue:
        state=queue.popleft();current,prev,older=state
        if current==target:end=state;break
        x,y=current
        for name in args.neighbor_order:
            dx,dy=directions[name];point=(x+dx,y+dy)
            if not(0<=point[0]<size and 0<=point[1]<size) or point in walls or point in forbidden:continue
            if mask and (point==prev or point==older):continue
            next_state=(point,current,prev)
            if next_state not in parent:parent[next_state]=state;queue.append(next_state)
    if end is None:return None
    segment=[];state=end
    while state is not None:segment.append(state[0]);state=parent[state]
    return list(reversed(segment))

rows=[]
for item in source['rows']:
    n=item['level'];order=item.get('order');level=levels[n]
    if not order:continue
    points=[tuple(level['depot']),*[tuple(h['p']) for h in level['homes']]]
    route=[list(points[0])];mask=0;failed_at=None
    for target in order[1:]:
        segment=leg(level,points,mask,route,target)
        if segment is None:failed_at=target;break
        route.extend([list(p) for p in segment[1:]])
        if target:mask|=1<<(target-1)
    rows.append({'level':n,'order':order,'referenceSteps':item['verifiedRouteSteps'],
                 'staticCandidateRoute':route if failed_at is None else None,
                 'echoAwareSteps':len(route)-1 if failed_at is None else None,
                 'failedAtHouse':failed_at})
output={'scope':'Echo-safe static legs for a preselected delivery order; moving actors, lantern and aftershock timer ignored.',
        'source':str(args.input),'neighborOrder':args.neighbor_order,'rows':rows}
args.output.write_text(json.dumps(output,indent=2),encoding='utf-8')
print(json.dumps({'levels':len(rows),'routes':sum(x['staticCandidateRoute'] is not None for x in rows),
                  'shorter':sum(x['echoAwareSteps'] is not None and x['echoAwareSteps']<x['referenceSteps'] for x in rows)}))
