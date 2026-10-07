"""Replay every authored Hunter chase against the archived completion route."""
from pathlib import Path
from collections import deque
import argparse,json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design/map-solutions-1000.json')
parser.add_argument('--base',type=Path,default=ROOT/'campaign/enhanced/hunters-v1')
args=parser.parse_args()
BASE=args.base
levels=json.loads((BASE/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((BASE/'route_proofs.json').read_text(encoding='utf-8'))
entries=json.loads(args.solutions.read_text(encoding='utf-8'))['levels']
assert len(levels)==len(proofs)>=40
assert [l['n'] for l in levels]==[p['level'] for p in proofs]
DIRS=((0,-1),(1,0),(0,1),(-1,0))
for level,proof in zip(levels,proofs):
    n=level['n'];assert 501<=n<=600 and level['hunterCadence']==2
    states=entries[n-1]['solutions'][0]['route']
    route=[tuple(s['p']) for s in states]
    first=next(i for i,s in enumerate(states) if s['mask'])
    assert first==proof['firstDeliveryStep'] and len(route)-1==proof['routeSteps']
    walls=set(level['walls'])
    repair=level.get('repair')
    if level['repairRequired'] and repair and repair['effect']=='open':
        walls.discard(f"{repair['tile'][0]},{repair['tile'][1]}")
    roads={(x,y) for y in range(level['grid']) for x in range(level['grid']) if f'{x},{y}' not in walls}
    hunter=tuple(level['hunterDen']);assert hunter==tuple(proof['den']) and hunter in roads
    near=0;first_near=None
    for t in range(first+1,len(route)):
        courier=route[t]
        assert courier!=hunter,(n,t,'entered Hunter tile')
        if (t-first)%2==0:
            queue=deque([courier]);distance={courier:0}
            while queue:
                p=queue.popleft()
                for dx,dy in DIRS:
                    q=(p[0]+dx,p[1]+dy)
                    if q in roads and q not in distance:
                        distance[q]=distance[p]+1;queue.append(q)
            choices=[(hunter[0]+dx,hunter[1]+dy) for dx,dy in DIRS]
            choices=[q for q in choices if q in roads]
            if choices:hunter=min(choices,key=lambda q:distance.get(q,10**9))
        assert courier!=hunter,(n,t,'Hunter caught courier')
        if abs(courier[0]-hunter[0])+abs(courier[1]-hunter[1])<=2:
            near+=1
            if first_near is None:first_near=t
    assert near==proof['nearSteps'] and first_near==proof['firstNearStep']
    assert route[-1]==tuple(level['depot']) and states[-1]['light']>=0
print(f'PASS: {len(levels)} Hunter chase routes complete; each Hunter approaches within two tiles.')
