"""Split one relay charge into remote stored light beyond the voltage gate."""
from pathlib import Path
from collections import Counter
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'campaign/enhanced/light-transfer-v1'
OUT.mkdir(exist_ok=True)
levels = json.loads((ROOT/'campaign/enhanced/light-overload-v1/authored_levels.json').read_text(encoding='utf-8'))
gate_proofs = json.loads((ROOT/'campaign/enhanced/light-overload-v1/route_proofs.json').read_text(encoding='utf-8'))
routes = json.loads((ROOT/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text(encoding='utf-8'))[300:400]
authored=[];proofs=[]
for level,gate,route in zip(levels,gate_proofs,routes):
    n=level['n'];assert n==gate['level']==route['level']
    points=[tuple(s['p']) for s in route['route']]
    counts=Counter(points)
    special={tuple(level[k]) for k in ('depot','fade','ice','dark','switch','gate') if level.get(k)}
    special.update(tuple(h['p']) for h in level['homes'])
    special.update((tuple(level['lumenNetwork']['relayTile']),tuple(level['lightOverloadGate']['tile']),
                    tuple(level['authoredEvent']['tile']),tuple(level['repair']['tile'])))
    choices=[i for i in range(gate['gateStep']+5,min(len(points)-5,gate['gateStep']+21))
             if counts[points[i]]==1 and points[i] not in special]
    assert choices,n
    receiver=min(choices,key=lambda i:(abs(i-(gate['gateStep']+10)),i))
    item=dict(level)
    item['lightTransfer']={'source':level['lumenNetwork']['relayTile'],
                           'receiver':list(points[receiver]),'storedLight':1,
                           'mode':'automatic_split_and_pickup'}
    item['brief']=level['brief']+' The relay sends one of its two light to a marked receiver beyond the voltage gate. Step on the receiver to reclaim it.'
    authored.append(item)
    proofs.append({'level':n,'relayStep':gate['relayStep'],'gateStep':gate['gateStep'],
                   'receiverStep':receiver,'receiver':list(points[receiver]),
                   'lightAtGateAfterSplit':gate['actualLightAtGate']-1,
                   'gateMinimum':level['lightOverloadGate']['minLight'],
                   'returnSteps':len(points)-1})
assert len(authored)==len(proofs)==100
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(proofs,indent=2),encoding='utf-8')
print('Authored 100 relay-to-receiver light transfers')
