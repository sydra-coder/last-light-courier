"""Find a meaningful first-delivery closure that preserves level 1004's route."""
from pathlib import Path
from collections import deque
import json,os

root=Path(__file__).resolve().parents[2]
n=int(os.environ.get('LLC_SALIENCE_LEVEL','1004'))
line=next(x for x in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if x.startswith('const LEVELS='))
level=json.loads(line[13:-2])[n-1]
route=json.loads((root/'campaign/enhanced/reference-hints-v1/normalized_routes.json').read_text())[n-201]
first=next(i for i,s in enumerate(route) if s[2])
source=tuple(route[first][:2]);targets=[tuple(h['p']) for h in level['homes'] if tuple(h['p'])!=source]+[tuple(level['depot'])]
walls={tuple(map(int,s.split(','))) for s in level['walls']}
used={tuple(s[:2]) for s in route[first+1:]}
protected={tuple(level['depot']),*(tuple(h['p']) for h in level['homes'])}
for name in ('fade','ice','dark','switch','gate'):
    if level.get(name):protected.add(tuple(level[name]))
for name in ('patrol','patrol2'):
    protected.update(tuple(p) for p in level.get(name,[]))
if level.get('repair'):protected.add(tuple(level['repair']['tile']))

def distances(extra=None):
    queue=deque([source]);found={source:0}
    while queue:
        x,y=queue.popleft()
        for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=p[0]<level['grid'] and 0<=p[1]<level['grid'] and p not in walls and p!=extra and p not in found:
                found[p]=found[(x,y)]+1;queue.append(p)
    return found

before=distances();rows=[]
for x in range(level['grid']):
    for y in range(level['grid']):
        p=(x,y)
        if p in walls or p in used or p in protected or p==source or p==tuple(level['authoredEvent']['tile']):continue
        after=distances(p)
        if any(t not in after for t in targets):continue
        increases=[after[t]-before[t] for t in targets]
        affected=sum(v>0 for v in increases)
        if affected:rows.append({'tile':[x,y],'affectedTargets':affected,'maxIncrease':max(increases),'sumIncrease':sum(increases)})
rows.sort(key=lambda r:(-r['affectedTargets'],-r['sumIncrease'],r['maxIncrease']))
output=root/f'campaign/enhanced/salient-event-{n}-candidates.json'
output.write_text(json.dumps({'level':n,'firstHouse':source,'current':level['authoredEvent']['tile'],'candidates':rows},indent=2))
print(json.dumps({'level':n,'candidates':len(rows),'top':rows[:8]}))
