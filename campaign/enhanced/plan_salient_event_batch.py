"""Find route-preserving closure candidates for currently weak late events."""
from pathlib import Path
from collections import deque,Counter
import json

root=Path(__file__).resolve().parents[2]
here=Path(__file__).resolve().parent
line=next(x for x in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if x.startswith('const LEVELS='))
levels=json.loads(line[13:-2])
routes=json.loads((here/'reference-hints-v1/normalized_routes.json').read_text())
weak=[x['level'] for x in json.loads((here/'event-salience-audit.json').read_text())['rows'] if x['affectedTargets']==0]

def points(value):
    if isinstance(value,list) and len(value)==2 and all(isinstance(v,int) for v in value):return [tuple(value)]
    if isinstance(value,list):return sum((points(v) for v in value),[])
    if isinstance(value,dict):return sum((points(v) for v in value.values()),[])
    return []

rows=[]
for n in weak:
    level=levels[n-1];route=routes[n-201]
    first=next(i for i,s in enumerate(route) if s[2]);source=tuple(route[first][:2])
    targets=[tuple(h['p']) for h in level['homes'] if tuple(h['p'])!=source]+[tuple(level['depot'])]
    walls={tuple(map(int,s.split(','))) for s in level['walls']}
    used={tuple(s[:2]) for s in route[first+1:]}
    protected={tuple(level['depot']),*(tuple(h['p']) for h in level['homes'])}
    for name in ('fade','ice','dark','switch','gate','patrol','patrol2','repair','stormWind','floodRoad','nightfall',
                 'dayNightCycle','shadowSpawner','lumenNetwork','lightOverloadGate','lightTransfer','chainEvent',
                 'transitLink','phaseChoice','aftershock','hiddenRoad','collapseTile','rechargeHouse',
                 'oneWayTile','lightBridge','shadowDoor','shadowLock','quakeEvent'):
        if level.get(name):protected.update(points(level[name]))
    size=level['grid']
    def distances(extra=None):
        found={source:0};queue=deque([source])
        while queue:
            x,y=queue.popleft()
            for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                if 0<=p[0]<size and 0<=p[1]<size and p not in walls and p!=extra and p not in found:
                    found[p]=found[(x,y)]+1;queue.append(p)
        return found
    before=distances();candidates=[]
    for x in range(size):
        for y in range(size):
            p=(x,y)
            if p in walls or p in used or p in protected or p==source or p==tuple(level['authoredEvent']['tile']):continue
            after=distances(p)
            if any(t not in after for t in targets):continue
            increases=[after[t]-before[t] for t in targets]
            affected=sum(v>0 for v in increases)
            if affected:candidates.append({'tile':[x,y],'affectedTargets':affected,'maxIncrease':max(increases),'sumIncrease':sum(increases)})
    candidates.sort(key=lambda r:(-r['affectedTargets'],-r['sumIncrease'],r['maxIncrease']))
    rows.append({'level':n,'oldTile':level['authoredEvent']['tile'],'candidates':candidates[:15],
                 'totalCandidates':len(candidates)})
output=here/'salient-event-batch-plan.json'
output.write_text(json.dumps({'scope':'Static target-distance effect and current canonical-route preservation; requires full-rule replay and event topology verification.',
                              'rows':rows},indent=2))
print(json.dumps({'weak':len(rows),'withCandidate':sum(bool(r['candidates']) for r in rows),
                  'byBand':dict(Counter((r['level']-1)//100 for r in rows if r['candidates']))}))
