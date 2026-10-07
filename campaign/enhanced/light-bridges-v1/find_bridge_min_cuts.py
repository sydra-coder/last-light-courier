"""Measure minimum street cuts needed to require each Light Bridge geometrically."""
from collections import deque,Counter
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[3]
line=next(line for line in (ROOT/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if line.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
archive=json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))['levels']
INF=10000

def minimum_cut(level,walls,protected,target):
    size=level['grid'];tiles=[(x,y) for y in range(size) for x in range(size) if (x,y) not in walls]
    ids={p:i for i,p in enumerate(tiles)};graph=[[] for _ in range(2*len(tiles))]
    def edge(a,b,cap):
        graph[a].append([b,cap,len(graph[b])]);graph[b].append([a,0,len(graph[a])-1])
    for p,i in ids.items():
        edge(2*i,2*i+1,INF if p in protected else 1)
        x,y=p
        for q in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if q in ids:edge(2*i+1,2*ids[q],INF)
    source=2*ids[tuple(level['depot'])]+1;sink=2*ids[target]
    flow=0
    while flow<INF:
        level_of=[-1]*len(graph);level_of[source]=0;queue=deque([source])
        while queue:
            a=queue.popleft()
            for b,capacity,_ in graph[a]:
                if capacity>0 and level_of[b]<0:level_of[b]=level_of[a]+1;queue.append(b)
        if level_of[sink]<0:break
        cursor=[0]*len(graph)
        def push(a,limit):
            if a==sink:return limit
            while cursor[a]<len(graph[a]):
                i=cursor[a];b,capacity,reverse=graph[a][i]
                if capacity>0 and level_of[b]==level_of[a]+1:
                    used=push(b,min(limit,capacity))
                    if used:
                        graph[a][i][1]-=used;graph[b][reverse][1]+=used;return used
                cursor[a]+=1
            return 0
        while (used:=push(source,INF)):flow+=used
    seen={source};queue=deque([source])
    while queue:
        a=queue.popleft()
        for b,capacity,_ in graph[a]:
            if capacity>0 and b not in seen:seen.add(b);queue.append(b)
    cut=[p for p,i in ids.items() if 2*i in seen and 2*i+1 not in seen]
    return flow,cut

rows=[]
for number in range(701,801):
    level=levels[number-1];walls={tuple(map(int,s.split(','))) for s in level['walls']}
    repair=level.get('repair')
    if repair and repair.get('effect')=='open':walls.discard(tuple(repair['tile']))
    walls.add(tuple(level['lightBridge']))
    protected={tuple(step['p']) for step in archive[number-1]['solutions'][0]['route']}
    protected|={tuple(level['depot'])}|{tuple(h['p']) for h in level['homes']}
    protected-=walls
    seen={tuple(level['depot'])};queue=deque(seen)
    while queue:
        x,y=queue.popleft()
        for tile in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if tile in protected and tile not in seen:seen.add(tile);queue.append(tile)
    reference_connected=sum(tuple(h['p']) in seen for h in level['homes'])
    options=[]
    for home in level['homes']:
        flow,cut=minimum_cut(level,walls,protected,tuple(home['p']))
        options.append((flow,cut,home['p']))
    flow,cut,target=min(options,key=lambda x:x[0])
    rows.append({'level':number,'minimumExtraWalls':flow if flow<INF else None,
                 'referenceCellsAlreadyConnectHomesWithoutBridge':reference_connected,'cut':[list(p) for p in cut],
                 'separatesHome':target})
output=Path(__file__).with_name('bridge_min_cut_screen.json')
output.write_text(json.dumps({'scope':'Static no-bridge vertex cuts with archived powered route protected; candidate walls require full rule and variety replay.','rows':rows},indent=2),encoding='utf-8')
print('Minimum wall counts:',dict(sorted(Counter(r['minimumExtraWalls'] for r in rows).items(),key=lambda x:(x[0] is None,x[0] or 0))))
print('Existing reference-cell network reaches all houses without bridge:',sum(r['referenceCellsAlreadyConnectHomesWithoutBridge']==len(levels[r['level']-1]['homes']) for r in rows))
print('First ten:',[(r['level'],r['minimumExtraWalls'],r['cut']) for r in rows[:10]])
