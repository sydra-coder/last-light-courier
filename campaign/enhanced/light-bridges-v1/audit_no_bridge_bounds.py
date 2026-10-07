"""Optimistic no-bridge step/light bounds for levels 701–800.

This ignores patrols, Echo, timers, and costly tiles. A bound above the maximum
possible light proves no-power completion impossible; other results are unknown.
"""
from collections import deque
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[3]
line=next(line for line in (ROOT/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if line.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])[700:800]
rows=[]

def bfs(level,start,walls):
    dist={tuple(start):0}; queue=deque([tuple(start)])
    while queue:
        x,y=queue.popleft()
        for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=p[0]<level['grid'] and 0<=p[1]<level['grid'] and p not in walls and p not in dist:
                dist[p]=dist[(x,y)]+1;queue.append(p)
    return dist

for l in levels:
    walls={tuple(map(int,key.split(','))) for key in l['walls']}
    walls.add(tuple(l['lightBridge']))
    repair=l.get('repair')
    if repair and repair.get('effect')=='open':walls.discard(tuple(repair['tile']))
    points=[tuple(l['depot'])]+[tuple(h['p']) for h in l['homes']]
    distances=[bfs(l,p,walls) for p in points]
    missing=[i for i,p in enumerate(points) if p not in distances[0]]
    shortest=None
    if not missing:
        n=len(points)-1;all_bits=(1<<n)-1
        dp={(1<<i,i):distances[0][points[i+1]] for i in range(n)}
        for mask in range(1,all_bits+1):
            for j in range(n):
                current=dp.get((mask,j))
                if current is None:continue
                for k in range(n):
                    if mask&(1<<k):continue
                    key=(mask|1<<k,k);candidate=current+distances[j+1][points[k+1]]
                    dp[key]=min(dp.get(key,10**9),candidate)
        shortest=min(dp[(all_bits,j)]+distances[j+1][points[0]] for j in range(n))
    # Initial cap plus two light for each first delivery. An optional beacon
    # repair raises cap by three; allow it optimistically even if unaffordable.
    maximum_light=l['cap']+2*len(l['homes'])+(3 if repair and repair.get('effect')=='beacon' else 0)
    status='geometrically blocked' if missing else 'light-bound impossible' if shortest>=maximum_light else 'not disproved'
    rows.append({'level':l['n'],'noBridgeGeometricSteps':shortest,'optimisticLightBudget':maximum_light,'status':status,'unreachablePoints':missing})

output=Path(__file__).with_name('no_bridge_bounds.json')
output.write_text(json.dumps({'scope':'Optimistic static lower bound only; no no-power completion claim','rows':rows},indent=2),encoding='utf-8')
from collections import Counter
print(Counter(row['status'] for row in rows))
print('Not disproved:',[row['level'] for row in rows if row['status']=='not disproved'])
