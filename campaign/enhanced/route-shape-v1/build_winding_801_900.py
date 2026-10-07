"""Stage winding replacements for the straight 801-900 quake band."""
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'campaign'/'expansion'))
from build_1000 import build,metrics,replay

HERE=Path(__file__).resolve().parent
archive=json.loads((ROOT/'design'/'map-solutions-1000.json').read_text(encoding='utf-8'))['levels']

def longest(route):
    points=[tuple(step['p']) for step in route]
    directions=[(b[0]-a[0],b[1]-a[1]) for a,b in zip(points,points[1:])]
    best=run=0;last=None
    for direction in directions:
        run=run+1 if direction==last else 1
        best=max(best,run);last=direction
    return best

results=[];failures=[]
for number in range(801,901):
    generated=build(number,winding=True)
    if generated is None:
        failures.append(number);continue
    game_map,route=generated
    before=archive[number-1]['solutions'][0]['route']
    assert replay(game_map,[step['p'] for step in route],game_map['repairRequired'])[-1]['light']>=0
    assert metrics(game_map,game_map['repairRequired'])['components']==1
    results.append({'level':number,'map':game_map,'route':route,
                    'beforeStraight':longest(before),'afterStraight':longest(route),
                    'beforeSteps':len(before)-1,'afterSteps':len(route)-1})
payload={'description':'Versioned winding replacements; not integrated','results':results,'failures':failures}
(HERE/'winding_801_900_candidates.json').write_text(json.dumps(payload,separators=(',',':')),encoding='utf-8')
summary={'generated':len(results),'failed':failures,
         'oldOver12':sum(x['beforeStraight']>12 for x in results),
         'newOver12':sum(x['afterStraight']>12 for x in results),
         'maxNewStraight':max((x['afterStraight'] for x in results),default=None),
         'medianBeforeSteps':sorted(x['beforeSteps'] for x in results)[len(results)//2] if results else None,
         'medianAfterSteps':sorted(x['afterSteps'] for x in results)[len(results)//2] if results else None}
(HERE/'winding_801_900_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(summary)
