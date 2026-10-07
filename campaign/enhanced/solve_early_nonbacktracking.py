"""Optimistic route search honoring Echo's no-immediate-reversal rule."""
from collections import deque
from pathlib import Path
import json,os

here=Path(__file__).resolve().parent
root=here.parents[1]
n=int(os.environ.get('LLC_EARLY_LEVEL','301'))
line=next(x for x in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if x.startswith('const LEVELS='))
level=json.loads(line[13:-2])[n-1]
size=level['grid'];depot=tuple(level['depot']);homes={tuple(h['p']):i for i,h in enumerate(level['homes'])}
walls={tuple(map(int,s.split(','))) for s in level['walls']}
repair=level.get('repair')
if level.get('repairRequired') and repair and repair.get('effect')=='open' and repair.get('cost')==0:
    walls.discard(tuple(repair['tile']))
bridge=tuple(level['lightBridge']) if level.get('lightBridgeRequiresPower') else None
if bridge:walls.discard(bridge)
oneway=tuple(level['oneWayTile']) if level.get('oneWayTile') else None
oneway_from=tuple(level['oneWayFrom']) if level.get('oneWayFrom') else None
full=(1<<len(homes))-1
start=(0,depot[0],depot[1],-1);parent={start:None};queue=deque([start]);goal=None
while queue:
    state=queue.popleft();mask,x,y,previous=state
    if mask==full and (x,y)==depot:goal=state;break
    for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
        p=(nx,ny);index=ny*size+nx
        if not(0<=nx<size and 0<=ny<size) or p in walls or index==previous:continue
        if bridge==p and mask==0:continue
        if oneway==p and (x,y)!=oneway_from:continue
        nextmask=mask|(1<<homes[p]) if p in homes else mask
        nextstate=(nextmask,nx,ny,y*size+x)
        if nextstate not in parent:parent[nextstate]=state;queue.append(nextstate)
if goal:
    route=[];state=goal
    while state is not None:
        route.append([state[1],state[2]]);state=parent[state]
    route.reverse();seen=set();order=[]
    for p in route:
        if tuple(p) in homes and homes[tuple(p)] not in seen:seen.add(homes[tuple(p)]);order.append(homes[tuple(p)])
    result={'level':n,'steps':len(route)-1,'order':order,'route':route,'states':len(parent),
            'scope':'Static walls, required free road repair, post-delivery bridge, one-way entry and Echo no-immediate-reversal; ignores patrol, light and other conditional roads.'}
else:result={'level':n,'steps':None,'states':len(parent),'scope':'No route under static walls and no-immediate-reversal.'}
output=here/f'early-nonbacktracking-{n}.json';output.write_text(json.dumps(result,indent=2))
print(json.dumps({k:result.get(k) for k in ('level','steps','order','states')}))
