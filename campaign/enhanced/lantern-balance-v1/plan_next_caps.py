"""Stage lantern tuning only for certified single-branch late routes."""
from pathlib import Path
import json

here=Path(__file__).resolve().parent
root=here.parents[2]
line=next(s for s in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
balance=json.loads((here.parent/'lantern-balance-audit.json').read_text())
by_level={x['level']:x for x in balance['rows'] if x['branch']=='default'}
exact={x['level'] for x in json.loads((here.parent/'event-aware-exact-minima-late.json').read_text())['certified']}
targets=(1508,1540,1549,1551,1610,1612,1626,1672,1680,1694,1698,1940)
caps=json.loads((here/'promoted_caps.json').read_text())
plan=[]
for n in targets:
    level=levels[n-1];row=by_level[n]
    assert n in exact and not any(level.get(k) for k in ('phaseChoice','transitLink','repairRequired','lightOverloadGate'))
    assert row['finishLight']>24 and row['cap']==level['cap']
    new_cap=row['cap']-(row['finishLight']-16)
    assert 0<new_cap<row['cap']
    caps[str(n)]=new_cap
    plan.append({'level':n,'currentCap':row['cap'],'stagedCap':new_cap,'currentFinishLight':row['finishLight'],'targetFinishLight':16})
(here/'stage_twentyone_caps.json').write_text(json.dumps(caps,indent=2))
(here/'stage_twentyone_plan.json').write_text(json.dumps(plan,indent=2))
print(json.dumps(plan))
