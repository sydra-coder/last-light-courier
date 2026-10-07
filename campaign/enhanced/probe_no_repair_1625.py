"""Generate optimistic no-repair routes using the second-delivery chain opening."""
from collections import deque
from itertools import permutations
from pathlib import Path
import json

root=Path(__file__).resolve().parents[2]
line=next(s for s in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if s.startswith('const LEVELS='))
level=json.loads(line[len('const LEVELS='):-2])[1624]
homes=[tuple(x['p']) for x in level['homes']];depot=tuple(level['depot'])
base={tuple(map(int,s.split(','))) for s in level['walls']}
event=tuple(level['authoredEvent']['tile']);chain=level['chainEvent']

def path(start,goal,walls,order,block_depot):
    q=deque([start]);prev={start:None};size=level['grid']
    dirs={'E':(1,0),'W':(-1,0),'N':(0,-1),'S':(0,1)}
    while q:
        p=q.popleft()
        if p==goal:
            out=[]
            while p is not None:out.append(p);p=prev[p]
            return list(reversed(out))
        for c in order:
            dx,dy=dirs[c];n=(p[0]+dx,p[1]+dy)
            if not(0<=n[0]<size and 0<=n[1]<size) or n in walls or n in prev or block_depot and n==depot:continue
            prev[n]=p;q.append(n)
    return None

rows=[]
for first_two in permutations((3,4)):
    for tail in permutations((0,1,2)):
        order=first_two+tail
        for direction in ('ENWS','WSEN','NESW','SWNE','EWSN'):
            route=[depot];last=depot;valid=True
            for i,target_index in enumerate(order):
                walls=set(base)
                if i>=1:walls.add(event)
                if i>=2:
                    walls.add(tuple(chain['close']))
                    for tile in chain['open']:walls.discard(tuple(tile))
                segment=path(last,homes[target_index],walls,direction,True)
                if not segment:valid=False;break
                route.extend(segment[1:]);last=homes[target_index]
            if not valid:continue
            walls=(base|{event,tuple(chain['close'])})-{tuple(x) for x in chain['open']}
            segment=path(last,depot,walls,direction,False)
            if not segment:continue
            route.extend(segment[1:])
            rows.append({'order':order,'directions':direction,'steps':len(route)-1,
                         'route':[list(p) for p in route]})
output=root/'campaign/enhanced/no-repair-1625-candidates.json'
output.write_text(json.dumps(rows))
print({'candidates':len(rows),'shortest':min((x['steps'] for x in rows),default=None)})
