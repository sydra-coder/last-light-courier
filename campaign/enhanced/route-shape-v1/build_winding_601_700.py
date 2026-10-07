"""Stage winding replacements for the Shadow Door band."""
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'campaign'/'expansion'))
from build_1000 import build,metrics,replay
HERE=Path(__file__).resolve().parent
archive=json.loads((ROOT/'design'/'map-solutions-1000.json').read_text(encoding='utf-8'))['levels']

def longest(route):
    pts=[tuple(step['p']) for step in route]
    dirs=[(b[0]-a[0],b[1]-a[1]) for a,b in zip(pts,pts[1:])]
    best=run=0;last=None
    for direction in dirs:
        run=run+1 if direction==last else 1
        best=max(best,run);last=direction
    return best

results=[];failed=[]
for number in range(601,701):
    generated=build(number,winding=True)
    if generated is None:failed.append(number);continue
    game_map,route=generated
    before=archive[number-1]['solutions'][0]['route']
    assert replay(game_map,[step['p'] for step in route],game_map['repairRequired'])[-1]['light']>=0
    assert metrics(game_map,game_map['repairRequired'])['components']==1
    results.append({'level':number,'map':game_map,'route':route,'beforeStraight':longest(before),
                    'afterStraight':longest(route),'beforeSteps':len(before)-1,'afterSteps':len(route)-1})
assert not failed and len(results)==100,failed
(HERE/'winding_601_700_candidates.json').write_text(json.dumps({'results':results,'failures':failed},separators=(',',':')),encoding='utf-8')
summary={'generated':100,'oldOver12':sum(x['beforeStraight']>12 for x in results),
         'newOver12':sum(x['afterStraight']>12 for x in results),
         'maxNewStraight':max(x['afterStraight'] for x in results),
         'medianBeforeSteps':sorted(x['beforeSteps'] for x in results)[50],
         'medianAfterSteps':sorted(x['afterSteps'] for x in results)[50]}
(HERE/'winding_601_700_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(summary)
