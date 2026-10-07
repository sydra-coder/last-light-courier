"""Stage two verified relay-and-spawner routes with matched lantern caps."""
from pathlib import Path
import json

here=Path(__file__).resolve().parent
root=here.parents[1]
stage=here/'relay-route-rebalance-v1';stage.mkdir(exist_ok=True)
audit=json.loads((here/'current-1501-shortcuts-audit.json').read_text())
levels=json.loads(next(line for line in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if line.startswith('const LEVELS='))[13:-2])
caps=json.loads((here/'lantern-balance-v1/promoted_caps.json').read_text())
routes=json.loads((here/'reference-hints-v1/route_overrides.json').read_text())
revisions=[]
for n,filename in ((1567,'event-aware-1501-1600-current-WENS.json'),(1588,'event-aware-1501-1600-current-EWSN.json')):
    proof=next(row for row in audit if row['level']==n and not row['powered'])
    row=next(row for row in json.loads((here/filename).read_text())['rows'] if row['level']==n)
    level=levels[n-1]
    assert proof['completed'] and proof['blockedAt'] is None and level.get('lumenNetwork') and level.get('shadowSpawner')
    cap=level['cap']-(proof['light']-12)
    assert cap>0 and len(row['staticCandidateRoute'])-1==proof['steps']
    caps[str(n)]=cap;routes[str(n)]=row['staticCandidateRoute']
    revisions.append({'level':n,'oldCap':level['cap'],'newCap':cap,'oldRouteSteps':proof['referenceSteps'],
                      'newRouteSteps':proof['steps'],'order':proof['order'],'expectedFinishLight':12})
(stage/'caps.json').write_text(json.dumps(caps,indent=2))
(stage/'route_overrides.json').write_text(json.dumps(routes))
(stage/'revisions.json').write_text(json.dumps(revisions,indent=2))
print(json.dumps(revisions))
