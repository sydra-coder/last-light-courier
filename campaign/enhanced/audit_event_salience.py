"""Check whether authored road closures change static post-delivery routes.

This is a geometry diagnostic: dynamic shadows, light, and other events can
make a closure meaningful even when this static distance stays the same.
"""
from collections import Counter, deque
from pathlib import Path
import json
import os

root=Path(__file__).resolve().parents[2]
preview=Path(os.environ.get('LLC_PREVIEW_PATH',root/'design/campaign-2000-preview/index.html'))
line=next(s for s in preview.open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
proofs=json.loads((root/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text())
current_routes=json.loads((root/'campaign/enhanced/reference-hints-v1/normalized_routes.json').read_text())

def distance(level,start,goal,extra_wall=None):
    wall=set(level['walls'])
    if extra_wall:wall.add(f'{extra_wall[0]},{extra_wall[1]}')
    q=deque([(tuple(start),0)]);seen={tuple(start)}
    while q:
        (x,y),d=q.popleft()
        if (x,y)==tuple(goal):return d
        for xx,yy in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            p=(xx,yy)
            if 0<=xx<level['grid'] and 0<=yy<level['grid'] and f'{xx},{yy}' not in wall and p not in seen:
                seen.add(p);q.append((p,d+1))
    return None

def distance_map(level,start,extra_wall=None):
    wall=set(level['walls'])
    if extra_wall:wall.add(f'{extra_wall[0]},{extra_wall[1]}')
    q=deque([tuple(start)]);found={tuple(start):0}
    while q:
        x,y=q.popleft()
        for xx,yy in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            p=(xx,yy)
            if 0<=xx<level['grid'] and 0<=yy<level['grid'] and f'{xx},{yy}' not in wall and p not in found:
                found[p]=found[(x,y)]+1;q.append(p)
    return found

rows=[]
for proof in proofs:
    n=proof['level'];level=levels[n-1]
    event=level.get('authoredEvent')
    if not event or event['kind']!='road_close':continue
    event_tile=(level['phaseChoice']['alternateClose']
                if os.environ.get('LLC_SALIENCE_PHASE_ALTERNATE')=='1' and level.get('phaseChoice')
                else event['tile'])
    route=[{'p':step[:2],'mask':step[2]} for step in current_routes[n-201]]
    first=next((s for s in route if s['mask']),None)
    if first is None:raise ValueError(f'{n}: no first delivery')
    first_pos=first['p'];remaining=[h['p'] for h in level['homes'] if h['p']!=first_pos]
    targets=remaining+[level['depot']]
    effects=[]
    for p in targets:
        before=distance(level,first_pos,p)
        after=distance(level,first_pos,p,event_tile)
        effects.append({'target':p,'before':before,'after':after,'increase':None if before is None or after is None else after-before})
    affected=[x for x in effects if x['before'] is not None and (x['after'] is None or (x['increase'] is not None and x['increase']>0))]
    all_first=[]
    for house in level['homes']:
        source=house['p'];other=[h['p'] for h in level['homes'] if h is not house]+[level['depot']]
        open_dist=distance_map(level,source);closed_dist=distance_map(level,source,event_tile)
        changes=sum(open_dist.get(tuple(p))!=closed_dist.get(tuple(p)) for p in other)
        all_first.append({'house':source,'changedTargets':changes})
    rows.append({'level':n,'tile':event_tile,'firstHouse':first_pos,'affectedTargets':len(affected),'maxIncrease':max((x['increase'] or 0 for x in effects),default=0),'affectedAnyFirstHouse':sum(x['changedTargets']>0 for x in all_first),'allFirstHouses':all_first,'effects':effects})

bands=[]
for start in range(1001,2001,100):
    subset=[x for x in rows if start<=x['level']<start+100]
    bands.append({'from':start,'to':start+99,'events':len(subset),'affectAtLeastOneTarget':sum(x['affectedTargets']>0 for x in subset),
                  'affectNoStaticTarget':sum(x['affectedTargets']==0 for x in subset),
                  'affectAnyFirstHouse':sum(x['affectedAnyFirstHouse']>0 for x in subset)})
report={'scope':'Static shortest distance from first delivered house to remaining houses/depot, before and after the authored road closes. Dynamic mechanics ignored.',
        'events':len(rows),'bands':bands,'rows':rows}
output=Path(os.environ.get('LLC_SALIENCE_OUTPUT',root/'campaign/enhanced/event-salience-audit.json'))
output.write_text(json.dumps(report,indent=2))
print(json.dumps({'events':len(rows),'bands':bands}))
