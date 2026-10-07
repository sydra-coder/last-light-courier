"""Certify recorded late routes only when they meet a safely relaxed tour bound.

The relaxed graph ignores shadows, light, timing, one-way rules and closures.
It opens every wall that any event or repair can remove, and offers transit
from the start. Its shortest delivery tour cannot exceed a legal run's steps.
"""
from collections import deque
from pathlib import Path
import json

root=Path(__file__).resolve().parents[2]
line=next(s for s in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
proofs=json.loads((root/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text())

def point(p):return tuple(p)

def distances(level,start,walls):
    size=level['grid'];q=deque([start]);seen={start:0}
    transit=level.get('transitLink',{}).get('stops')
    stops=[point(p) for p in transit] if transit else []
    while q:
        x,y=q.popleft();neighbors=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        if stops and (x,y) in stops:neighbors.append(stops[1] if (x,y)==stops[0] else stops[0])
        for p in neighbors:
            if not (0<=p[0]<size and 0<=p[1]<size) or p in walls or p in seen:continue
            seen[p]=seen[(x,y)]+1;q.append(p)
    return seen

def bound(level):
    walls={tuple(map(int,s.split(','))) for s in level['walls']}
    opened=[]
    if level.get('repair',{}).get('effect')=='open':opened.append(level['repair']['tile'])
    for name in ('quakeEvent','chainEvent'):
        opened.extend(level.get(name,{}).get('open',[]))
    for p in opened:walls.discard(point(p))
    sites=[point(level['depot']),*[point(h['p']) for h in level['homes']]]
    maps=[distances(level,p,walls) for p in sites]
    matrix=[[m.get(p) for p in sites] for m in maps]
    count=len(sites)-1
    dp={(1<<i,i):matrix[0][i+1] for i in range(count) if matrix[0][i+1] is not None}
    for mask in range(1,1<<count):
        for i in range(count):
            value=dp.get((mask,i))
            if value is None:continue
            for j in range(count):
                if mask&(1<<j) or matrix[i+1][j+1] is None:continue
                key=(mask|(1<<j),j);candidate=value+matrix[i+1][j+1]
                if candidate<dp.get(key,10**9):dp[key]=candidate
    return min((dp[((1<<count)-1,i)]+matrix[i+1][0] for i in range(count)
                if ((1<<count)-1,i) in dp and matrix[i+1][0] is not None),default=None)

rows=[]
for proof in proofs:
    n=proof['level'];level=levels[n-1]
    assert n>=1001 and level['n']==n and level['required']==len(level['homes'])
    lower=bound(level);steps=len(proof['route'])-1
    assert steps==proof['steps']
    rows.append({'level':n,'optimisticBound':lower,'recordedSteps':steps,
                 'gap':None if lower is None else steps-lower,
                 'certifiedExact':lower==steps})
bad=[r for r in rows if r['gap'] is not None and r['gap']<0]
missing=[r for r in rows if r['optimisticBound'] is None]
if bad or missing:raise RuntimeError(f'Invalid relaxation: {bad[:3]}, unreachable: {missing[:3]}')
report={'scope':'Walking routes through a relaxed grid: dynamic walls removed; closures, shadows, light and one-way limits ignored; transit offered from start.',
        'levels':len(rows),'certifiedExact':sum(r['certifiedExact'] for r in rows),
        'medianGap':sorted(r['gap'] for r in rows)[len(rows)//2],
        'rows':rows}
output=root/'campaign/enhanced/optimistic-route-bounds.json'
output.write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='rows'}))
