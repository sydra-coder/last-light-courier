"""Recheck relay charge and exact lantern range at every overload gate."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
base=ROOT/'campaign/enhanced/light-overload-v1'
levels=json.loads((base/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((base/'route_proofs.json').read_text(encoding='utf-8'))
routes=json.loads((ROOT/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text(encoding='utf-8'))[300:400]
assert len(levels)==len(proofs)==len(routes)==100
for level,proof,route in zip(levels,proofs,routes):
    n=level['n'];assert n==proof['level']==route['level']
    records=route['route'];points=[s['p'] for s in records]
    gate=level['lightOverloadGate'];step=proof['gateStep'];relay_step=proof['relayStep']
    assert step>relay_step>route['triggerStep']
    assert points[step]==gate['tile']==proof['gateTile'] and points.count(gate['tile'])==1
    assert points[relay_step]==level['lumenNetwork']['relayTile']
    assert all(s['p']!=level['authoredEvent']['tile'] for s in records[route['triggerStep']+1:])
    cap=level['cap']+(3 if level['repairRequired'] and level['repair']['effect']=='beacon' else 0)
    delta=0;actual=[]
    for i,s in enumerate(records):
        value=min(cap,s['light']+delta)
        if i==relay_step:value=min(cap,value+level['lumenNetwork']['charge'])
        delta=value-s['light'];actual.append(value)
        if i<len(records)-1:assert value>0,(n,i)
    assert actual[relay_step]==proof['actualLightAfterRelay']
    assert actual[step]==proof['actualLightAtGate']
    assert [gate['minLight'],gate['maxLight']]==proof['allowed']
    assert gate['minLight']<=actual[step]<=gate['maxLight']
    assert actual[step]+2>gate['maxLight'] and actual[step]+2<=cap
    assert actual[-1]>=0 and points[-1]==level['depot']
print('PASS: 100 relay routes enter the light-range gate safely; two extra light would overload each gate.')
