"""Stage the full-rule level 1236 shortcut and matching lantern budget."""
from pathlib import Path
import json

here=Path(__file__).resolve().parent
root=here.parents[1]
stage=here/'spawner-route-rebalance-v1';stage.mkdir(exist_ok=True)
row=next(x for x in json.loads((here/'event-aware-1201-1300-current-WENS.json').read_text())['rows'] if x['level']==1236)
proof=next(x for x in json.loads((here/'current-1236-shortcut-audit.json').read_text()) if not x['powered'])
level=json.loads(next(line for line in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if line.startswith('const LEVELS='))[13:-2])[1235]
assert proof['completed'] and proof['blockedAt'] is None and level.get('shadowSpawner')
cap=level['cap']-(proof['light']-12)
assert cap>0
caps=json.loads((here/'lantern-balance-v1/promoted_caps.json').read_text());caps['1236']=cap
routes=json.loads((here/'reference-hints-v1/route_overrides.json').read_text());routes['1236']=row['staticCandidateRoute']
revision={'level':1236,'oldCap':level['cap'],'newCap':cap,'oldRouteSteps':proof['referenceSteps'],
          'newRouteSteps':proof['steps'],'order':row['order'],'expectedFinishLight':12}
(stage/'caps.json').write_text(json.dumps(caps,indent=2))
(stage/'route_overrides.json').write_text(json.dumps(routes))
(stage/'revisions.json').write_text(json.dumps([revision],indent=2))
print(json.dumps(revision))
