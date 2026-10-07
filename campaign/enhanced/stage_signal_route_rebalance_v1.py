"""Stage two verified short routes for both phase-choice states."""
from pathlib import Path
import json

here=Path(__file__).resolve().parent
root=here.parents[1]
stage=here/'signal-route-rebalance-v1';stage.mkdir(exist_ok=True)
source={row['level']:row for row in json.loads((here/'event-aware-1801-1900-current-WENS.json').read_text())['rows']}
replay={row['level']:row for row in json.loads((here/'event-aware-1801-1900-current-WENS-replay.json').read_text())['rows']}
signals={row['level']:row for row in json.loads((here/'event-aware-1801-1820-signal-current-WENS-replay.json').read_text())['completedRoutes']}
levels=json.loads(next(line for line in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if line.startswith('const LEVELS='))[13:-2])
caps=json.loads((here/'lantern-balance-v1/promoted_caps.json').read_text())
routes=json.loads((here/'reference-hints-v1/route_overrides.json').read_text())
signal_overrides={}
revisions=[]
for n in (1805,1817):
    proof=replay[n];signal=signals[n];level=levels[n-1]
    assert proof['completed'] and proof['shorterThanCurrent'] and signal['completed'] and level.get('phaseChoice')
    route=source[n]['staticCandidateRoute']
    assert route==signal['route'] and len(route)-1==proof['steps']==signal['steps']
    cap=level['cap']-(proof['light']-12)
    assert cap>0
    caps[str(n)]=cap;routes[str(n)]=route;signal_overrides[str(n)]=route
    revisions.append({'level':n,'oldCap':level['cap'],'newCap':cap,'oldRouteSteps':proof['referenceSteps'],
                      'newRouteSteps':proof['steps'],'newSignalSteps':signal['steps'],
                      'order':proof['order'],'expectedFinishLight':12})
(stage/'caps.json').write_text(json.dumps(caps,indent=2))
(stage/'route_overrides.json').write_text(json.dumps(routes))
(stage/'signal_route_overrides.json').write_text(json.dumps(signal_overrides))
(stage/'revisions.json').write_text(json.dumps(revisions,indent=2))
print(json.dumps(revisions))
