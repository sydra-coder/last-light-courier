"""Author one-light bridges for River of Glass levels 701–800."""
from pathlib import Path
from collections import Counter
import argparse,json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design'/'map-solutions-1000.json')
parser.add_argument('--out',type=Path,default=ROOT/'campaign'/'enhanced'/'light-bridges-v1')
args=parser.parse_args()
OUT=args.out
OUT.mkdir(parents=True,exist_ok=True)
entries=json.loads(args.solutions.read_text(encoding='utf-8'))['levels'][700:800]
assert [e['level'] for e in entries]==list(range(701,801))

authored=[];proofs=[]
for entry in entries:
    l=entry['map'];states=entry['solutions'][0]['route'];points=[s['p'] for s in states]
    first=next(i for i,s in enumerate(states) if s['mask'])
    counts=Counter(map(tuple,points))
    special={tuple(l[k]) for k in ('depot','fade','ice','dark','switch','gate') if l[k]}
    special.update(tuple(h['p']) for h in l['homes'])
    if l.get('repair'):special.add(tuple(l['repair']['tile']))
    candidates=[]
    for i in range(first+2,len(points)-5):
        tile=points[i]
        if tuple(tile) in special or counts[tuple(tile)]!=1:continue
        minimum_future=min(s['light'] for s in states[i:])
        if minimum_future<2:continue
        candidates.append((abs(i-len(points)*.55),i,minimum_future,tile))
    assert candidates,l['n']
    _,i,minimum_future,tile=min(candidates)
    item=dict(l)
    item['lightBridge']=tile
    item['bridgeCost']=1
    item['lightBridgeRequiresPower']=True
    item['brief']=l['brief']+' After your first delivery, use the Light Bridge charge and one lantern light to build the marked crossing.'
    authored.append(item)
    proofs.append({'level':l['n'],'bridge':tile,'firstDeliveryStep':first,
                   'bridgeEntryStep':i,'powerUseBeforeStep':i,'minimumLightAfterEntryWithoutBridge':minimum_future,
                   'routeSteps':entry['solutions'][0]['steps']})

assert len(authored)==len(proofs)==100
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(proofs,separators=(',',':')),encoding='utf-8')
print('Authored 100 one-light bridges in levels 701–800.')
