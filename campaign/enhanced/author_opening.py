"""Align the first 50 playable maps with the handover opening sequence."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'campaign/enhanced/opening-v1'
OUT.mkdir(exist_ok=True)
levels=json.loads((ROOT/'CAMPAIGN_1000_LEVELS.json').read_text(encoding='utf-8'))[:50]
solutions=json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))['levels'][:50]
proofs=[]
for level,result in zip(levels,solutions):
    n=level['n']
    assert n==result.get('level',result.get('n'))
    candidates=[s for s in result['solutions'] if not s['repairPurchased'] and s['status']=='solved']
    assert candidates,n
    reference=min(candidates,key=lambda s:(s['steps'],-s['route'][-1]['light']))
    if n<=7:
        level['noShadow']=True
        if n<=5:level['repair']=None
        if n==4:level['brief']='Deliver to two houses and compare their return routes.'
        if n==5:level['brief']='Plan your deliveries with enough light for the depot return.'
    if 41<=n<=50:
        original=level['cap'];finish=reference['route'][-1]['light']
        reduction=finish-2
        assert reduction>=2,(n,finish)
        level['cap']=original-reduction
        assert min(s['light']-reduction for s in reference['route'][:-1])>0,n
        assert reference['route'][-1]['light']-reduction==2,n
        level['brief']+=' Lantern light is tight: the recorded no-repair route ends with two light.'
        proofs.append({'level':n,'oldCap':original,'newCap':level['cap'],
                       'oldFinishLight':finish,'newFinishLight':2,
                       'routeSteps':reference['steps'],
                       'minimumIntermediateLight':min(s['light']-reduction for s in reference['route'][:-1])})
assert len(proofs)==10
(OUT/'authored_levels.json').write_text(json.dumps(levels,separators=(',',':')),encoding='utf-8')
(OUT/'light_proofs.json').write_text(json.dumps(proofs,indent=2),encoding='utf-8')
print('Authored 1–7 without active shadows; 1–5 without repairs; 41–50 with two-light reference finishes')
