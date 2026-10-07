"""Check exact lantern balance through split relay, voltage gate, and receiver."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
folder=ROOT/'campaign/enhanced/light-transfer-v1'
levels=json.loads((folder/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((folder/'route_proofs.json').read_text(encoding='utf-8'))
routes=json.loads((ROOT/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text(encoding='utf-8'))[300:400]
assert len(levels)==len(proofs)==len(routes)==100
for level,proof,route in zip(levels,proofs,routes):
    n=level['n'];assert n==proof['level']==route['level']
    records=route['route'];points=[s['p'] for s in records]
    relay=proof['relayStep'];gate=proof['gateStep'];receiver=proof['receiverStep']
    assert route['triggerStep']<relay<gate<receiver<len(records)-1
    assert points[relay]==level['lightTransfer']['source']==level['lumenNetwork']['relayTile']
    assert points[receiver]==level['lightTransfer']['receiver']==proof['receiver']
    assert points.count(points[receiver])==1
    assert points[gate]==level['lightOverloadGate']['tile']
    assert level['lightTransfer']['storedLight']==1 and level['lumenNetwork']['charge']==2
    cap=level['cap']+(3 if level['repairRequired'] and level['repair']['effect']=='beacon' else 0)
    delta=0
    for i,record in enumerate(records):
        light=min(cap,record['light']+delta)
        if i==relay:light=min(cap,light+1)
        if i==receiver:light=min(cap,light+1)
        delta=light-record['light']
        if i<len(records)-1:assert light>0,(n,i,light)
        if i==gate:
            assert light==proof['lightAtGateAfterSplit']==proof['gateMinimum']
            assert level['lightOverloadGate']['minLight']<=light<=level['lightOverloadGate']['maxLight']
        if i==receiver:assert delta==2,(n,i,delta)
    assert records[-1]['p']==level['depot'] and light>=0
print('PASS: 100 light-transfer routes split relay charge, pass voltage gate at minimum, reclaim stored light, and finish')
