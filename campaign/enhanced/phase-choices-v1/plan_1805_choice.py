"""Find closure tiles that force a local detour on level 1805's live fast route."""
from pathlib import Path
from collections import deque
import json,os

root=Path(__file__).resolve().parents[3]
here=Path(__file__).resolve().parent
line=next(x for x in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if x.startswith('const LEVELS='))
n=int(os.environ.get('LLC_CHOICE_LEVEL','1805'))
level=json.loads(line[13:-2])[n-1]
checkpoints=json.loads((here.parent/'reference-hints-v1/normalized_routes.json').read_text())[n-201]
route=[tuple(x[:2]) for x in checkpoints]
first=next(i for i,x in enumerate(checkpoints) if x[2])
walls={tuple(map(int,x.split(','))) for x in level['walls']}
protected={tuple(level['depot']),*(tuple(h['p']) for h in level['homes'])}
for name in ('fade','ice','dark','switch','gate','oneWayTile','lightBridge','shadowDoor','shadowLock'):
    if level.get(name) and isinstance(level[name],list) and len(level[name])==2 and all(isinstance(v,int) for v in level[name]):
        protected.add(tuple(level[name]))
def shortest(a,b,blocked):
    q=deque([a]);parents={a:None}
    while q:
        p=q.popleft()
        if p==b:
            out=[]
            while p is not None:out.append(p);p=parents[p]
            return list(reversed(out))
        for t in ((p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)):
            if 0<=t[0]<level['grid'] and 0<=t[1]<level['grid'] and t not in walls and t!=blocked and t not in parents:
                parents[t]=p;q.append(t)
    return None
candidates=[]
for i in range(first+2,len(route)-2):
    tile=route[i]
    if tile in protected or tile in walls or tile in route[:first+1]:continue
    # Replace a single used tile with a legal nearby detour. Avoid another
    # required delivery inside the replacement, then let full replay judge it.
    around=shortest(route[i-1],route[i+1],tile)
    if not around or any(p in protected for p in around[1:-1]):continue
    extra=len(around)-3
    if 2<=extra<=8:
        candidate=route[:i]+around[1:-1]+route[i+1:]
        candidates.append({'close':tile,'atStep':i,'extraSteps':extra,'route':[list(p) for p in candidate]})
candidates.sort(key=lambda x:(-x['extraSteps'],x['atStep']))
out=here/f'level-{n}-choice-candidates.json'
out.write_text(json.dumps({'level':n,'firstDeliveryStep':first,'candidates':candidates},indent=2))
print(json.dumps({'level':n,'firstDeliveryStep':first,'candidates':len(candidates),
                  'best':[{'tile':x['close'],'step':x['atStep'],'extra':x['extraSteps']} for x in candidates[:10]]}))
