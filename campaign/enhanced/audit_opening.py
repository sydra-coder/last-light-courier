"""Verify revised opening pacing and recorded no-repair route light margins."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
folder=ROOT/'campaign/enhanced/opening-v1'
levels=json.loads((folder/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((folder/'light_proofs.json').read_text(encoding='utf-8'))
original=json.loads((ROOT/'CAMPAIGN_1000_LEVELS.json').read_text(encoding='utf-8'))[:50]
solutions=json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))['levels'][:50]
assert len(levels)==len(original)==len(solutions)==50 and len(proofs)==10
for level,old,result in zip(levels,original,solutions):
    n=level['n'];assert n==old['n']
    if n<=7:
        assert level['noShadow'] and level['patrol']==old['patrol']
        if n<=5:assert level['repair'] is None
    else:assert not level.get('noShadow')
    candidates=[s for s in result['solutions'] if not s['repairPurchased'] and s['status']=='solved']
    assert candidates,n
    route=min(candidates,key=lambda s:(s['steps'],-s['route'][-1]['light']))['route']
    assert route[-1]['p']==level['depot'] and route[-1]['light']>=0
    if n<=7:
        assert all(s['light']>0 for s in route[:-1])
        # This route was legal with a moving shadow, and removing that threat
        # cannot invalidate its geometry or lantern sequence.
        assert level['cap']==old['cap']
    if 41<=n<=50:
        proof=proofs[n-41];assert proof['level']==n
        reduction=old['cap']-level['cap']
        assert reduction==proof['oldFinishLight']-2
        assert all(s['light']-reduction>0 for s in route[:-1]),n
        assert route[-1]['light']-reduction==2,n
        assert level['walls']==old['walls'] and level['homes']==old['homes']
print('PASS: 1–7 shadow-free, 1–5 repair-free, and 41–50 recorded routes finish with two light')
