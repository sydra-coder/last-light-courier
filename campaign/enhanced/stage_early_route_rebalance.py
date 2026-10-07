"""Stage verified alternate early routes with a 12-light finish target."""
from pathlib import Path
import json

here=Path(__file__).resolve().parent
root=here.parents[1]
stage=here/'early-route-rebalance-v1'
stage.mkdir(exist_ok=True)
rows=json.loads((here/'early-alternate-route-audit.json').read_text(encoding='utf-8'))['allRows']
line=next(x for x in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if x.startswith('const LEVELS='))
levels=json.loads(line[13:-2])
caps=json.loads((here/'lantern-balance-v1/promoted_caps.json').read_text(encoding='utf-8'))
routes=json.loads((here/'reference-hints-v1/route_overrides.json').read_text(encoding='utf-8'))
changes=[]
for row in rows:
    n=row['level']
    proof=json.loads((here/f'early-nonbacktracking-{n}-replay.json').read_text(encoding='utf-8'))
    assert proof['completed'] and proof['finishLight']==row['alternateFinishLight']
    assert proof['steps']==row['alternateSteps']
    new_cap=levels[n-1]['cap']-(proof['finishLight']-12)
    assert new_cap>0
    caps[str(n)]=new_cap
    routes[str(n)]=proof['route']
    changes.append({'level':n,'oldCap':levels[n-1]['cap'],'newCap':new_cap,
                    'oldRouteSteps':row['referenceSteps'],'newRouteSteps':proof['steps'],
                    'oldRouteOrder':row['referenceOrder'],'newRouteOrder':proof['staticOrder'],
                    'expectedFinishLight':12})
(stage/'caps.json').write_text(json.dumps(caps,indent=2),encoding='utf-8')
(stage/'route_overrides.json').write_text(json.dumps(routes),encoding='utf-8')
(stage/'revisions.json').write_text(json.dumps(changes,indent=2),encoding='utf-8')
print(json.dumps({'staged':len(changes),'capRange':[min(x['newCap'] for x in changes),max(x['newCap'] for x in changes)]}))
