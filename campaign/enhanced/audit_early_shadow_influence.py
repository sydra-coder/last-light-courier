"""Validate 2x2 influence placement against archived completion routes."""
from pathlib import Path
import argparse
import json

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'campaign/enhanced'
parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design/map-solutions-1000.json')
parser.add_argument('--base',type=Path,default=BASE/'shadow-influence-v1')
args=parser.parse_args()
maps=json.loads((args.base/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((args.base/'route_proofs.json').read_text(encoding='utf-8'))
routes=json.loads(args.solutions.read_text(encoding='utf-8'))['levels']
assert len(maps)==len(proofs)==25
for level,proof in zip(maps,proofs):
    n=level['n'];assert 201<=n<=250 and proof['level']==n
    route=routes[n-1]['solutions'][0]['route']
    first=next(i for i,step in enumerate(route) if step['mask'])
    assert first==proof['triggerStep'] and len(route)-1==proof['routeSteps']
    field=level['shadowInfluence2x2']
    x,y=field['origin']
    cells={tuple(cell) for cell in field['cells']}
    assert field['trigger']=='first_delivery' and cells=={(x,y),(x+1,y),(x,y+1),(x+1,y+1)}
    assert all(0<=a<level['grid'] and 0<=b<level['grid'] and f'{a},{b}' not in level['walls'] for a,b in cells)
    assert not cells & {tuple(step['p']) for step in route}
    assert not cells & ({tuple(h['p']) for h in level['homes']}|{tuple(level['depot'])}|{tuple(level['hiddenRoad'])})
    adjacent={p for a,b in cells for p in ((a+1,b),(a-1,b),(a,b+1),(a,b-1))}-cells
    assert adjacent & {tuple(step['p']) for step in route[first:]}
print('PASS: 25 early 2x2 fields occupy open streets near but outside completed routes')
