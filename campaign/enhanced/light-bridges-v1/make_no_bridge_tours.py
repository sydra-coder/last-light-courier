"""Create geometric tours that avoid the powered bridge for rule replay.

These are candidate routes, not no-power proofs or global game-rule minima.
"""
from collections import deque
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[3]
line=next(line for line in (ROOT/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if line.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])[700:800]

def graph(level,start,walls,block_depot=False):
    dist={start:0};parent={};q=deque([start])
    while q:
        x,y=q.popleft()
        for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if block_depot and p==tuple(level['depot']):continue
            if 0<=p[0]<level['grid'] and 0<=p[1]<level['grid'] and p not in walls and p not in dist:
                dist[p]=dist[(x,y)]+1;parent[p]=(x,y);q.append(p)
    return dist,parent

def segment(parent,a,b):
    out=[b]
    while out[-1]!=a:out.append(parent[out[-1]])
    return list(reversed(out))[1:]

rows=[]
for l in levels:
    walls={tuple(map(int,x.split(','))) for x in l['walls']}
    walls.add(tuple(l['lightBridge']))
    repair=l.get('repair')
    if repair and repair.get('effect')=='open':walls.discard(tuple(repair['tile']))
    points=[tuple(l['depot'])]+[tuple(h['p']) for h in l['homes']]
    full=[graph(l,p,walls) for p in points]
    no_depot={i:graph(l,points[i],walls,True) for i in range(1,len(points))}
    n=len(points)-1;all_bits=(1<<n)-1
    distances=[[0 if i==j else (full[i][0] if i==0 or j==0 else no_depot[i][0])[points[j]] for j in range(n+1)] for i in range(n+1)]
    dp={(1<<j,j):distances[0][j+1] for j in range(n)}
    previous={(1<<j,j):-1 for j in range(n)}
    for mask in range(1,all_bits+1):
        for j in range(n):
            cost=dp.get((mask,j))
            if cost is None:continue
            for k in range(n):
                if mask&(1<<k):continue
                key=(mask|1<<k,k);candidate=cost+distances[j+1][k+1]
                if candidate<dp.get(key,10**9):dp[key]=candidate;previous[key]=j
    end=min(range(n),key=lambda j:dp[(all_bits,j)]+distances[j+1][0])
    order=[];mask=all_bits;j=end
    while j>=0:
        order.append(j+1);old=previous[(mask,j)];mask^=1<<j;j=old
    order=[0]+list(reversed(order))+[0]
    route=[points[0]]
    for a,b in zip(order,order[1:]):
        parents=full[a][1] if a==0 or b==0 else no_depot[a][1]
        route.extend(segment(parents,points[a],points[b]))
    rows.append({'level':l['n'],'steps':len(route)-1,'route':route})

Path(__file__).with_name('no_bridge_tours.json').write_text(json.dumps(rows,separators=(',',':')),encoding='utf-8')
print(f'Generated {len(rows)} no-bridge geometric tours')
