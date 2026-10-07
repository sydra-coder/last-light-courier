"""Stage 701–800 bridge shortcuts that completed in the full runtime."""
from pathlib import Path
import json

here=Path(__file__).resolve().parent
root=here.parents[1]
stage=here/'bridge-route-rebalance-v1'
stage.mkdir(exist_ok=True)
line=next(x for x in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if x.startswith('const LEVELS='))
levels=json.loads(line[13:-2])
caps=json.loads((here/'lantern-balance-v1/promoted_caps.json').read_text(encoding='utf-8'))
routes=json.loads((here/'reference-hints-v1/route_overrides.json').read_text(encoding='utf-8'))
references=json.loads((here/'reference-hints-v1/normalized_routes.json').read_text(encoding='utf-8'))
changes=[]
for n in range(701,801):
    proof=json.loads((here/f'early-nonbacktracking-{n}-replay.json').read_text(encoding='utf-8'))
    if not proof.get('completed'):continue
    level=levels[n-1]
    assert level.get('lightBridgeRequiresPower') and not level.get('repairRequired')
    cap=level['cap']-(proof['finishLight']-12)
    assert cap>0
    old=references[n-201]
    old_order=[];mask=old[0][2]
    for point in old[1:]:
        new=point[2]&~mask
        old_order.extend(i for i in range(20) if new&(1<<i))
        mask=point[2]
    caps[str(n)]=cap
    routes[str(n)]=proof['route']
    changes.append({'level':n,'oldCap':level['cap'],'newCap':cap,
                    'oldRouteSteps':len(old)-1,'newRouteSteps':proof['steps'],
                    'oldRouteOrder':old_order,'newRouteOrder':proof['staticOrder'],
                    'expectedFinishLight':12})
assert len(changes)==20
(stage/'caps.json').write_text(json.dumps(caps,indent=2),encoding='utf-8')
(stage/'route_overrides.json').write_text(json.dumps(routes),encoding='utf-8')
(stage/'revisions.json').write_text(json.dumps(changes,indent=2),encoding='utf-8')
print(json.dumps({'staged':len(changes),'changedOrder':sum(x['oldRouteOrder']!=x['newRouteOrder'] for x in changes),
                  'savedRange':[min(x['oldRouteSteps']-x['newRouteSteps'] for x in changes),max(x['oldRouteSteps']-x['newRouteSteps'] for x in changes)]}))
