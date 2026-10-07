"""Choose a second-delivery gate on a recorded route, off its opening prefix."""
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

def distance(level,start,walls):
    size=level['grid'];q=deque([start]);found={start:0}
    while q:
        x,y=q.popleft()
        for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=p[0]<size and 0<=p[1]<size and p not in walls and p not in found:
                found[p]=found[(x,y)]+1;q.append(p)
    return found

report=[]
for n in (1625,2000):
    level=levels[n-1];route=proofs[n]['route']
    second_step=next(i for i,s in enumerate(route) if s['mask'].bit_count()>=2)
    third_step=next(i for i,s in enumerate(route) if s['mask'].bit_count()>=3)
    second=tuple(route[second_step]['p'])
    prefix={tuple(s['p']) for s in route[:second_step+1]}
    protected=set(coords(level))
    walls={tuple(map(int,s.split(','))) for s in level['walls']}
    repair=tuple(level['repair']['tile']);event=tuple(level['authoredEvent']['tile'])
    targets=[tuple(h['p']) for h in level['homes'] if not route[second_step]['mask']&(1<<level['homes'].index(h))]
    targets.append(tuple(level['depot']))
    base=(walls-{repair})|{event,tuple(level['chainEvent']['close'])}
    after=distance(level,second,base)
    candidates=[]
    for i in range(second_step+1,third_step):
        tile=tuple(route[i]['p'])
        if tile in prefix or tile in protected or tile in walls:continue
        before=distance(level,second,base|{tile})
        affected=sum(t in after and (t not in before or before[t]>after[t]) for t in targets)
        if not affected:continue
        candidates.append({'tile':list(tile),'routeStep':i,'stepsAfterSecond':i-second_step,
                           'affectedTargets':affected})
    candidates.sort(key=lambda x:(-x['affectedTargets'],x['stepsAfterSecond']))
    report.append({'level':n,'secondDeliveryStep':second_step,'thirdDeliveryStep':third_step,
                   'oldOpen':level['chainEvent']['open'],'candidates':candidates})
output=root/'campaign/enhanced/repair-chain-gate-search.json'
output.write_text(json.dumps(report,indent=2))
print(json.dumps([{'level':x['level'],'candidates':len(x['candidates']),
                   'best':x['candidates'][:6]} for x in report]))
