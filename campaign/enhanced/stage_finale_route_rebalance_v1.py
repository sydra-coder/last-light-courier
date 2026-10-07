"""Stage eight full-rule finale shortcuts; hold the signaled 1943 conflict."""
from pathlib import Path
import json

here=Path(__file__).resolve().parent
root=here.parents[1]
stage=here/'finale-route-rebalance-v1';stage.mkdir(exist_ok=True)
selection={1903:'SWNE',1906:'WSEN',1911:'NESW',1919:'SWNE',1928:'SWNE',1934:'SWNE',1944:'SWNE',1952:'SWNE'}
sources={order:{row['level']:row for row in json.loads((here/f'event-aware-1901-2000-current-{order}.json').read_text())['rows']} for order in set(selection.values())}
audit=json.loads((here/'current-finale-shortcuts-audit.json').read_text())
levels=json.loads(next(line for line in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if line.startswith('const LEVELS='))[13:-2])
caps=json.loads((here/'lantern-balance-v1/promoted_caps.json').read_text())
routes=json.loads((here/'reference-hints-v1/route_overrides.json').read_text())
revisions=[]
for n,order in selection.items():
    proof=next(row for row in audit if row['level']==n and row['choice']=='default')
    powered=next(row for row in audit if row['level']==n and row['choice']=='power')
    level=levels[n-1];route=sources[order][n]['staticCandidateRoute']
    assert proof['completed'] and powered['completed'] and powered['powerUsed'] and not level.get('phaseChoice')
    cap=level['cap']-(proof['light']-12)
    assert cap>0 and len(route)-1==proof['steps']<proof['referenceSteps']
    caps[str(n)]=cap;routes[str(n)]=route
    revisions.append({'level':n,'oldCap':level['cap'],'newCap':cap,'oldRouteSteps':proof['referenceSteps'],
                      'newRouteSteps':proof['steps'],'order':proof['order'],'expectedFinishLight':12,'sourceOrder':order})
(stage/'caps.json').write_text(json.dumps(caps,indent=2))
(stage/'route_overrides.json').write_text(json.dumps(routes))
(stage/'revisions.json').write_text(json.dumps(revisions,indent=2))
print(json.dumps(revisions))
