"""Verify Sentinel influence never blocks the authored no-power route."""
from pathlib import Path
import argparse,json,sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'campaign'/'expansion'))
from build_1000 import replay,key

parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design'/'map-solutions-1000.json')
parser.add_argument('--base',type=Path,default=ROOT/'campaign'/'enhanced'/'sentinels-v1')
args=parser.parse_args()
BASE=args.base
levels=json.loads((BASE/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((BASE/'route_proofs.json').read_text(encoding='utf-8'))
entries=json.loads(args.solutions.read_text(encoding='utf-8'))['levels']
assert len(levels)==len(proofs)==100
assert [l['n'] for l in levels]==list(range(501,601))
for l,proof in zip(levels,proofs):
    n=l['n'];center=l['sentinelCenter']
    assert n==proof['level'] and center==proof['center'] and l['sentinelRadius']==1
    assert key(center) not in l['walls']
    sol=entries[n-1]['solutions'][0]
    route=[s['p'] for s in sol['route']]
    activation=next(i for i,s in enumerate(sol['route']) if s['mask'])
    assert activation==proof['activationStep']
    assert all(max(abs(center[0]-p[0]),abs(center[1]-p[1]))>1 for p in route[activation:])
    checked=replay(l,route,sol['repairPurchased'])
    assert len(checked)-1==proof['routeSteps']
    assert checked[-1]['mask'].bit_count()>=l['required']
print('PASS: 100 Sentinel fields activate after first delivery; all recorded completions avoid their 3×3 influence.')
