"""Find a static wall that stops a chain opening bypassing mandatory repair."""
from collections import deque
from pathlib import Path
import json

root=Path(__file__).resolve().parents[2]
line=next(s for s in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
proofs={x['level']:x for x in json.loads((root/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text())}

def coords(value):
    if isinstance(value,list):
        if len(value)==2 and all(isinstance(x,int) for x in value):yield tuple(value)
        else:
            for item in value:yield from coords(item)
    elif isinstance(value,dict):
        for name,item in value.items():
            if name not in ('walls','spine','route'):yield from coords(item)

def distances(level,start,walls):
    size=level['grid'];q=deque([start]);found={start:0}
    while q:
        x,y=q.popleft()
        for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=p[0]<size and 0<=p[1]<size and p not in walls and p not in found:
                found[p]=found[(x,y)]+1;q.append(p)
    return found

report=[]
for n in (1625,):
    level=levels[n-1];repair=tuple(level['repair']['tile'])
    opened=tuple(level['chainEvent']['open'][0]);closed=tuple(level['chainEvent']['close'])
    walls={tuple(map(int,s.split(','))) for s in level['walls']}
    protected=set(coords(level))|{tuple(s['p']) for s in proofs[n]['route']}
    homes=[tuple(h['p']) for h in level['homes']];depot=tuple(level['depot'])
    candidates=[]
    for x in range(level['grid']):
        for y in range(level['grid']):
            tile=(x,y)
            if tile in walls or tile in protected:continue
            no_repair=distances(level,depot,(walls-{opened})|{repair,closed,tile})
            unreachable=[i for i,p in enumerate(homes) if p not in no_repair]
            if len(homes)-len(unreachable)>=level['required']:continue
            repaired=distances(level,depot,(walls-{opened,repair})|{closed,tile})
            if not all(p in repaired for p in homes):continue
            before_walls=(walls-{repair})|{tile,closed}
            after_walls=(walls-{repair,opened})|{tile,closed}
            effects=0
            for source in homes:
                before=distances(level,source,before_walls)
                after=distances(level,source,after_walls)
                effects+=sum(t in after and (t not in before or after[t]<before[t])
                             for t in [depot,*homes] if t!=source)
            candidates.append({'tile':list(tile),'unreachableWithoutRepair':unreachable,
                               'openingAffectedConnections':effects,
                               'distanceFromOpening':abs(x-opened[0])+abs(y-opened[1])})
    candidates.sort(key=lambda x:(-x['openingAffectedConnections'],x['distanceFromOpening']))
    report.append({'level':n,'opening':list(opened),'candidates':candidates})
output=root/'campaign/enhanced/repair-bypass-wall-search.json'
output.write_text(json.dumps(report,indent=2))
print(json.dumps([{'level':x['level'],'candidates':len(x['candidates']),
                   'best':x['candidates'][:12]} for x in report]))
