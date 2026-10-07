"""Find a single non-reference wall that makes the bridge an objective cut."""
from collections import deque
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[3]
line=next(line for line in (ROOT/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if line.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
archive=json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))['levels']

def missing(level,walls):
    q=deque([tuple(level['depot'])]);seen={q[0]}
    while q:
        x,y=q.popleft()
        for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=p[0]<level['grid'] and 0<=p[1]<level['grid'] and p not in walls and p not in seen:
                seen.add(p);q.append(p)
    return [i for i,h in enumerate(level['homes']) if tuple(h['p']) not in seen]

results=[]
for number in range(701,801):
    l=levels[number-1]
    walls={tuple(map(int,w.split(','))) for w in l['walls']}
    old=[tuple(s['p']) for s in archive[number-1]['solutions'][0]['route']]
    protected=set(old)|{tuple(l['depot']),tuple(l['lightBridge'])}|{tuple(h['p']) for h in l['homes']}
    possible=[]
    for y in range(l['grid']):
        for x in range(l['grid']):
            p=(x,y)
            if p in walls or p in protected:continue
            no_bridge=walls|{p,tuple(l['lightBridge'])}
            cut=missing(l,no_bridge)
            if cut and not missing(l,walls|{p}):possible.append({'wall':[x,y],'unreachableHomes':cut})
    results.append({'level':number,'singleWallCuts':possible})

Path(__file__).with_name('single_wall_cuts.json').write_text(json.dumps(results,separators=(',',':')),encoding='utf-8')
print('Levels with an available single-wall cut:',sum(bool(x['singleWallCuts']) for x in results))
print('Verified bypass levels with a cut:',[x['level'] for x in results if x['singleWallCuts'] and x['level'] in {702,707,711,715,718,726,728,729,737,741,743,750,753,756,760,762,764,769,771,782,785,786,793,797}])
