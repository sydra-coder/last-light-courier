"""Add a visible six-night/four-day cycle and a night-only road."""
from pathlib import Path
from collections import Counter
import json

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'campaign/enhanced/day-night-v1'
OUT.mkdir(exist_ok=True)
levels=json.loads((ROOT/'campaign/enhanced/nightfall-v1/authored_levels.json').read_text(encoding='utf-8'))
routes=json.loads((ROOT/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text(encoding='utf-8'))[100:200]
authored=[];proofs=[]
for level,record in zip(levels,routes):
    n=level['n'];assert n==record['level']
    points=[tuple(s['p']) for s in record['route']];counts=Counter(points)
    trigger=record['triggerStep']
    special={tuple(level[k]) for k in ('depot','fade','ice','dark','switch','gate') if level.get(k)}
    special.update(tuple(h['p']) for h in level['homes'])
    special.update((tuple(level['nightfall']['tile']),tuple(level['authoredEvent']['tile']),tuple(level['repair']['tile'])))
    choices=[i for i in range(trigger+11,len(points)-5)
             if (i-1-trigger)%10<5 and counts[points[i]]==1 and points[i] not in special]
    assert choices,n
    gate=min(choices,key=lambda i:(abs(i-(trigger+15)),i))
    item=dict(level)
    item['dayNightCycle']={'nightMoves':6,'dayMoves':4,'starts':'first_delivery',
                           'moonRoad':list(points[gate]),'entryChecks':'phase_before_move'}
    item['brief']=level['brief']+' After the first delivery, night lasts six moves and day lasts four. Fog and the dusk surcharge apply at night; the marked moon road opens only at night.'
    authored.append(item)
    proofs.append({'level':n,'triggerStep':trigger,'moonRoadStep':gate,
                   'moonRoad':list(points[gate]),'entryAge':gate-1-trigger,
                   'steps':record['steps']})
assert len(authored)==len(proofs)==100
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(proofs,indent=2),encoding='utf-8')
print('Authored 100 day/night cycles and night-only moon roads')
