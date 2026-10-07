"""Stage full-rule shorter day/night routes without changing the live package."""
from pathlib import Path
import json

here=Path(__file__).resolve().parent
root=here.parents[1]
stage=here/'night-route-rebalance-v1'
stage.mkdir(exist_ok=True)
source={row['level']:row for row in json.loads((here/'event-aware-1101-1200-current-WENS.json').read_text())['rows']}
replay={row['level']:row for row in json.loads((here/'event-aware-1101-1200-current-WENS-replay.json').read_text())['rows']}
levels=json.loads(next(line for line in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if line.startswith('const LEVELS='))[13:-2])
caps=json.loads((here/'lantern-balance-v1/promoted_caps.json').read_text())
routes=json.loads((here/'reference-hints-v1/route_overrides.json').read_text())
revisions=[]
for n in (1115,1136,1145):
    proof=replay[n]
    assert proof['completed'] and proof['blocked'] is None
    level=levels[n-1]
    assert level.get('dayNightCycle') and level['reviewPower']=='lumen_flask'
    cap=level['cap']-(proof['light']-12)
    assert cap>0 and len(source[n]['staticCandidateRoute'])-1==proof['steps']
    caps[str(n)]=cap
    routes[str(n)]=source[n]['staticCandidateRoute']
    revisions.append({'level':n,'oldCap':level['cap'],'newCap':cap,
                      'oldRouteSteps':proof['referenceSteps'],'newRouteSteps':proof['steps'],
                      'order':proof['order'],'expectedFinishLight':12})
(stage/'caps.json').write_text(json.dumps(caps,indent=2))
(stage/'route_overrides.json').write_text(json.dumps(routes))
(stage/'revisions.json').write_text(json.dumps(revisions,indent=2))
print(json.dumps(revisions))
