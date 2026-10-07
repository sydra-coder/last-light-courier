"""Place deterministic pursuing Hunters in Hunting Dark, levels 501-600."""
from pathlib import Path
from collections import deque
import argparse,json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design/map-solutions-1000.json')
parser.add_argument('--sentinels',type=Path,default=ROOT/'campaign/enhanced/sentinels-v1/authored_levels.json')
parser.add_argument('--out',type=Path,default=ROOT/'campaign/enhanced/hunters-v1')
args=parser.parse_args()
OUT=args.out;OUT.mkdir(parents=True,exist_ok=True)
levels=json.loads(args.sentinels.read_text(encoding='utf-8'))
entries=json.loads(args.solutions.read_text(encoding='utf-8'))['levels']
assert len(levels)==100 and [l['n'] for l in levels]==list(range(501,601))
key=lambda p:f'{p[0]},{p[1]}'
DIRS=((0,-1),(1,0),(0,1),(-1,0))

def distance_map(target,roads):
    todo=deque([(target,0)]);dist={target:0}
    while todo:
        p,d=todo.popleft()
        for dx,dy in DIRS:
            q=(p[0]+dx,p[1]+dy)
            if q in roads and q not in dist:dist[q]=d+1;todo.append((q,d+1))
    return dist

authored=[];proofs=[];failed=[]
for level in levels:
    solution=entries[level['n']-1]['solutions'][0]
    route=[tuple(s['p']) for s in solution['route']]
    first=next(i for i,s in enumerate(solution['route']) if s['mask'])
    walls=set(level['walls'])
    if solution['repairPurchased'] and level.get('repair') and level['repair']['effect']=='open':
        walls.discard(key(level['repair']['tile']))
    roads={(x,y) for y in range(level['grid']) for x in range(level['grid']) if key((x,y)) not in walls}
    special={tuple(level[k]) for k in ('depot','fade','ice','dark','switch','gate','sentinelCenter') if level.get(k)}
    special.update(tuple(h['p']) for h in level['homes'])
    if level.get('repair'):special.add(tuple(level['repair']['tile']))
    special.update(tuple(p) for p in (level['patrol'] or [])+(level['patrol2'] or []))
    dist_cache={p:distance_map(p,roads) for p in set(route[first+1:])}
    choices=[]
    for den in sorted(roads-special-set(route)):
        if min(abs(den[0]-p[0])+abs(den[1]-p[1]) for p in route[first+1:first+25])>5:continue
        pos=den;near=0;closest=99;first_near=None;safe=True
        for t in range(first+1,len(route)):
            courier=route[t]
            if courier==pos:safe=False;break
            if (t-first)%2==0:
                distances=dist_cache[courier]
                options=[(pos[0]+dx,pos[1]+dy) for dx,dy in DIRS]
                options=[q for q in options if q in roads]
                if options:pos=min(options,key=lambda q:distances.get(q,10**9))
            if courier==pos:safe=False;break
            distance=abs(courier[0]-pos[0])+abs(courier[1]-pos[1])
            closest=min(closest,distance)
            if distance<=2:
                near+=1
                if first_near is None:first_near=t
        if safe and near>=1:
            choices.append((min(near,12),-first_near,-closest,den,near,first_near))
    if not choices:
        failed.append(level['n']);continue
    _,_,_,den,near,first_near=max(choices)
    item=dict(level)
    item['hunterDen']=list(den)
    item['hunterCadence']=2
    item['hunterWakes']='first_delivery'
    item['brief']=level['brief']+' A Hunter wakes after the first delivery. It takes one shortest-path step toward you every two courier moves.'
    authored.append(item)
    proofs.append({'level':level['n'],'den':list(den),'firstDeliveryStep':first,
                   'nearSteps':near,'firstNearStep':first_near,'routeSteps':solution['steps']})

(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(proofs,separators=(',',':')),encoding='utf-8')
(OUT/'report.json').write_text(json.dumps({'attempted':100,'authored':len(authored),'failed':failed},indent=2),encoding='utf-8')
print(f'Hunters {len(authored)}/100; failed={failed}')
