"""Verify one-way entry and post-collapse completion routes for 401–500."""
from pathlib import Path
import argparse,json, sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'campaign'/'expansion'))
from build_1000 import replay,key

parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design'/'map-solutions-1000.json')
parser.add_argument('--base',type=Path,default=ROOT/'campaign'/'enhanced'/'causeways-v1')
args=parser.parse_args()
BASE=args.base
levels=json.loads((BASE/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((BASE/'route_proofs.json').read_text(encoding='utf-8'))
entries=json.loads(args.solutions.read_text(encoding='utf-8'))['levels']
assert len(levels)==len(proofs)==100
assert [l['n'] for l in levels]==list(range(401,501))
counts={'one_way':0,'collapse':0}
for l,proof in zip(levels,proofs):
    n=l['n'];assert proof['level']==n
    sol=entries[n-1]['solutions'][0]
    route=[s['p'] for s in sol['route']]
    i=proof['referenceStep'];tile=proof['tile']
    assert route[i]==tile and route[i-1]==proof['entryFrom']
    assert key(tile) not in l['walls'] and proof['openNeighborCount']>=3
    if proof['kind']=='one_way':
        assert l['oneWayTile']==tile and l['oneWayFrom']==route[i-1]
        assert all(p!=tile or route[j-1]==l['oneWayFrom'] for j,p in enumerate(route) if j>0)
    else:
        assert l['collapseTile']==tile
        assert all(p!=tile for p in route[i+1:]),n
    checked=replay(l,route,sol['repairPurchased'])
    assert len(checked)-1==proof['routeSteps']
    assert checked[-1]['mask'].bit_count()>=l['required']
    counts[proof['kind']]+=1
assert counts=={'one_way':50,'collapse':50}
print('PASS: 50 one-way routes enter from the allowed side; 50 completion routes avoid collapsed roads after leaving.')
