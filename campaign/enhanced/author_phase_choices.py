"""Author two player-selected first-delivery road states for 1801–1900."""
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--candidates',type=Path,default=ROOT/'campaign/enhanced/candidates-v3')
parser.add_argument('--out',type=Path,default=ROOT/'campaign/enhanced/phase-choices-v1')
args=parser.parse_args()
OUT=args.out;OUT.mkdir(parents=True,exist_ok=True)
levels=json.loads((args.road_events/'authored_levels.json').read_text(encoding='utf-8'))[800:900]
default=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[800:900]
baseline=json.loads((args.candidates/'ROUTES_1001_2000_BASELINE.json').read_text(encoding='utf-8'))[800:900]
authored=[];proofs=[];failed=[]
for l,d,b in zip(levels,default,baseline):
    assert l['n']==d['level']==b['level']
    original=b['solutions'][0]
    route=[tuple(s['p']) for s in original['route']]
    first=next(i for i,s in enumerate(original['route']) if s['mask'])
    assert first==d['triggerStep'] and original['repairPurchased']==bool(l.get('repairRequired'))
    post=[tuple(s['p']) for s in d['route']]
    special={tuple(l[k]) for k in ('depot','fade','ice','dark','switch','gate') if l.get(k)}
    special.update(tuple(h['p']) for h in l['homes'])
    special.add(tuple(l['authoredEvent']['tile']))
    if l.get('repair'):special.add(tuple(l['repair']['tile']))
    walls=set(l['walls']);future=set(route[first+1:]);all_route=set(route)
    candidates=[]
    for i,p in enumerate(post[first+1:],first+1):
        if p in all_route or p in special or f'{p[0]},{p[1]}' in walls:continue
        candidates.append((0,abs(i-(first+8)),p))
    if not candidates:
        for x in range(l['grid']):
          for y in range(l['grid']):
            p=(x,y)
            if p in all_route or p in special or f'{x},{y}' in walls:continue
            distance=min(abs(x-q[0])+abs(y-q[1]) for q in future)
            if distance<=2:candidates.append((1,distance,p))
    if not candidates:
        failed.append(l['n']);continue
    _,_,alternate=min(candidates)
    # Signal is a free-turn depot action. Charge one light only where its
    # verified route is shorter; equal-length variants stay a map choice.
    lights=[s['light'] for s in original['route']]
    signal_cost=int(d['steps']>original['steps'])
    assert all(v>signal_cost for v in lights[:-1]) and lights[-1]>=signal_cost,l['n']
    item=dict(l)
    item['phaseChoice']={'decision':'depot_signal_before_first_delivery','signalLightCost':signal_cost,
                         'defaultClose':l['authoredEvent']['tile'],'alternateClose':list(alternate)}
    item['brief']=l['brief']+(' At the depot, spend one light to signal a shorter route; the normal detour remains available.' if signal_cost else ' At the depot, choose which road will close at first delivery. Both choices have verified routes.')
    authored.append(item)
    proofs.append({'level':l['n'],'firstDeliveryStep':first,'defaultClosed':d['tile'],
                   'alternateClosed':list(alternate),'alternateOnDefaultDetour':alternate in set(post[first+1:]),
                   'defaultSteps':d['steps'],'defaultFinishLight':d['finishLight'],
                   'signalSteps':original['steps'],'signalLightCost':signal_cost,'signalFinishLight':lights[-1]-signal_cost,
                   'signalRepairPurchased':original['repairPurchased']})
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(proofs,separators=(',',':')),encoding='utf-8')
(OUT/'report.json').write_text(json.dumps({'attempted':100,'authored':len(authored),'failed':failed,
    'alternateClosesDefaultDetour':sum(p['alternateOnDefaultDetour'] for p in proofs)},indent=2),encoding='utf-8')
print(f'Phase choices {len(authored)}/100; alternate closes default detour in {sum(p["alternateOnDefaultDetour"] for p in proofs)}; failed={failed}')
