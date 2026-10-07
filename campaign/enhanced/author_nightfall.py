"""Add deterministic fog and a newly costly street to Long Night maps 1101–1200."""
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--out',type=Path,default=ROOT/'campaign/enhanced/nightfall-v1')
args=parser.parse_args()
OUT=args.out; OUT.mkdir(parents=True,exist_ok=True)
levels=json.loads((args.road_events/'authored_levels.json').read_text(encoding='utf-8'))[100:200]
proofs=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[100:200]
authored=[];evidence=[]
for level,proof in zip(levels,proofs):
    assert level['n']==proof['level']
    route=[tuple(s['p']) for s in proof['route']]
    trigger=proof['triggerStep']
    special={tuple(level[k]) for k in ('depot','fade','ice','dark','switch','gate') if level.get(k)}
    special.update(tuple(h['p']) for h in level['homes'])
    special.add(tuple(level['authoredEvent']['tile']))
    if level.get('repair'):special.add(tuple(level['repair']['tile']))
    counts={p:route[trigger+1:].count(p) for p in set(route[trigger+1:])}
    candidates=[(abs(i-len(route)*.6),i,p) for i,p in enumerate(route) if i>trigger+1 and p not in special and p not in route[:trigger+1] and counts[p]==1]
    assert candidates,level['n']
    _,index,tile=min(candidates)
    paid=proof['finishLight']>=1
    # The sole zero-margin route has a visible optional dusk street, but its
    # reference route remains on the baseline road. This avoids inventing light.
    if not paid:
        occupied=set(route)
        free=[(abs(x-tile[0])+abs(y-tile[1]),(x,y)) for x in range(level['grid']) for y in range(level['grid'])
              if (x,y) not in occupied and (x,y) not in special and f'{x},{y}' not in level['walls']]
        assert free,level['n']
        _,tile=min(free)
    item=dict(level)
    item['nightfall']={'trigger':'first_delivery','tile':list(tile),'extraLight':1,'fogRadius':3}
    item['brief']=level['brief']+' After the first delivery, fog limits the visible streets and the marked dusk road costs one extra light.'
    authored.append(item)
    evidence.append({'level':level['n'],'triggerStep':trigger,'duskTile':list(tile),'paidOnRoute':paid,
                     'entryStep':index if paid else None,'finishLightAfterSurcharge':proof['finishLight']-int(paid),
                     'postEventSteps':proof['steps']})
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(evidence,separators=(',',':')),encoding='utf-8')
print(f'Nightfall authored {len(authored)} maps; surcharge used on {sum(e["paidOnRoute"] for e in evidence)} routes')
