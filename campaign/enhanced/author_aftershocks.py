"""Place a visible eight-move aftershock in late Quake Frontier maps."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'campaign/enhanced/aftershocks-v1'
OUT.mkdir(exist_ok=True)
levels=json.loads((ROOT/'campaign/enhanced/quakes-v1/authored_levels.json').read_text(encoding='utf-8'))[150:]
routes=json.loads((ROOT/'campaign/enhanced/quakes-v1/post_event_routes.json').read_text(encoding='utf-8'))[150:]
authored=[];proofs=[]
for level,proof in zip(levels,routes):
    n=level['n'];assert n==proof['level'] and 951<=n<=1000
    route=proof['route'];trigger=proof['triggerStep']
    special={tuple(level[k]) for k in ('depot','fade','ice','dark','switch','gate') if level.get(k)}
    special.update(tuple(h['p']) for h in level['homes'])
    special.update(tuple(t) for t in level['quakeEvent']['open'])
    special.add(tuple(level['quakeEvent']['close']))
    special.add(tuple(level['repair']['tile']))
    choices=[]
    for i in range(trigger+1,trigger+8):
        tile=tuple(route[i]['p'])
        if tile in special or any(tuple(s['p'])==tile for s in route[i+1:]):continue
        choices.append((i,tile))
    assert choices,n
    i,tile=max(choices)
    item=dict(level)
    item['aftershock']={'tile':list(tile),'trigger':'first_delivery','closeAfter':8}
    item['brief']=level['brief']+' An aftershock closes the marked road eight moves after the first quake. Cross it before the countdown ends.'
    authored.append(item)
    proofs.append({'level':n,'triggerStep':trigger,'crossStep':i,'crossAge':i-trigger,
                   'closeStep':trigger+8,'tile':list(tile),'routeSteps':proof['postEventSteps']})
assert len(authored)==len(proofs)==50
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(proofs,indent=2),encoding='utf-8')
print('Authored 50 late Quake Frontier aftershocks')
