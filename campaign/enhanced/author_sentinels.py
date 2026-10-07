"""Author stationary 3×3 Sentinel influence in levels 501–600."""
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design'/'map-solutions-1000.json')
parser.add_argument('--out',type=Path,default=ROOT/'campaign'/'enhanced'/'sentinels-v1')
args=parser.parse_args()
OUT=args.out
OUT.mkdir(parents=True,exist_ok=True)
entries=json.loads(args.solutions.read_text(encoding='utf-8'))['levels'][500:600]
assert [e['level'] for e in entries]==list(range(501,601))

authored=[];proofs=[]
for entry in entries:
    l=entry['map'];route=entry['solutions'][0]['route']
    activation=next(i for i,s in enumerate(route) if s['mask'])
    future=[s['p'] for s in route[activation:]]
    walls=set(l['walls']);options=[]
    for y in range(1,l['grid']-1):
        for x in range(1,l['grid']-1):
            if f'{x},{y}' in walls:continue
            if any(max(abs(x-p[0]),abs(y-p[1]))<=1 for p in future):continue
            proximity=min(max(abs(x-p[0]),abs(y-p[1])) for p in future)
            if proximity>2:continue
            open_zone=sum(f'{x+dx},{y+dy}' not in walls for dx in (-1,0,1) for dy in (-1,0,1))
            if open_zone<4:continue
            options.append((-open_zone,abs(x-l['grid']//2)+abs(y-l['grid']//2),x,y))
    assert options,l['n']
    _,_,x,y=min(options)
    item=dict(l)
    item['sentinelCenter']=[x,y]
    item['sentinelRadius']=1
    item['brief']=l['brief']+' A stationary Sentinel wakes after the first delivery and controls a 3×3 area.'
    authored.append(item)
    proofs.append({'level':l['n'],'center':[x,y],'activationStep':activation,
                   'routeSteps':entry['solutions'][0]['steps'],
                   'influenceOpenTiles':-min(options)[0]})

assert len(authored)==len(proofs)==100
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(proofs,separators=(',',':')),encoding='utf-8')
print('Authored 100 stationary 3×3 Sentinel fields in levels 501–600.')
