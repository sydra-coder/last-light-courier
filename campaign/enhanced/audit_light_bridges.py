"""Verify light-paid bridge routes under the extra crossing cost."""
from pathlib import Path
import argparse,json,sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'campaign'/'expansion'))
from build_1000 import replay,key

parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design'/'map-solutions-1000.json')
parser.add_argument('--base',type=Path,default=ROOT/'campaign'/'enhanced'/'light-bridges-v1')
args=parser.parse_args()
BASE=args.base
levels=json.loads((BASE/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((BASE/'route_proofs.json').read_text(encoding='utf-8'))
entries=json.loads(args.solutions.read_text(encoding='utf-8'))['levels']
assert len(levels)==len(proofs)==100
assert [l['n'] for l in levels]==list(range(701,801))
for l,proof in zip(levels,proofs):
    n=l['n'];assert proof['level']==n and l['bridgeCost']==1
    sol=entries[n-1]['solutions'][0]
    route=[s['p'] for s in sol['route']]
    bridge=l['lightBridge'];i=proof['bridgeEntryStep']
    assert l['lightBridgeRequiresPower'] and proof['powerUseBeforeStep']==i
    assert route[i]==bridge and route.count(bridge)==1
    assert key(bridge) not in l['walls']
    assert proof['firstDeliveryStep']<i
    assert all(p!=bridge for p in route[:proof['firstDeliveryStep']+1])
    replayed=replay(l,route,sol['repairPurchased'])
    assert len(replayed)-1==proof['routeSteps']
    cap=l['cap']+(3 if sol['repairPurchased'] and l['repair'] and l['repair']['effect']=='beacon' else 0)
    light=cap;mask=0;paid=False
    for step,p in enumerate(route[1:],1):
        cost=2 if p==l['dark'] and not(sol['repairPurchased'] and l['repair'] and l['repair']['effect']=='lamp') else 1
        if step==i and not paid:
            assert p==bridge
            assert mask!=0
            light-=l['bridgeCost'];paid=True
            assert light>0,(n,step,'power use left no light')
        light-=cost
        for h_index,h in enumerate(l['homes']):
            if p==h['p'] and not(mask&(1<<h_index)):
                mask|=1<<h_index
                light=min(cap,light+2)
        assert light>0 or p==l['depot'] and step==len(route)-1,(n,step,light)
    assert paid and mask.bit_count()>=l['required'] and light>=0
print('PASS: 100 bridge routes complete after player builds the marked crossing before entry for one light.')
