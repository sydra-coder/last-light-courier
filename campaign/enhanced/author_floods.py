"""Add a four-move low-road flood countdown to every Storm March map."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'campaign/enhanced/floods-v1'
OUT.mkdir(exist_ok=True)
levels=json.loads((ROOT/'campaign/enhanced/storms-v1/authored_levels.json').read_text(encoding='utf-8'))
routes=json.loads((ROOT/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text(encoding='utf-8'))[:100]
authored=[];proofs=[]
for level,record in zip(levels,routes):
    assert level['n']==record['level']
    route=record['route'];trigger=record['triggerStep']
    special={tuple(level[k]) for k in ('depot','fade','ice','dark','switch','gate') if level.get(k)}
    special.update(tuple(h['p']) for h in level['homes'])
    special.update((tuple(level['authoredEvent']['tile']),tuple(level['stormWind']['from']),
                    tuple(level['stormWind']['to']),tuple(level['repair']['tile'])))
    choices=[]
    for i in range(trigger+1,min(len(route),trigger+4)):
        tile=tuple(route[i]['p'])
        if tile in special or any(tuple(s['p'])==tile for s in route[i+1:]):continue
        choices.append((i,tile))
    assert choices,level['n']
    i,tile=max(choices)
    item=dict(level)
    item['floodRoad']={'tile':list(tile),'trigger':'first_delivery','closeAfter':4}
    item['brief']=level['brief']+' A marked low road floods four moves after the first delivery. Cross it before the countdown ends.'
    authored.append(item)
    proofs.append({'level':level['n'],'triggerStep':trigger,'crossStep':i,
                   'crossAge':i-trigger,'floodStep':trigger+4,
                   'tile':list(tile),'routeSteps':record['steps']})
assert len(authored)==len(proofs)==100
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(proofs,indent=2),encoding='utf-8')
print('Authored 100 four-move flood roads')
