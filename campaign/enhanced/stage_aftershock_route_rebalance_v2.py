"""Stage full-rule Echo-safe quake routes from levels 901–940."""
from pathlib import Path
import json

here=Path(__file__).resolve().parent
root=here.parents[1]
stage=here/'aftershock-route-rebalance-v2';stage.mkdir(exist_ok=True)
line=next(x for x in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if x.startswith('const LEVELS='))
levels=json.loads(line[13:-2])
caps=json.loads((here/'lantern-balance-v1/promoted_caps.json').read_text(encoding='utf-8'))
routes=json.loads((here/'reference-hints-v1/route_overrides.json').read_text(encoding='utf-8'))
changes=[]
for span in ('941-960','961-980','981-1000'):
    source={x['level']:x for x in json.loads((here/f'echo-aware-{span}.json').read_text(encoding='utf-8'))['rows']}
    replay=json.loads((here/f'echo-aware-{span}-replay.json').read_text(encoding='utf-8'))['rows']
    for proof in replay:
        if not proof['completed']:continue
        n=proof['level'];level=levels[n-1];route=source[n]['staticCandidateRoute']
        assert route and len(route)-1==proof['steps'] and not level.get('repairRequired')
        cap=level['cap']-(proof['light']-12)
        assert cap>0
        caps[str(n)]=cap;routes[str(n)]=route
        changes.append({'level':n,'oldCap':level['cap'],'newCap':cap,
                        'oldRouteSteps':proof['referenceSteps'],'newRouteSteps':proof['steps'],
                        'newRouteOrder':proof['order'],'expectedFinishLight':12})
assert len(changes)==21
(stage/'caps.json').write_text(json.dumps(caps,indent=2),encoding='utf-8')
(stage/'route_overrides.json').write_text(json.dumps(routes),encoding='utf-8')
(stage/'revisions.json').write_text(json.dumps(changes,indent=2),encoding='utf-8')
print(json.dumps({'staged':len(changes),'savedRange':[min(x['oldRouteSteps']-x['newRouteSteps'] for x in changes),
                                                max(x['oldRouteSteps']-x['newRouteSteps'] for x in changes)],
                  'capRange':[min(x['newCap'] for x in changes),max(x['newCap'] for x in changes)]}))




