"""Replace bridge uses in archived routes with geometric detours for rule replay."""
from collections import deque
from pathlib import Path
import json
import os

ROOT=Path(__file__).resolve().parents[3]
preview=Path(os.environ.get('LLC_PREVIEW_PATH',ROOT/'design/campaign-2000-preview/index.html'))
line=next(line for line in preview.open(encoding='utf-8') if line.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
archive=json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))['levels']
orders=['EWSN','ENWS','WSEN','NESW','SWNE']
directions={'E':(1,0),'W':(-1,0),'N':(0,-1),'S':(0,1)}

def shortest(level,a,b,order,extra_block=None):
    walls={tuple(map(int,w.split(','))) for w in level['walls']}
    walls.add(tuple(level['lightBridge']))
    if extra_block is not None:walls.add(tuple(extra_block))
    repair=level.get('repair')
    if repair and repair.get('effect')=='open':walls.discard(tuple(repair['tile']))
    a,b=tuple(a),tuple(b)
    q=deque([a]);parents={a:None}
    while q:
        x,y=q.popleft()
        for char in order:
            dx,dy=directions[char];p=(x+dx,y+dy)
            if p==tuple(level['depot']) and p!=b:continue
            if 0<=p[0]<level['grid'] and 0<=p[1]<level['grid'] and p not in walls and p not in parents:
                parents[p]=(x,y);q.append(p)
        if b in parents:break
    if b not in parents:return None
    path=[b]
    while path[-1]!=a:path.append(parents[path[-1]])
    return [list(p) for p in reversed(path)]

rows=[]
for number in range(701,801):
    level=levels[number-1]
    old=[s['p'] for s in archive[number-1]['solutions'][0]['route']]
    bridge=level['lightBridge']
    for order in orders:
        route=[old[0]];i=1;uses=0;failed=False
        while i<len(old):
            if old[i]==bridge:
                if i+1>=len(old):failed=True;break
                path=shortest(level,route[-1],old[i+1],order)
                if path is None:failed=True;break
                route.extend(path[1:]);uses+=1;i+=2
            else:route.append(old[i]);i+=1
        if not failed:rows.append({'level':number,'order':order,'bridgeUsesReplaced':uses,'steps':len(route)-1,'route':route})
Path(os.environ.get('LLC_BRIDGE_TOURS_OUT',Path(__file__).with_name('bridge_detour_tours.json'))).write_text(json.dumps(rows,separators=(',',':')),encoding='utf-8')
print(f'Generated {len(rows)} detour candidates')
