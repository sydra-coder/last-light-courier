"""Add a lantern-range gate to each source-powered relay level."""
from pathlib import Path
from collections import Counter
import json

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'campaign/enhanced/light-overload-v1'
OUT.mkdir(parents=True,exist_ok=True)
levels=json.loads((ROOT/'campaign/enhanced/light-networks-v1/authored_levels.json').read_text(encoding='utf-8'))
routes=json.loads((ROOT/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text(encoding='utf-8'))[300:400]
assert len(levels)==len(routes)==100

authored=[];proofs=[];failed=[]
for level,record in zip(levels,routes):
    assert level['n']==record['level']
    states=record['route'];points=[tuple(s['p']) for s in states]
    relay=tuple(level['lumenNetwork']['relayTile'])
    relay_step=points.index(relay)
    assert relay_step>record['triggerStep']
    cap=level['cap']+(3 if level['repairRequired'] and level['repair']['effect']=='beacon' else 0)
    delta=0;actual=[]
    for i,s in enumerate(states):
        value=min(cap,s['light']+delta)
        if i==relay_step:
            value=min(cap,value+level['lumenNetwork']['charge'])
        delta=value-s['light']
        actual.append(value)
    special={tuple(level[k]) for k in ('depot','fade','ice','dark','switch','gate') if level.get(k)}
    special.update(tuple(h['p']) for h in level['homes'])
    special.update((relay,tuple(level['authoredEvent']['tile']),tuple(level['repair']['tile'])))
    counts=Counter(points)
    choices=[]
    for i in range(relay_step+2,len(points)-5):
        p=points[i]
        if p in special or counts[p]!=1 or actual[i]<3 or actual[i]>cap-3:continue
        choices.append((abs(i-(relay_step+6)),i,p))
    if not choices:
        failed.append(level['n']);continue
    _,step,tile=min(choices)
    light=actual[step]
    item=dict(level)
    item['lightOverloadGate']={'tile':list(tile),'minLight':light-1,'maxLight':light+1,
                               'check':'light_after_entry','opens':'always_if_in_range'}
    item['brief']=level['brief']+f' The marked voltage gate accepts {light-1}–{light+1} lantern light after entry; excess light overloads it.'
    authored.append(item)
    proofs.append({'level':level['n'],'relayStep':relay_step,'gateStep':step,'gateTile':list(tile),
                   'actualLightAfterRelay':actual[relay_step], 'actualLightAtGate':light,
                   'allowed':[light-1,light+1], 'routeSteps':record['steps']})

(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(proofs,separators=(',',':')),encoding='utf-8')
(OUT/'report.json').write_text(json.dumps({'attempted':100,'authored':len(authored),'failed':failed},indent=2),encoding='utf-8')
print(f'Light-overload gates {len(authored)}/100; failed={failed}')
